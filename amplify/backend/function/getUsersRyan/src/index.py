import json
import boto3
import os
from decimal import Decimal

CORS_HEADERS = {
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}

def error_response(status_code, error, message):
    return {
        'statusCode': status_code,
        'headers': CORS_HEADERS,
        'body': json.dumps({
            'success': False,
            'error': error,
            'message': message
        })
    }

def handler(event, context):
    try:
        if event.get('httpMethod') != 'GET':
            return error_response(405, 'Method not allowed', 'Only GET method is supported')
        
        query_params = event.get('queryStringParameters') or {}
        user_id = query_params.get('id')
        user_email = query_params.get('email')
        
        if not user_id and not user_email:
            return error_response(400, 'Missing parameters', 'Either id or email parameter is required')
        
        if user_id and user_email:
            user_email = None
        
        dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'eu-west-1'))
        table = dynamodb.Table(os.environ.get('STORAGE_USERS_NAME', 'users-dev'))
        
        user_data = None
        
        if user_id:
            response = table.get_item(
                Key={'id': user_id},
                ProjectionExpression='id, email, #n',
                ExpressionAttributeNames={'#n': 'name'}
            )
            user_data = response.get('Item')
            
        elif user_email:
            try:
                response = table.query(
                    IndexName='emailIndex',
                    KeyConditionExpression='email = :email',
                    ExpressionAttributeValues={':email': user_email},
                    ProjectionExpression='id, email, #n',
                    ExpressionAttributeNames={'#n': 'name'}
                )
                user_data = response['Items'][0] if response['Items'] else None
            except:
                response = table.scan(
                    FilterExpression='email = :email',
                    ExpressionAttributeValues={':email': user_email},
                    ProjectionExpression='id, email, #n',
                    ExpressionAttributeNames={'#n': 'name'}
                )
                user_data = response['Items'][0] if response['Items'] else None
        
        if not user_data:
            search_criteria = f"ID: {user_id}" if user_id else f"email: {user_email}"
            return error_response(404, 'User not found', f'No user found with {search_criteria}')
        
        cleaned_user = {
            key: float(value) if isinstance(value, Decimal) else value
            for key, value in user_data.items()
        }
        
        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps({
                'success': True,
                'user': {
                    'id': cleaned_user.get('id', ''),
                    'email': cleaned_user.get('email', ''),
                    'name': cleaned_user.get('name', '')
                },
                'search_method': 'id' if user_id else 'email'
            })
        }
        
    except Exception as e:
        return error_response(500, 'Internal server error', str(e))