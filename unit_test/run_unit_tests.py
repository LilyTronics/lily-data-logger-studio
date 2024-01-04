"""
Runs all the unit tests
"""

import os

from lily_unit_test import TestRunner

options = {
    'report_folder': os.path.join(os.path.dirname(__file__), 'test_reports'),
    'create_html_report': True,
    'open_in_browser': True,
    'no_log_files': True,
    # Exclude our own test suite
    'exclude_test_suites': [
        'TestSuite'
    ]
}

TestRunner.run('../src', options)
