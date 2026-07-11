from fastapi import FastAPI
from route import router
from model import Base
from database import engine
Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(router)


