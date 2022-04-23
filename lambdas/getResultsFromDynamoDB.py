import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    name = event['name']
    
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('cse546')
    
    response = table.scan(FilterExpression=Attr('name').eq(name))
    data = response['Items']
    print(response, data)
    return data
    