from models.history import History
from .driver import Database

database = Database()


async def read_history():
    histories = []
    db = await database.db_connection()
    #### Người quen thì nối với user để lấy ra tên #####
    cursor = db.history.aggregate([
        {"$match": {'userId': {'$nin': ['UNKNOWN']}}},
        {"$addFields": {"userId": {"$toObjectId": "$userId"}}},
        {"$lookup": {
            "from": "user",
            "localField": "userId",
            "foreignField": "_id",
            "as": "linked_user"
        }}])
    if cursor:
        async for history in cursor:
            history["userId"] = str(history["userId"])
            history["fullname"] = history["linked_user"][0]["fullname"]
            history["room"] = history["linked_user"][0]["room"]
            del history["linked_user"]
            histories.append(History(**history))
    #### Người lạ thì thôi #####
    cursor = db.history.find({"userId": "UNKNOWN"})
    if cursor:
        async for history in cursor:
            history["fullname"] = "Người lạ"
            history["room"] = "Chưa thuê phòng"
            histories.append(History(**history))
    return histories


async def read_history_by_user_id(id: str):
    db = await database.db_connection()
    cursor = db.history.find({"userId": id})
    histories = []
    if cursor:
        async for history in cursor:
            histories.append(History(**history))
        return histories
    return histories


async def create_history(history_data: dict):
    db = await database.db_connection()
    history = await db.history.insert_one(history_data)
    new_history = await db.history.find_one({"_id": history.inserted_id})
    return History(**new_history)
