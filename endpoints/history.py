from fastapi import APIRouter

router = APIRouter(
    prefix="/history",
    tags=["History"],
    responses={404: {"description": "Not found"}},
)
