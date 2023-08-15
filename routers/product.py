from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.product import Product as ProductModel
from config import db
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
import redis, json
from services import host,password,port,json,r


try:
    response = r.ping()
    print("Connected to Redis Cloud:", response)
except redis.exceptions.ConnectionError:
    print("Could not connect to Redis Cloud")
    
cache_key = "cache:/products/"
r.delete(cache_key)

router = APIRouter()
collection = db["products"]

@router.post('/create-product/')
async def createProduct(product:ProductModel):
    try:
        product_dict = jsonable_encoder(product)
        response = await collection.insert_one(product_dict)
        
    except Exception as e:
        print(e)
    return {"message": "Product created successfully "}

    
@router.get('/products/')
async def getAllProducts():
    try:
        cached_response =  r.get('products_list')
        if cached_response:
            return JSONResponse(content=json.loads(cached_response.decode('UTF-8')))
        else:
            products = await collection.find({}).to_list(length=10)
            prod_list = []
            for item in products:
                item['title'] = str(item['title'])
                prod_list.append(item['title'])
            if prod_list:
                r.setex('products_list',300,json.dumps(prod_list))
                return prod_list
            else:
                raise HTTPException(status_code=500, detail="No products found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving products")
    

@router.get('/product-detail/{id}')
async def getProduct(id:str):
    try:
        cached_response = r.get('product')
        if cached_response:
            return JSONResponse(content=json.loads(cached_response.decode('UTF-8')))
        else:
            result = await collection.find_one({"_id":ObjectId(id)})
            if result:
                product = ProductModel(**result)
                r.setex('product',120,json.dumps(product))
                return product
            else:
                raise HTTPException(status_code=500, detail="No product found with the mentioned Id")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving products")
    

@router.put('/update-product/{id}')
async def updateProduct(id:str, update_data:ProductModel):
    try:
        result = await collection.update_one({"_id":ObjectId(id)},{"$set": jsonable_encoder(update_data)})
        if result.modified_count == 1:
            return {"message": "Product updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Product not found or not updated")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating Product")
    

@router.delete('delete-product/{id}/')
async def deleteProduct(id:str):
    try:
        result = await collection.find_one({"_id":ObjectId(id)})
        if result:
            collection.delete_one({"_id":ObjectId(id)})
            return {"message": "Product deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting Product")