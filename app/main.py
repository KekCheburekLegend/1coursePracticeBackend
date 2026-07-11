from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import uvicorn
import os
import sys
from pathlib import Path
from bd_SQLite.encode import *
from bd_SQLite.Work_with_BD import *

app = FastAPI()


@app.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest):
    original_url = str(request.url)
    short_Link = Path_new_url(original_url)
    return URLResponse(
        short_url=f"http://localhost:8000/{short_Link}",
        original_url=original_url,
    )


@app.get("/{short_Link}")
def redirect_to_url(short_Link: str):

    link = Try_find_short(short_Link)
    if link is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    return RedirectResponse(
        url=link,
        status_code=302
    )
