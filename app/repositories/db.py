from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.helpers.jaeger import setup_jaeger_sqlalchemy

engine = create_engine(url=settings.DATABASE_URL, pool_pre_ping=True, future=True)

if settings.JAEGER_ENABLED and settings.JAEGER_MODE:
    setup_jaeger_sqlalchemy(engine=engine)

def get_session() -> Generator:
    with Session(bind=engine, autocommit=False, autoflush=True) as session:
        yield session
