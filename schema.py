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


class token(BaseModel):
    access_token: str
    refresh_token: str
