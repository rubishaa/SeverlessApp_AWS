import boto3
import os
import json
from decimal import Decimal


def get_all_flights(event, context):
    table_name = os.environ.get('TABLEN', 'Flights') + "-"+os.environ.get('STAGE', 'dev')
    region = os.environ.get('REGION', 'us-east-1')
    aws_environment = os.environ.get('AWSENV')
    print (region)
    if aws_environment == 'AWS_SAM_LOCAL':
        flights_table = boto3.resource(
            'dynamodb',
            region_name=region,
            endpoint_url='http://127.0.0.1:8000'
        )
    else:
        flights_table = boto3.resource(
            'dynamodb',
            region_name=region
        )

    table = flights_table.Table(table_name)
    response = table.scan()
    print(response)
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'], cls=DecimalEncoder)
    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)