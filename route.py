from fastapi import APIRouter, responses, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exc
from model import Base, Users, URLS
from database import session_local, get_db
from schema import UserCreate, UserResponse, URLCreate, URLResponse
import secrets
import string

router = APIRouter()


def generate_short_code(length: int = 6) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


# @router.get("/me")
# async def get_me():
#     return


@router.post("/post/url", response_model=URLResponse)
async def create_short_url(url: URLCreate, db: Session = Depends(get_db)):
    short_code = generate_short_code()
    exist = db.query(URLS).filter(URLS.id == short_code).first()
    while exist:
        short_code = generate_short_code()
    new_url = URLS(id=short_code, url=str(url.url))
    try:
        db.add(new_url)
        db.commit()
        db.refresh(new_url)
    except exc.SQLAlchemyError as e:
        db.rollback()
    return new_url


@router.get("/{short}")
async def redirect(short: str, db: Session = Depends(get_db)):
    url_entry = db.query(URLS).filter(URLS.id == short).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return responses.RedirectResponse(url=url_entry.url, status_code=302)
