"""
Runs all the unit tests
"""

from lily_unit_test import TestRunner

options = {
    'create_html_report': True,
    'open_in_browser': True,
    'no_log_files': True
}

TestRunner.run('../src', options)
