from fastapi import FastAPI
from route import router
from model import Base
from database import engine
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000)
