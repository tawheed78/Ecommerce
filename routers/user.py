from fastapi import APIRouter, HTTPException
from models.user import User as UserModel
from config import db
# from controllers.user import User as userService
from bson import ObjectId

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
        result = await collection.find_one({"_id":ObjectId(id)})
        if result:
            user = UserModel(**result)
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving user")


# @router.put('/{id}')
# async def updateUser(id:str):
#     try:
#         result = await collection.update_one({"id":ObjectId(id)})
