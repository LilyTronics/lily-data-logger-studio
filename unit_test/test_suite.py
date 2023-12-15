"""
Test suite class.
"""

from unit_test.models.logger import Logger


class TestSuite(object):

    def __init__(self, logger=None):
        self.log = Logger() if logger is None else logger

    def run(self):
        test_suite_name = self.__class__.__name__
        self.log.info('Run test suite: {}'.format(test_suite_name))

        n_tests = 0
        n_passed = 0
        try:
            test_methods = sorted(list(filter(lambda x: x.startswith('test_'), dir(self))))
            n_tests = len(test_methods)
            assert n_tests > 0, 'No methods starting with test_ found'

            # Run the setup
            self.setup()

            # Run the test methods
            for test_method in test_methods:
                test_case_name = '{}.{}'.format(test_suite_name, test_method)
                self.log.info('Run test case: {}'.format(test_case_name))
                try:
                    method_result = getattr(self, test_method)()
                    if method_result is None or method_result:
                        n_passed += 1
                        self.log.info('Test case {}: PASSED'.format(test_case_name))
                    else:
                        self.log.error('Test case {}: FAILED'.format(test_case_name))

                except Exception as e:
                    self.log.error('Test case {}: FAILED by exception: {}'.format(test_case_name, e))

            # Run the teardown
            self.teardown()

        except Exception as e:
            self.log.error('Test suite {}: FAILED by exception: {}'.format(test_suite_name, e))

        if n_tests > 0:
            ratio = 100 * n_passed / n_tests
            result = '{} of {} tests passed ({:.1f}%)'.format(n_passed, n_tests, ratio)
            if n_tests == n_passed:
                self.log.info('Test suite {}: PASSED, {}'.format(test_suite_name, result))
            else:
                self.log.error('Test suite {}: FAILED, {}'.format(test_suite_name, result))

        self.log.shutdown()

    ##############################
    # Override these when needed #
    ##############################

    def setup(self): pass
    def teardown(self): pass


if __name__ == '__main__':

    from unit_test.test_classes.test_class_empty import TestClassEmpty
    from unit_test.test_classes.test_class_pass import TestClassPass
    from unit_test.test_classes.test_class_fail import TestClassFail

    test_suite_classes = [
        TestClassEmpty,
        TestClassPass,
        TestClassFail
    ]

    for test_suite_class in test_suite_classes:
        test_suite_class().run()
        print()
