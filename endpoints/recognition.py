from fastapi import APIRouter, File, UploadFile
from models.ResponseModel import ResponseModel
from models.recognition import Recognition
import numpy as np
import cv2


router = APIRouter(
    prefix="/recognition",
    tags=["Recognition"],
    responses={404: {"description": "Not found"}},
)


@router.post("/get_identity/")
async def get_identity(image: UploadFile = File(...)):
    image = read_image(await image.read())
    # Mock predict
    predict = Recognition(identity=str(image.shape), distance=0.5)
    return ResponseModel(predict, 200, "Recognition successfully.", False)


def read_image(file: bytes):
    # Convert bytes sang OpenCV nparray
    img = np.asarray(bytearray(file), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img
