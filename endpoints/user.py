from database.user import read_user, read_user_by_id, create_user, update_user, delete_user
from models.ResponseModel import ResponseModel
from models.user import UserUpsert
from fastapi import APIRouter


router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read():
    products = await read_user()
    return ResponseModel(products, 200, "Users retrieved successfully.", False)


@router.get("/{id}")
async def read_by_id(id: str):
    product = await read_user_by_id(id)
    return ResponseModel(product, 200, "User retrieved successfully.", False)


@router.post("/")
async def create(user: UserUpsert):
    user_dict = user.dict(by_alias=True)
    user_dict["FeatureVector"] = [[""]]
    new_user = await create_user(user_dict)
    return ResponseModel(new_user, 200, "User added successfully.", False)


@router.put("/")
async def update(id: str, user: UserUpsert):
    user_dict = user.dict(by_alias=True)
    updated_user = await update_user(id, user_dict)
    return ResponseModel(updated_user, 200, "User updated successfully.", False)


@router.delete("/")
async def delete(id: str):
    deleted_user = await delete_user(id)
    return ResponseModel(deleted_user, 200, "Product deleted successfully.", False)
