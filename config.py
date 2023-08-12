from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))

if client:
    print("******MongoDB connection successful.******")
else:
    print("connection failed!")

db = client["ecommerce"]