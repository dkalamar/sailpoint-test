from github import Github

from .config import Config


class GithubService:
    def __init__(self):
        self._hub = None
        self.connect(Config.GITHUB_ACCESS_TOKEN)

    def connect(self, token=None):
        self._hub = Github(login_or_token=token)

    @property
    def hub(self):
        return self._hub
