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
    requests = await read_userRequest()
    return ResponseModel(requests, 200, "UserRequest retrieved successfully.", False)


@router.get("/{id}")
async def read_by_id(id: str):
    request = await read_userRequest_by_id(id)
    return ResponseModel(request, 200, "UserRequest retrieved successfully.", False)


@router.post("/")
async def create(userRequest: UserRequestUpsert):
    userRequest_dict = userRequest.dict(by_alias=True)
    new_userRequest = await create_userRequest(userRequest_dict)
    return ResponseModel(new_userRequest, 200, "User Request added successfully.", False)
