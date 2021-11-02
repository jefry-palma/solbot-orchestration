import boto3
import json
import os
from src.main.lambdas.utils.logs import logger


def trigger_sns_topic(arn,message):

    sns_client = boto3.client('sns')

    sns_client.publish(
        TargetArn=arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )

def get_table(table_name):
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['REGION'])
    table = dynamodb.Table(table_name)
    return table

def put_item_dynamo(execution_id,status_object,origin,to):

    table = get_table('solbot_executions')
    table.put_item(
        Item = {'execution_id': execution_id, 'execution_status': status_object, 'origin': origin,'to': to }
    )

def update_item_status_dynamo(execution_id,feature,status):

    table = get_table('solbot_executions')

    table.update_item(
        Key={
            'execution_id': execution_id
        },
        UpdateExpression="SET execution_status.#feature.current_status = :val",  
        ExpressionAttributeNames={  
            "#feature": feature  
        },  
        ExpressionAttributeValues={  
            ":val": status  
        }  
    )
