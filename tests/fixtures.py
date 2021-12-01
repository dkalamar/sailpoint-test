import pytest
from github.Repository import Repository
from GitReports.github_service import GithubService


@pytest.fixture(scope='session')
def sample_ext() -> str:
    return 'mui-org/material-ui-x'


@pytest.fixture(scope='session')
def sample_repo() -> Repository:
    git = GithubService()
    repo = git.hub.get_repo('mui-org/material-ui-x')
    yield repo
