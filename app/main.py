from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from bd_SQLite.encode import *
from bd_SQLite.Work_with_BD import *
from bd_SQLite.func import * 

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


@app.get("/{short_Link}/status")
def get_status_for_user(short_Link):
    id_url = Get_ID(short_Link)
    if id_url is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )
    stats = Get_stats(id_url)
    
    return stats