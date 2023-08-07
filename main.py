from fastapi import FastAPI
from routers.user import router as userRouter
from routers.product import router as productRouter


app = FastAPI()

app.include_router(userRouter, prefix="/users")

app.include_router(productRouter, prefix="/products")