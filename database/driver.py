import motor.motor_asyncio
import json

# Load cluster url từ file json
with open("../config.json", "r") as file:
    config = json.load(file)

MONGODB_URL = config["cluster"]
DATABASE_NAME = "pbl5"


class Database():
    def __init__(self) -> None:
        self.connected = False
        self.client = None

    async def db_connection(self):
        if self.connected == False:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
            self.connected = True
        return self.client[DATABASE_NAME]
