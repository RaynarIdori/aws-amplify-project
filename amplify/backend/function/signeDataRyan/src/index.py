import json
import boto3
import os
from datetime import datetime
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def handler(event, context):
    print('received event:', event)

    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3')

    dynamodb_table_name = os.environ.get('STORAGE_CRYPTOPRICESRYAN_NAME')
    s3_bucket_name = "ryanawsb92b69ae7d62437b86e9b13f73c3e8f3b4f61-ryan"

    if not dynamodb_table_name:
        print("Error: STORAGE_CRYPTOPRICESRYAN_NAME environment variable not set.")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'DynamoDB table name environment variable not set'})
        }
    if not s3_bucket_name:
        print("Error: STORAGE_CRYPTOEXPORTBUCKETRYAN_BUCKETNAME environment variable not set.")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'S3 bucket name environment variable not set'})
        }

    table = dynamodb.Table(dynamodb_table_name)

    try:
        response = table.scan()
        items = response.get('Items', [])
        
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))

        print(f"Scanned {len(items)} items from DynamoDB table {dynamodb_table_name}")

        try:
            items.sort(key=lambda x: x.get('timestamp', '')) 
            print("Data sorted by timestamp.")
        except Exception as e:
            print(f"Warning: Could not sort data by timestamp. Proceeding with unsorted data. Error: {str(e)}")


        timestamp_str = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        file_name = f"crypto_{timestamp_str}.json"
        s3_key = f"exports/{file_name}"
        
        json_data = json.dumps(items, cls=DecimalEncoder, indent=4)
        print(f"Generated JSON data for S3. File name will be: {file_name}")

        s3.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=json_data, ContentType='application/json')
        print(f"Successfully uploaded {file_name} to S3 bucket {s3_bucket_name} at key {s3_key}")

        presigned_url = s3.generate_presigned_url('get_object',
            Params={'Bucket': s3_bucket_name, 'Key': s3_key},
            ExpiresIn=3600
        )
        print(f"Generated pre-signed URL: {presigned_url}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'message': 'Export successful', 'presigned_url': presigned_url})
        }

    except Exception as e:
        print(f"Error during Lambda execution: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }