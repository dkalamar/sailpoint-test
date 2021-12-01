import pytest
from GitReports.github_service import GithubService

from .fixtures import sample_ext


@pytest.mark.dependency
def test_github_connection(sample_ext):
    git = GithubService()
    repo = git.hub.get_repo(sample_ext)
    assert repo
