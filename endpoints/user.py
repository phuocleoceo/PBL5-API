from database.user import (read_user, read_user_by_id, create_user,
                           save_image_user, update_user, delete_user)
from models.ResponseModel import ResponseModel
from models.user import UserUpsert, UserImage
from fastapi import APIRouter
import cloudinary
import json

# Load cloudinary config
with open("./config.json", "r") as file:
    config = json.load(file)

# Cấu hình Cloudinary
cloudinary.config(
    cloud_name=config["cloud_name"],
    api_key=config["api_key"],
    api_secret=config["api_secret"]
)


router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read():
    """
    Hàm lấy về danh sách user
    """
    products = await read_user()
    return ResponseModel(products, 200, "Users retrieved successfully.", False)


@router.get("/{id}")
async def read_by_id(id: str):
    """
    Hàm lấy user theo id
    """
    product = await read_user_by_id(id)
    return ResponseModel(product, 200, "User retrieved successfully.", False)


@router.post("/")
async def create(user: UserUpsert):
    """
    Hàm tạo user, bỏ trống 2 trường image và FeatureVector
    """
    user_dict = user.dict(by_alias=True)
    user_dict["image"] = [""]
    user_dict["FeatureVector"] = [[""]]
    new_user = await create_user(user_dict)
    return ResponseModel(new_user, 200, "User added successfully.", False)


@router.post("/save_image")
async def save_image(user_image: UserImage):
    """
    Hàm lưu ảnh vào MongoDB cho user, trả về link của ảnh trên Cloudinary
    """
    list_url = await save_image_user(user_image.user_id, user_image.image)
    return ResponseModel(list_url, 200, "Save image successfully.", False)


@router.put("/")
async def update(id: str, user: UserUpsert):
    """
    Hàm cập nhật thông tin cho user
    """
    user_dict = user.dict(by_alias=True)
    updated_user = await update_user(id, user_dict)
    return ResponseModel(updated_user, 200, "User updated successfully.", False)


@router.delete("/")
async def delete(id: str):
    """
    Hàm xóa user theo id
    """
    deleted_user = await delete_user(id)
    return ResponseModel(deleted_user, 200, "Product deleted successfully.", False)
