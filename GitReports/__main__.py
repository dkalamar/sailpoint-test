import logging
from datetime import datetime, timedelta

from GitReports.email import SendGrid

from .db import TestDB
from .github_service import GithubService
from .report import ReportBuilder

logging.info(msg="Loading Reports")

git = GithubService()
db = TestDB()
mail = SendGrid()

for ext, recipients in db.iter_repos():
    try:
        repo = git.hub.get_repo(ext)
        rb = ReportBuilder(repo)
        html = rb.build(cutoff=datetime.utcnow() - timedelta(days=7))
        logging.info(msg=f"Sending Report for {ext}")
        mail.send(recipients, 'Test', html)
    except Exception as err:
        logging.error(str(err))

logging.info(msg="Reports Complete")
