from abc import ABC, abstractmethod
class IValidator(ABC):

    @abstractmethod
    def validate(self, value):
        pass

    @abstractmethod
    def message_generator(self, value):
        pass