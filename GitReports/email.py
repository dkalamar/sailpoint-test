from abc import ABC, abstractmethod
from typing import List

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .config import Config


class EmailService(ABC):
    def __init__(self):
        self._authenticate()

    @abstractmethod
    def _authenticate(self):
        pass

    @abstractmethod
    def send(self, recipients: List[str], subject: str, body: str):
        pass


class TestMail(EmailService):
    def _authenticate(self):
        pass

    def send(self, recipients: List[str], subject: str, body: str):
        body = f"""
        <!--
            To: {'; '.join(recipients)}
            Subject: {subject}
        -->
        """ + body
        with open('tmp/sample_build.html', 'w') as fp:
            fp.write(body)


class SendGrid(EmailService):
    def _authenticate(self):
        self.sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        if not Config.SENDGRID_EMAIL:
            raise ValueError("Config SENDGRID_EMAIL must be set")
        self.from_email = Config.SENDGRID_EMAIL

    def send(self, recipients: List[str], subject: str, body: str):
        message = Mail(from_email=self.from_email,
                       to_emails=recipients,
                       subject=subject,
                       html_content=body)
        _ = self.sg.send(message)
