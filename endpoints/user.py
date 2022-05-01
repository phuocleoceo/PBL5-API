from database.user import read_user, read_user_by_id, create_user, update_user, delete_user
from fastapi import APIRouter
from models.user import User


router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)
