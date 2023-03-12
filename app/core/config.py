import os

from dotenv import load_dotenv
from pydantic import BaseSettings

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


settings = Settings()
