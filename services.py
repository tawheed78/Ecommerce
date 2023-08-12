import redis, json
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("HOST")
port = os.getenv("PORT")
password = os.getenv("PASSWORD")

r = redis.Redis(
  host=host,
  port=port,
  password=password)