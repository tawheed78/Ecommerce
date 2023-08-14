from fastapi import FastAPI
from routers.user import router as userRouter
from routers.product import router as productRouter
from routers.orders import router as orderRouter


app = FastAPI()

app.include_router(userRouter)

app.include_router(productRouter)

app.include_router(orderRouter)