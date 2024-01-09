"""
Main controller for the application.
"""

import wx

from src.views.view_logger import ViewLogger
from src.views.view_main import ViewMain


class ControllerMain(object):

    def __init__(self, view_title, logger, show_log_window=False):
        self._logger = logger
        self._view = ViewMain(view_title)

        self._view.Bind(wx.EVT_CLOSE, self._on_view_close)
        self._view.Bind(wx.EVT_TOOL, self._on_show_log, id=self._view.ID_TOOL_SHOW_LOG)

        self._log_view = None

        if show_log_window:
            wx.CallAfter(self._show_log)

    ##################
    # Event handlers #
    ##################

    def _on_show_log(self, event):
        self._show_log()
        event.Skip()

    def _on_close_log(self, event):
        self._log_view = None
        event.Skip()

    def _on_view_close(self, event):
        if self._log_view is not None:
            print('close log')
            self._log_view.Close()
        event.Skip()

    ###########
    # Private #
    ###########

    def _show_log(self):
        if self._log_view is None:
            self._log_view = ViewLogger('Log Messages')
            self._log_view.Bind(wx.EVT_CLOSE, self._on_close_log)
            self._log_view.show()

    ##########
    # Public #
    ##########

    def show_view(self):
        self._view.Show()


if __name__ == '__main__':

    from src.models.logger import Logger

    test_logger = Logger()

    app = wx.App(redirect=False)

    controller = ControllerMain('ControllerMain Test', test_logger, True)
    controller.show_view()

    app.MainLoop()
