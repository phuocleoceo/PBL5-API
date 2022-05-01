from .PyObjectId import PyObjectId
from pydantic import BaseModel
from typing import List


class User(BaseModel):
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
