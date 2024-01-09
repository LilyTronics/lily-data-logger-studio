"""
Main controller for the application.
"""

import wx

from src.views.view_main import ViewMain


class ControllerMain(object):

    def __init__(self, view_title, logger):
        self._logger = logger
        self._view = ViewMain(view_title)

    def show_view(self):
        self._view.Show()


if __name__ == '__main__':

    from src.models.logger import Logger

    test_logger = Logger()

    app = wx.App(redirect=False)

    controller = ControllerMain('ControllerMain Test', test_logger)
    controller.show_view()

    app.MainLoop()