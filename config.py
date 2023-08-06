from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb+srv://tawheed:xTHlamoaGlPhFZGq@cluster0.izcnild.mongodb.net/?retryWrites=true&w=majority")

if client:
    print("******MongoDB connection successful.******")
else:
    print("connection failed!")

db = client["ecommerce"]