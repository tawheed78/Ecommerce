
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models.orders import Order as OrderModel
from config import db
from fastapi.encoders import jsonable_encoder
import json
from bson import ObjectId


router = APIRouter()
collection = db["users"]


@router.post('/place-order/')
async def placeOrder(id:str):
    try:
        order = await collection.aggregate([
            {"$match": {"_id": ObjectId(id)}},
            {"$project":{"cart":1,"_id":0}}
        ]).to_list(length=None)

        cart_item_ids = order[0].get('cart', [])

        order_total = 0
        for item_id in cart_item_ids:
            item = await db.products.find_one({"_id":ObjectId(item_id)})
            if item:
                price = item.get('price', 0)
                discounted_price = price.get('discounted_price',0)
                q = item['avail_quantity'] - 1
                await db.products.update_one({"_id":ObjectId(item_id)}, {"$set": {"avail_quantity": q}})
                order_total += discounted_price
        order_document = {
            "user_id" : id,
            "items" : cart_item_ids,
            "order_total": order_total,
            "order_date": {"$currentDate": True}
        }
        db.orders.insert_one(order_document)

        return {"message": "Order placed successfully"}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error placing order")
    

@router.get('orders/{id}')
async def getUserOrders(user_id:str):
    try:
        response = await db.orders.aggregate([
            {"$match": {"user_id": user_id}},
            {"$project": { "_id": 1}}
        ]).to_list(length=None)
    
        order_item_ids = [order['_id'] for order in response]
       
        order_list = []
        for item_id in order_item_ids:
            item = await db.orders.find_one({"_id": ObjectId(item_id)})

            item['_id'] = str(item['_id'])
            item['user_id'] = str(item['user_id'])
            item['items'] = [str(itm) for itm in item['items']]

            order_list.append(item)
            
        return order_list
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error retrieving previous orders")    
 