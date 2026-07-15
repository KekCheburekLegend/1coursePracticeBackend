from fastapi import APIRouter, responses, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy import exc
from model import Users, URLS
from database import session_local, get_db
from schema import URLCreate, URLResponse, StatsResponse
import secrets
import string
from auth_jwt import get_current_user

router = APIRouter()


def generate_short_code(length: int = 7) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


@router.post("/post/url", response_model=URLResponse)
async def create_short_url(url: URLCreate, db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
    result = await db.execute(
        select(URLS).where(
            URLS.url == str(url.url),
            URLS.user_id == current_user.id
        )
    )
    existing_url = result.scalar_one_or_none()

    if existing_url:
        return URLResponse(
            id=existing_url.id,
            url=existing_url.url,
            click=existing_url.click
        )

    short_code = generate_short_code()
    new_url = URLS(
        id=short_code,
        url=str(url.url),
        user_id=current_user.id
    )
    db.add(new_url)
    await db.commit()
    await db.refresh(new_url)

    return URLResponse(
        id=new_url.id,
        url=new_url.url,
        click=new_url.click
    )


@router.get("/{short}")
async def redirect(short: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(URLS).where(URLS.id == short)
    )
    url_entry = result.scalar_one_or_none()

    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")
    url = url_entry.url
    await db.execute(
        update(URLS)
        .where(URLS.id == short)
        .values(click=URLS.click + 1)
    )
    try:
        await db.commit()
    except exc.SQLAlchemyError:
        raise HTTPException(status_code=500, detail="BD ERROR")
    return responses.RedirectResponse(url=url, status_code=302)


@router.get("/stats/url", response_model=StatsResponse)
async def get_stats(short: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(URLS).where(URLS.id == short)
    )
    url = result.scalar_one_or_none()
    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return StatsResponse(id_url=url.id, full_url=url.url, click=url.click)


@router.get("/stats/my-urls", response_model=list[URLResponse])
async def get_my_urls(
    current_user: Users = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(URLS).where(URLS.user_id == current_user.id)
    )
    urls = result.scalars().all()
    return [
        URLResponse(
            id=url.id,
            url=url.url,
            click=url.click
        )
        for url in urls
    ]
