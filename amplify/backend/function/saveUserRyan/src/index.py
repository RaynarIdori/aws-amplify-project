import json
import boto3
import os
import uuid

def handler(event, context):
    body = json.loads(event['body'])
    
    table = boto3.resource('dynamodb', region_name='eu-west-1').Table(os.environ['STORAGE_USERS_NAME'])
    user_id = str(uuid.uuid4())
    table.put_item(Item={'id': user_id, 'name': body['name'], 'email': body['email']})
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'success': True, 'user_id': user_id})
    }