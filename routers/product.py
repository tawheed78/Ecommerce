from fastapi import APIRouter, HTTPException
from models.product import Product as ProductModel
from config import db
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

router = APIRouter()
collection = db["products"]

@router.post('/create-product/')
async def createProduct(product:ProductModel):
    try:
        product_dict = jsonable_encoder(product)
        response = await collection.insert_one(product_dict)
        # return response
    except Exception as e:
        print(e)
    return {"message": "Product created successfully "}

@router.get('/products/')
async def getAllProducts():
    try:
        products = await collection.find({}).to_list(length=10)
        prod_list = []
        for item in products:
            item['title'] = str(item['title'])
            prod_list.append(item['title'])
        if prod_list:
            return prod_list
        else:
            raise HTTPException(status_code=500, detail="No products found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving products")
    
@router.get('/product/{id}')
async def getProduct(id:str):
    try:
        result = await collection.find_one({"_id":ObjectId(id)})
        if result:
            product = ProductModel(**result)
            return product
        else:
            raise HTTPException(status_code=500, detail="No product found with the mentioned Id")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving products")
    

@router.put('product/{id}')
async def updateProduct(id:str, update_data:ProductModel):
    try:
        result = await collection.update_one({"_id":ObjectId(id)},{"$set": jsonable_encoder(update_data)})
        if result.modified_count == 1:
            return {"message": "Product updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Product not found or not updated")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating Product")