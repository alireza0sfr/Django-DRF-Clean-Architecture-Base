from abc import ABC, abstractmethod

class IMapper(ABC):
    
    @abstractmethod
    def map(cls, dto, model):
      pass