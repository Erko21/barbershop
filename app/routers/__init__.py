from fastapi import APIRouter

from .auth import router as auth_router
from .propositions import router as proposition_router
from .records import router as record_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(proposition_router)
router.include_router(record_router)
