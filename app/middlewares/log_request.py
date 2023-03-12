import logging
import re
import typing

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.config import settings
from app.helpers.enums import ContentTypeEnum
from app.helpers.re import SPACES_AND_TAB_REGEX

logger = logging.getLogger(__name__)

class LogRequestMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.excluded_urls = [url for url in settings.LOGGING_EXCLUDED_URL.split(',') if url]

    async def dispatch(self, request: Request, call_next: typing.Awaitable[Response]):
        if settings.LOGGING_PARAMS_REQUEST_ENABLED and not self.path_is_in_excluded_urls(path=request.scope.get('path')):
            await self.log_request(request)
        response: Response = await call_next(request)
        return response
    
    async def log_request(self, request: Request):
        log_dict = {
            'Method': request.method,
            'Path': request.scope.get('path'),
            'Params': request.query_params,
        }

        log_str = await self.build_log_str_from_dict(log_dict)
        logger.info(f"Incoming request: {log_str}")
    
    def path_is_in_excluded_urls(self, path: str):
        for url in self.excluded_urls:
            if url in path:
                return True
        return False

    async def build_log_str_from_dict(self, dict: dict):
        arr_log = [f"{k}: {v if v else None}" for k, v in dict.items()]
        return ', '.join(arr_log)

def get_content_type(dict: dict):
    for k, v in dict.items():
        if k.lower() == 'content-type':
            return v

async def log_request_body(request: Request):
    # Log request body in api_router instead of middleware.
    if settings.LOGGING_BODY_REQUEST_ENABLED:
        content_type = get_content_type(request.headers)
        if request.method.upper() != 'GET' and content_type == ContentTypeEnum.ApplicationJson.value:
            buff: bytes = await request.body()
            body: str = re.sub(SPACES_AND_TAB_REGEX, "", buff.decode('utf-8'))
            logger.info(f"Request body: {body}")
