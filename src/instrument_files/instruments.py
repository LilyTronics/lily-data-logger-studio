"""
Package containing the instrument files.
"""

import glob
import json
import lily_unit_test
import os


JSON_PATH = os.path.dirname(__file__)


def get_list_of_instrument_names():
    names = []
    for filename in glob.glob(os.path.join(JSON_PATH, '*.json')):
        data = json.load(open(filename, 'r'))
        names.append(data['name'])

    return names


def get_instrument_data_by_name(name):
    for filename in glob.glob(os.path.join(JSON_PATH, '*.json')):
        data = parse_json_file(filename)
        if name == data['name']:
            return data

    return {}


def parse_json_file(filename):
    data = {}
    try:
        data = json.load(open(filename, 'r'))
    except Exception as e:
        raise Exception('Error loading JSON file {}:\n{}'.format(filename, e))

    return data


class TestInstrumentNames(lily_unit_test.TestSuite):

    EXPECTED_NAMES = ['Multimeter UDP', 'Temperature chamber UDP']

    def test_01_list_names(self):
        result = True
        names = get_list_of_instrument_names()
        for name in self.EXPECTED_NAMES:
            if name not in names:
                self.log.error('Instrument {} is not in the list'.format(name))
                result = False

        for name in names:
            if name not in self.EXPECTED_NAMES:
                self.log.error('Instrument {} is in the list, but not expected'.format(name))
                result = False

        return result

    def test_02_get_instrument_data(self):
        result = True
        names = get_list_of_instrument_names()
        for name in names:
            data = get_instrument_data_by_name(name)
            if 'name' not in data.keys():
                self.log.error('Instrument with name {} is not found'.format(name))
                result = False

        data = get_instrument_data_by_name('not_existing_instrument')
        if 'name' in data.keys():
            self.log.error('Instrument with name not_existing_instrument is found, but should not be found')
            result = False

        return result

    def test_03_invalid_files(self):
        n_failed = 0
        for filename in ['empty.json']:
            file_path = os.path.join(os.path.dirname(__file__), 'invalid_files', filename)
            try:
                parse_json_file(file_path)
                self.log.error('Loading file {} passed, but expected to fail'.format(filename))
                n_failed += 1
            except Exception as e:
                if file_path not in str(e):
                    self.log.error('The error message did not contain the filename {}'.format(filename))
                    self.log.debug(e)
                    n_failed += 1

        return n_failed == 0


if __name__ == '__main__':

    TestInstrumentNames().run()