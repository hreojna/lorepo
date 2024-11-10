import logging
from typing import Generic, TypeVar, Type

from psycopg2 import errors
from sqlalchemy import exc
from sqlmodel import SQLModel, Session

T = TypeVar('T', bound=SQLModel)

logger = logging.getLogger(__name__)

class BaseRepository(Generic[T]):
    def __init__(self, session, base: Type[T]):
        self.__session: Session = session
        self.__base = base

    @property
    def session(self):
        return self.__session

    def add(self, obj: T) -> T:
        try:
            self.session.add(obj)
        except exc.IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.UniqueViolation):
                logger.warning(f'The {obj} is already in the table {obj.__tablename__}')
            else:
                raise e
        else:
            self.session.commit()
            logger.info(f'Added new {obj} to the table {obj.__tablename__}')
        return obj