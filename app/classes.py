from pydantic import BaseModel, HttpUrl, Field
from typing import Optional


class URLRequest(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    short_url: str
    original_url: str