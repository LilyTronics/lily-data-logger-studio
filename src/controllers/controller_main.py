"""
Main controller for the application.
"""

import wx

from src.views.view_main import ViewMain


class ControllerMain(object):

    def __init__(self, view_title):
        self._view = ViewMain(view_title)

    def show_view(self):
        self._view.Show()


if __name__ == '__main__':

    app = wx.App(redirect=False)

    controller = ControllerMain('ControllerMain Test')
    controller.show_view()

    app.MainLoop()