"""
Test class for use with the unit test.
"""

from unit_test.test_suite import TestSuite


class TestClassSetupFailException(TestSuite):

    def setup(self):
        _a = 1 / 0

    def test_01_pass_by_return_none(self):
        return None

    def test_02_pass_by_return_true(self):
        return True


if __name__ == '__main__':
    TestClassSetupFailException().run()
