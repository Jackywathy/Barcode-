import wx
from frontend import view_item

def main():
    app = wx.App()
    view_item.ViewFrame(None, title="Move ya as")
    app.MainLoop()

if __name__ == "__main__":
    main()
