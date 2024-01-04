"""
Our own test suite class derived from the lily-unit-test test suite.
"""

import lily_unit_test


class TestSuite(lily_unit_test.TestSuite):
    pass


if __name__ == '__main__':

    class _TestClass(TestSuite):
        pass

    _TestClass().run()
    