from abc import ABC, abstractmethod

from common.models.models import Match


class BaseStrategy(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def prenext(self):
        pass

    @abstractmethod
    def next(self, match):
        pass

    @abstractmethod
    def reset(self):
        pass
