from database.user import read_user, read_user_by_id, create_user, update_user, delete_user
from models.ResponseModel import ResponseModel
from models.user import User, UserUpsert
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
    pass


@router.put("/")
async def update(id: str, user_data: dict):
    pass


@router.delete("/")
async def delete(id: str):
    pass
