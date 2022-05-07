from pydantic import BaseModel


class Predict(BaseModel):
    identity: str
    distance: float
