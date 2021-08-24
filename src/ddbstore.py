import logging
from decimal import Decimal
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import json
import os
from exceptions import DataStoreException
import response
import participant
import episode
import immutable
import config
import utils

dynamodb = boto3.resource('dynamodb')

ddb_table_env_map = config.DDB_TABLE_ENV_MAP

resource_validator_map = {
    "response": response,
    config.PARTICIPANT_RESOURCE_NAME: participant,
    "game": immutable,
    "question": immutable,
    "episode": episode
}


def create_resource_inddb(resource_name, item):
    table_name = os.environ[ddb_table_env_map[resource_name]]
    table = dynamodb.Table(table_name)
    try:
        response = table.put_item(Item=item)
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
    else:
        return response


def create_resource(resource_name, data):
    item = json.loads(data)

    handler = resource_validator_map[resource_name]
    if handler:
        handler.handle_post(item)

    return create_resource_inddb(resource_name, item)


def load_resource(resource_name, resource_id):
    table_name = os.environ[ddb_table_env_map[resource_name]]
    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(Key={'id': resource_id})
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
    else:
        if "Item" in response.keys():
            return response['Item']
        else:
            return None


def load_participant(episode_id, user_id):
    table_name = os.environ[ddb_table_env_map[config.PARTICIPANT_RESOURCE_NAME]]
    table = dynamodb.Table(table_name)

    response = table.get_item(
        Key={'episode_id': episode_id, 'user_id': user_id})
    if "Item" in response.keys():
        return response['Item']


def load_response(episode_id, user_id, question_id):
    table_name = os.environ[ddb_table_env_map["response"]]
    table = dynamodb.Table(table_name)

    response = table.query(
        KeyConditionExpression=Key('episode_id').eq(episode_id) & Key('user_id').eq(user_id))

    if "Items" in response.keys():
        items = response['Items']
        for item in items:
            if item["question_id"] == question_id:
                return item

    return None


def eliminate_participant(participant):
    participant["eliminated"] = True
    table_name = os.environ[ddb_table_env_map[config.PARTICIPANT_RESOURCE_NAME]]
    table = dynamodb.Table(table_name)
    try:
        # TODO: use update_item instead
        response = table.put_item(Item=participant)
        logging.info("Participant {} has been eliminated from episode {}".format(
            participant["user_id"], participant["episode_id"]))
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
        raise DataStoreException("Can not save participant {} for episode {}".format(
            participant["user_id"], participant["episode_id"]))
    else:
        return response


def update_episode_state(episode_id, state):
    table_name = os.environ[ddb_table_env_map[config.EPISODE_RESOURCE_NAME]]
    table = dynamodb.Table(table_name)

    table.update_item(
        Key={
            'id': episode_id
        },
        UpdateExpression='SET #s = :val',
        ExpressionAttributeNames={
            "#s": "state"
        },
        ExpressionAttributeValues={
            ':val': state
        },
        ReturnValues="UPDATED_NEW"
    )


def update_episode_state_qindex(episode_id, state, qindex):
    table_name = os.environ[ddb_table_env_map[config.EPISODE_RESOURCE_NAME]]
    table = dynamodb.Table(table_name)

    table.update_item(
        Key={
            'id': episode_id
        },
        UpdateExpression='SET #s = :sval, #i = :ival, #t = :tsval ',
        ExpressionAttributeNames={
            "#s": "state",
            "#i": "current_question_index",
            "#t": "question_start_timestamp"
        },
        ExpressionAttributeValues={
            ':sval': state,
            ':ival': qindex,
            ':tsval': int(utils.get_timestamp_utc()) + config.SET_START_TIME_IN_FUTURE_SECONDS
        },
        ReturnValues="UPDATED_NEW"
    )


def update_response_statistics(resp):
    logging.info(
        "Updating statistics with response {}".format(json.dumps(resp)))
    answer = resp["answer"]
    episode_id = resp["episode_id"]
    question_id = resp["question_id"]
    field = utils. get_answer_fieldname(answer)
    table_name = os.environ[ddb_table_env_map[config.RESPONSE_STAT_RESOURCE_NAME]]
    table = dynamodb.Table(table_name)

    table.update_item(
        Key={
            'episode_id': episode_id,
            'question_id': question_id
        },
        UpdateExpression='SET #s = #s + :val',
        ExpressionAttributeNames={
            "#s": field
        },
        ExpressionAttributeValues={
            ':val': Decimal(1)
        },
        ReturnValues="UPDATED_NEW"
    )


def update_participant_statistics(participant):
    logging.info(
        "Updating episode participant count with registration {}".format(json.dumps(participant)))
    episode_id = participant["episode_id"]

    table_name = os.environ[ddb_table_env_map[config.EPISODE_RESOURCE_NAME]]
    table = dynamodb.Table(table_name)

    table.update_item(
        Key={
            'id': episode_id
        },
        UpdateExpression='SET #s = #s + :val',
        ExpressionAttributeNames={
            "#s": "participant_count"
        },
        ExpressionAttributeValues={
            ':val': Decimal(1)
        },
        ReturnValues="UPDATED_NEW"
    )


def update_eliminated_statistics(episode_id, user_id):
    logging.info(
        "Updating episode eliminated count after {} is eliminated".format(user_id))

    table_name = os.environ[ddb_table_env_map[config.EPISODE_RESOURCE_NAME]]
    table = dynamodb.Table(table_name)

    table.update_item(
        Key={
            'id': episode_id
        },
        UpdateExpression='SET #s = #s + :val',
        ExpressionAttributeNames={
            "#s": "eliminated_count"
        },
        ExpressionAttributeValues={
            ':val': Decimal(1)
        },
        ReturnValues="UPDATED_NEW"
    )
