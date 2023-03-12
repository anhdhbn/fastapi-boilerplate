from abc import ABC

from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.repositories.db import get_session


class AbstractRepository(ABC):
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
