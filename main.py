from fastapi import FastAPI
from routers.user import router as userRouter
from routers.product import router as productRouter
from routers.orders import router as orderRouter


app = FastAPI()

app.include_router(userRouter, prefix="/users")

app.include_router(productRouter, prefix="/products")

app.include_router(orderRouter, prefix="/orders")