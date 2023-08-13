from fastapi import APIRouter, HTTPException
from models.orders import Order as OrderModel
from config import db
from fastapi.encoders import jsonable_encoder
from bson import ObjectId, Timestamp

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
        order_place = db.orders.insert_one(order_document)

        return {"message": "Order placed successfully"}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error placing order")