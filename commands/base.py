from abc import ABC, abstractmethod
from main import Quick_Navigate


class BaseCommand(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.qn = Quick_Navigate()

    @abstractmethod
    def execute(self,):
        ...