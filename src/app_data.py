"""
Application data
"""

import os


class AppData(object):
    APP_NAME = 'Lily Data Logger Studio'
    VERSION = '0.1'
    EXE_NAME = 'LilyDataLoggerStudio'
    USER_FOLDER = os.path.join(os.path.join(os.path.expanduser('~')), EXE_NAME)


if __name__ == '__main__':

    print('App name   :', AppData.APP_NAME)
    print('App version:', AppData.VERSION)
    print('Exe name   :', AppData.EXE_NAME)
    print('User folder:', AppData.USER_FOLDER)
