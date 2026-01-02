import sagemaker
from sagemaker.sklearn.estimator import SKLearn
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")
region_name = os.getenv("region_name")

print("Loaded:", aws_access_key_id, aws_secret_access_key, region_name)

boto_session = boto3.Session(aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key,
                             region_name=region_name)

sagemaker_session = sagemaker.Session(boto_session=boto_session)
role = 'arn:aws:iam::0368-6845-1123:role/SageMakerRole'

sklearn_estimator = SKLearn(
    entry_point='train.py',
    role=role,
    instance_type='ml.m5.xlarge',
    framework_version='0.23-1',
    sagemaker_session=sagemaker_session
)

sklearn_estimator.fit({'train': 's3://rajneesh-bucket1/train1.csv'})
