"""
Test runner class.
Runs all test suites from a specific package (recursive)
"""

import inspect
import os
import shutil

from unit_test.models.logger import Logger
from unit_test.test_suite import TestSuite


class TestRunner(object):

    project_path = os.path.dirname(os.path.dirname(__file__))
    output_folder = os.path.join(project_path, 'test_reports')

    ###########
    # Private #
    ###########

    @classmethod
    def _populate_test_suites(cls, root_path):
        test_suites = []
        for current_folder, sub_folders, filenames in os.walk(root_path):
            sub_folders.sort()
            for filename in filter(lambda x: x.endswith('.py'), filenames):
                import_path = '{}.{}'.format(current_folder[len(cls.project_path) + 1:].replace(os.sep, '.'),
                                             filename.replace('.py', ''))
                module = __import__(import_path, fromlist=['*'])
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if inspect.isclass(attribute):
                        classes = inspect.getmro(attribute)
                        if len(classes) > 2 and TestSuite in classes:
                            test_suites.append(attribute)

        return test_suites

    ##########
    # Public #
    ##########

    @classmethod
    def run(cls, package, tests_to_run=None):
        if tests_to_run is None:
            tests_to_run = []
        if os.path.isdir(cls.output_folder):
            shutil.rmtree(cls.output_folder)
        os.makedirs(cls.output_folder)

        test_runner_log = Logger(False)

        package_folder = os.path.dirname(package.__file__)
        test_suites = cls._populate_test_suites(package_folder)
        if len(tests_to_run) > 0:
            test_suites = list(filter(lambda x: x.__name__ in tests_to_run, test_suites))
        n_test_suites = len(test_suites)
        n_digits = len(str(n_test_suites))
        report_name_format = '{{:0{}d}}_{{}}.txt'.format(n_digits)
        if n_test_suites > 0:
            n_test_suites_passed = 0
            test_runner_log.info('Run {} test suites from folder: {}'.format(n_test_suites, package_folder))

            for i, test_suite in enumerate(test_suites):
                test_suite_name = test_suite.__name__
                test_runner_log.empty_line()
                test_runner_log.info('Run test suite: {}'.format(test_suite_name))
                ts = test_suite()
                result = ts.run()
                if result is None or result:
                    n_test_suites_passed += 1
                    test_runner_log.info('Test suite {}: PASSED'.format(test_suite_name))
                else:
                    test_runner_log.info('Test suite {}: FAILED'.format(test_suite_name))

                with open(os.path.join(cls.output_folder, report_name_format.format(i + 2, test_suite_name)), 'w') as fp:
                    fp.writelines(map(lambda x: '{}\n'.format(x), ts.log.get_log_messages()))

            test_runner_log.empty_line()
            ratio = 100 * n_test_suites_passed / n_test_suites
            test_runner_log.info('{} of {} test suites passed ({:.1f}%)'.format(n_test_suites_passed, n_test_suites, ratio))
            if n_test_suites == n_test_suites_passed:
                test_runner_log.info('Test runner result: PASSED')
            else:
                test_runner_log.error('Test runner result: FAILED')

        else:
            test_runner_log.info('No test suites found in folder: {}'.format(package_folder))

        test_runner_log.shutdown()
        with open(os.path.join(cls.output_folder, report_name_format.format(1, 'test_runner')), 'w') as fp:
            fp.writelines(map(lambda x: '{}\n'.format(x), test_runner_log.get_log_messages()))


if __name__ == '__main__':

    from unit_test import test_classes

    TestRunner.run(test_classes)
