from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl, Field
from sqids import Sqids
from typing import Optional, Dict
import uvicorn
from datetime import datetime, timedelta
import os

app = FastAPI()

sqids = Sqids(
    min_length=6,
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
)

url_storage: Dict[str, str] = {}
reverse_lookup: Dict[str, str] = {}
counter = 1

class URLRequest(BaseModel):
    url: HttpUrl
    custom_Link: Optional[str] = Field(None, min_length=6, max_length=9)  

class URLResponse(BaseModel):
    short_url: str
    original_url: str

def encode_url(url: str):
    global counter
    url_id = counter
    counter += 1
    return sqids.encode([url_id])

def decode_code(Link: str):
    try:
        decoded = sqids.decode(Link)  
        return decoded[0] if decoded else None
    except:
        return None

@app.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest):
    global counter
    original_url = str(request.url)
    
    # Проверка существующей ссылки
    if original_url in reverse_lookup:
        short_Link = reverse_lookup[original_url]
        return URLResponse(
            short_url=f"http://localhost:8000/{short_Link}",
            original_url=original_url
        )
    
    # Проверка пользовательской ссылки
    if request.custom_Link:  
        if request.custom_Link in url_storage:
            raise HTTPException(
                status_code=409,  
                detail=f"Custom Link '{request.custom_Link}' is already taken"
            )
        
        # Проверка блоклиста
        if hasattr(sqids, 'blocklist') and request.custom_Link in sqids.blocklist:
            raise HTTPException(
                status_code=400,  # Было status_Link=400
                detail=f"Link '{request.custom_Link}' is not allowed"
            )
        
        short_Link = request.custom_Link
        reverse_lookup[original_url] = short_Link
        url_storage[short_Link] = original_url  # Добавлено сохранение
    else:
        # Генерация короткой ссылки
        short_Link = encode_url(original_url)
        
        while short_Link in url_storage:
            short_Link = encode_url(original_url + str(counter))
        
        reverse_lookup[original_url] = short_Link
        url_storage[short_Link] = original_url
    
    return URLResponse(
        short_url=f"http://localhost:8000/{short_Link}",
        original_url=original_url,
    )

@app.get("/{short_Link}")
def redirect_to_url(short_Link: str):
    if short_Link not in url_storage:
        raise HTTPException(
            status_code=404,  # Было status_Link=404
            detail="Short URL not found"
        )
    
    original_url = url_storage[short_Link]
    return RedirectResponse(
        url=original_url, 
        status_code=302  
    )