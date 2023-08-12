from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.user import User as UserModel
# from models.orders import Order as OrderModel
from models.addtocart import Add_to_Cart as AddToCartModel
from config import db
from fastapi.encoders import jsonable_encoder
from bson import ObjectId, json_util
from services import host,port,password,r,json

router = APIRouter()
collection = db["users"]

@router.post('/add')
async def addUser(user:UserModel):
    try:
        user = user.model_dump()
        result = await collection.insert_one(user)
    except Exception as e:
        print(e)
    return {"message": "User created successfully "}

@router.get('/{id}')
async def getUserDetail(id:str):
    try:
        cached_response = r.get(f'user_detail:{id}')
        if cached_response:
            return JSONResponse(content=jsonable_encoder(cached_response.decode('UTF-8')))
        
        result = await collection.find_one({"_id":ObjectId(id)})
        if result:
            result['cart'] = [str(item) for item in result.get('cart', [])]
            user = UserModel(**result)
            r.setex(f'user_detail:{id}',1200,json.dumps(result))
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error retrieving user")


@router.put('user/{id}')
async def updateUser(id:str, update_data:UserModel):
    try:
        result = await collection.update_one({"_id":ObjectId(id)},{"$set": jsonable_encoder(update_data)})
        if result.modified_count == 1:
            return {"message": "User updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found or not updated")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating user")


@router.post('/add-to-cart/')
async def addToCart(cart:AddToCartModel, id:str):
    try: 
        response = await collection.update_one({"_id":ObjectId(id)}, {"$push":{"cart": ObjectId(cart.prodId)}})
        print(response)
        return {"message":"Product added succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating cart")
    

@router.get('cart-details/{id}')
async def getUserCart(id:str):
    try:
        cached_response = r.get(f'cart_products:{id}')
        if cached_response:
            return JSONResponse(content=jsonable_encoder(cached_response.decode('UTF-8')))
        
        response = collection.aggregate([
            {"$match": {"_id": ObjectId(id)}},
            {"$lookup": {
                "from": 'products',
                "localField": "cart",
                "foreignField": "_id",
                "as": "cart_details"
            }},
            {"$project": {"cart_details": 1, "_id": 0}}
        ])
        
        cart_list = []
        async for item in response:
            for document in item['cart_details']:
                document['_id'] = str(document['_id'])
                cart_list.append(document)
        r.setex(f'cart_products:{id}',1800,json.dumps(cart_list, default=json_util.default))
        return cart_list
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error updating cart")


@router.delete('delete-cart')
async def delFromCart(id:str, product):
    try:
        response = await collection.update_one({"_id": ObjectId(id)}, {"$pull": {'cart': ObjectId(product)}})
        return {"message":"Product removed succesfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error updating cart")