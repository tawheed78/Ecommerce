# from fastapi import APIRouter, HTTPException
# from models.orders import Order as OrderModel
# from config import db
# from fastapi.encoders import jsonable_encoder
# from bson import ObjectId

# router = APIRouter()
# collection = db["orders"]

# @router.post('/add-to-cart/')
# async def addToCart(cart):
#     response = await collect