from pydantic import BaseModel, HttpUrl


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class URLCreate(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    id: str
    url: str

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    id_url: str
    full_url: str
    click: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int
