import logging

from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from app.core.dependencies import lang_header
from app.i18n.lang import MultiLanguage
from app.schemas.sche_base import DataResponse, ResponseSchemaBase

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/live", response_model=ResponseSchemaBase, response_class=ORJSONResponse)
async def get(lang: MultiLanguage = Depends(lang_header)):
    return ResponseSchemaBase().success_response(lang)

@router.get("/ready", response_model=DataResponse[str], response_class=ORJSONResponse)
async def get(lang: MultiLanguage = Depends(lang_header)):
    return DataResponse().success_response(None, lang)
