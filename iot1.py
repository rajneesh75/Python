import boto3
import os
from dotenv import load_dotenv

load_dotenv()
print("Loaded:", os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_SECRET_ACCESS_KEY"), os.getenv("REGION_NAME"))

iot = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("REGION_NAME")
)

iot(
    topic='rajneesh/sensor/temp',
    qos=1,
    payload='{"temperature": 25.5}'
)
