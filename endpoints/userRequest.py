from fastapi import APIRouter

router = APIRouter(
    prefix="/userRequest",
    tags=["UserRequest"],
    responses={404: {"description": "Not found"}},
)
