from models.PyObjectId import PyObjectId
from .driver import Database

database = Database()


async def read_user():
    db = await database.db_connection()
    users = await db.user.find({})
    if users:
        return to_user_list(users)
    return None


async def read_user_by_id(id: str):
    db = await database.db_connection()
    user = await db.user.find_one({"_id": PyObjectId(id)})
    if user:
        return to_user(user)
    return None


async def create_user(user_data: dict):
    db = await database.db_connection()
    user = await db.user.insert_one(user_data)
    new_user = await db.user.find_one({"_id": user.inserted_id})
    return to_user(new_user)


async def update_user(id: str, user_data: dict):
    if len(user_data) < 1:
        return False
    db = await database.db_connection()
    user = await db.user.find_one({"_id": PyObjectId(id)})
    if user:
        user["username"] = user_data.get("username")
        user["password"] = user_data.get("password")
        user["fullname"] = user_data.get("fullname")
        user["gender"] = user_data.get("gender")
        user["address"] = user_data.get("address")
        user["mobile"] = user_data.get("mobile")
        user["indentityNumber"] = user_data.get("indentityNumber")
        user["role"] = user_data.get("role")
        user["image"] = user_data.get("image")
        user["FeatureVector"] = user_data.get("FeatureVector")
        updated_user = await db.user.update_one({"_id": PyObjectId(id)}, {"$set": user})
        return updated_user.acknowledged
    return False


async def delete_user(id: str):
    db = await database.db_connection()
    user = await db.user.find_one({"_id": PyObjectId(id)})
    if user:
        await db.user.delete_one({"_id": PyObjectId(id)})
        return True
    else:
        return False


def to_user(user) -> dict:
    return {
        "id": str(user.get("_id")),
        "username": user.get("username"),
        "password": user.get("password"),
        "fullname": user.get("fullname"),
        "gender": user.get("gender"),
        "address": user.get("address"),
        "mobile": user.get("mobile"),
        "indentityNumber": user.get("indentityNumber"),
        "role": user.get("role"),
        "image": user.get("image"),
        "FeatureVector": user.get("FeatureVector")
    }


def to_user_list(users) -> list:
    return [to_user(user) for user in users]
