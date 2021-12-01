from datetime import datetime, timedelta

import pytest
from GitReports.report import ReportBuilder

from .fixtures import sample_repo


def test_report_build(sample_repo):
    rb = ReportBuilder(sample_repo)
    html = rb.build(cutoff=datetime.utcnow() - timedelta(days=7))
    assert html
