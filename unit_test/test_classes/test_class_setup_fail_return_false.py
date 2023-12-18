"""
Test class for use with the unit test.
"""

from unit_test.test_suite import TestSuite


class TestClassSetupFailReturnFalse(TestSuite):

    def setup(self):
        return False

    def test_dummy(self):
        return True


if __name__ == '__main__':
    TestClassSetupFailReturnFalse().run()
