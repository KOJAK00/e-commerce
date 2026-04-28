from typing import List,Optional
from pydantic import BaseModel,ConfigDict,EmailStr
import hashing
from datetime import date

class user(BaseModel):
    username : str
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_verified: bool
    join_date: date

    class Config:
        from_attributes = True
class BusinessCreate(BaseModel):
    business_name: str
    city: str
    region: str
    business_description: str | None = None
    logo: Optional[str] = None
class BusinessResponse(BaseModel):
    id: int
    business_name: str
    city: str
    region: str
    business_description: str | None
    logo: Optional[str] | None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None