from abc import ABC, abstractmethod
class IValidator(ABC):

    @staticmethod
    @abstractmethod
    def validate(value):
        pass

    @staticmethod
    @abstractmethod
    def message_generator(value):
        pass