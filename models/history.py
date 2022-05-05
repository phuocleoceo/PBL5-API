from pydantic import BaseModel, Field
from .PyObjectId import PyObjectId
from typing import Optional, List
from bson import ObjectId


class History(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    timestamps: str
    imageURi: str
    isVerify: str
    userId: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class HistoryUpsert(BaseModel):
    timestamps: str
    imageURi: str
    isVerify: str
    userId: str
