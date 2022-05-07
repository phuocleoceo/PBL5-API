from pydantic import BaseModel
from typing import List


class Recognition(BaseModel):
    identity: str
    distance: float


class Image(BaseModel):
    uri: str
