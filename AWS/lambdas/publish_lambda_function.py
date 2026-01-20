import math
import boto3
import json
from decimal import Decimal

# Get dynamodb resource
dynamodb = boto3.resource('dynamodb')
def lambda_handler(event, context):
   
    # JSON object from IoT core has timestamp field
    if 'timestamp' in event:
        # Get table
        table = dynamodb.Table('dht22_poc_table')
        
        # Put item into table
        response = table.put_item(
        Item={
        'app_id': "sensor", # Primary key
        'timestamp': event['timestamp'], # Sort key
        'temp': event['temp'],
        'hum': event['hum']
        }
        )
        
        # Print put_item response
        print(response)
        
        # Get recently written item
        response = table.get_item(
        Key={'app_id': "sensor", 'timestamp': event['timestamp']}
        )
        
        # Print get_item response
        #print(response)
        
        # Print table scan results
        #print(table.scan()['Items'])
        table = dynamodb.Table('dht22_poc_ws_connection_id')
   
        response = table.get_item(
        Key={'app_id': "connectionid"}
        )
        print(response)
        
        if 'Item' in response:
            api_client = boto3.client('apigatewaymanagementapi',endpoint_url='https://bpcy4gu0ld.execute-api.us-east-1.amazonaws.com/production')
            connectionId=response['Item']['id']
            api_client.post_to_connection(ConnectionId=connectionId, Data=json.dumps({'temp': event['temp'],'hum':event['hum']}))
            print(connectionId)
        
        
        # Return
        return "DB updated"
    
    