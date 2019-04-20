import boto3
from aws_utils import aws_keys

TABLE_NAME = 'GitTrendingRepo'
PRIMARY_KEY = 'url'
SORT_KEY = 'language'

REGION_NAME = 'ap-south-1'

dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME, aws_access_key_id=aws_keys.dynamodb_access_key_id,
                          aws_secret_access_key=aws_keys.dynamodb_secret_access_key)


def insert_data(data):
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item={key: value for key, value in data.items() if value})


def check_if_exists(p_key, sort_key):
    table = dynamodb.Table(TABLE_NAME)
    response = table.get_item(Key={PRIMARY_KEY: p_key, SORT_KEY : sort_key})
    return 'Item' in response


