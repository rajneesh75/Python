import boto3
import os
from dotenv import load_dotenv

load_dotenv()


boto_session = boto3.Session(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                             aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                             region_name=os.getenv("REGION_NAME"))

ec2 = boto3.client(
    'ec2',
    aws_access_key_id=os.getenv("aws_access_key_id"),
    aws_secret_access_key=os.getenv("aws_secret_access_key"),
    region_name=os.getenv("REGION_NAME")
)

# List running EC2 instances
response = ec2.describe_instances()
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        print(f"Instance ID: {instance['InstanceId']} - State: {instance['State']['Name']}")