from fastapi import APIRouter

from backend.api.admin.routes import router as admin_router
from backend.api.auth.routes import router as auth_router
from backend.api.fraud.routes import router as fraud_router
from backend.api.helpdesk.routes import router as helpdesk_router
from backend.api.transactions.routes import router as tx_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(tx_router, prefix="/transactions", tags=["transactions"])
api_router.include_router(fraud_router, prefix="/fraud", tags=["fraud"])
api_router.include_router(helpdesk_router, prefix="/helpdesk", tags=["helpdesk"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
