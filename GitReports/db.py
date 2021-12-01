from abc import ABC, abstractmethod
from collections import defaultdict, namedtuple
from typing import Iterator, List

Document = namedtuple('Document', ['github_ext', 'user_email'])


class DB(ABC):
    def __init__(self):
        self._authenticate()

    @abstractmethod
    def _authenticate(self, ):
        pass

    @abstractmethod
    def _pull_documents(self) -> List[Document]:
        pass

    def iter_repos(self) -> Iterator:
        groups = defaultdict(list)
        for doc in self._pull_documents():
            groups[doc.github_ext].append(doc.user_email)
        return groups.items()


class TestDB(DB):
    def _authenticate(self):
        pass

    def _pull_documents(self) -> List[Document]:
        return [
            Document('mui-org/material-ui-x', 'sample.data1@gmail.com'),
            Document('mui-org/material-ui-x', 'sample.email2@gmail.com')
        ]
