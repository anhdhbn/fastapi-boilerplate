import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings

from app.helpers.enums import JaegerModeEnum

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'Fastapi project')
    DEBUG: bool = os.getenv('DEBUG', 'False')
    BACKEND_CORS_ORIGINS = ['*']
    
    # db
    DATABASE_URL = os.getenv('SQL_DATABASE_URL', 'sqlite:///.db')

    # logging
    LOGGING_PARAMS_REQUEST_ENABLED: bool = os.getenv('LOGGING_PARAMS_REQUEST_ENABLED', 'False')
    LOGGING_BODY_REQUEST_ENABLED: bool = os.getenv('LOGGING_BODY_REQUEST_ENABLED', 'False')
    LOGGING_EXCLUDED_URL = os.getenv('LOGGING_EXCLUDED_URL', '/api/healthcheck,/docs,/re-doc,/openapi.json')


    # Jaeger logging
    JAEGER_ENABLED: bool = os.getenv('JAEGER_ENABLED', 'False')
    JAEGER_INSECURE: bool = os.getenv('JAEGER_INSECURE', 'True')
    JAEGER_MODE: Optional[JaegerModeEnum] = os.getenv('JAEGER_MODE', None)
    JAEGER_EXCLUDED_URLS = os.getenv('JAEGER_EXCLUDED_URLS', '/api/healthcheck,/docs,/re-doc,/openapi.json')
    JAEGER_COLLECTOR_ENDPOINT = os.getenv('JAEGER_COLLECTOR_ENDPOINT', '')
    JAEGER_HOST = os.getenv('JAEGER_HOST', 'localhost')
    JAEGER_PORT = int(os.getenv('JAEGER_PORT', '6831'))
    JAEGER_SAMPLING_RATE = float(os.getenv('JAEGER_SAMPLING_RATE', '1'))

settings = Settings()
