import os

from main import run
from models import Scandata


def remove_test_report(report_path):
    os.remove(report_path)
    dirname = os.path.dirname(report_path)
    if not os.listdir(dirname):
        os.rmdir(dirname)


def test_main_run_function():
    report_path = run()
    scans_counts = Scandata.select().count()

    assert os.path.isfile(report_path)

    remove_test_report(report_path)

    assert scans_counts > 0