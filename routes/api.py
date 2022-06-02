from endpoints import user, userRequest, history, auth
from fastapi import APIRouter

router = APIRouter()
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(userRequest.router)
router.include_router(history.router)
