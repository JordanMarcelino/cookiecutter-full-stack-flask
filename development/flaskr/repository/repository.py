from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Generic
from typing import TypeVar
from typing import Union

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    @abstractmethod
    def get(self, id: Union[int | str]) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def add(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: Union[int | str]) -> None:
        raise NotImplementedError
