from abc import ABC, abstractmethod
from typing import List


class EmailService(ABC):
    def __init__(self):
        self._authenticate()

    @abstractmethod
    def _authenticate(self, ):
        pass

    @abstractmethod
    def send(self, recipients: List[str], subject: str, body: str):
        pass


class TestMail(EmailService):
    def _authenticate(self):
        pass

    def send(self, recipients: List[str], subject: str, body: str):
        with open('tmp/sample_build.html', 'w') as fp:
            fp.write(body)
