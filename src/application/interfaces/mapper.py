from abc import ABC, abstractmethod

class IMapper(ABC):

    @classmethod
    @abstractmethod
    def map(cls, dto, model):
      pass