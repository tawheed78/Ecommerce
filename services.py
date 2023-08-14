import redis, json
from dotenv import load_dotenv
import os
import boto3

load_dotenv()

host = os.getenv("HOST")
port = os.getenv("PORT")
password = os.getenv("PASSWORD")
region_name = os.getenv("AWS_REGION")
aws_access_key_id = os.getenv("ACCESS_KEY")
aws_secret_access_key = os.getenv("SECRET_ACCESS_KEY")
queue_url = os.getenv("QUEUE_URL")

r = redis.Redis(
  host=host,
  port=port,
  password=password)


sqs = boto3.client(
    'sqs',
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

queue_url = queue_url