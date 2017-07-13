import wx

class MyApp(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(300,300))
        self.init_ui()

        self.Move((0, 0))
        self.Center()
        self.Show()

    def init_ui(self):
        menu_bar = wx.MenuBar()

        # create menu Item + quit item
        file_menu = wx.Menu()
        quit_item = file_menu.Append(wx.ID_EXIT, "Quit", "Quit Appication")
        self.Bind(wx.EVT_MENU, self.on_quit_handler, quit_item)

        # add menu items to menu bar
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)

    def on_quit_handler(self, e):
        self.Close()


def main():
    app = wx.App()
    MyApp(None, title="Move ya as")
    app.MainLoop()

if __name__ == "__main__":
    main()
