from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings

engine = create_engine(url=settings.DATABASE_URL, pool_pre_ping=True, future=True)

def get_session() -> Generator:
    with Session(bind=engine, autocommit=False, autoflush=True) as session:
        yield session
