from models.PyObjectId import PyObjectId
from models.userRequest import UserRequest
from .driver import Database

database = Database()


async def read_userRequest():
    db = await database.db_connection()
    cursor = db.userRequest.find({})
    userRequests = []
    if cursor:
        async for userRequest in cursor:
            userRequests.append(UserRequest(**userRequest))
        return userRequests
    return userRequests


async def read_userRequest_by_id(id: str):
    db = await database.db_connection()
    userRequest = await db.userRequest.find_one({"_id": PyObjectId(id)})
    if userRequest:
        return UserRequest(**userRequest)
    return None


async def create_userRequest(userRequest_data: dict):
    db = await database.db_connection()
    userRequest = await db. userRequest.insert_one(userRequest_data)
    new_userRequest = await db. userRequest.find_one({"_id": userRequest.inserted_id})
    return UserRequest(**new_userRequest)
