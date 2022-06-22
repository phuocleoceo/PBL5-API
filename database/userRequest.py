from models.userRequest import UserRequest
from .driver import Database

database = Database()


async def read_userRequest():
    db = await database.db_connection()
    cursor = db.userRequest.aggregate([
        {"$addFields": {"userId": {"$toObjectId": "$userId"}}},
        {"$lookup": {
            "from": "user",
            "localField": "userId",
            "foreignField": "_id",
            "as": "linked_user"
        }}])
    userRequests = []
    if cursor:
        async for userRequest in cursor:
            userRequest["userId"] = str(userRequest["userId"])
            userRequest["fullname"] = userRequest["linked_user"][0]["fullname"]
            userRequest["room"] = userRequest["linked_user"][0]["room"]
            del userRequest["linked_user"]
            userRequests.append(UserRequest(**userRequest))
    return userRequests


async def create_userRequest(userRequest_data: dict):
    db = await database.db_connection()
    userRequest = await db. userRequest.insert_one(userRequest_data)
    new_userRequest = await db.userRequest.find_one({"_id": userRequest.inserted_id})
    new_userRequest["fullname"] = ""
    new_userRequest["room"] = ""
    return UserRequest(**new_userRequest)
