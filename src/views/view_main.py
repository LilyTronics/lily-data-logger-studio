"""
Main view for the application
"""

import wx


class ViewMain(wx.Frame):
    
    def __init__(self, title):
        super().__init__(None, wx.ID_ANY, title)


if __name__ == '__main__':

    app = wx.App(redirect=False)

    frame = ViewMain('ViewMain Test')
    frame.Show()

    app.MainLoop()
