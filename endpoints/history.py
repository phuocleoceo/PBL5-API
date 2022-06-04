from database.history import read_history, read_history_by_user_id, create_history
from models.ResponseModel import ResponseModel
from models.history import HistoryUpsert
from fastapi import APIRouter

router = APIRouter(
    prefix="/history",
    tags=["History"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read():
    histories = await read_history()
    return ResponseModel(histories, 200, "Histories retrieved successfully.", False)


@router.get("/{id}")
async def read_by_user_id(id: str):
    history = await read_history_by_user_id(id)
    return ResponseModel(history, 200, "UserRequest retrieved successfully.", False)


@router.post("/")
async def create(history: HistoryUpsert):
    history_dict = history.dict(by_alias=True)
    new_history = await create_history(history_dict)
    return ResponseModel(new_history, 200, "History added successfully.", False)
