from pydantic import BaseModel
from typing import List


class Recognition(BaseModel):
    identity: str
    distance: float


class Image(BaseModel):
    uri: str


class SVM_Train(BaseModel):
    train_acc: float
    test_acc: float
