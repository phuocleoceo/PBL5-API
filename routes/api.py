from endpoints import user, userRequest, history
from fastapi import APIRouter

router = APIRouter()
router.include_router(user.router)
router.include_router(userRequest.router)
router.include_router(history.router)
