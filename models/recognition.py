from pydantic import BaseModel


class Recognition(BaseModel):
    identity: str
    distance: float
