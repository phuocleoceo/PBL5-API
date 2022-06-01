from fastapi import Depends, HTTPException, status
from models.user import UserLogin, Token, User, TokenData
from fastapi.security import OAuth2PasswordBearer
from models.PyObjectId import PyObjectId
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from .driver import Database
import json


database = Database()

# Load cluster url từ file json
with open("./config.json", "r") as file:
    config = json.load(file)

SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = config["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = config["ACCESS_TOKEN_EXPIRE_MINUTES"]


crypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta):
    """
    Hàm tạo AccessToken
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    """
    Hàm xác thực mật khẩu gốc vs mật khẩu đã được hash
    """
    return crypt_context.verify(plain_password, hashed_password)


async def get_user_by_un(username: str):
    try:
        db = await database.db_connection()
        user = await db.user.find_one({"username": username})
        return User(**user)
    except User.DoesNotExist:
        return None


async def authenticate(username, password):
    """
    Hàm tổng hợp : kiểm tra thông tin đăng nhập có đúng không
    """
    try:
        user = await get_user_by_un(username)
        password_check = verify_password(password, user["password"])
        return password_check
    except User.DoesNotExist:
        return False


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_un(token_data.username)
    if user is None:
        raise credentials_exception
    return user
