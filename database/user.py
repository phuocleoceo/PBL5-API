from models.PyObjectId import PyObjectId
from models.user import User
from .driver import Database

database = Database()


async def read_user():
    db = await database.db_connection()
    cursor = db.user.find({})
    users = []
    if cursor:
        async for user in cursor:
            users.append(User(**user))
        return users
    return users


async def read_user_by_id(id: str):
    db = await database.db_connection()
    user = await db.user.find_one({"_id": PyObjectId(id)})
    if user:
        return User(**user)
    return None


async def create_user(user_data: dict):
    db = await database.db_connection()
    user = await db.user.insert_one(user_data)
    new_user = await db.user.find_one({"_id": user.inserted_id})
    return User(**new_user)


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
