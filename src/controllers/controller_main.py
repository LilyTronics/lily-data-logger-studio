"""
Main controller for the application.
"""

import wx

from src.models.settings import Settings
from src.views.view_logger import ViewLogger
from src.views.view_main import ViewMain


class ControllerMain(object):

    def __init__(self, view_title, logger, show_log_window=False):
        self._logger = logger
        self._logger.debug('Load main controller')

        self._settings = Settings()

        self._view = ViewMain(view_title)
        size = self._settings.get_main_window_size()
        if -1 not in size:
            self._view.SetSize(size)
        pos = self._settings.get_main_window_position()
        if -1 not in pos:
            self._view.SetPosition(pos)
        self._view.Maximize(self._settings.get_main_window_maximized())

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
        self._settings.store_log_window_maximized(self._log_view.IsMaximized())
        if not self._log_view.IsMaximized():
            self._settings.store_log_window_size(*self._log_view.GetSize())
            self._settings.store_log_window_position(*self._log_view.GetPosition())
        self._log_view = None
        event.Skip()

    def _on_view_close(self, event):
        if self._log_view is not None:
            self._log_view.Close()

        self._settings.store_main_window_maximized(self._view.IsMaximized())
        if not self._view.IsMaximized():
            self._settings.store_main_window_size(*self._view.GetSize())
            self._settings.store_main_window_position(*self._view.GetPosition())

        event.Skip()

    ###########
    # Private #
    ###########

    def _show_log(self):
        if self._log_view is None:
            self._log_view = ViewLogger('Log Messages')

            size = self._settings.get_log_window_size()
            if -1 not in size:
                self._log_view.SetSize(size)
            pos = self._settings.get_log_window_position()
            if -1 not in pos:
                self._log_view.SetPosition(pos)
            self._log_view.Maximize(self._settings.get_log_window_maximized())

            self._log_view.Bind(wx.EVT_CLOSE, self._on_close_log)
            self._log_view.show()

    ##########
    # Public #
    ##########

    def show_view(self):
        self._logger.debug('Show main view')
        self._view.Show()


if __name__ == '__main__':

    from src.models.logger import Logger

    test_logger = Logger()

    app = wx.App(redirect=False)

    controller = ControllerMain('ControllerMain Test', test_logger, True)
    controller.show_view()

    app.MainLoop()
