from models.recognition import Recognition, Image, SVM_Train
from models.ResponseModel import ResponseModel
from Face.Inference.Facenet import Facenet
from Face.Classifier.SVM import SVM
from fastapi import APIRouter
from typing import List
import numpy as np
import base64
import cv2

fn = Facenet()
svm = SVM()

router = APIRouter(
    prefix="/recognition",
    tags=["Recognition"],
    responses={404: {"description": "Not found"}},
)


@router.post("/get_identity/")
async def get_identity(image: Image):
    image = read_image(image.uri)
    # Mock predict
    identity, distance = fn.Get_People_Identity_SVM(image)[0]
    # Kết quả nhận dạng 1 người
    predict = Recognition(identity=identity, distance=distance)
    # Phản hồi kết quả
    return ResponseModel(predict, 200, "Recognition successfully.", False)


def read_image(uri: str):
    # Chuyển phần mã hóa base64 sang cv2 array
    nparr = np.fromstring(base64.b64decode(uri), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


@router.get("/svm/")
async def retrain_svm():
    train_acc, test_acc = svm.train()
    svm_train = SVM_Train(train_acc=train_acc, test_acc=test_acc)
    return ResponseModel(svm_train, 200, "Train SVM successfully.", False)


@router.post("/vector")
async def save_feature_vector(user_id: List):
    pass
