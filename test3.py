import ctypes
import tkinter as tk
from tkinter import Frame
from webview.window import Window
from webview.platforms.edgechromium import EdgeChrome
from System.Windows.Forms import Control
from System.Threading import Thread, ApartmentState, ThreadStart, SynchronizationContext, SendOrPostCallback

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Threading')
user32 = ctypes.windll.user32

class WebView2(Frame):
    def __init__(self, parent, width: int, height: int, url: str = '', **kw):
        Frame.__init__(self, parent, width=width, height=height, **kw)
        control = Control()
        uid = 'master'
        window = Window(uid, str(id(self)), url=None, html=None, js_api=None, width=width, height=height, x=None, y=None,
                        resizable=True, fullscreen=False, min_size=(200, 100), hidden=False,
                        frameless=False, easy_drag=True,
                        minimized=False, on_top=False, confirm_close=False, background_color='#FFFFFF',
                        transparent=False, text_select=True, localization=None,
                        zoomable=True, draggable=True, vibrancy=False)
        self.window = window
        self.web_view = EdgeChrome(control, window, None)
        self.control = control
        self.web = self.web_view.web_view
        self.width = width
        self.height = height
        self.parent = parent
        self.chwnd = int(str(self.control.Handle))
        user32.SetParent(self.chwnd, self.winfo_id())
        user32.MoveWindow(self.chwnd, 0, 0, width, height, True)
        self.loaded = window.events.loaded
        self.__go_bind()
        if url != '':
            self.load_url(url)
        self.core = None
        #self.web.CoreWebView2InitializationCompleted += self.__load_core

    def __go_bind(self):
        self.bind('<Destroy>', lambda event: self.web.Dispose())
        self.bind('<Configure>', self.__resize_webview)
        self.newwindow = None

    def __resize_webview(self, event):
        user32.MoveWindow(self.chwnd, 0, 0, self.winfo_width(), self.winfo_height(), True)

    def __load_core(self, sender, _):
        self.core = sender.CoreWebView2
        self.core.NewWindowRequested -= self.web_view.on_new_window_request
        # Prevent opening new windows or browsers
        self.core.NewWindowRequested += lambda _, args: args.Handled(True)

        if self.newwindow != None:
            self.core.NewWindowRequested += self.newwindow
        settings = sender.CoreWebView2.Settings  # 设置
        settings.AreDefaultContextMenusEnabled = False  # 菜单
        settings.AreDevToolsEnabled = False  # 开发者工具
        # self.core.DownloadStarting+=self.__download_file

    def load_url(self, url):
        self.web_view.load_url(url)

    def reload(self):
        self.core.Reload()

def have_runtime():  # 检测是否含有webview2 runtime
    from webview.platforms.winforms import _is_chromium
    return _is_chromium()


def install_runtime():  # 安装webview2 runtime
    from urllib import request
    import subprocess
    import os
    url = r'https://go.microsoft.com/fwlink/p/?LinkId=2124703'
    path = os.getcwd() + '\\webview2runtimesetup.exe'
    unit = request.urlopen(url).read()
    with open(path, mode='wb') as uf:
        uf.write(unit)
    cmd = path
    p = subprocess.Popen(cmd, shell=True)
    return_code = p.wait()  # 等待子进程结束
    os.remove(path)
    return return_code

def main():
    if not have_runtime():  # 没有webview2 runtime
        install_runtime()
    root = tk.Tk()
    video_box = tk.Frame(root)
    video_box.place(relheight=1, relwidth=1, relx=0, rely=0)

    def run():
        frame2 = WebView2(video_box, 500, 500)
        frame2.place(relheight=1, relwidth=1, relx=0, rely=0)
        frame2.load_url(f'file:///C:/Users/HEZRON%20WEKESA/Downloads/Lecture%207%20-%20Cloud%20Computing%20System%20III.ppt.pdf')
    tk.Button(video_box, command=run).pack()
    root.mainloop()

if __name__ == "__main__":

    t = Thread(ThreadStart(main))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()
