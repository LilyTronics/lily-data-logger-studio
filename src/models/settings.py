"""
Model for storing and recalling the application settings.
"""

import json
import os
import lily_unit_test

from src.app_data import AppData


class Settings(object):

    def __init__(self):
        self._settings_file = os.path.join(AppData.USER_FOLDER,  "%s.json" % AppData.EXE_NAME)

    def _read_settings(self):
        d = {}
        try:
            with open(self._settings_file, 'r') as fp:
                d = json.load(fp)
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass

        return d

    def _write_settings(self, settings):
        with open(self._settings_file, 'w') as fp:
            json.dump(settings, fp, indent=2)

    def _get_property(self, main_key, sub_key, default=None):
        d = self._read_settings()
        return d.get(main_key, {}).get(sub_key, default)

    def _store_property(self, main_key, sub_key, value):
        d = self._read_settings()
        if main_key not in d.keys():
            d[main_key] = {}
        d[main_key][sub_key] = value
        self._write_settings(d)

    ########################
    # Main window settings #
    ########################

    def get_main_window_size(self):
        return self._get_property('main_window', 'width', -1), self._get_property('main_window', 'height', -1)

    def store_main_window_size(self, width, height):
        self._store_property('main_window', 'width', width)
        self._store_property('main_window', "height", height)

    def get_main_window_position(self):
        return self._get_property('main_window', 'left', -1), self._get_property('main_window', 'top', -1)

    def store_main_window_position(self, left, top):
        self._store_property('main_window', 'left', left)
        self._store_property('main_window', 'top', top)

    def get_main_window_maximized(self):
        return self._get_property('main_window', 'maximized', False)

    def store_main_window_maximized(self, is_maximized):
        self._store_property('main_window', 'maximized', is_maximized)

    #######################
    # Log window settings #
    #######################

    def get_log_window_size(self):
        return self._get_property('log_window', 'width', -1), self._get_property('log_window', 'height', -1)

    def store_log_window_size(self, width, height):
        self._store_property('log_window', 'width', width)
        self._store_property('log_window', "height", height)

    def get_log_window_position(self):
        return self._get_property('log_window', 'left', -1), self._get_property('log_window', 'top', -1)

    def store_log_window_position(self, left, top):
        self._store_property('log_window', 'left', left)
        self._store_property('log_window', 'top', top)

    def get_log_window_maximized(self):
        return self._get_property('log_window', 'maximized', False)

    def store_log_window_maximized(self, is_maximized):
        self._store_property('log_window', 'maximized', is_maximized)


class TestSetting(lily_unit_test.TestSuite):

    def setup(self):
        self._settings = Settings()
        if os.path.isfile(self._settings._settings_file):
            os.remove(self._settings._settings_file)

    def test_main_window_size(self):
        self.fail_if(self._settings.get_main_window_size() != (-1, -1), 'Default settings incorrect')
        self._settings.store_main_window_size(100, 100)
        self.fail_if(self._settings.get_main_window_size() != (100, 100), 'Failed storing settings')

    def test_main_window_position(self):
        self.fail_if(self._settings.get_main_window_position() != (-1, -1), 'Default settings incorrect')
        self._settings.store_main_window_position(10, 10)
        self.fail_if(self._settings.get_main_window_position() != (10, 10), 'Failed storing settings')

    def test_main_window_maximized(self):
        self.fail_if(self._settings.get_main_window_maximized(), 'Default settings incorrect')
        self._settings.store_main_window_maximized(True)
        self.fail_if(not self._settings.get_main_window_maximized(), 'Failed storing settings')
        self._settings.store_main_window_maximized(False)

    def test_log_window_size(self):
        self.fail_if(self._settings.get_log_window_size() != (-1, -1), 'Default settings incorrect')
        self._settings.store_log_window_size(200, 200)
        self.fail_if(self._settings.get_log_window_size() != (200, 200), 'Failed storing settings')

    def test_log_window_position(self):
        self.fail_if(self._settings.get_log_window_position() != (-1, -1), 'Default settings incorrect')
        self._settings.store_log_window_position(20, 20)
        self.fail_if(self._settings.get_log_window_position() != (20, 20), 'Failed storing settings')

    def test_log_window_maximized(self):
        self.fail_if(self._settings.get_log_window_maximized(), 'Default settings incorrect')
        self._settings.store_log_window_maximized(True)
        self.fail_if(not self._settings.get_log_window_maximized(), 'Failed storing settings')
        self._settings.store_log_window_maximized(False)


if __name__ == '__main__':

    TestSetting().run()
