from models.PyObjectId import PyObjectId
from models.history import History
from .driver import Database

database = Database()

async def read_history():
    db = await database.db_connection()
    cursor = db.history.find({})
    histories = []
    if cursor:
        async for history in cursor:
            histories.append(History(**history))
        return histories
    return histories

async def read_history_by_id(id: str):
    db = await database.db_connection()
    history = await db.history.find_one({"_id": PyObjectId(id)})
    if history:
        return History(**history)
    return None


async def create_history(history_data: dict):
    db = await database.db_connection()
    history = await db.history.insert_one(history_data)
    new_history = await db.history.find_one({"_id": history.inserted_id})
    return History(**new_history)