from fastapi import FastAPI
from routers.user import router as userRouter


app = FastAPI()

app.include_router(userRouter, prefix="/users")