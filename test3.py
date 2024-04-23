import ctypes
import tkinter as tk
from webview.window import Window
from webview.platforms.edgechromium import EdgeChrome

user32 = ctypes.windll.user32


class WebView2(tk.Frame):
    def __init__(self, parent, width: int, height: int, url: str = '', **kw):
        global bg_color
        tk.Frame.__init__(self, parent, width=width, height=height, **kw)
        self.parent = parent
        self.width = width
        self.height = height
        self.url = url

        self.__create_web_view()

    def __create_web_view(self):
        self.web_view = EdgeChrome(self, None, None)
        self.web = self.web_view.web_view

        self.bind('<Destroy>', lambda event: self.web.Dispose())
        self.bind('<Configure>', self.__resize_webview)

        self.load_url(self.url)

    def __resize_webview(self, event):
        self.web_view.resize(self.winfo_width(), self.winfo_height())

    def load_url(self, url):
        self.web_view.load_url(url)

    def reload(self):
        self.web.Reload()
root = tk.Tk()
pdf_view_frame = WebView2(root, 500, 500)
pdf_view_frame.place(relheight=1, relwidth=1, relx=0, rely=0)
root.mainloop()