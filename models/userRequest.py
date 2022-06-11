from pydantic import BaseModel, Field
from .PyObjectId import PyObjectId
from typing import Optional, List
from bson import ObjectId
import datetime


class UserRequest(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    userId: str
    timestamps: str
    imageUri: str
    response: str
    fullname: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class UserRequestUpsert(BaseModel):
    userid: str
    timestamps: str
    imageUri: str
    response: str
