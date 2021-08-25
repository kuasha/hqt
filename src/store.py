import logging
from decimal import Decimal
import json
import config
import utils
import ddb

import response
import participant
import episode
import immutable

RESOURCE_HANDLER_MAP = {
    config.RESPONSE_RESOURCE_NAME: response,
    config.PARTICIPANT_RESOURCE_NAME: participant,
    config.GAME_RESOURCE_NAME: immutable,
    config.QUESTION_RESOURCE_NAME: immutable,
    config.EPISODE_RESOURCE_NAME: episode
}


def get_resource_handler(resource_name):
    return RESOURCE_HANDLER_MAP[resource_name]


def create_raw_resource(resource_name, item):
    return ddb.create_resource(resource_name, item)


def create_resource(resource_name, item):
    handler = get_resource_handler(resource_name)
    if handler:
        handler.handle_post(item)

    return ddb.create_resource(resource_name, item)


def load_resource(resource_name, resource_id):
    return ddb.load_resource(resource_name, resource_id)


def load_participant(episode_id, user_id):
    key = {'episode_id': episode_id, 'user_id': user_id}
    return ddb.get_item(config.PARTICIPANT_RESOURCE_NAME, key)


def load_response(episode_id, user_id, question_id):
    query = "episode_id = :episode_id  and user_id = :user_id"
    query_var_values = {":episode_id": episode_id, ":user_id": user_id}
    items = ddb.query("response", query, query_var_values)

    # we should have less than 20 questions in an episode
    # otherwise create a ddb index
    for item in items:
        if item["question_id"] == question_id:
            return item

    return None


def eliminate_participant(participant, participant_id):
    resource_name = config.EPISODE_RESOURCE_NAME
    participant_id = participant["user_id"]
    key = {'id': participant_id}
    query = 'SET #e = :val'
    query_names = {"#e": "eliminated"}
    query_values = {':val': True}
    response = ddb.update_item(
        resource_name, key, query, query_names, query_values)
    logging.info("Participant {} has been eliminated from episode {}".format(
        participant["user_id"], participant["episode_id"]))
    return response


def update_episode_state(episode_id, state):
    resource_name = config.EPISODE_RESOURCE_NAME
    key = {'id': episode_id}
    query = 'SET #s = :val'
    query_names = {"#s": "state"}
    query_values = {':val': state}
    return ddb.update_item(resource_name, key, query, query_names, query_values)


def update_episode_state_qindex(episode_id, state, qindex):
    resource_name = config.EPISODE_RESOURCE_NAME
    key = {'id': episode_id}
    query = 'SET #s = :sval, #i = :ival, #t = :tsval'
    query_names = {"#s": "state", "#i": "current_question_index",
                   "#t": "question_start_timestamp"}
    query_values = {
        ':sval': state,
        ':ival': qindex,
        ':tsval': int(utils.get_timestamp_utc()) + config.SET_START_TIME_IN_FUTURE_SECONDS
    }

    return ddb.update_item(resource_name, key, query, query_names, query_values)


def update_response_statistics(resp):
    logging.info(
        "Updating statistics with response {}".format(json.dumps(resp)))
    answer = resp["answer"]
    episode_id = resp["episode_id"]
    question_id = resp["question_id"]
    field = utils. get_answer_fieldname(answer)

    resource_name = config.RESPONSE_STAT_RESOURCE_NAME
    key = {'episode_id': episode_id, 'question_id': question_id}
    query = 'SET #s = #s + :val'
    query_names = {"#s": field}
    query_values = {':val': Decimal(1)}

    return ddb.update_item(resource_name, key, query, query_names, query_values)


def update_participant_statistics(participant):
    logging.info(
        "Updating episode participant count with registration {}".format(json.dumps(participant)))

    episode_id = participant["episode_id"]
    resource_name = config.EPISODE_RESOURCE_NAME
    key = {'id': episode_id}
    query = 'SET #s = #s + :val'
    query_names = {"#s": "participant_count"}
    query_values = {':val': Decimal(1)}
    return ddb.update_item(resource_name, key, query, query_names, query_values)


def update_eliminated_statistics(episode_id, user_id):
    logging.info(
        "Updating episode eliminated count after {} is eliminated".format(user_id))

    resource_name = config.EPISODE_RESOURCE_NAME
    key = {'id': episode_id}
    query = 'SET #s = #s + :val'
    query_names = {"#s": "eliminated_count"}
    query_values = {':val': Decimal(1)}
    return ddb.update_item(resource_name, key, query, query_names, query_values)
