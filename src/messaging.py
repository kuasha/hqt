import os
import logging
import boto3

sqs_client = boto3.client('sqs')


def get_queue_url_from_queue_name(queue_name):
    if queue_name in os.environ.keys():
        return os.environ[queue_name]
    else:
        # for local developemnt - run a http server and return 200 for everything :D
        return "http://localhost:8443/sqs/EPISODE_WORKER_SQS_QUEUE"


def send_message(queue_name, message, delay):
    logging.info("Sending message to {}".format(queue_name))

    queue_url = get_queue_url_from_queue_name(queue_name)
    queue_url = get_queue_url_from_queue_name(queue_url)

    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message,
        DelaySeconds=delay)

    logging.warn("Sent message with ID: {}".format(response['MessageId']))
