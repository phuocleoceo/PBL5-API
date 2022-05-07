from models.recognition import Recognition, Image
from models.ResponseModel import ResponseModel
from fastapi import APIRouter
from typing import List
import numpy as np
import base64
import cv2


router = APIRouter(
    prefix="/recognition",
    tags=["Recognition"],
    responses={404: {"description": "Not found"}},
)


@router.post("/get_identity/")
async def get_identity(image: Image):
    image = read_image("data:image/png;base64,"+image.uri)
    # Mock predict
    predict = Recognition(identity=str(image.shape), distance=0.5)
    return ResponseModel(predict, 200, "Recognition successfully.", False)


def read_image(uri: str):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


@router.get("/svm/")
async def retrain_svm():
    pass


@router.post("/vector")
async def save_feature_vector(user_id: List):
    pass
