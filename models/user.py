from pydantic import BaseModel, Field
from .PyObjectId import PyObjectId
from typing import Optional, List
from bson import ObjectId


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str
    password: str
    fullname: str
    gender: str
    address: str
    mobile: str
    identityNumber: str
    floor: int
    room: str
    role: str
    image: List[str]
    FeatureVector: List[List]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class UserUpsert(BaseModel):
    username: str
    password: str
    fullname: str
    gender: str
    address: str
    mobile: str
    identityNumber: str
    floor: int
    room: str
    role: str


class UserImage(BaseModel):
    user_id: str
    image: List[str]


class UserInfor(BaseModel):
    fullname: str
    gender: str
    address: str
    mobile: str
    identityNumber: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
