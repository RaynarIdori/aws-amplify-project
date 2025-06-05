import json
import requests
from datetime import datetime

def handler(event, context):
    print('received event:', event)
    
    headers = {
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    }
    
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur"
        api_headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": "CG-x6GZDvgEMRyp4JJDjeyuxqJm"
        }
        
        response = requests.get(url, headers=api_headers)
        response.raise_for_status()
        
        crypto_data = response.json()
        timestamp = datetime.now().isoformat()
        
        print(f"Successfully fetched {len(crypto_data)} cryptocurrencies from CoinGecko API")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': f'Successfully fetched {len(crypto_data)} cryptocurrencies',
                'timestamp': timestamp,
                'data': crypto_data
            })
        }
            
    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Failed to fetch crypto data'})
        }
    
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Internal server error'})
        }