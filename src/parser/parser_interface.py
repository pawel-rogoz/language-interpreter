from abc import ABC, abstractmethod


class ParserInterface(ABC):
    @abstractmethod
    def parse_program(self):
        pass
