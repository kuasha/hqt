import os
import logging
import boto3
from botocore.exceptions import ClientError
import config

dynamodb = boto3.resource('dynamodb')

ddb_table_env_map = config.DDB_TABLE_ENV_MAP


def get_resource_table_name(resource_name):
    return os.environ[ddb_table_env_map[resource_name]]


def create_resource(resource_name, item):
    table_name = get_resource_table_name(resource_name)
    table = dynamodb.Table(table_name)
    try:
        response = table.put_item(Item=item)
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
    else:
        return response


def load_resource(resource_name, resource_id):
    table_name = os.environ[ddb_table_env_map[resource_name]]
    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(Key={'id': resource_id})
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
        return None
    else:
        if "Item" in response.keys():
            return response['Item']
        else:
            return None


def get_item(resource_name, key):
    table_name = os.environ[ddb_table_env_map[resource_name]]
    table = dynamodb.Table(table_name)

    response = table.get_item(Key=key)
    if "Item" in response.keys():
        return response['Item']
    else:
        return None


def query(resource_name, query, query_variables):
    table_name = os.environ[ddb_table_env_map[resource_name]]
    table = dynamodb.Table(table_name)

    response = table.query(
        KeyConditionExpression=query,
        ExpressionAttributeValues=query_variables)
    items = []
    if "Items" in response.keys():
        items = response['Items']

    return items


def update_item(resource_name, key, query, query_names, query_values):
    table_name = os.environ[ddb_table_env_map[resource_name]]
    table = dynamodb.Table(table_name)

    return table.update_item(
        Key=key,
        UpdateExpression=query,
        ExpressionAttributeNames=query_names,
        ExpressionAttributeValues=query_values,
        ReturnValues="UPDATED_NEW")
