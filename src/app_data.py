"""
Application data
"""

import os
import sys


class AppData(object):
    APP_NAME = 'Lily Data Logger Studio'
    VERSION = '0.1'
    EXE_NAME = 'LilyDataLoggerStudio'
    USER_FOLDER = os.path.join(os.path.join(os.path.expanduser('~')), EXE_NAME)
    # Application path depends on if run from script or from the executable
    if EXE_NAME in sys.executable:
        APP_PATH = os.path.dirname(sys.executable)
    else:
        APP_PATH = os.path.dirname(os.path.dirname(__file__))


if __name__ == '__main__':

    print('App name   :', AppData.APP_NAME)
    print('App version:', AppData.VERSION)
    print('Exe name   :', AppData.EXE_NAME)
    print('User folder:', AppData.USER_FOLDER)
    print('App folder :', AppData.APP_PATH)
