import boto3
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)

load_dotenv()
print("Loaded:", os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_SECRET_ACCESS_KEY"), os.getenv("REGION_NAME"))

session = boto3.Session(region_name=os.getenv("REGION_NAME"),
                        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                        )
s3 = session.resource('s3')
s3.meta.client.upload_file(Filename='train1.csv', Bucket='rajneesh-bucket1', Key='s3_output_key')
print("✅ File uploaded to S3")


