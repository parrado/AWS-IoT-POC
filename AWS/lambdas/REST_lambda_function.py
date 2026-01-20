import json
import boto3
from decimal import Decimal

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):
    # Get dynamodb resource
    dynamodb = boto3.resource('dynamodb')

    if event['resource']=='/data':
        # Get table
        table = dynamodb.Table('dht22_poc_table')
        # Print table scan results
        body=table.scan()['Items']
        return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body,cls=JSONEncoder)
        }


