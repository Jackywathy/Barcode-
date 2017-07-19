import wx

class ViewFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title)
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#ffffff")

        divider = wx.BoxSizer(wx.HORIZONTAL)
        left_panel = wx.Panel(panel)
        left_panel.BackgroundColour = ("#ff4323")
        self.init_left(left_panel)
        right_panel = wx.Panel(panel)
        right_panel.BackgroundColour = ("#402af2")
        self.init_right(right_panel)
        divider.Add(left_panel, proportion=1, flag=wx.LEFT | wx.EXPAND, border=10)
        divider.Add(right_panel, proportion=1, flag=wx.RIGHT | wx.EXPAND, border=10)


        panel.SetSizer(divider)
        self.Center()
        self.Show()


    def init_left(self, panel):
        """
        Initalizes and creates all controls on the left panel
        :type panel: wx.Panel
        :return: None
        """
        # create a button
        self.back_button = wx.Button(panel, label="Return")

    def init_right(self, panel):
        pass