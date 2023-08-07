from fastapi import APIRouter, HTTPException
from models.user import User as UserModel
from config import db
# from controllers.user import User as userService
from fastapi.encoders import jsonable_encoder
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


@router.put('user/{id}')
async def updateUser(id:str, update_data:UserModel):
    try:
        # json_compatible_user_data = jsonable_encoder(update_data)
        # collection[id] = json_compatible_user_data
        result = await collection.update_one({"_id":ObjectId(id)},{"$set": jsonable_encoder(update_data)})
        if result.modified_count == 1:
            return {"message": "User updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found or not updated")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating user")

