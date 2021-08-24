import logging
import boto3

sqs_client = boto3.client('sqs')


def send_message(queue_url, message, delay):
    logging.warn("Sending message to {}".format(queue_url))

    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message,
        DelaySeconds=delay)

    logging.warn("Sent message with ID: {}".format(response['MessageId']))
