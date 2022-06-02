from models.user import UserLogin, User
from passlib.context import CryptContext
from .driver import Database


database = Database()
# Password Hash
crypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])


def get_password_hash(password):
    return crypt_context.hash(password)


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
    # Trả về khi đăng nhập thất bại
    fake_user = User(id="", username="", password="", fullname="", role="", gender="", address="",
                     mobile="", identityNumber="", floor=0, room="", image=[""], FeatureVector=[[""]])
    """
    Hàm tổng hợp : kiểm tra thông tin đăng nhập có đúng không
    """
    try:
        user = await get_user_by_un(username)
        # Không cần trả về các Vector đặc trưng (nặng)
        user.FeatureVector = [[""]]
        password_check = verify_password(password, user.password)
        # Đúng TK, MK thì trả về thông tin user luôn
        if password_check:
            return True, user
        else:
            return False, fake_user
    except:
        return False, fake_user
