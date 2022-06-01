from database.user import (read_user, read_user_by_id, create_user,
                           save_image_user, update_user, delete_user)
from models.ResponseModel import ResponseModel
from models.user import UserUpsert, UserImage
from fastapi import APIRouter
import json

# Load cloudinary config
with open("./config.json", "r") as file:
    config = json.load(file)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)
