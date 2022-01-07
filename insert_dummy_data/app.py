import boto3
import os
import json
from decimal import Decimal


# import requests
def handle(event, context):
    table_name = os.environ.get('TABLEN', 'Flights') + "-" + os.environ.get('STAGE', 'dev')
    region = os.environ.get('REGION', 'us-east-1')
    aws_environment = os.environ.get('AWSENV')
    s3_client = boto3.client('s3')

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
    bucket = os.environ.get('BUCKETNAME', '')
    json_file_name = event["Records"][0]["s3"]["object"]["key"]
    flights_object = s3_client.get_object(Bucket=bucket, Key=json_file_name)
    flights_file_reader = flights_object['Body'].read()
    flights_dit = json.loads(flights_file_reader, parse_float=Decimal)

    for flight in flights_dit:
        table.put_item(Item=flight)
    return {
        'statusCode': 200,
        'body': json.dumps('Done')
    }
