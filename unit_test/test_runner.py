"""
Test runner class.
Runs all test suites from a specific package (recursive)
"""

import inspect
import os

from unit_test.models.logger import Logger


class TestRunner(object):

    @classmethod
    def _populate_test_suites(cls, root_path):
        project_path = os.path.dirname(os.path.dirname(__file__))
        test_suites = []
        for current_folder, sub_folders, filenames in os.walk(root_path):
            sub_folders.sort()
            for filename in filenames:
                if filename.endswith('.py'):
                    print(current_folder, filename)
                    module_name = filename.replace('.py', '')
                    import_path = current_folder[len(project_path) + 1:].replace(os.sep, '.') + '.' + module_name
                    module = __import__(import_path, fromlist=['*'])
                    print(module)
                    for attribute_name in dir(module):
                        attribute = getattr(module, attribute_name)
                        if inspect.isclass(attribute):
                            classes = inspect.getmro(attribute)
                            print(classes)

        return test_suites

    @classmethod
    def run(cls, package):
        log = Logger()
        package_folder = os.path.dirname(package.__file__)
        test_suites = cls._populate_test_suites(package_folder)

        #log.info('Run all test suites from folder: {}'.format(package_folder))

        log.shutdown()


if __name__ == '__main__':

    from unit_test import test_classes

    TestRunner.run(test_classes)
