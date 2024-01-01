"""
Main view for the application
"""

import lily_unit_test
import wx

from src.models.image_data import ImageData
from wx.dataview import DataViewTreeCtrl
from wx.dataview import NullDataViewItem


class ViewMain(wx.Frame):

    _GAP = 10

    def __init__(self, title):
        super().__init__(None, wx.ID_ANY, title)
        panel = wx.Panel(self)

        main_box = wx.BoxSizer(wx.HORIZONTAL)
        main_box.Add(self._create_instruments_controls(panel), 1, wx.EXPAND | wx.ALL, self._GAP)

        panel.SetSizer(main_box)

    ###########
    # Private #
    ###########

    def _create_instruments_controls(self, parent):
        box = wx.StaticBoxSizer(wx.StaticBox(parent, wx.ID_ANY, ' Instruments: '), wx.VERTICAL)

        btn_add_instrument = wx.Button(parent, size=(36, 36))
        btn_add_instrument.SetBitmap(ImageData.add_instrument_24.Bitmap)
        btn_add_instrument.SetToolTip('Add instrument')
        btn_delete_instrument = wx.Button(parent, size=(36, 36))
        btn_delete_instrument.SetBitmap(ImageData.delete_instrument_24.Bitmap)
        btn_delete_instrument.SetToolTip('Delete instrument')

        btn_add_io = wx.Button(parent, size=(36, 36))
        btn_add_io.SetBitmap(ImageData.add_io_24.Bitmap)
        btn_add_io.SetToolTip('Add input or output')
        btn_delete_io = wx.Button(parent, size=(36, 36))
        btn_delete_io.SetBitmap(ImageData.delete_io_24.Bitmap)
        btn_delete_io.SetToolTip('Delete input or output')

        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(btn_add_instrument, 0)
        buttons.Add(btn_delete_instrument, 0)
        buttons.Add(btn_add_io, 0)
        buttons.Add(btn_delete_io, 0)

        self.instruments = DataViewTreeCtrl(parent)

        box.Add(buttons, 0, wx.ALL, self._GAP)
        box.Add(self.instruments, 1, wx.EXPAND | wx.RIGHT | wx.BOTTOM | wx.LEFT, self._GAP)

        return box


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
