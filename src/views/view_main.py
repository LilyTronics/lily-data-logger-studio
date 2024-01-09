"""
Main view for the application
"""

import wx.grid

from src.models.image_data import ImageData
from wx.dataview import DataViewTreeCtrl


class ViewMain(wx.Frame):

    ID_TOOL_OPEN_CONFIGURATION = 100
    ID_TOOL_SAVE_CONFIGURATION = 101
    ID_TOOL_EDIT_CONFIGURATION = 102
    ID_TOOL_CHECK_INSTRUMENTS = 103
    ID_TOOL_START_PROCESS = 104
    ID_TOOL_STOP_PROCESS = 105
    ID_TOOL_EXPORT_CSV = 106
    ID_TOOL_SHOW_LOG = 107

    _GAP = 5

    _LIST_COL_INDEX_SIZE = 30
    _LIST_COL_STEP_SIZE = 120
    _LIST_COL_DATA_SIZE = 120
    _TABLE_MIN_COL_WIDTH = 100

    _LED_SIZE = (16, 16)
    _COLOR_LED_OFF = '#060'

    _MINIMUM_WINDOW_SIZE = (1100, 700)

    def __init__(self, title):
        super().__init__(None, wx.ID_ANY, title)
        panel = wx.Panel(self)

        lab_box = wx.BoxSizer(wx.HORIZONTAL)
        lab_box.Add(self._create_instruments_controls(panel), 20, wx.EXPAND | wx.TOP | wx.LEFT | wx.BOTTOM, self._GAP)
        lab_box.Add(self._create_process_box(panel), 30, wx.EXPAND | wx.ALL, self._GAP)
        lab_box.Add(self._create_measurement_box(panel), 50, wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, self._GAP)

        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(self._create_toolbar(panel), 0, wx.EXPAND | wx.ALL, self._GAP)
        main_box.Add(self._create_config_info(panel), 0, wx.EXPAND | wx.ALL, self._GAP)
        main_box.Add(lab_box, 1, wx.EXPAND)

        panel.SetSizer(main_box)

        self.SetInitialSize(self._MINIMUM_WINDOW_SIZE)

    ###########
    # Private #
    ###########

    def _create_toolbar(self, parent):
        tools = [
            (self.ID_TOOL_OPEN_CONFIGURATION, ImageData.open_config.Bitmap, 'Open configuration'),
            (self.ID_TOOL_SAVE_CONFIGURATION, ImageData.save_config.Bitmap, 'Save configuration'),
            (0,),
            (self.ID_TOOL_EDIT_CONFIGURATION, ImageData.settings.Bitmap, 'Configuration settings'),
            (0,),
            (self.ID_TOOL_CHECK_INSTRUMENTS, ImageData.check_instruments.Bitmap, 'Check instruments'),
            (0,),
            (self.ID_TOOL_START_PROCESS, ImageData.start.Bitmap, 'Start'),
            (self.ID_TOOL_STOP_PROCESS, ImageData.stop.Bitmap, ' Stop'),
            (0,),
            (self.ID_TOOL_EXPORT_CSV, ImageData.export_csv.Bitmap, 'Export to CSV'),
            (0,),
            (self.ID_TOOL_SHOW_LOG, ImageData.show_log.Bitmap, 'Show log'),
        ]
        self._toolbar = wx.ToolBar(parent, style=wx.TB_HORIZONTAL | wx.TB_FLAT | wx.TB_NODIVIDER)
        for tool in tools:
            if tool[0] > 0:
                self._toolbar.AddTool(tool[0], '', tool[1], tool[2])
            else:
                self._toolbar.AddSeparator()

        self._toolbar.Realize()

        return self._toolbar

    def _create_config_info(self, parent):
        box = wx.StaticBoxSizer(wx.StaticBox(parent, wx.ID_ANY, ' Configuration: '), wx.HORIZONTAL)

        lbl_sample_time = wx.StaticText(parent, wx.ID_ANY, 'Sample time:')
        self._lbl_sample_time = wx.StaticText(parent, wx.ID_ANY, '-')
        self._lbl_end_time = wx.StaticText(parent, wx.ID_ANY, 'End time:')
        self._value_end_time = wx.StaticText(parent, wx.ID_ANY, '-')
        self._lbl_total_samples = wx.StaticText(parent, wx.ID_ANY, 'Total samples:')
        self._value_total_samples = wx.StaticText(parent, wx.ID_ANY, '-')
        lbl_elapsed_time = wx.StaticText(parent, wx.ID_ANY, 'Elapsed time:')
        self._lbl_elapsed_time = wx.StaticText(parent, wx.ID_ANY, '-')
        self._activity_led = wx.Panel(parent, wx.ID_ANY, size=self._LED_SIZE, style=wx.BORDER_SIMPLE)
        self._activity_led.SetBackgroundColour(self._COLOR_LED_OFF)

        box.Add(lbl_sample_time, 0, wx.ALL, self._GAP)
        box.Add(self._lbl_sample_time, 0, wx.ALL, self._GAP)
        box.Add(self._lbl_end_time, 0, wx.ALL, self._GAP)
        box.Add(self._value_end_time, 0, wx.ALL, self._GAP)
        box.Add(self._lbl_total_samples, 0, wx.ALL, self._GAP)
        box.Add(self._value_total_samples, 0, wx.ALL, self._GAP)
        box.Add(lbl_elapsed_time, 0, wx.ALL, self._GAP)
        box.Add(self._lbl_elapsed_time, 0, wx.ALL, self._GAP)
        box.Add(self._activity_led, 0, wx.ALL, self._GAP)

        return box

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


if __name__ == '__main__':

    app = wx.App(redirect=False)

    frame = ViewMain('ViewMain Test')
    frame.Show()

    app.MainLoop()
