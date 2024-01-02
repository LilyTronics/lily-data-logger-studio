"""
Main view for the application
"""

import lily_unit_test
import wx.grid

from wx.dataview import DataViewTreeCtrl


class ViewMain(wx.Frame):

    _GAP = 5

    _LIST_COL_INDEX_SIZE = 30
    _LIST_COL_STEP_SIZE = 120
    _LIST_COL_DATA_SIZE = 120
    _TABLE_MIN_COL_WIDTH = 100

    _MINIMUM_WINDOW_SIZE = (1100, 700)

    def __init__(self, title):
        super().__init__(None, wx.ID_ANY, title)
        panel = wx.Panel(self)

        lab_box = wx.BoxSizer(wx.HORIZONTAL)
        lab_box.Add(self._create_instruments_controls(panel), 20, wx.EXPAND | wx.TOP | wx.LEFT | wx.BOTTOM, self._GAP)
        lab_box.Add(self._create_process_box(panel), 30, wx.EXPAND | wx.ALL, self._GAP)
        lab_box.Add(self._create_measurement_box(panel), 50, wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, self._GAP)

        panel.SetSizer(lab_box)

        self.SetInitialSize(self._MINIMUM_WINDOW_SIZE)

    ###########
    # Private #
    ###########

    def _create_instruments_controls(self, parent):
        box = wx.StaticBoxSizer(wx.StaticBox(parent, wx.ID_ANY, ' Instruments: '), wx.VERTICAL)

        self.instruments = DataViewTreeCtrl(parent)

        btn_add_instrument = wx.Button(parent, wx.ID_ANY, 'Add')
        btn_delete_instrument = wx.Button(parent, wx.ID_ANY, 'Delete')

        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(btn_add_instrument, 0)
        buttons.Add(btn_delete_instrument, 0)

        box.Add(self.instruments, 1, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(buttons, 0, wx.ALL, self._GAP)

        return box

    def _create_process_box(self, parent):
        box = wx.StaticBoxSizer(wx.StaticBox(parent, wx.ID_ANY, " Process: "), wx.VERTICAL)

        self._lst_process = wx.ListCtrl(parent, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES |
                                        wx.LC_VRULES)
        self._lst_process.SetInitialSize((-1, 100))
        self._lst_process.InsertColumn(0, '#', width=self._LIST_COL_INDEX_SIZE)
        self._lst_process.InsertColumn(1, 'Step', width=self._LIST_COL_STEP_SIZE)
        self._lst_process.InsertColumn(2, 'Data', width=self._LIST_COL_DATA_SIZE)

        btn_add_step = wx.Button(parent, wx.ID_ANY, 'Add')
        btn_insert_step = wx.Button(parent, wx.ID_ANY, 'Insert')
        btn_delete_step = wx.Button(parent, wx.ID_ANY, 'Delete')

        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(btn_add_step, 0)
        buttons.Add(btn_insert_step, 0)
        buttons.Add(btn_delete_step, 0)

        box.Add(self._lst_process, 1, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(buttons, 0, wx.ALL, self._GAP)

        return box

    def _create_measurement_box(self, parent):
        box = wx.StaticBoxSizer(wx.StaticBox(parent, wx.ID_ANY, ' Measurements: '), wx.VERTICAL)

        grid_panel = wx.Panel(parent, wx.ID_ANY)
        grid_panel.SetBackgroundColour('#abadb3')

        self._grid_measurements = wx.grid.Grid(grid_panel, wx.ID_ANY)
        self._grid_measurements.CreateGrid(0, 1)
        self._grid_measurements.SetColLabelValue(0, 'Time')
        self._grid_measurements.SetColMinimalWidth(0, self._TABLE_MIN_COL_WIDTH)
        self._grid_measurements.AutoSizeColLabelSize(0)
        self._grid_measurements.EnableEditing(False)
        self._grid_measurements.EnableDragRowSize(False)
        self._grid_measurements.EnableDragColMove(False)
        self._grid_measurements.EnableDragColSize(False)

        btn_add_measurement = wx.Button(parent, wx.ID_ANY, 'Add')
        btn_delete_measurement = wx.Button(parent, wx.ID_ANY, 'Delete')

        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(btn_add_measurement, 0)
        buttons.Add(btn_delete_measurement, 0)

        grid_box = wx.BoxSizer(wx.VERTICAL)
        grid_box.Add(self._grid_measurements, 1, wx.EXPAND | wx.ALL, 1)
        grid_panel.SetSizer(grid_box)

        box.Add(grid_panel, 1, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(buttons, 0, wx.ALL, self._GAP)

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
