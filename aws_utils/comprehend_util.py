import boto3
from aws_utils import aws_keys

REGION_NAME = 'us-east-1'

comprehend = boto3.client('comprehend', region_name=REGION_NAME, aws_access_key_id=aws_keys.comprehend_access_key_id,
                          aws_secret_access_key=aws_keys.comprehend_secret_access_key)


def detect_language(text):
    response = comprehend.detect_dominant_language(
        Text=text
    )
    language = max(response['Languages'], key=lambda x: x['Score'])
    language_code = language['LanguageCode']
    print(language_code)
    return language_code
