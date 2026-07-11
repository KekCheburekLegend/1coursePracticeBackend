from pydantic import BaseModel, HttpUrl, Field
from sqids import Sqids
from typing import Optional, Dict
import os

sqids = Sqids(
    min_length=6,
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
)


class URLRequest(BaseModel):
    url: HttpUrl
    custom_Link: Optional[str] = Field(None, min_length=6, max_length=9)  


class URLResponse(BaseModel):
    short_url: str
    original_url: str


def encode_url( id: int):
    url_id = id
    return sqids.encode([url_id])


def decode_code(Link: str):
    try:
        decoded = sqids.decode(Link)  
        return decoded[0] if decoded else None
    except:
        return None