"""
Start up script for the application
"""

import wx

from src.app_data import AppData
from src.controllers.controller_main import ControllerMain

app = wx.App(redirect=False)

controller = ControllerMain('{} V{}'.format(AppData.APP_NAME, AppData.VERSION))
controller.show_view()

app.MainLoop()
