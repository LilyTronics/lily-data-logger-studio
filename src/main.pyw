"""
Start up script for the application
"""

import os
import wx

from src.app_data import AppData
from src.controllers.controller_main import ControllerMain
from src.models.logger import Logger


if not os.path.isdir(AppData.USER_FOLDER):
    os.makedirs(AppData.USER_FOLDER)

logger = Logger()
logger.info('Start application')
logger.debug('Application path: {}'.format(AppData.APP_PATH))

app = wx.App(redirect=False)

controller = ControllerMain('{} V{}'.format(AppData.APP_NAME, AppData.VERSION))
controller.show_view()

app.MainLoop()

logger.info('Application stopped')
logger.shut_down()
