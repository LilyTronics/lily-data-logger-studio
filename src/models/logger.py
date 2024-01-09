"""
Logger for the application.
"""

import lily_unit_test
import os
import sys
import threading

from src.app_data import AppData
from datetime import datetime


class Logger(object):

    TYPE_INFO = 'INFO'
    TYPE_DEBUG = 'DEBUG'
    TYPE_ERROR = 'ERROR'
    TYPE_STDOUT = 'STDOUT'
    TYPE_STDERR = 'STDERR'

    _TIME_STAMP_FORMAT = '%Y%m%d %H:%M:%S.%f'
    _LOG_FORMAT = '{} | {:6} | {}\n'

    _FILENAME = os.path.join(AppData.USER_FOLDER, '%s.log' % AppData.EXE_NAME)

    class _StdLogger(object):

        def __init__(self, logger, std_type):
            self._logger = logger
            self._type = std_type

        def write(self, message):
            self._logger.handle_message(self._type, message)

        def flush(self):
            pass

    def __init__(self, log_to_stdout=False):
        self._log_to_stdout = log_to_stdout
        open(self._FILENAME, 'w').close()
        self._output = ''

        self._orgStdout = sys.stdout
        self._orgStderr = sys.stderr
        sys.stdout = self._StdLogger(self, self.TYPE_STDOUT)
        sys.stderr = self._StdLogger(self, self.TYPE_STDERR)

    @classmethod
    def get_filename(cls):
        return cls._FILENAME

    def shut_down(self):
        sys.stdout = self._orgStdout
        sys.stderr = self._orgStderr

    def info(self, message):
        self.handle_message(self.TYPE_INFO, '{}\n'.format(message))

    def debug(self, message):
        self.handle_message(self.TYPE_DEBUG, '{}\n'.format(message))

    def error(self, message):
        self.handle_message(self.TYPE_ERROR, '{}\n'.format(message))

    def handle_message(self, message_type, message_text):
        timestamp = datetime.now().strftime(self._TIME_STAMP_FORMAT)[:-3]
        self._output += message_text
        while '\n' in self._output:
            index = self._output.find('\n')
            message = self._LOG_FORMAT.format(timestamp, message_type, self._output[:index])
            self._output = self._output[index + 1:]
            with open(self._FILENAME, 'a') as fp:
                fp.write(message)
            if self._log_to_stdout:
                self._orgStdout.write(message)


class TestLogger(lily_unit_test.TestSuite):

    _TEST_MESSAGES = [
        ('info', 'This is an info message'),
        ('debug', 'This is a debug message'),
        ('error', 'This is a error message'),
        ('stdout', 'This is a standard output message'),
        ('info', 'This is a\nmulti line message'),
    ]

    @staticmethod
    def _generate_error():
        _dummy = 1 / 0

    def setup(self):
        self._logger = Logger()

    def test_log_file_empty(self):
        filename = self._logger.get_filename()
        with open(filename, 'r') as fp:
            content = fp.read().strip()
        self.fail_if(content != '', 'The log file is not empty')

    def test_logger(self):
        for message in self._TEST_MESSAGES:
            if message[0] == 'info':
                self._logger.info(message[1])
            elif message[0] == 'debug':
                self._logger.debug(message[1])
            elif message[0] == 'error':
                self._logger.error(message[1])
            elif message[0] == 'stdout':
                print(message[1])

        filename = self._logger.get_filename()
        with open(filename, 'r') as fp:
            lines = list(map(lambda x: x.rstrip(), fp.readlines()))
        self.fail_if(len(lines) == 0, 'The log file is empty')

        for message in self._TEST_MESSAGES:
            # Split up multi line messages
            parts = message[1].split('\n')
            n_found = 0
            for part in parts:
                for line in lines:
                    if line.endswith('| {}'.format(part)) and '| {:6} |'.format(message[0].upper()) in line:
                        n_found += 1
            if n_found != len(parts):
                self.fail('Message {} not found in the log file'.format(message))

    def test_exception(self):
        # Clear the file
        filename = self._logger.get_filename()
        open(filename, 'w').close()
        # To prevent this from failing, we generate an error in a thread
        t = threading.Thread(target=self._generate_error)
        t.start()
        while t.is_alive():
            pass

        with open(filename, 'r') as fp:
            lines = list(map(lambda x: x.rstrip(), fp.readlines()))
        self.fail_if(len(lines) == 0, 'The log file is empty')
        self.fail_if(len(lines) < 4, 'The log file has less than 4 lines')

        for line in lines:
            self.fail_if('| STDERR |' not in line, 'Message is not type STDERR {}'.format(line))

        self.fail_if('| STDERR | Exception in thread Thread-1 (_generate_error):' not in lines[0],
                     'First line does not match with the exception message {}'.format(lines[0]))

        self.fail_if('| STDERR | Traceback (most recent call last):' not in lines[1],
                     'Second line does not match with the traceback message {}'.format(lines[1]))

        self.fail_if('| STDERR | ZeroDivisionError: division by zero' not in lines[-1],
                     'Last line does not match with the division by zero message {}'.format(lines[-1]))

    def teardown(self):
        self._logger.shut_down()


if __name__ == "__main__":

    TestLogger().run()
