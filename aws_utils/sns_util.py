import boto3
from aws_utils import aws_keys
import constants

REGION_NAME = 'ap-south-1'

sns = boto3.client('sns', region_name=REGION_NAME, aws_access_key_id=aws_keys.sns_access_key_id,
                   aws_secret_access_key=aws_keys.sns_secret_access_key)

TOPIC_ARN = 'arn:aws:sns:ap-south-1:041279377441:GitTrendingRepo'


def send_notification(msg):
    sns.publish(
        TopicArn=TOPIC_ARN,
        Message=msg,
        Subject=constants.GITHUB_TRENDING_REPOSITORY
    )
    print("sent message!")
