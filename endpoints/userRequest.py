from database.userRequest import read_userRequest, read_userRequest_by_id, create_userRequest
from models.ResponseModel import ResponseModel
from models.userRequest import UserRequestUpsert
from fastapi import APIRouter

router = APIRouter(
    prefix="/userRequest",
    tags=["UserRequest"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read():
    products = await read_userRequest()
    return ResponseModel(products, 200, "UserRequest retrieved successfully.", False)


@router.get("/{id}")
async def read_by_id(id: str):
    product = await read_userRequest_by_id(id)
    return ResponseModel(product, 200, "UserRequest retrieved successfully.", False)


@router.post("/")
async def create(userRequest: UserRequestUpsert):
    userRequest_dict = userRequest.dict(by_alias=True)
    new_userRequest = await create_user(userRequest_dict)
    return ResponseModel(new_userRequest, 200, "User Request added successfully.", False)
