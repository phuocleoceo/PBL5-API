from models.ResponseModel import ResponseModel
from database.auth import authenticate
from models.user import UserLogin
from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
async def login(userLogin: UserLogin):
    username = userLogin.username
    password = userLogin.password
    password_check, user = await authenticate(username, password)
    if password_check:
        return ResponseModel(user, 200, "Login Successfully", False)
    else:
        return ResponseModel(user, 400, "Login Fail ! Incorrect username or password", True)
