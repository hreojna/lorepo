from typing import Generic, TypeVar, Type

from sqlmodel import SQLModel, Session

T = TypeVar('T', bound=SQLModel)


class BaseRepository(Generic[T]):
    def __init__(self, session, base: Type[T]):
        self.__session: Session = session
        self.__base = base
