from fastapi import APIRouter, Depends

from app.api.api_v1 import api_healthcheck
from app.middlewares.log_request import log_request_body

router = APIRouter(dependencies=[Depends(log_request_body)])

router.include_router(api_healthcheck.router, tags=["Healthcheck"], prefix="/healthcheck")
