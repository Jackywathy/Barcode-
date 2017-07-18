import wx

class ViewFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title)
        self.sizer = wx.GridSizer(rows=0, cols=2, vgap=0, hgap=10)
        self.sizer.Add(wx.Button(self, label='Cls'))

        self.Center()
        self.Show()
