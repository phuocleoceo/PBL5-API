from pydantic import BaseModel, Field
from .PyObjectId import PyObjectId
from typing import Optional, List


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str
    password: str
    fullname: str
    gender: str
    address: str
    mobile: str
    indentityNumber: str
    role: str
    image: List
    FeatureVector: List


class UserUpsert(BaseModel):
    username: str
    password: str
    fullname: str
    gender: str
    address: str
    mobile: str
    indentityNumber: str
    role: str
    image: List
