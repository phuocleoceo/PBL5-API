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
    indentityNumber: str
    role: str
    image: List
    FeatureVector: List

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
    indentityNumber: str
    role: str
    image: List
