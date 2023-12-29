"""
Main view for the application
"""

import lily_unit_test
import wx


class ViewMain(wx.Frame):
    
    def __init__(self, title):
        super().__init__(None, wx.ID_ANY, title)


class ViewMainTest(lily_unit_test.TestSuite):

    WINDOW_NAME = 'ViewMain Test'

    def setup(self):
        self.app = wx.App(redirect=False)
        self.frame = ViewMain(self.WINDOW_NAME)

    def test_01_show_frame(self):
        self.frame.Show()

    def teardown(self):
        if not hasattr(self, 'do_not_close') or hasattr(self, 'do_not_close') and not self.do_not_close:
            self.frame.Close()
        self.app.MainLoop()


if __name__ == '__main__':

    ts = ViewMainTest()
    ts.do_not_close = True
    ts.run()
