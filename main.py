#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
ZetCode wxPython tutorial

This example creates a checked
menu item.

author: Jan Bodnar
website: www.zetcode.com
last modified: September 2011
'''

import wx


class Example(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.init_ui()

    def init_ui(self):
        menu_bar = wx.MenuBar()

        file_menu = wx.Menu()
        view_menu = wx.Menu()

        # FILE
        # create and append items
        new_item = file_menu.Append(wx.ID_NEW, "&New", "Create new item")
        close_item = file_menu.Append(wx.ID_CLOSE, "&Exit", "Exit the application")

        # bind events
        self.Bind(wx.EVT_MENU, self.app_quit, close_item)



        # VIEW
        # create checkboxs and check them
        self.status_checkbox = view_menu.Append(wx.ID_ANY, "Show status bar", "Show status bar", kind=wx.ITEM_CHECK) # type: wx.MenuItem
        self.toolbar_checkbox = view_menu.Append(wx.ID_ANY, "Show tool bar", "Show tool bar", kind=wx.ITEM_CHECK) # type: wx.MenuItem
        self.status_checkbox.Check()
        self.toolbar_checkbox.Check()
        # bind to handlers
        self.Bind(wx.EVT_MENU, self.toggle_status_bar, self.status_checkbox)
        self.Bind(wx.EVT_MENU, self.toggle_toolbar, self.toolbar_checkbox)
        # append to Menu()
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(view_menu, "&View")


        self.SetMenuBar(menu_bar)

        self.toolbar = self.CreateToolBar() # type: wx.ToolBar
        self.toolbar.AddLabelTool




        self.Show()

    def toggle_status_bar(self, e):
        if self.status_checkbox.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def toggle_toolbar(self, e):
        if self.toolbar_checkbox.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()

    def app_quit(self, e):
        self.Close()





def main():
    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
