from abc import ABC, abstractmethod


class IRedisService(ABC):

    @staticmethod
    @abstractmethod
    def delete_by_prefix(key: str):
        pass
