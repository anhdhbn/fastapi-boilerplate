import logging

import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from app.api.api import router
from app.core.config import settings
from app.core.logging import LOGGING_CONF
from app.helpers.exception_handler import (CustomException,
                                           fastapi_error_handler,
                                           http_exception_handler,
                                           validation_exception_handler)
from app.helpers.jaeger import setup_jaeger_app
from app.middlewares.log_request import LogRequestMiddleware

logging.config.dictConfig(LOGGING_CONF)

def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f'/openapi.json',
        docs_url='/docs', redoc_url="/re-doc",
        description=settings.PROJECT_NAME,
        debug=settings.DEBUG,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    application.add_middleware(LogRequestMiddleware)
    application.add_middleware(CorrelationIdMiddleware)

    application.include_router(router=router, prefix='/api')
    application.add_exception_handler(CustomException, http_exception_handler)
    application.add_exception_handler(RequestValidationError, validation_exception_handler)
    application.add_exception_handler(Exception, fastapi_error_handler)

    if settings.JAEGER_ENABLED and settings.JAEGER_MODE:
        setup_jaeger_app(app=application)

    return application

app = get_application()

if __name__ == '__main__':
    uvicorn.run(app)
