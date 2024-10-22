# ============================================= Used libraries ==========================================================================================
import mysql.connector
import sys
import base64
import pygame
import hashlib
import time
import socket
import tkinter as tk
import ctypes as ct
import threading
from PIL import Image, ImageTk
import io
import base64
from PIL import Image
from PIL import Image, ImageTk
import io
import requests
from cryptography.fernet import Fernet
import datetime
from gradientai import Gradient, SummarizeParamsLength, ExtractParamsSchemaValueType
from tkinter import filedialog
# import docx
import ctypes
import shutil
from tkinter import ttk, filedialog, messagebox
import google.generativeai as genai
import re
import ast

# ------------------------------ pip install gradient_haystack==0.2.0
from gradient_haystack.embedders.gradient_document_embedder import GradientDocumentEmbedder
from gradient_haystack.embedders.gradient_text_embedder import GradientTextEmbedder
from gradient_haystack.generator.base import GradientGenerator
from haystack import Document, Pipeline
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack.components.builders.answer_builder import AnswerBuilder

# ------------------------------
from langchain.chains import LLMChain
from langchain_community.llms import GradientLLM
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os
from gradientai import Gradient

# ------------------------------- Speech recogniation libraries --------------------------------------------------------------------------------------------
from queue import Queue
from threading import Thread
import pyaudio
import json
from vosk import Model, KaldiRecognizer
import whisper  # pip install -U openai-whisper
import wave
from pydub import AudioSegment  # used for converting .wav to .mp3
# --------------------------------- FireBase config data/labraries ---------------------------------------------------------------------------------------
import pyrebase

config = {
    'apiKey': "AIzaSyAL6KeL8SGTc7GvHtWQLhVXQ3A_pfs0fgA",
    'authDomain': "mentalhealth-badb3.firebaseapp.com",
    'databaseURL': "https://trialauth-7eeal-7eeal.firebaseio.com",
    'projectId': "mentalhealth-badb3",
    'storageBucket': "mentalhealth-badb3.appspot.com",
    'messagingSenderId': "668556041575",
    'appId': "1:668556041575:web:8170d74edf2fdbcf8f23c2",
    'measurementId': "G-168YG4NVDE"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()  # Authentication
# ------------------------------- img-to-text -------------------------------------------------------------------------------------------------------------

from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

draw_ocr = ocr_model = None


def paddleocr_import():
    global draw_ocr, ocr_model
    from paddleocr import PaddleOCR, draw_ocr  # [ pip install paddleocr , pip install protobuf==3.20.0]
    draw_ocr = draw_ocr
    ocr_model = PaddleOCR(lang='en', use_gpu=False)  # You can enable GPU by setting use_gpu=True


threading.Thread(target=paddleocr_import).start()
# -------------------------------  ------------------------------------------------------------------------------------------------------------------------

from docx2pdf import convert  # pip install docx2pdf
import pdfplumber  # used for extracting data from pdf
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

from docx import Document as txt_to_doc

# =============================== Global variable decoration  ============================================================================================
root = None
screen_width: int
screen_height: int

session = None
closed = False
user_id = None
pygame.mixer.init()
First_name = None
Second_Name = None
Last_Name = None
Email = None
user_Photo = None
side_bar_widget_list: list = []
side_bar_widget_list2: list = []
active_users_data: list = []
connection_status = False

gradient_ai_access_key = ''
gradient_ai_workspace_id = ''
assemblyai_access_key = ''
gradient_ai_finetuned_id = ''
gradient_ai_base_model_id = ''

Gem_Key = ''
gem_Extract_model = None
gem_Suggestion_model = None

User_Name = ''
User_Email = ''
User_Phone = ''
User_Pass = ''
User_Image = ''

keys = None
vosk_model = None
wisper_model_base = None
wisper_model_tiny = None
rag_pipeline = None
llm_chain = None
llm_chain2 = None
llm_chain3 = None
llm_chain4 = None
bg_color = '#FFFFFF'
fg_color = 'black'
fg_hovercolor = 'red'
bg_hovercolor = 'lightgreen'
current_theme = 'window(light)'
nav_bg = "white"
nav_widg = None
Home_page_frame = None
setting_status = False
rag_data = None
rag_widget = None
extraced_img_data = None
sammary_data = None
Recording = False
Recording_paused = False
Recording_data = ''
Recording_entity = ''
found_entities = []
entity_widg_list = []
Recording_summary = ''
audio_frames = None
downloading_audio = False
path_exe = os.getcwd()
cipher_suite = None
Key_Fernet = None
clinical_Note_upload_btn = None
proccessed_img_url = None
font_size = 15
ref_btn = None
text_list_widget = []
floating_frame = None
host_name = user_namem = password_key = database_name = None
pause_output_live = False
now_date = datetime.datetime.now()

# ========================== CLASSES DEFINITIONS  ====================================================================================================

# ------------------------------- web-Integration ---------------------------------------------------------------------------------------------------

import ctypes
from webview.window import Window
from webview.platforms.edgechromium import EdgeChrome
from System import IntPtr, Int32, Func, Type, Environment
from System.Windows.Forms import Control
from System.Threading import ApartmentState, ThreadStart, SynchronizationContext, SendOrPostCallback
from System.Threading import Thread as System_Thread

user32 = ctypes.windll.user32


class WebView2(tk.Frame):
    def __init__(self, parent, width: int, height: int, url: str = '', **kw):
        global bg_color
        tk.Frame.__init__(self, parent, width=width, height=height, **kw)
        control = Control()
        uid = 'master'
        window = Window(uid, str(id(self)), url=None, html=None, js_api=None, width=width, height=height, x=None, y=None,
                        resizable=True, fullscreen=False, min_size=(200, 100), hidden=False,
                        frameless=False, easy_drag=True,
                        minimized=False, on_top=False, confirm_close=False, background_color=bg_color,
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
        self.web.CoreWebView2InitializationCompleted += self.__load_core

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


def modify_css():
    # Read the content of the CSS file
    global bg_color, fg_color

    css_files = ['./html/styles.css']
    css_style = ":root { \n --global-color-bg:" + bg_color + ";\n  --global-color-fg:" + fg_color + ";\n}"

    for i in css_files:
        # Write the modified content back to the CSS file
        with open(i, 'w') as file:
            file.write(css_style)


# ---------------------------------------------- HTTP_ Local Server  -------------------------------------------------------------------------
httpd = None
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
from PIL import Image
from io import BytesIO


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global llm_chain, clinical_Note_upload_btn, proccessed_img_url
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            received_data = data.get('data')  # Extract the data received from the HTML form
            #print("Data received from HTML:", received_data)

            if received_data.startswith("image_Bit"):
                received_data = received_data.replace("image_Bit", '')

                base64_data = received_data.replace('data:image/jpeg;base64,', '')
                base64_data = base64_data.replace('data:image/png;base64,', '')
                base64_data = base64_data.replace('data:image/jpg;base64,', '')

                # Decode the base64 data
                image_data = base64.b64decode(base64_data)

                # Open the image using PIL
                image = Image.open(BytesIO(image_data))

                # Save the image to the specified output path
                image.save("./local_img.jpg")
                proccessed_img_url = os.getcwd() + "/local_img.jpg"
                clinical_Note_upload_btn.invoke()
                processed_data = " Img Recived"
            else:
                if llm_chain is None:
                    llm_inference_initializ()

                Answer = llm_chain.invoke(input=f"{received_data}")
                Answer = Answer['text']

                processed_data = Answer.replace("\n", "<br>")
                if "|" in processed_data:
                    table = "<table>"
                    rows = processed_data.split("<br>")
                    headers = "<tr>" + "<th>" + "</th><th>".join(rows[0].split("|")) + "</th>" + "</tr>"
                    table_rows = ''
                    for row in rows[1:]:
                        table_rows += "<tr>"
                        table_rows += "<td>" + "</td><td>".join(row.split("|")) + "</td>"
                        table_rows += "</tr>"

                    table += headers + table_rows
                    table += "</table>"
                    processed_data = table

            # Print the received data and the processed data

            print("Processed data:", processed_data)

            # Send a response back to the client
            response_data = {'message': 'Data received and processed successfully', 'processed_data': processed_data}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_error(404, "Not found")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


def run_server():
    def run_server_thread():
        global httpd
        print("server_running")
        server_address = ('localhost', 8080)
        httpd = HTTPServer(server_address, RequestHandler)
        httpd.serve_forever()
        print("server_stopped")

    threading.Thread(target=run_server_thread).start()


# =============================== Functions definition ============================================================================================

# --------------------------------- Themes --------------------------------------------------------------------------------------------------------
def title_bar_color(window, color):
    # import ctypes as ct
    try:
        window.update()
        if color.startswith('#'):
            blue = color[5:7]
            green = color[3:5]
            red = color[1:3]
            color = blue + green + red
        else:
            blue = color[4:6]
            green = color[2:4]
            red = color[0:2]
            color = blue + green + red
        get_parent = ct.windll.user32.GetParent
        HWND = get_parent(window.winfo_id())

        color = '0x' + color
        color = int(color, 16)

        ct.windll.dwmapi.DwmSetWindowAttribute(HWND, 35, ct.byref(ct.c_int(color)), ct.sizeof(ct.c_int))

    except Exception as e:
        print("title_bar_color fun error : ", e)



def change_color(widget, button):
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor, current_theme, nav_bg, nav_widg
    global root, floating_frame
    button_text = button.cget("text")
    print("color_change: ", button_text)
    if button_text == 'window(light)':
        button.config(text='window(dark_gray)')
        bg_color = '#353839'
        fg_color = 'white'
        current_theme = 'window(dark_gray)'
        nav_bg = bg_color

    elif button_text == 'window(dark_gray)':
        button.config(text='window(dark_blue)')
        bg_color = '#36454F'
        fg_color = 'white'
        current_theme = 'window(dark_blue)'
        nav_bg = bg_color

    elif button_text == 'window(dark_blue)':
        button.config(text='window(Blackberry)')
        bg_color = '#3A3A38'
        fg_color = 'white'
        current_theme = 'window(Blackberry)'
        nav_bg = bg_color

    elif button_text == 'window(Blackberry)':
        button.config(text='window(dark_green)')
        bg_color = '#555D50'
        fg_color = 'white'
        current_theme = 'window(dark_green)'
        nav_bg = bg_color

    elif button_text == 'window(dark_green)':
        button.config(text='window(Jacket)')
        bg_color = '#253529'
        fg_color = 'white'
        current_theme = 'window(Jacket)'
        nav_bg = bg_color

    elif button_text == 'window(Jacket)':
        button.config(text='window(Air Force blue)')
        bg_color = '#5D8AA8'
        fg_color = 'white'
        current_theme = 'window(Air Force blue)'
        nav_bg = bg_color

    elif button_text == 'window(Air Force blue)':
        button.config(text='window(Steel Blue)')
        bg_color = '#4682B4'
        fg_color = 'white'
        current_theme = 'window(Steel Blue)'
        nav_bg = bg_color

    elif button_text == 'window(Steel Blue)':
        button.config(text='window(Carolina Blue)')
        bg_color = '#4B9CD3'
        fg_color = 'white'
        current_theme = 'window(Carolina Blue)'
        nav_bg = bg_color

    elif button_text == 'window(Carolina Blue)':
        button.config(text='window(Turkish Blue)')
        bg_color = '#4F97A3'
        fg_color = 'white'
        current_theme = 'window(Turkish Blue)'
        nav_bg = bg_color

    elif button_text == 'window(Turkish Blue)':
        button.config(text='window(Maya Blue)')
        bg_color = '#73C2FB'
        fg_color = 'white'
        current_theme = 'window(Maya Blue)'
        nav_bg = bg_color

    elif button_text == 'window(Maya Blue)':
        button.config(text='window(Independence Blue)')
        bg_color = '#4C516D'
        fg_color = 'white'
        current_theme = 'window(Independence Blue)'
        title_bar_color(root, bg_color)
        nav_bg = bg_color

    elif button_text == 'window(Independence Blue)':
        button.config(text='window(Yale Blue)')
        bg_color = '#00356B'
        fg_color = 'white'
        current_theme = 'window(Yale Blue)'
        nav_bg = bg_color

    elif button_text == 'window(Yale Blue)':
        button.config(text='window(Prussian blue)')
        bg_color = '#003153'
        fg_color = 'white'
        current_theme = 'window(Prussian blue)'
        nav_bg = bg_color

    elif button_text == 'window(Prussian blue)':
        button.config(text='window(Aegean Blue)')
        bg_color = '#4E6E81'
        fg_color = 'white'
        current_theme = 'window(Aegean Blue)'
        title_bar_color(root, bg_color)
        nav_bg = bg_color

    elif button_text == 'window(Aegean Blue)':
        button.config(text='window(Braves Navy)')
        bg_color = '#13274F'
        fg_color = 'white'
        current_theme = 'window(Braves Navy)'
        nav_bg = bg_color

    elif button_text == 'window(Braves Navy)':
        button.config(text='window(Parchment)')
        bg_color = '#F1E9D2'
        fg_color = 'black'
        current_theme = 'window(Parchment)'
        nav_bg = bg_color

    elif button_text == 'window(Parchment)':
        button.config(text='window(Alabaster)')
        bg_color = '#EDEAE0'
        fg_color = 'black'
        current_theme = 'window(Alabaster)'
        nav_bg = bg_color

    elif button_text == 'window(Alabaster)':
        button.config(text='window(White smoke)')
        bg_color = '#F5F5F5'
        fg_color = 'black'
        current_theme = 'window(White smoke)'
        nav_bg = bg_color

    elif button_text == 'window(White smoke)':
        button.config(text='window(light)')
        bg_color = '#F8FBF8'
        fg_color = 'black'
        current_theme = 'window(light)'

        nav_bg = bg_color
    else:
        return

    def change_all(wdget=widget):
        global bg_color, fg_color, fg_hovercolor, bg_hovercolor, current_theme, Home_page_frame, text_list_widget

        if isinstance(wdget, tk.Frame):
            wdget.config(bg=bg_color)

        elif isinstance(wdget, tk.Button):
            wdget.config(bg=bg_color, activebackground=bg_color, fg=fg_color, activeforeground=fg_color)

        elif isinstance(wdget, tk.Label):
            wdget.config(bg=bg_color, fg=fg_color)

        elif isinstance(wdget, tk.Text):
            wdget.config(bg=bg_color, fg=fg_color)
            for wd in text_list_widget:
                try:
                    wd.config(bg=darken_hex_color(bg_color), fg=fg_color)
                except:
                    text_list_widget.remove(wd)

        elif isinstance(wdget, tk.Entry):
            wdget.config(bg=bg_color, fg=fg_color)
        elif isinstance(wdget, tk.Canvas):
            wdget.config(bg=bg_color)
        elif isinstance(wdget, tk.Checkbutton):
            wdget.config(bg=bg_color, activebackground=bg_color)
        elif isinstance(wdget, tk.PanedWindow):
            wdget.config(bg=bg_color)

        else:
            # widget.config(bg=bg_icolor, fg='white')
            pass

        children = wdget.winfo_children()
        for child in children:
            change_all(child)

        for iw in nav_widg:
            iw.config(bg=nav_bg)
            children = iw.winfo_children()
            for child in children:
                child.config(bg=nav_bg)

        Home_page_frame.config(bg=fg_color)

        save_themes()

    modify_css()
    title_bar_color(root, bg_color)
    title_bar_color(floating_frame, bg_color)
    threading.Thread(target=change_all).start()


# --------------------------------- NLP and LLM  --------------------------------------------------------------------------------------------------------


def entity_highlight_words(widget):
    def Run():
        global found_entities, fg_color, closed
        if fg_color == 'black':
            widget.tag_configure("highlight", background="gold")  # Configure a tag for highlighting
        else:
            widget.tag_configure("highlight", background="#737000")
        print("found_entities : - ", found_entities)
        for word in found_entities:
            start = 1.0
            entites = word.split(",")
            if len(entites) == 1:
                while not closed:
                    start = widget.search(word, start, stopindex=tk.END)
                    if not start:
                        break
                    end = f"{start}+{len(word)}c"
                    widget.tag_add("highlight", start, end)
                    start = end

                start = 1.0
                while not closed:
                    start = widget.search(word.capitalize(), start, stopindex=tk.END)
                    if not start:
                        break
                    end = f"{start}+{len(word)}c"
                    widget.tag_add("highlight", start, end)
                    start = end

                start = 1.0
                word = word[0].lower() + word[1:]
                while not closed:
                    start = widget.search(word, start, stopindex=tk.END)
                    if not start:
                        break
                    end = f"{start}+{len(word)}c"
                    widget.tag_add("highlight", start, end)
                    start = end

            else:
                print("entites :", entites)
                for g_word in entites:
                    start = 1.0
                    print("entites word:", g_word)
                    if (g_word == "or") or (g_word == "OR") or (g_word == "and") or (g_word == "AND") or (g_word == "when") or (g_word == "to"):
                        continue
                    g_word = g_word.strip(",")
                    g_word = g_word.strip(".")

                    while not closed:
                        start = widget.search(g_word, start, stopindex=tk.END)
                        if not start:
                            break
                        end = f"{start}+{len(g_word)}c"
                        widget.tag_add("highlight", start, end)
                        start = end

                    start = 1.0
                    while not closed:
                        start = widget.search(g_word.capitalize(), start, stopindex=tk.END)
                        if not start:
                            break
                        end = f"{start}+{len(g_word)}c"
                        widget.tag_add("highlight", start, end)
                        start = end
                    start = 1.0
                    g_word = g_word[0].lower() + g_word[1:]
                    while not closed:
                        start = widget.search(g_word, start, stopindex=tk.END)
                        if not start:
                            break
                        end = f"{start}+{len(g_word)}c"
                        widget.tag_add("highlight", start, end)
                        start = end

    threading.Thread(target=Run).start()


def Entity_Extraction(document_widget, widget=None, delete_hist=True):
    def run(document_widget=document_widget, widget=widget, delete_hist=delete_hist):
        global Recording, Recording_paused, Recording_entity, Recording_data, Recording_summary
        global found_entities, entity_widg_list

        mygradient = Gradient()

        document = document_widget.get("1.0", "end")
        if len(document) < 0:
            print("No value to Extract")
            return

        document = (document.strip())
        schema = '{'
        for i in entity_widg_list:
            schema += '"' + i[1].get() + '": { "type": ExtractParamsSchemaValueType.' + str(i[2].cget("text")) + ', "required": ' + str(i[3].get()) + ', }, '
        schema += '}'
        print(schema)
        dictionary = eval(schema)
        try:
            result = mygradient.extract(
                document=document,
                schema_=dictionary,
            )
            # widget.config(state=tk.NORMAL)

            Recording_entity = ''
            found_entities = []
            print('result["entity"].items() :', len(result["entity"].items()))
            for key, value in result["entity"].items():
                Recording_entity += key + " : " + value + "\n"
                found_entities.append(value)

            entity_highlight_words(document_widget)

            if widget is not None:
                if delete_hist:
                    widget.delete(1.0, tk.END)
                widget.insert(tk.END, "\n------------------------ EXTRACTED ENTITIES ------------------------------------------- \n\n ", "ASR")
                widget.insert(tk.END, Recording_entity + "\n\n")
                widget.insert(tk.END, "\n--------------------------------------------------------------------------------------- \n\n ", "ASR")
                widget.see(tk.END)  # Scroll to the end of the text widget
            else:
                Recording_entity = Recording_entity

        except Exception as e:
            # print(type(e).__name__)
            pass
            """
            if type(e).__name__ == 'BadRequestException':
                error = "Error :" + str(type(e).__name__) + " -Missing Entity Definitions. Please define your entities properly. If you have already defined them, ensure they adhere to the required format"
                widget.config(state=tk.NORMAL)
                widget.delete(1.0, tk.END)
                widget.insert(tk.END, e,  'error_config')
                widget.config(state=tk.DISABLED)
            elif type(e).__name__ == 'MaxRetryError':
                error = "Error :"  + " : Check Your internet conection"
                widget.config(state=tk.NORMAL)
                widget.delete(1.0, tk.END)
                widget.insert(tk.END, e,  'error_config')
                widget.config(state=tk.DISABLED)
            elif type(e).__name__ == 'ServiceException':
                error = "Error :" + " : Payment Due for Service Utilization. Please Upgrade your account"
                widget.config(state=tk.NORMAL)
                widget.delete(1.0, tk.END)
                widget.insert(tk.END, e)
                widget.config(state=tk.DISABLED)
            elif type(e).__name__ == 'ValidationError':
                error = "Error :" + " : No data provide for extraction"
                widget.config(state=tk.NORMAL)
                widget.delete(1.0, tk.END)
                widget.insert(tk.END, e, 'error_config')
                widget.config(state=tk.DISABLED)
            AttributeError
            """

    threading.Thread(target=run).start()


def D_Summary(widget1, widget=None, delete_hist=True):
    def run_f(widget1=widget1, widget=widget, delete_hist=delete_hist):
        global Recording, Recording_paused, Recording_summary
        gradient = Gradient()
        document = widget1.get("1.0", "end")
        document = (document.strip())

        if len(document) < 5:
            return
        try:
            Recording_summary = ''
            summary_length = SummarizeParamsLength.LONG
            result = gradient.summarize(
                document=document,
                length=summary_length
            )

            if widget is not None:
                widget.config(state=tk.NORMAL)
                if delete_hist:
                    widget.delete(1.0, tk.END)
                widget.insert(tk.END, '\n\n------------------------ CONVERSATION SUMMARY -----------------------------------------------------\n\n', 'ASR')
                widget.insert(tk.END, result['summary'] + '\n\n')
                widget.insert(tk.END, '\n\n------------------------   --------------- ---------------------------------------------------------\n\n', 'ASR')
                widget.see(tk.END)  # Scroll to the end of the text widget
            else:
                Recording_summary = result['summary']


        except Exception as e:
            # print(e)
            pass

    threading.Thread(target=run_f).start()


def rag_initialize(data=None):
    print("rag_initializ_start")
    global rag_pipeline, rag_data, gradient_ai_workspace_id, gradient_ai_access_key

    rag_pipeline = None

    if data is None and rag_data is None:
        return

    elif data is None and rag_data is not None:
        data = rag_data

    document_store = InMemoryDocumentStore()
    writer = DocumentWriter(document_store=document_store)

    document_embedder = GradientDocumentEmbedder(
        access_token=gradient_ai_access_key,
        workspace_id=gradient_ai_workspace_id,
    )

    docs = [
        Document(content=data)
    ]
    try:
        indexing_pipeline = Pipeline()
        indexing_pipeline.add_component(instance=document_embedder, name="document_embedder")
        indexing_pipeline.add_component(instance=writer, name="writer")
        indexing_pipeline.connect("document_embedder", "writer")
        indexing_pipeline.run({"document_embedder": {"documents": docs}})

        text_embedder = GradientTextEmbedder(
            access_token=os.environ["GRADIENT_ACCESS_TOKEN"],
            workspace_id=os.environ["GRADIENT_WORKSPACE_ID"],
        )

        generator = GradientGenerator(
            access_token=os.environ["GRADIENT_ACCESS_TOKEN"],
            workspace_id=os.environ["GRADIENT_WORKSPACE_ID"],
            # model_adapter_id=fine_tuned_Model_Id,
            base_model_slug="nous-hermes2",
            max_generated_token_count=350,
        )

        prompt = """You are helpful assistant ment to answer questions to help in clinical documentation. Answer the query, based on the
        content in the documents. if you dont know the answer say you don't know.
        {{documents}}
        Query: {{query}}
        \nAnswer:
        """

        retriever = InMemoryEmbeddingRetriever(document_store=document_store)
        prompt_builder = PromptBuilder(template=prompt)

        rag_pipeline = Pipeline()
        rag_pipeline.add_component(instance=text_embedder, name="text_embedder")
        rag_pipeline.add_component(instance=retriever, name="retriever")
        rag_pipeline.add_component(instance=prompt_builder, name="prompt_builder")
        rag_pipeline.add_component(instance=generator, name="generator")
        rag_pipeline.add_component(instance=AnswerBuilder(), name="answer_builder")
        rag_pipeline.connect("generator.replies", "answer_builder.replies")
        rag_pipeline.connect("retriever", "answer_builder.documents")
        rag_pipeline.connect("text_embedder", "retriever")
        rag_pipeline.connect("retriever", "prompt_builder.documents")
        rag_pipeline.connect("prompt_builder", "generator")
        # widget.config(fg='green')
    except Exception as e:
        print(e)
        # widget.config(fg='red')
        rag_pipeline = None
        return


def rag_chat(question_widget, widget, widget1):
    global rag_pipeline, rag_data
    print(rag_pipeline)

    def run_function(question_widget=question_widget, widget=widget, widget1=widget1):
        question = question_widget.get("1.0", tk.END)
        widget1.config(text='▫▫▫▫')
        question = question.strip()
        if question == '' or rag_pipeline == None:
            widget1.config(text='▶')
            widget.insert(tk.END, f'ERROR: PLEASE UPLOAD FILE FIRST \n\n\n', 'error_config')

            return

        widget.config(state=tk.NORMAL)
        widget.insert(tk.END, f"🆈🅾🆄\n{question}\n\n")
        widget.config(state=tk.DISABLED)

        try:
            result = rag_pipeline.run(
                {
                    "text_embedder": {"text": question},
                    "prompt_builder": {"query": question},
                    "answer_builder": {"query": question}
                }
            )
            widget.config(state=tk.NORMAL)
            widget.insert(tk.END, f'🅱🅾🆃\n{result["answer_builder"]["answers"][0].data}\n\n', 'llm_config')
            widget.see(tk.END)  # Scroll to the end of the text widget
            widget.config(state=tk.DISABLED)
            question_widget.delete(1.0, tk.END)
            widget1.config(text='▶')
            # return result["answer_builder"]["answers"][0].data
        except Exception as e:
            print(e)
            widget.config(state=tk.NORMAL)
            widget.insert(tk.END, f'ERROR: PLEASE UPLOAD FILE FIRST \n\n\n', 'error_config')
            widget.config(state=tk.DISABLED)
            widget1.config(text='▶')

            print(f"UPLOAD ERROR\n {e}")

    threading.Thread(target=run_function).start()


def extract_pdf_text(path=None):
    if path is None:
        return

    def run():
        global rag_data
        with pdfplumber.open(path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        print(text)
        rag_data = text
        rag_initialize(data=text)

    threading.Thread(target=run).start()


def Upload_rag_file(pdf_view_frame):
    pdf_view_frame.load_url('file:///' + path_exe + "/html/LoadFile_Animation1.html")

    def run(pdf_view_frame=pdf_view_frame):
        global bg_color, path_exe

        filetypes = [("File_type", "*.pdf;*.doc;*.docx;*.txt")]
        file_path = filedialog.askopenfilename(filetypes=filetypes)

        if file_path:

            raw_text_data = ''
            pdf_file_name = 'uploaded.pdf'
            path = path_exe
            url_file = "file:///" + path
            path_r = path + '/uploaded.pdf'

            if file_path.endswith('.doc') or file_path.endswith('.docx'):
                convert(rf"{file_path}", f"./{pdf_file_name}")

                url_file += f"/{pdf_file_name}"
                print(url_file)

            elif file_path.endswith('.pdf'):
                url_file = "file:///" + f"{file_path}"
                path_r = file_path
                print(url_file)

            elif file_path.endswith('.txt'):
                f = open(rf"{file_path}", "r")
                for x in f:
                    raw_text_data += x
                print("raw_text_data - ", raw_text_data)

                pdf_document = SimpleDocTemplate(pdf_file_name)
                pdf_elements = []
                styles = getSampleStyleSheet()
                paragraph = Paragraph(raw_text_data, styles["Normal"])
                pdf_elements.append(paragraph)
                pdf_document.build(pdf_elements)

                pdf_document = SimpleDocTemplate(pdf_file_name)
                pdf_elements = []
                styles = getSampleStyleSheet()
                paragraph = Paragraph(raw_text_data, styles["Normal"])
                pdf_elements.append(paragraph)
                pdf_document.build(pdf_elements)

                url_file += f"/{pdf_file_name}"
                print(file_path)
                print(url_file)
            else:
                return

            extract_pdf_text(path_r)
            pdf_view_frame.load_url(url_file)

        else:
            pdf_view_frame.load_url('file:///' + path_exe + "/html/LoadFile_Animation.html")
            print("No file selected")

    run()

    # threading.Thread(target=run).start()


def clear_rag_file(pdf_view_frame):
    global rag_pipeline, rag_data
    pdf_view_frame.load_url('file:///' + path_exe + "/html/LoadFile_Animation.html")
    rag_pipeline = None
    rag_data = None


def llm_inference_initializ():
    global llm_chain, llm_chain2, llm_chain3, llm_chain4
    fine_tuned_Model_Id = "d189f721-ae17-4545-a0ad-f95194e857f5_model_adapter"  # initializes a GradientLLM with our fine-tuned model by specifying our model ID.

    gradient = Gradient()
    base_model = gradient.get_base_model(base_model_slug="nous-hermes2")

    # ================================================ chat bot1 section
    llm = GradientLLM(
        model=base_model.id,
        model_kwargs=dict(max_generated_token_count=510),
    )

    # template = """### Instruction: {Instruction} \n\n### Response:"""
    template = """You are a AI having a conversation with a human.
    {chat_history}
    Human: {Instruction}
    Chatbot:"""

    prompt = PromptTemplate(template=template, input_variables=["Instruction", 'chat_history'])
    memory = ConversationBufferMemory(memory_key="chat_history")
    llm_chain = LLMChain(prompt=prompt, llm=llm, memory=memory)

    # ================================================ chat bot2 section

    template2 = """You are a AI that analyzes data exacted from images and present it in a formatted way. 
    Human: {Instruction}
    Chatbot:"""

    prompt2 = PromptTemplate(template=template2, input_variables=["Instruction"])
    llm_chain2 = LLMChain(prompt=prompt2, llm=llm)

    # ================================================ chat bot3 section

    template3 = """You are a AI that extracts useful information clinical information from text data. Extract data from the provided Text.
        Text Data: {Instruction}
        Chatbot:"""

    prompt3 = PromptTemplate(template=template3, input_variables=["Instruction"])
    llm_chain3 = LLMChain(prompt=prompt3, llm=llm)

    # ================================================ chat bot3 section

    template4 = """
            Your are an AI Chatbot that answers following questions based on the given conversation.
            Question:
            1.What are the main symptoms or concerns mentioned by the patient in the conversation?
            2.Can you identify any specific medical conditions or diagnoses discussed by the patient?
            3.Are there any medications or treatments mentioned by the patient?
            4.Can you summarize the overall context or purpose of the conversation?
            5.What follow-up questions would you suggest to gather more details about the patient's condition?
            6.Do you detect any emotional cues or concerns expressed by the patient?
            7.Are there any references to past medical history or previous treatments?
            8.Can you identify any potential risk factors or red flags mentioned by the patient?
            9.Do you suggest any specific resources or educational materials based on the conversation?
            10.Are there any important dates or events mentioned in the conversation, such as appointments or procedures?
            
            Converastion: "{Instruction}
            Chatbot:"""

    prompt4 = PromptTemplate(template=template4, input_variables=["Instruction"])
    llm_chain4 = LLMChain(prompt=prompt4, llm=llm)


def Chat_bot_inference(widget0, widget1, widget2):
    global llm_chain

    def run(widget0=widget0, widget1=widget1, widget2=widget2):
        Question = widget0.get("1.0", "end-1c")
        Question = Question.strip()
        if llm_chain == None:
            llm_inference_initializ()
        if len(Question) == 0:
            return
        widget2.config(state=tk.NORMAL)
        widget2.insert(tk.END, f"🆈🅾🆄\n{Question}\n\n")

        try:
            Answer = llm_chain.invoke(input=f"\n{Question}")
            widget2.insert(tk.END, f"🅱🅾🆃\n{Answer['text']}\n\n")
        except Exception as e:
            print(e)
            widget2.insert(tk.END, f"🅱🅾🆃\nError: check your internet connection or ensure all invoices are paid and your payment method is up to date \n\n")

        widget2.config(state=tk.DISABLED)
        widget2.see(tk.END)  # Scroll to the end of the text widget
        widget0.delete(1.0, tk.END)
        widget1.forget()
        widget1.place(relheight=0.05, relwidth=0.6, rely=0.9, relx=0.2)

    threading.Thread(target=run).start()


def GEMINI_LLMs():
    global gem_Extract_model, gem_Suggestion_model, Gem_Key, closed
    while not closed:
        if Gem_Key != '':
            genai.configure(api_key=Gem_Key)
            gem_Extract_model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction="""You are an AI that Extract Medical infomation from the given conversation"""
            )

            gem_Suggestion_model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction="You are an AI answers Medical question relating to the given medical conversation."
            )

            break


def Medical_Information(text_widget, display_widget):
    def run_Medical_Information(text_widget=text_widget, display_widget=display_widget):
        global gem_Extract_model, closed
        text = text_widget.get("1.0", "end")
        while not closed:
            try:
                response = gem_Extract_model.generate_content(
                    {'role': 'user',
                     'parts': [text]}
                )
                data = response.text
                data = data.replace("**", "")
                data = "conversation: " + data.replace("*", "\t* ")
                display_widget.insert(tk.END, "\n------------ Extracted Medical Information ----------------------------------\n\n", 'ASR')
                display_widget.insert(tk.END, data)
                display_widget.insert(tk.END, "\n-----------------------------------------------------------------------------\n", 'ASR')
                break
            except Exception as e:
                time.sleep(3)

    threading.Thread(target=run_Medical_Information).start()
# =============================== Speech recognition Functions ==============================================================================================================

def Initialize_VOSK():
    global vosk_model, wisper_model_base, wisper_model_tiny
    # vosk_model = Model(model_name="vosk-model-en-us-0.22")
    # vosk_model = Model(model_name="vosk-model-en-us-0.42-gigaspeech")
    vosk_model = Model(model_name="vosk-model-small-en-us-0.15")

    wisper_model_tiny = whisper.load_model("tiny")
    wisper_model_base = whisper.load_model("base")
    print('SR Initialized')


threading.Thread(target=Initialize_VOSK).start()


def RUN_OFFLINE_speech_recognition(widget, widget1=None, widget2=None, Record_btn=None, clock_wideth=None, Conversation_Name_widget=None):
    global closed, Recording, Recording_paused, Recording_data, vosk_model
    global fg_color, bg_color, miniute, second, hour
    global audio_frames, index
    global pause_output_live

    def start_recording():
        global Recording
        messages.put(True)
        print("Starting...")
        Recording = True
        Record_btn.config(fg="green")

        Thread(target=record_microphone).start()
        Thread(target=speech_recognition, args=(widget,)).start()

    def record_microphone(chunk=1024, RECORD_SECONDS=2):
        global closed, Recording_paused, Recording

        p = pyaudio.PyAudio()
        FRAME_RATE = 16000
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        input_device_index=0,
                        frames_per_buffer=chunk)
        frames = []
        while not messages.empty():
            if closed:
                break
            if Recording == False:
                break
            if Recording_paused:
                continue
            Record_btn.config(fg="green")
            data = stream.read(chunk)
            frames.append(data)
            if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
                recordings.put(frames.copy())
                frames = []

        stream.stop_stream()
        stream.close()
        p.terminate()

    def speech_recognition(widget=widget, widget1=widget1, widget2=widget2):
        global closed, Recording_data, Recording_paused, Recording, audio_frames
        global running_scribe, previous_data, Recording_summary, Recording_entity
        global index
        running_scribe = False
        print("scanning")
        audio_frames = []
        previous_data = ''
        pos = 0

        while not messages.empty():
            if closed:
                print('speech_recognition closed')
                break
            if not Recording:
                break
            if Recording_paused:
                continue
            try:
                frames = recordings.get()

                rec.AcceptWaveform(b''.join(frames))
                result = rec.Result()
                vosk_text = json.loads(result)["text"]
                if (vosk_text.strip() != "huh") and (vosk_text.strip() != ''):
                    audio_frames.extend(frames)
                    text = grammar(frames)
                    widget.insert(tk.END, f" {text}", 'ASR')
                    widget.see(tk.END)
                    if pos == 10:
                        start_idx = index
                        end_idx = len(audio_frames) - 1
                        index = end_idx
                        transcribe_audio(audio_frames[start_idx: end_idx], widget1)
                        # transcribe_audio(audio_frames, widget1)
                        widget2.delete(1.0, tk.END)

                        if not pause_output_live:
                            if Recording_entity != "":
                                widget2.insert(tk.END, "------------------------ EXTRACTED ENTITIES ------------------------------------------- \n", "ASR")
                                widget2.insert(tk.END, Recording_entity)
                            if Recording_summary != "":
                                widget2.insert(tk.END, "------------------------ CONVERSATION SUMMARY ------------------------------------------- \n", "ASR")
                                widget2.insert(tk.END, Recording_summary)

                            Medical_Information(widget1, widget2)
                        pos = 0

                    pos += 1
                else:
                    pass
                    """
                    if index != len(audio_frames) - 1:
                        start_idx = index
                        end_idx = len(audio_frames) - 1
                        index = end_idx
                        transcribe_audio(audio_frames[start_idx: end_idx], widget1, 1)
                    """

            except Exception as e:
                print(e)

    def grammar(frames):
        global wisper_model_tiny, wisper_model_base

        # Define audio parameters
        channels = 1  # Mono
        sample_width = 2  # 16-bit audio
        sample_rate = 16000  # Sample rate (Hz)
        output_file = "./temp_files/ASR_real_time_temp.wav"
        # Open the output file in write mode
        with wave.open(output_file, 'wb') as output_wave:
            # Set audio parameters
            output_wave.setnchannels(channels)
            output_wave.setsampwidth(sample_width)
            output_wave.setframerate(sample_rate)

            # Write the audio frames to the file
            output_wave.writeframes(b''.join(frames))

        result = wisper_model_tiny.transcribe(output_file)

        return result["text"]

    def transcribe_audio(frames, widget, last=None):
        global running_scribe, previous_data
        global wisper_model_tiny, wisper_model_base

        if running_scribe and last == None:
            return
        running_scribe = True
        # Define audio parameters
        channels = 1  # Mono
        sample_width = 2  # 16-bit audio
        sample_rate = 16000  # Sample rate (Hz)
        output_file = './temp_files/transcribe_real_time_temp.wav'
        # Open the output file in write mode
        with wave.open(output_file, 'wb') as output_wave:
            # Set audio parameters
            output_wave.setnchannels(channels)
            output_wave.setsampwidth(sample_width)
            output_wave.setframerate(sample_rate)

            # Write the audio frames to the file
            output_wave.writeframes(b''.join(frames))

        # print("Audio file saved successfully.")
        result = wisper_model_base.transcribe(output_file)
        # widget.delete(1.0, tk.END)
        widget.insert(tk.END, result["text"] + ". ")
        widget.see(tk.END)
        Entity_Extraction(widget)
        D_Summary(widget)
        running_scribe = False

        # integrate_strings(previous_data, widget.get("1.0", "end"), result["text"])

    if Recording:
        Recording = False
        miniute = second = hour = 0

        Record_btn.config(fg=fg_color)
        Recording_paused = False
        current_time_seconds = time.time()
        current_time_struct = time.localtime(current_time_seconds)
        current_time_words = time.strftime("%A %B %Y,  %I %p", current_time_struct)

        file_name = Conversation_Name_widget.get()
        output_file = path_exe + '\\Audio_Records\\' + f'{file_name} ({current_time_words}).wav'
        save_recoded_conversation(rf"{output_file}")
        Conversation_Name_widget.configure(state='normal')
        transcribe_audio(audio_frames, widget1)
        return

    while True:
        """
        if vosk_model == None:
            continue
        """
        messages = Queue()
        recordings = Queue()
        index = 0
        FRAME_RATE = 16000
        rec = KaldiRecognizer(vosk_model, FRAME_RATE)
        rec.SetWords(True)
        threading.Thread(target=start_recording).start()
        speech_record_time(clock_wideth)
        Conversation_Name_widget.configure(state='disabled', disabledbackground=darken_hex_color(bg_color))
        break


def speech_record_time(widget):
    def Run(widget=widget):
        global closed, Recording, Recording_paused
        miniute = 0
        hour = 0
        sec = 0
        while True:
            if closed or not Recording:
                break
            if Recording_paused:
                continue

            time_text = f"{hour}:{miniute}:{sec}"
            sec = sec + 1
            if sec == 60:
                sec = 0
                miniute = miniute + 1
                if miniute == 60:
                    miniute = 0
                    hour = hour + 1
            widget.config(text=time_text)
            time.sleep(1)

        widget.config(text='0:0:0')

    threading.Thread(target=Run).start()


def set_recording_paused(widget):
    def run(widget=widget):
        global Recording_paused, fg_color, Recording
        print('set_recording_paused')
        if Recording:
            if Recording_paused == False:
                widget.config(fg='green')
                Recording_paused = True
            else:
                widget.config(fg=fg_color)
                Recording_paused = False
        else:
            widget.config(fg=fg_color)

    threading.Thread(target=run).start()


def upload_audio_file(widget, bt_widget):
    def run(widget=widget, bt_widget=bt_widget):
        global audio_processing
        audio_processing = False
        filetypes = [("Audio Files", "*.mp3;*.wav;*.ogg;*.flac;*.aac")]
        file_path = filedialog.askopenfilename(filetypes=filetypes)

        def visual(bt_widget=bt_widget):
            global audio_processing
            global fg_color
            color = 'yellow'
            while audio_processing:
                if color == 'yellow':
                    bt_widget.config(fg=color)
                    color = 'red'
                else:
                    bt_widget.config(fg=color)
                    color = 'yellow'
                time.sleep(0.1)

            bt_widget.config(fg=fg_color)

        if file_path:
            audio_processing = True
            threading.Thread(target=visual).start()
            model = whisper.load_model("base")
            result = model.transcribe(rf"{file_path}")
            print(result["text"])
            widget.delete(1.0, tk.END)
            widget.insert(tk.END, result["text"])
            audio_processing = False

    threading.Thread(target=run).start()


def download_transcribed_audio(widget):
    def visual(bt_widget=widget):
        global downloading_audio
        global fg_color
        color = 'yellow'
        while downloading_audio:
            if color == 'yellow':
                bt_widget.config(fg=color)
                color = 'gold'
            else:
                bt_widget.config(fg=color)
                color = 'yellow'
            time.sleep(0.1)
        bt_widget.config(fg=fg_color)

    def run(widget=widget):
        global audio_frames, downloading_audio
        if not downloading_audio:
            downloading_audio = True

            folder_selected = filedialog.askdirectory()
            if folder_selected:
                threading.Thread(target=visual).start()
                channels = 1  # Mono
                sample_width = 2  # 16-bit audio
                sample_rate = 16000  # Sample rate (Hz)
                output_file = rf'{folder_selected}/conversation_scribe.wav'
                print(folder_selected)
                save_recoded_conversation(output_file)

            downloading_audio = False

    threading.Thread(target=run).start()


def save_recoded_conversation(output_file):
    global saving_audio
    saving_audio = True

    def visual():
        global ref_btn
        global saving_audio
        global fg_color
        color = 'yellow'
        while saving_audio:
            if color == 'yellow':
                ref_btn.config(fg=color)
                color = 'gold'
            else:
                ref_btn.config(fg=color)
                color = 'yellow'
            time.sleep(0.1)
        ref_btn.config(fg=fg_color)

    def save_recoded_conversation_thread(output_file=output_file):
        global audio_frames, saving_audio
        print("save_recoded_conversation: ", output_file)
        threading.Thread(target=visual).start()
        channels = 1  # Mono
        sample_width = 2  # 16-bit audio
        sample_rate = 16000  # Sample rate (Hz)
        # Open the output file in write mode
        with wave.open(output_file, 'wb') as output_wave:
            # Set audio parameters
            output_wave.setnchannels(channels)
            output_wave.setsampwidth(sample_width)
            output_wave.setframerate(sample_rate)
            output_wave.writeframes(b''.join(audio_frames))

        mp3_file = output_file.strip(".wav")
        mp3_file = mp3_file + ".mp3"
        convert_wav_to_mp3(output_file, mp3_file)
        os.remove(output_file)

        saving_audio = False

    threading.Thread(target=save_recoded_conversation_thread).start()


def convert_wav_to_mp3(wav_file, mp3_file):
    # Load the WAV file
    audio = AudioSegment.from_wav(wav_file)

    # Export the audio as MP3
    audio.export(mp3_file, format="mp3")


def integrate_strings(old, edited, new):
    old = old.split()
    edited = edited.split()
    new = new.split()
    print(len(old))
    pos = len(old) - 1
    data = new[pos:]
    edited.extend(data)
    integrate = ''
    for i in edited:
        integrate += i + ' '
    print("============= ", integrate)


# =============================== OCR Functions definition ===============================================================================================================

def image_text_extract_printed(image_path):
    etracted_clincal_text = pytesseract.image_to_string(Image.open(image_path))
    print(etracted_clincal_text)


def view_data_update():
    def run_function():
        global extraced_img_data

        processed_data = extraced_img_data.replace("\n", "<br>")
        if "|" in processed_data:
            table = "<table>"
            rows = processed_data.split("<br>")
            headers = "<tr>" + "<th>" + "</th><th>".join(rows[0].split("|")) + "</th>" + "</tr>"
            table_rows = ''
            for row in rows[1:]:
                table_rows += "<tr>"
                table_rows += "<td>" + "</td><td>".join(row.split("|")) + "</td>"
                table_rows += "</tr>"

            table += headers + table_rows
            table += "</table>"
            processed_data = table

        html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                    <link rel="stylesheet" type="text/css" href="./styles.css" />
                    <link rel="stylesheet" type="text/css" href="./Analyzed_Output_.css" />
                    <style id="dynamic-css"></style>
            </head>
            <body> 
            """ + processed_data + """
            </body>
        
            <script>
        
            //--------------- auto refresh CSS --code block-----------------------------------------
            function reloadCSS() {
              const link = document.querySelector('link[rel="stylesheet"]');
              const url = new URL(link.href);
              url.searchParams.set('v', Math.random()); // Or use Date.now() for timestamps
              link.href = url.toString();
            }
            reloadCSS();
            setInterval(reloadCSS, 1000);
            </script>
            </html>
            """
        file_path = "./html/Analyzed_Output_.html"

        # Write the HTML content to the file
        with open(file_path, "w") as html_file:
            html_file.write(html_content)

    threading.Thread(target=run_function).start()


def image_text_extract_Handwriten(view_wid, displ_widg):
    def run1():
        global llm_chain2
        if llm_chain2 == None:
            llm_inference_initializ()

    def run_image_text_extract_Handwriten(view_wid=view_wid, displ_widg=displ_widg):
        global ocr_model, extraced_img_data, llm_chain2, proccessed_img_url

        threading.Thread(target=run1).start()
        view_wid.load_url('file:///' + path_exe + "./html/load_anmation2.html")
        print("error loading Html")
        file_url = "file:///" + os.getcwd()


        if proccessed_img_url != None:

            file_path = proccessed_img_url
            proccessed_img_url = None
        else:
            filetypes = [("Images", "*.png;*.jpg")]
            file_path = filedialog.askopenfilename(filetypes=filetypes)

        if file_path:
            image_path = rf"{file_path}"
            result = ocr_model.ocr(image_path)

            boxes = [res[0] for res in result[0]]  #
            texts = [res[1][0] for res in result[0]]
            scores = [res[1][1] for res in result[0]]

            text = ''
            for idx in range(len(result)):
                res = result[idx]
                for line in res:
                    text += line[1][0] + "\n"
            extraced_img_data = text
            #print(text)

            displ_widg.delete(1.0, tk.END)

            try:
                Question1 = f"""extracted data from an image: "{text}"
                        Dont explain the data, just analyze the extracted data and present it in a formatted way eg a table or a list. 
                    """
                Answer = llm_chain2.invoke(input=f"{str(Question1)}")
                Answer2 = llm_chain2.invoke(input=f"{str(text)}")
                llm_analysis = Answer['text']
                extraced_img_data = llm_analysis
                llm_analysis = llm_analysis + '\n\n' + Answer2['text']
                view_data_update()
            except Exception as e:
                llm_analysis = extraced_img_data
                view_data_update()

            displ_widg.insert(tk.END, llm_analysis)



            font_path = "./Assets/latin.ttf"

            image = Image.open(image_path).convert('RGB')
            annotated = draw_ocr(image, boxes, texts, scores, font_path=font_path)

            # show the image using matplotlib

            im_show = Image.fromarray(annotated)
            im_show.save('./temp_files/extraced_img.jpg')
            file_url += "\\temp_files\\extraced_img.jpg"

            print(file_url)
            view_wid.load_url(file_url)
        else:
            displ_widg.load_url('file:///' + path_exe + "/html/Load_img_request.html")

    view_wid.load_url('file:///' + path_exe + "./html/load_anmation2.html")
    run_image_text_extract_Handwriten()
    #threading.Thread(target=run_image_text_extract_Handwriten).start()

# =============================== scroll Functions definition ===============================================================================================================


def on_mouse_wheel(widget, event):  # Function to handle mouse wheel scrolling
    # Scroll the canvas up or down based on the mouse wheel direction
    if event.delta < 0:
        widget.yview_scroll(1, "units")
    else:
        widget.yview_scroll(-1, "units")


def on_frame_configure(widget, event):  # Update the canvas scrolling region when the large frame changes size
    widget.configure(scrollregion=widget.bbox("all"))
    children = widget.winfo_children()


prevy = 0


def on_touch_scroll(widget, event):
    global prevy

    def xxx(widget=widget, increment=None):
        current_scroll = float(widget.yview()[0])
        new_scroll = max(0.0, min(1.0, current_scroll + increment))
        widget.yview_moveto(new_scroll)

    nowy = event.y_root

    if nowy > prevy:
        xxx(widget, -0.008)
        # widget.yview_scroll(-1, "units")
    elif nowy < prevy:
        xxx(widget, 0.008)
        # widget.yview_scroll(1, "units")

    else:
        event.delta = 0
    prevy = nowy
    widget.unbind_all("<Button-1>"), "+"


def widget_scroll_bind(widget):
    widget.bind("<Configure>", lambda e: on_frame_configure(widget, e))
    widget.bind("<MouseWheel>", lambda e: on_mouse_wheel(widget, e))
    widget.bind("<B1-Motion>", lambda e: on_touch_scroll(widget, e))


def attach_scroll(widget, color=None):
    global bg_color
    if color is None:
        color = bg_color
    FRAME_2 = tk.Frame(widget, bg=color)
    FRAME_2.place(relwidth=1, relheight=1, relx=0, rely=0)
    canvas_FRAME_2 = tk.Canvas(FRAME_2, highlightthickness=0, bg=color)  # Create a Canvas widget to hold the frame and enable scrolling
    canvas_FRAME_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    canvas_FRAME_2_scrollbar = tk.Scrollbar(widget,
                                            command=canvas_FRAME_2.yview)  # Create a Scrollbar and connect it to the Canvas
    canvas_FRAME_2.config(yscrollcommand=canvas_FRAME_2_scrollbar.set)
    canvas_FRAME_2_frame = tk.Frame(canvas_FRAME_2, bg=color)  # Create a frame to hold your content of the canvers
    canvas_FRAME_2.create_window((0, 0), window=canvas_FRAME_2_frame, anchor=tk.NW)
    widget_scroll_bind(canvas_FRAME_2)  # Bind the mouse wheel event to the canvas
    return canvas_FRAME_2_frame, canvas_FRAME_2


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def download_configuration():
    def run_download_configuration():
        global closed
        while True:

            try:
                url = "https://raw.githubusercontent.com/ice-black/Digital-Scribe/main/Data_Raw/system.keys.json"
                filename = './Data_Raw/system.keys.json'
                response = requests.get(url)

                with open(filename, 'wb') as f:
                    f.write(response.content)
                break
            except:
                if closed:
                    break

    threading.Thread(target=run_download_configuration).start()


def Set_Configuration():
    def run_Set_Configuration():
        global gradient_ai_workspace_id, gradient_ai_access_key, assemblyai_access_key, Gem_Key, cipher_suite
        global gradient_ai_finetuned_id, gradient_ai_base_model_id
        global closed
        download_configuration()
        while not closed:
            try:
                with open('./Data_Raw/system.keys.json', 'r') as openfile:  # Reading from json file
                    configs = json.load(openfile)

                    gradient_ai_access_key = configs['_GA_']
                    gradient_ai_workspace_id = configs['_GW_']
                    gradient_ai_finetuned_id = configs['_G_FT_M_']
                    gradient_ai_base_model_id = configs['_G_B_M_']
                    assemblyai_access_key = configs['_AAI_']
                    Gem_Key = configs['_GemAI_']
                    Key_Fernet = configs['CPR_Suite']

                    os.environ['GRADIENT_ACCESS_TOKEN'] = gradient_ai_access_key
                    os.environ['GRADIENT_WORKSPACE_ID'] = gradient_ai_workspace_id
                    print(Key_Fernet.encode())
                    cipher_suite = Fernet(Key_Fernet.encode())
                    threading.Thread(target=GEMINI_LLMs).start()
                    break
            except Exception as e:
                print("Set_Configuration Function:", e)

    run_Set_Configuration()
    # threading.Thread(target=run_Set_Configuration).start()


def themes_configurations():
    global User_Name, User_Pass, User_Image, User_Email, User_Phone
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor, current_theme, nav_bg
    try:
        with open('./Data_Raw/themes_config.json', 'r') as openfile:  # Reading from json file
            keys = json.load(openfile)

            bg_color = keys['bg_color']
            fg_color = keys['fg_color']
            fg_hovercolor = keys['fg_hovercolor']
            bg_hovercolor = keys['bg_hovercolor']
            current_theme = keys['current_theme']
            nav_bg = keys['nav_bg']

            modify_css()
    except Exception as e:
        print("themes_configurations Function:", e)
        modify_css()


def save_themes():
    global User_Name, User_Pass, User_Image, User_Email, User_Phone
    global llm_chain
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor, current_theme, nav_bg

    dic = {
        "bg_color": bg_color,
        "fg_color": fg_color,
        "fg_hovercolor": fg_hovercolor,
        "bg_hovercolor": bg_hovercolor,
        "current_theme": current_theme,
        "nav_bg": nav_bg,
    }

    json_object = json.dumps(dic, indent=4)

    with open("./Data_Raw/themes_config.json", "w") as outfile:
        outfile.write(json_object)


def text_pdf_save(btn_widget, widgets: list):
    def text_pdf_save_visual(bt_widget=btn_widget):
        global downloading_audio
        global fg_color
        color = 'yellow'
        while downloading_audio:
            if color == 'yellow':
                bt_widget.config(fg=color)
                color = 'gold'
            else:
                bt_widget.config(fg=color)
                color = 'yellow'
            time.sleep(0.1)
        bt_widget.config(fg=fg_color)

    def text_pdf_save_run(widgets=widgets):
        global audio_frames, downloading_audio
        if not downloading_audio:
            downloading_audio = True

            folder_selected = filedialog.askdirectory()
            if folder_selected:
                raw_text_data = ''
                for wid in widgets:
                    raw_text_data += "\n\n" + wid.get("1.0", "end")
                pdf_file_name = rf'{folder_selected}/Digital_Scribe(Analysis).docx'
                doc = txt_to_doc()
                doc.add_paragraph(raw_text_data)
                doc.save(pdf_file_name)

            downloading_audio = False

    threading.Thread(target=text_pdf_save_run).start()


def Export_to_TXT_file(wid, file_Name):
    def run_Save_CN_NOTE(wid=wid, file_Name= file_Name):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            with open(f'{folder_selected}/{file_Name}', 'w') as file:
                file.write(wid.get("1.0", "end"))
    threading.Thread(target=run_Save_CN_NOTE ).start()
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def lighten_hex_color(hex_color, factor=0.2):
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')

    # Convert hex to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    # Increase RGB values to lighten the color
    r = min(255, int(r * (1 + factor)))
    g = min(255, int(g * (1 + factor)))
    b = min(255, int(b * (1 + factor)))

    # Convert back to hex
    light_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)

    return light_hex


def darken_hex_color(hex_color, factor=0.2):
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')

    # Convert hex to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    # Decrease RGB values to darken the color
    r = max(0, int(r * (1 - factor)))
    g = max(0, int(g * (1 - factor)))
    b = max(0, int(b * (1 - factor)))

    # Convert back to hex
    dark_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)

    return dark_hex


def change_bg_OnHover(widget, colorOnHover, colorOnLeave=None):  # Color change bg on Mouse Hover
    global bg_color
    widget.bind("<Enter>", func=lambda e: widget.config(background=colorOnHover))
    if colorOnLeave is not None:
        widget.bind("<Leave>", func=lambda e: widget.config(background=colorOnLeave))
    else:
        widget.bind("<Leave>", func=lambda e: widget.config(background=bg_color))


def change_bg_OnHover_light(widget):  # Color change bg on Mouse Hover
    global bg_color
    widget.bind("<Enter>", func=lambda e: widget.config(background=lighten_hex_color(bg_color, factor=0.2)))
    widget.bind("<Leave>", func=lambda e: widget.config(background=bg_color))


def change_bg_OnHover_dark(widget1, widget2):  # Color change bg on Mouse Hover
    global bg_color
    widget1.bind("<Enter>", func=lambda e: (widget1.config(background=lighten_hex_color(bg_color, factor=0.2)), widget2.config(background=lighten_hex_color(bg_color, factor=0.2))))
    widget1.bind("<Leave>", func=lambda e: (widget1.config(background=darken_hex_color(bg_color, factor=0.2)), widget2.config(background=bg_color)))


def change_fg_OnHover(widget, colorOnHover, colorOnLeave=None):  # Color change fg on Mouse Hover
    global fg_color
    widget.bind("<Enter>", func=lambda e: widget.config(fg=colorOnHover))
    if colorOnLeave is not None:
        widget.bind("<Leave>", func=lambda e: widget.config(fg=colorOnLeave))
    else:
        widget.bind("<Leave>", func=lambda e: widget.config(fg=fg_color))


def imagen(image_path, screen_width, screen_height, widget):
    def load_image():
        try:
            image = Image.open(image_path)
        except:
            try:
                image = Image.open(io.BytesIO(image_path))
            except:
                binary_data = base64.b64decode(image_path)  # Decode the string
                image = Image.open(io.BytesIO(binary_data))

        image = image.resize((screen_width, screen_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        widget.config(image=photo)
        widget.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected

    image_thread = threading.Thread(target=load_image)  # Create a thread to load the image asynchronously
    image_thread.start()


def Service_Section(widget):
    nav_bar_color = "white"
    Service_widget = tk.Frame(widget, bg=nav_bar_color)
    # Service_widget.place(relheight=0.3, relwidth=1, rely=0.02, relx=0)

    t2 = tk.Frame(Service_widget, bg=nav_bar_color)
    t2.place(relheight=0.4, relwidth=0.3, rely=0.02, relx=0.02)
    hh = tk.Label(t2, bg=nav_bar_color)
    hh.place(relheight=1, relwidth=0.45, rely=0, relx=0.55)
    imagen('Xtest/12.png', 259, 307, hh)
    tk.Label(t2, bg=nav_bar_color, text='Services', font=("Bauhaus 93", 18)).place(relheight=0.15, relwidth=0.35,
                                                                                   rely=0.04, relx=0.1)
    tk.Label(t2, bg=nav_bar_color, text='Get accesses to therapy, \nMedication Management, \nPersonalized treatment.',
             font=("Calibri", 15)).place(relheight=0.6, relwidth=0.45, rely=0.21, relx=0.05)

    t3 = tk.Frame(Service_widget, bg=nav_bar_color)
    t3.place(relheight=0.4, relwidth=0.15, rely=0.02, relx=0.35)
    tk.Label(t3, bg=nav_bar_color, text='Therapy', anchor='w', font=("Bauhaus 93", 18)).place(relheight=0.11,
                                                                                              relwidth=1, rely=0,
                                                                                              relx=0)

    t3_link_btn1 = tk.Button(t3, bg=nav_bar_color, text='Individual therapy', anchor='w', borderwidth=0, border=0,
                             activebackground=nav_bar_color, font=("Calibri", 13))
    t3_link_btn1.place(relheight=0.1, relwidth=1, rely=0.12, relx=0)
    change_fg_OnHover(t3_link_btn1, 'brown', 'black')
    t3_link_btn2 = tk.Button(t3, bg=nav_bar_color, text='Couples Therapy', anchor='w', borderwidth=0, border=0,
                             activebackground=nav_bar_color, font=("Calibri", 13))
    t3_link_btn2.place(relheight=0.1, relwidth=1, rely=0.23, relx=0)
    change_fg_OnHover(t3_link_btn2, 'brown', 'black')
    t3_link_btn3 = tk.Button(t3, bg=nav_bar_color, text='Therapy For Veterans', anchor='w', borderwidth=0, border=0,
                             activebackground=nav_bar_color, font=("Calibri", 13))
    t3_link_btn3.place(relheight=0.1, relwidth=1, rely=0.34, relx=0)
    change_fg_OnHover(t3_link_btn3, 'brown', 'black')
    t3_link_btn4 = tk.Button(t3, bg=nav_bar_color, text='Messaging therapy', anchor='w', borderwidth=0, border=0,
                             activebackground=nav_bar_color, font=("Calibri", 13))
    t3_link_btn4.place(relheight=0.1, relwidth=1, rely=0.45, relx=0)
    change_fg_OnHover(t3_link_btn4, 'brown', 'black')
    t3_link_btn5 = tk.Button(t3, bg=nav_bar_color, text='Teen therapy', anchor='w', borderwidth=0, border=0, activebackground=nav_bar_color, font=("Calibri", 13))
    t3_link_btn5.place(relheight=0.1, relwidth=1, rely=0.56, relx=0)
    change_fg_OnHover(t3_link_btn5, 'brown', 'black')

    t4 = tk.Frame(Service_widget, bg=nav_bar_color)
    t4.place(relheight=0.4, relwidth=0.15, rely=0.02, relx=0.82)
    tk.Label(t4, bg=nav_bar_color, text='Get treatment for', anchor='w', font=("Bauhaus 93", 18)).place(relheight=0.11, relwidth=1, rely=0, relx=0)

    t4_link_btn1 = tk.Button(t4, bg=nav_bar_color, text='Depression', anchor='w', borderwidth=0, border=0, activebackground=nav_bar_color, font=("Calibri", 13))
    t4_link_btn1.place(relheight=0.1, relwidth=1, rely=0.12, relx=0)
    change_fg_OnHover(t4_link_btn1, 'brown', 'black')
    t4_link_btn2 = tk.Button(t4, bg=nav_bar_color, text='Anxiety', anchor='w', borderwidth=0, border=0, activebackground=nav_bar_color, font=("Calibri", 13))
    t4_link_btn2.place(relheight=0.1, relwidth=1, rely=0.23, relx=0)
    change_fg_OnHover(t4_link_btn2, 'brown', 'black')
    t4_link_btn3 = tk.Button(t4, bg=nav_bar_color, text='Bipolar disorder For Veterans', anchor='w', borderwidth=0,
                             border=0, activebackground=nav_bar_color, font=("Calibri", 13))
    t4_link_btn3.place(relheight=0.1, relwidth=1, rely=0.34, relx=0)
    change_fg_OnHover(t4_link_btn3, 'brown', 'black')
    t4_link_btn4 = tk.Button(t4, bg=nav_bar_color, text='OCD', anchor='w', borderwidth=0, border=0,
                             activebackground=nav_bar_color, font=("Calibri", 13))
    t4_link_btn4.place(relheight=0.1, relwidth=1, rely=0.45, relx=0)
    change_fg_OnHover(t4_link_btn4, 'brown', 'black')
    t4_link_btn5 = tk.Button(t4, bg=nav_bar_color, text='PTSD', anchor='w', borderwidth=0, border=0,
                             activebackground=nav_bar_color, font=("Calibri", 13))
    t4_link_btn5.place(relheight=0.1, relwidth=1, rely=0.56, relx=0)
    change_fg_OnHover(t4_link_btn5, 'brown', 'black')
    t4_link_btn6 = tk.Button(t4, bg=nav_bar_color, text='Post-partum depression', anchor='w', borderwidth=0, border=0,
                             activebackground=nav_bar_color, font=("Calibri", 13))
    t4_link_btn6.place(relheight=0.1, relwidth=1, rely=0.67, relx=0)
    change_fg_OnHover(t4_link_btn6, 'brown', 'black')
    t4_link_btn7 = tk.Button(t4, bg=nav_bar_color, text='Panic disorder', anchor='w', borderwidth=0, border=0,
                             activebackground=nav_bar_color, font=("Calibri", 13))
    t4_link_btn7.place(relheight=0.1, relwidth=1, rely=0.67, relx=0)
    change_fg_OnHover(t4_link_btn7, 'brown', 'black')

    return Service_widget


def image_to_byte_string(image_path):
    with open(image_path, "rb") as image_file:
        byte_string = base64.b64encode(image_file.read()).decode('utf-8')
    return byte_string


def imagen(image_path, screen_width, screen_height, widget):  # image processing
    def load_image():
        global closed
        while not closed:

            global User_Image
            try:
                image = Image.open(image_path)
            except Exception as e:
                try:
                    image = Image.open(io.BytesIO(image_path))
                except Exception as e:
                    print("imagen: ", e)
                    binary_data = base64.b64decode(image_path)  # Decode the string
                    image = Image.open(io.BytesIO(binary_data))

            image = image.resize((screen_width, screen_height), Image.LANCZOS)
            try:
                photo = ImageTk.PhotoImage(image)
            except:
                continue
            widget.config(image=photo)
            widget.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected
            break

    # load_image()
    threading.Thread(target=load_image).start()


def sign_out_request():
    global Home_page_frame, root
    Home_page_frame.destroy()
    os.remove("./Data_Raw/CUR_user.json")


def encrypt_data(text):
    global cipher_suite
    encoded_text = text.encode()
    encrypted_text = cipher_suite.encrypt(encoded_text)
    return encrypted_text


def decrypt_data(encrypted_text):
    global cipher_suite
    decrypted_text = cipher_suite.decrypt(encrypted_text)
    return decrypted_text.decode()


def login_Request(email, passw, widget=None):
    global root, User_Email, User_Pass, User_Name, User_Image, User_Phone
    global now_date
    email = email.strip()
    passw = passw.strip()
    try:
        auth.sign_in_with_email_and_password(email, passw)
        userInfo = auth.current_user
        idToken = userInfo['idToken']
        displayName = userInfo['displayName']
        expiresIn = userInfo['expiresIn']
        email = userInfo['email']

        if widget is not None:
            widget.config(text="")

        User_Email = email
        User_Pass = passw
        User_Name = ''
        User_Image = ''
        User_Phone = ''

        dic = {
            "_E_token_": encrypt_data(email).decode(),
            "_P_token_": encrypt_data(passw).decode(),
            "_CERT_DT_": now_date.strftime("%Y,%m,%d")
        }

        json_object = json.dumps(dic, indent=4)

        with open("./Data_Raw/CUR_user.json", "w") as outfile:
            outfile.write(json_object)

        User_Home_page(root)

    except Exception as e:
        print("Loging process error :", e)
        if widget is not None:
            widget.config(text="Login Authentication Error. Check your login cridentials !!")


def sign_up_Request(email, passw, status_widget):
    email = email.strip()
    passw = passw.strip()
    try:
        auth.create_user_with_email_and_password(email, passw)
        status_widget.config(text='')
    except Exception as e:
        status_widget.config(text='Sign Up Error. Please Try Again')
        print(e)


def forgot_pass_Request(email, status_widget):
    email = email.strip()
    try:
        auth.send_password_reset_email(email)
        status_widget.config(text="Successful:  Check your Email", fg='green')
    except:
        status_widget.config(text='Error: check your technical details', fg='red')


def resize(widget, width, heigh):
    global root, screen_width, screen_height

    # Prevent resizing by setting the widget's size to its original size
    widget.config(width=width, height=heigh)
    print("resized")


def on_closing():
    global root, closed, httpd
    print("closing")
    closed = True
    httpd.shutdown()
    httpd.server_close()
    root.destroy()

    # time.sleep(2)
    """
    while True:
        time.sleep(10)
        for thread in threading.enumerate():
            print("- ", thread.name)
    """
    print("closed")
    sys.exit()


# =============================== Pages Functions definition =======================================================================================

def create_floating_frame(transcribed_text_widget):
    global floating_frame, bg_color, fg_color, screen_width, screen_height
    global side_bar_list, gem_Suggestion_model, messages, pop_sugestion_generated

    conversation = transcribed_text_widget.get(1.0, "end")
    conversation = "Medical Conversation: " + conversation

    messages = []
    messages.append({'role': 'user', 'parts': ["REPORT: \n\n" + conversation]})
    pop_sugestion_generated = []

    def contains_any_element(lst, elements):
        for i in lst:
            if i == elements:
                return True
        return False


    def AI_Suggetions(qusstion):
        global gem_Suggestion_model, messages

        messages.append({'role': 'user',
                         'parts': [qusstion]})

        response = gem_Suggestion_model.generate_content(messages)
        messages.append({'role': 'model',
                         'parts': [response.text]})

        response = response.text.replace("\n", "")
        pattern = r'\[.*?\]'
        print("response : \n", response)
        print("\n\nmessages : \n", messages)
        matches = re.findall(pattern, response)
        match = ''
        for match in matches:
            print(match)

        list_from_string = ast.literal_eval(match)
        print("LG_I", list_from_string)

        return list_from_string

    def choosen_option(widget, text):
        widget.insert(0, text)

    def Show_PopUp(widget0, widget, qestion, btn=None):
        def Run_Show_PopUp(widget0=widget0, widget=widget, qestion=qestion, btn=btn):
            global pop_sugestion_generated
            global v_status, fg_color, bg_color

            v_status = True

            def visual(wd):
                global v_status, fg_color
                color = "yellow"
                while  v_status:
                    if color != "yellow":
                         color = "yellow"
                         wd.config(fg=color)
                    else:
                        color = "white"
                        wd.config(fg=color)

                    time.sleep(0.4)


                wd.config(fg=fg_color)

            if contains_any_element(pop_sugestion_generated, widget ):
                return
            else:
                threading.Thread(target= visual, args=(btn,)).start()
                pop_ = tk.Frame(widget0, bg=darken_hex_color(bg_color))
                relx = widget.place_info()["relx"]
                rely = widget.place_info()["rely"]
                relwidth = widget.place_info()["relwidth"]
                relheight = widget.place_info()["relheight"]

                rely = float(float(rely) + float(relheight))
                relheight = float(float(relheight) + float(0.2))

                pop_.place(relheight=relheight, relwidth=relwidth, rely=rely, relx=relx)
                pop_.bind("<Leave>", func=lambda e: pop_.place_forget())
                btn.bind("<Enter>", func=lambda e: pop_.place(relheight=relheight, relwidth=relwidth, rely=rely, relx=relx))

                k = AI_Suggetions(qestion)
                ry = 0
                for i in k:
                    tk.Button(pop_, text=i, bg=darken_hex_color(bg_color), fg=fg_color, font=("Times New Roman", 11, "italic"), anchor="w", command=lambda k = i: choosen_option(widget, k)).place(relheight=0.1, relwidth=1, relx=0, rely=ry)
                    ry += 0.1
                pop_sugestion_generated.append(widget)
                v_status = False

        threading.Thread(target=Run_Show_PopUp).start()

    def active_side_bar(widget):
        global side_bar_list
        for i in side_bar_list:
            if i == widget:
                i.config(fg="yellow")
            else:
                i.config(fg=fg_color)

    if floating_frame is not None:
        if floating_frame.winfo_exists():
            floating_frame.deiconify()
            return
        else:
            floating_frame = None
            side_bar_list = None
    print('transcribed_text_widget', transcribed_text_widget)
    # Create a new Toplevel window (floating frame)
    side_bar_list = []
    floating_frame = tk.Toplevel(root)
    floating_frame.attributes('-toolwindow', True)
    title_bar_color(floating_frame, bg_color)
    floating_frame.config(bg=darken_hex_color(bg_color))

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    frame_width = int(screen_width * 3 / 4)
    frame_height = int(screen_height * 3 / 4)

    # Calculate the position to center the frame on the screen

    x_position = (screen_width // 2) - (frame_width // 2)
    y_position = (screen_height // 2) - (frame_height // 2)
    floating_frame.geometry(f"{frame_width}x{frame_height}+{x_position}+{y_position}")  # Set the size of the floating frame

    # --------------------------------------------------------------------------------------------------------------------------------------------------
    side_bar = tk.Frame(floating_frame, bg=bg_color)
    side_bar.place(relwidth=0.2, relheight=1, rely=0, relx=0)

    btn0 = tk.Button(side_bar, borderwidth=0, border=0, text="\tMEDICAL HISTORY", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: (container0.tkraise(), active_side_bar(btn0)))
    btn0.place(relheight=0.07, relwidth=1, relx=0, rely=0)
    btn1 = tk.Button(side_bar, borderwidth=0, border=0, text="\tALLERGIES", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: (container1.tkraise(), active_side_bar(btn1)))
    btn1.place(relheight=0.07, relwidth=1, relx=0, rely=0.07)
    btn2 = tk.Button(side_bar, borderwidth=0, border=0, text="\tEXAMINATION", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: (container2.tkraise(), active_side_bar(btn2)))
    btn2.place(relheight=0.07, relwidth=1, relx=0, rely=0.14)
    btn3 = tk.Button(side_bar, borderwidth=0, border=0, text="\tVITALS", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: (container3.tkraise(), active_side_bar(btn3)))
    btn3.place(relheight=0.07, relwidth=1, relx=0, rely=0.21)
    btn4 = tk.Button(side_bar, borderwidth=0, border=0, text="\tDIAGNOSES", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: (container4.tkraise(), active_side_bar(btn4)))
    btn4.place(relheight=0.07, relwidth=1, relx=0, rely=0.28)
    side_bar_list.extend([btn0, btn1, btn2, btn3, btn4])

    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container0 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container0.place(relheight=1, relwidth=0.79, relx=0.21, rely=0)

    MHL_00 = tk.Label(container0, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="History Type", anchor="sw", font=("Times New Roman", 11, "italic"))
    MHL_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0)
    MHE_00 = tk.Entry(container0, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    MHE_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.05)
    pop1 = tk.Button(container0, text="V", bg=bg_color, fg=fg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, borderwidth=0, border=0,
                     command=lambda: Show_PopUp(container0, MHE_00, "in python list format extract Medical History types from the conversations. start with [ and end with ]", pop1))
    pop1.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.05)

    MHL_11 = tk.Label(container0, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Notes", anchor="sw", font=("Times New Roman", 11, "italic"))
    MHL_11.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.11)
    MHE_11 = tk.Text(container0, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    MHE_11.place(relheight=0.8, relwidth=0.9, relx=0.05, rely=0.16)

    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container1 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container1.place(relheight=1, relwidth=0.79, relx=0.21, rely=0)

    ALl_00 = tk.Label(container1, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Allergy Category", anchor="sw", font=("Times New Roman", 11, "italic"))
    ALl_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0)
    ALe_00 = tk.Entry(container1, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    ALe_00.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.05)
    pop_ALe_00 = tk.Button(container1, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                           command=lambda: Show_PopUp(container1, ALe_00, "in python list format extract Allergy Category from the conversations. start with [ and end with ]", pop_ALe_00))
    pop_ALe_00.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.05)

    ALLlB_11 = tk.Label(container1, borderwidth=0, border=0, text="Allergen", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11, "italic"))
    ALLlB_11.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0)
    ALLEN_11 = tk.Entry(container1, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    ALLEN_11.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.05)
    pop_EN_11 = tk.Button(container1, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                          command=lambda: Show_PopUp(container1, ALLEN_11, "in python list format extract Allergen from the conversations. start with [ and end with ]", pop_EN_11))
    pop_EN_11.place(relheight=0.05, relwidth=0.015, relx=0.95, rely=0.05)

    SElB_22 = tk.Label(container1, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Severity", anchor="sw", font=("Times New Roman", 11, "italic"))
    SElB_22.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.14)
    SEEN_22 = tk.Entry(container1, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    SEEN_22.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.19)
    pop_EN_22 = tk.Button(container1, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                          command=lambda: Show_PopUp(container1, SEEN_22, "in python list format extract Allergen Severity from the conversations. start with [ and end with ]", pop_EN_22))
    pop_EN_22.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.19)

    lB_44 = tk.Label(container1, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Note", anchor="sw", font=("Times New Roman", 11, "italic"))
    lB_44.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.28)
    EN_44 = tk.Text(container1, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EN_44.place(relheight=0.6, relwidth=0.9, relx=0.05, rely=0.33)

    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container2 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container2.place(relheight=1, relwidth=0.79, relx=0.21, rely=0)

    EXL_00 = tk.Label(container2, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Examination Type", anchor="sw", font=("Times New Roman", 11, "italic"))
    EXL_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0)
    EXE_00 = tk.Entry(container2, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EXE_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.05)
    pop_EXE_00 = tk.Button(container2, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                           command=lambda: Show_PopUp(container2, EXE_00, "in python list format extract Examination Type performed by the doctor from the conversations. start with [ and end with ]", pop_EXE_00))
    pop_EXE_00.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.05)

    EXL_11 = tk.Label(container2, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Notes", anchor="sw", font=("Times New Roman", 11, "italic"))
    EXL_11.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.11)
    EXE_11 = tk.Text(container2, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EXE_11.place(relheight=0.8, relwidth=0.9, relx=0.05, rely=0.16)

    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container3 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container3.place(relheight=1, relwidth=0.79, relx=0.21, rely=0)

    BTlB_00 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Body Temperature ('C)", anchor="sw", font=("Times New Roman", 11, "italic"))
    BTlB_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0)
    BTBEN_00 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    BTBEN_00.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.05)
    pop_DEN_00 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                           command=lambda: Show_PopUp(container3, BTBEN_00, "in python list format extract Body Temperature's from the conversations. start with [ and end with ]", pop_DEN_00))
    pop_DEN_00.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.05)

    RRlB_11 = tk.Label(container3, borderwidth=0, border=0, text="Respiration Rate (BPM)", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11, "italic"))
    RRlB_11.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0)
    RRREN_11 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    RRREN_11.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.05)
    pop_DEN_11 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                           command=lambda: Show_PopUp(container3, RRREN_11, "in python list format extract Respiration Rate's from the conversations. start with [ and end with ]", pop_DEN_11))
    pop_DEN_11.place(relheight=0.05, relwidth=0.015, relx=0.95, rely=0.05)

    HRlB_22 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Heart Rate (BPM)", anchor="sw", font=("Times New Roman", 11, "italic"))
    HRlB_22.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.14)
    HREN_22 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    HREN_22.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.19)
    pop_DEN_22 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                           command=lambda: Show_PopUp(container3, HREN_22, "in python list format extract Heart Rate (BPM) from the conversations. start with [ and end with ]", pop_DEN_22))
    pop_DEN_22.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.19)

    OSlB_33 = tk.Label(container3, borderwidth=0, border=0, text="Oxygen saturation (BPM)", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11, "italic"))
    OSlB_33.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0.14)
    OSEN_33 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    OSEN_33.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.19)
    pop_DEN_33 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                           command=lambda: Show_PopUp(container3, OSEN_33, "in python list format extract Oxygen saturation (BPM) from the conversations. start with [ and end with ]", pop_DEN_33))
    pop_DEN_33.place(relheight=0.05, relwidth=0.015, relx=0.95, rely=0.19)

    SBlB_44 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Systolic Blood Pressure", anchor="sw", font=("Times New Roman", 11, "italic"))
    SBlB_44.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.28)
    SBEN_44 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    SBEN_44.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.33)
    pop_DEN_55 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                           command=lambda: Show_PopUp(container3, SBEN_44, "in python list format extract Systolic Blood Pressure from the conversations. start with [ and end with ]", pop_DEN_55))
    pop_DEN_55.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.33)

    DBlB_55 = tk.Label(container3, borderwidth=0, border=0, text="Diastolic Blood Pressure", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11, "italic"))
    DBlB_55.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0.28)
    DBEN_55 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    DBEN_55.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.33)
    pop_DEN_66 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                           command=lambda: Show_PopUp(container3, DBEN_55, "in python list format extract Diastolic Blood Pressure from the conversations. start with [ and end with ]", pop_DEN_66))
    pop_DEN_66.place(relheight=0.05, relwidth=0.015, relx=0.95, rely=0.33)

    PlB_66 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Pulse Rate", anchor="sw", font=("Times New Roman", 11, "italic"))
    PlB_66.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.42)
    PEN_66 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    PEN_66.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.47)
    pop_DEN_66 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                           command=lambda: Show_PopUp(container3, PEN_66, "in python list format extract Pulse Rate from the conversations. start with [ and end with ]"))
    pop_DEN_66.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.47)

    HlB_77 = tk.Label(container3, borderwidth=0, border=0, text="Height (cm)", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11, "italic"))
    HlB_77.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0.42)
    HEN_77 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    HEN_77.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.47)
    pop_DEN_77 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                           command=lambda: Show_PopUp(container3, HEN_77, "in python list format extract patient Height (cm) from the conversations. start with [ and end with ]", pop_DEN_77))
    pop_DEN_77.place(relheight=0.05, relwidth=0.015, relx=0.95, rely=0.47)

    WlB_88 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Weight (KG)", anchor="sw", font=("Times New Roman", 11, "italic"))
    WlB_88.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.56)
    WEN_88 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    WEN_88.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.61)
    pop_DEN_88 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                           command=lambda: Show_PopUp(container3, WEN_88, "in python list format extract patient Weight (KG) from the conversations. start with [ and end with ]", pop_DEN_88))
    pop_DEN_88.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.61)

    BMlB_11 = tk.Label(container3, borderwidth=0, border=0, text="BM", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11, "italic"))
    BMlB_11.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0.56)
    BMEN_11 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    BMEN_11.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.61)
    #pop_DEN_00 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container3, BMEN_11, "Hel"))
    #pop_DEN_00.place(relheight=0.05, relwidth=0.015, relx=0.95, rely=0.61)

    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container4 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container4.place(relheight=1, relwidth=0.795, relx=0.205, rely=0)

    DlB_00 = tk.Label(container4, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Clinical Impression Type", anchor="sw", font=("Times New Roman", 11, "italic"))
    DlB_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0)
    DEN_00 = tk.Entry(container4, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    DEN_00.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.05)
    pop_DEN_00 = tk.Button(container4, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                           command=lambda: Show_PopUp(container4, DEN_00, "in python list format extract Clinical Impression Type from the conversations. start with [ and end with ]", pop_DEN_00))
    pop_DEN_00.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.05)

    DlB_11 = tk.Label(container4, borderwidth=0, border=0, text="Differential Diagnoses", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11, "italic"))
    DlB_11.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0)
    DEN_11 = tk.Entry(container4, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    DEN_11.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.05)
    pop_DEN_11 = tk.Button(container4, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                           command=lambda: Show_PopUp(container4, DEN_11, "in python list format extract Differential Diagnoses from the conversations. start with [ and end with ]", pop_DEN_11))
    pop_DEN_11.place(relheight=0.05, relwidth=0.015, relx=0.95, rely=0.05)

    DlB_22 = tk.Label(container4, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Co-Existing Conditions", anchor="sw", font=("Times New Roman", 11, "italic"))
    DlB_22.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.14)
    DEN_22 = tk.Entry(container4, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    DEN_22.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.19)
    pop_DEN_22 = tk.Button(container4, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0,
                           command=lambda: Show_PopUp(container4, DEN_22, "in python list format extract Co-Existing Conditions from the conversations. start with [ and end with ]", pop_DEN_22))
    pop_DEN_22.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.19)

    lB_44 = tk.Label(container4, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Notes", anchor="sw", font=("Times New Roman", 11, "italic"))
    lB_44.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.28)
    EN_44 = tk.Text(container4, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EN_44.place(relheight=0.6, relwidth=0.9, relx=0.05, rely=0.33)

    container0.tkraise()
    active_side_bar(btn0)


def Login_Section_widget(widget):
    global screen_width, screen_height, bg_color, fg_color
    nav_bar_color = darken_hex_color(bg_color)
    Login_widget = tk.Frame(widget, bg=nav_bar_color)

    # Login_widget.place(relheight=0.3, relwidth=1, rely=0.02, relx=0)

    # ---------------------------------------------------------------- Forgot password section --------------------------------------------------

    Forgot_section = tk.Frame(Login_widget, bg=nav_bar_color, borderwidth=0, border=0)
    Forgot_section.place(relheight=0.7, relwidth=0.25, rely=0.05, relx=0.01)

    tk.Label(Forgot_section, bg=nav_bar_color, fg=lighten_hex_color(bg_color), text='🔎', font=("Bahnschrift SemiLight Condensed", 36), borderwidth=0, border=0).place(relheight=0.1, relwidth=1, rely=0, relx=0)
    tk.Label(Forgot_section, bg=nav_bar_color, fg=lighten_hex_color(bg_color), text='Forgot your password?', font=("Bahnschrift SemiLight Condensed", 36), borderwidth=0, border=0).place(relheight=0.1, relwidth=1, rely=0.1, relx=0)
    tk.Label(Forgot_section, bg=nav_bar_color, fg=lighten_hex_color(bg_color), text='Please enter the email address you used to register.\nWe’ll send a link with instructions to reset your password', font=("Bahnschrift SemiLight Condensed", 12), borderwidth=0, border=0).place(relheight=0.12, relwidth=1, rely=0.2, relx=0)
    tk.Label(Forgot_section, bg=nav_bar_color, fg=lighten_hex_color(bg_color), text='email', anchor='w', font=("Batang", 9), borderwidth=0, border=0).place(relheight=0.03, relwidth=0.8, rely=0.395, relx=0.1)

    email_password_entry_widg = tk.Entry(Forgot_section, bg=bg_color, fg=fg_color, font=("Courier New", 13), relief="solid", borderwidth=1, border=1)
    email_password_entry_widg.place(relheight=0.1, relwidth=0.8, rely=0.43, relx=0.1)
    change_bg_OnHover(email_password_entry_widg, 'lightblue', lighten_hex_color(bg_color))

    password_reset__btn = tk.Button(Forgot_section, bg='#1C352D', fg=lighten_hex_color(bg_color), activebackground='#8A9A5B', text='Request Password reset', font=('Aptos Narrow', 11, 'bold'), relief="solid", borderwidth=0, border=0, command=lambda: forgot_pass_Request(email_password_entry_widg.get(), forgot_pass_status))
    password_reset__btn.place(relheight=0.1, relwidth=0.8, rely=0.6, relx=0.1)
    change_bg_OnHover(password_reset__btn, '#004830', '#1C352D')

    tk.Label(Forgot_section, bg=nav_bar_color, fg=lighten_hex_color(bg_color), activebackground='#8A9A5B', text='No Account ?', font=('Aptos Narrow', 10), relief="solid", anchor='w', borderwidth=0, border=0).place(relheight=0.04, relwidth=0.2, rely=0.72, relx=0.1)
    sign_up_link_0 = tk.Button(Forgot_section, bg=nav_bar_color, fg='#A8E4A0', activeforeground='#A8E4A0', activebackground=nav_bar_color, text='Sign-Up', font=('Aptos Narrow', 10, 'bold'), relief="solid", anchor='w', borderwidth=0, border=0)
    sign_up_link_0.place(relheight=0.04, relwidth=0.3, rely=0.72, relx=0.31)
    change_fg_OnHover(sign_up_link_0, '#00AB66', '#A8E4A0')

    tk.Label(Forgot_section, bg=nav_bar_color, fg=lighten_hex_color(bg_color), activebackground='#8A9A5B', text='Go to Login?', font=('Aptos Narrow', 10), relief="solid", anchor='w', borderwidth=0, border=0).place(relheight=0.04, relwidth=0.2, rely=0.78, relx=0.1)
    Jump_to_login_link = tk.Button(Forgot_section, bg=nav_bar_color, fg='#A8E4A0', activeforeground='#A8E4A0', activebackground=nav_bar_color, text='Login', font=('Aptos Narrow', 10, 'bold'), relief="solid", anchor='w', borderwidth=0, border=0, command=lambda: login_section.tkraise())
    Jump_to_login_link.place(relheight=0.04, relwidth=0.3, rely=0.78, relx=0.31)
    change_fg_OnHover(Jump_to_login_link, '#00AB66', '#A8E4A0')

    forgot_pass_status = tk.Label(Forgot_section, bg=nav_bar_color, fg='red', font=("Bahnschrift", 8, 'italic'))
    forgot_pass_status.place(relheight=0.07, relwidth=1, relx=0, rely=0.93)

    # ---------------------------------------------------------------- sign-up section --------------------------------------------------

    sign_up_section = tk.Frame(Login_widget, bg=nav_bar_color, borderwidth=0, border=0)
    sign_up_section.place(relheight=0.7, relwidth=0.25, rely=0.05, relx=0.01)

    tk.Label(sign_up_section, text='CREATE AN ACCOUNT', bg=nav_bar_color, fg=lighten_hex_color(bg_color), font=("Bahnschrift SemiLight Condensed", 26), borderwidth=0, border=0).place(relheight=0.1, relwidth=1, rely=0, relx=0)
    tk.Label(sign_up_section, text='sign up with us for better doctor-patient medical conversation analysis', fg=lighten_hex_color(bg_color), bg=nav_bar_color, font=("Bahnschrift SemiLight Condensed", 12), borderwidth=0, border=0).place(relheight=0.2, relwidth=1, rely=0.1, relx=0)

    tk.Label(sign_up_section, bg=nav_bar_color, text='email', fg=lighten_hex_color(bg_color), font=("Batang", 9), anchor='w', borderwidth=0, border=0).place(relheight=0.04, relwidth=0.98, rely=0.31, relx=0.01)
    Email_entry_widg = tk.Entry(sign_up_section, fg=fg_color, bg=lighten_hex_color(bg_color), font=("Courier New", 13), relief="solid", borderwidth=1)
    Email_entry_widg.place(relheight=0.08, relwidth=0.98, rely=0.35, relx=0.01)
    change_bg_OnHover(Email_entry_widg, 'lightblue', lighten_hex_color(bg_color))

    tk.Label(sign_up_section, bg=nav_bar_color, text='password', fg=lighten_hex_color(bg_color), font=("Batang", 9), anchor='w', borderwidth=1, border=1).place(relheight=0.04, relwidth=0.98, rely=0.44, relx=0.01)
    password_entry_widg = tk.Entry(sign_up_section, fg=fg_color, bg=lighten_hex_color(bg_color), font=("Courier New", 13), relief="solid", borderwidth=1)
    password_entry_widg.place(relheight=0.08, relwidth=0.98, rely=0.48, relx=0.01)
    change_bg_OnHover(password_entry_widg, 'lightblue', lighten_hex_color(bg_color))

    login_btn = tk.Button(sign_up_section, bg='#1C352D', fg='white', activebackground='#8A9A5B', text='SIGN UP', foreground=lighten_hex_color(bg_color), font=("Aptos", 15, 'bold'), borderwidth=1, border=0, command=lambda: sign_up_Request(Email_entry_widg.get(), password_entry_widg.get(), sign_up_status))
    login_btn.place(relheight=0.08, relwidth=0.98, rely=0.72, relx=0.01)
    change_bg_OnHover(login_btn, '#004830', '#1C352D')

    tk.Label(sign_up_section, bg=nav_bar_color, text="Have an account?", font=("Aptos Narrow", 10), fg=lighten_hex_color(bg_color), anchor='w', borderwidth=0, border=0).place(relheight=0.04, relwidth=0.4, rely=0.81, relx=0.01)
    Sign_up_login_link = tk.Button(sign_up_section, bg=nav_bar_color, fg='#A8E4A0', activeforeground='#A8E4A0', activebackground=nav_bar_color, text="login", command=lambda: login_section.tkraise(), font=("Aptos Narrow", 11, 'bold'), anchor='w', borderwidth=0, border=0)
    Sign_up_login_link.place(relheight=0.04, relwidth=0.4, rely=0.81, relx=0.41)
    change_fg_OnHover(Sign_up_login_link, '#00AB66', '#A8E4A0')

    tk.Label(sign_up_section, bg=nav_bar_color, text="Forgot Password", font=("Aptos Narrow", 10), fg=lighten_hex_color(bg_color), anchor='w', borderwidth=0, border=0).place(relheight=0.04, relwidth=0.4, rely=0.86, relx=0.01)
    sign_up_link = tk.Button(sign_up_section, bg=nav_bar_color, fg='#A8E4A0', activeforeground='#A8E4A0', activebackground=nav_bar_color, text="passw reset", command=lambda: Forgot_section.tkraise(), font=("Aptos Narrow", 11, 'bold'), anchor='w', borderwidth=0, border=0)
    sign_up_link.place(relheight=0.04, relwidth=0.4, rely=0.86, relx=0.41)
    change_fg_OnHover(sign_up_link, '#00AB66', '#A8E4A0')

    sign_up_status = tk.Label(sign_up_section, bg=nav_bar_color, fg='red', font=("Bahnschrift", 8, 'italic'))
    sign_up_status.place(relheight=0.07, relwidth=1, relx=0, rely=0.93)

    # ---------------------------------------------------------------- Loging section -----------------------------------------------------------------------------

    login_section = tk.Frame(Login_widget, bg=nav_bar_color)
    login_section.place(relheight=0.7, relwidth=0.25, rely=0.05, relx=0.01)
    # .place(relheight=0.7, relwidth=0.25, rely=0.05, relx=0.03)

    tk.Label(login_section, text='Log in to your account', bg=nav_bar_color, fg=lighten_hex_color(bg_color), font=("Bahnschrift SemiLight Condensed", 26), borderwidth=0, border=0).place(relheight=0.1, relwidth=1, rely=0, relx=0)
    tk.Label(login_section, text='Log in to continue your medical scribe journey \ntowards a happier you.', fg=lighten_hex_color(bg_color), bg=nav_bar_color, font=("Bahnschrift SemiLight Condensed", 12), borderwidth=0, border=0).place(relheight=0.2, relwidth=1, rely=0.1, relx=0)

    tk.Label(login_section, bg=nav_bar_color, text='email', fg=lighten_hex_color(bg_color), font=("Batang", 9), anchor='w', borderwidth=0, border=0).place(relheight=0.04, relwidth=0.98, rely=0.31, relx=0.01)
    Email_entry_widg = tk.Entry(login_section, fg=fg_color, bg=lighten_hex_color(bg_color), font=("Courier New", 13), relief="solid", borderwidth=1)
    Email_entry_widg.place(relheight=0.08, relwidth=0.98, rely=0.35, relx=0.01)
    change_bg_OnHover(Email_entry_widg, 'lightblue', lighten_hex_color(bg_color))
    # Email_entry_widg.insert(0, 'm@gmail')

    tk.Label(login_section, bg=nav_bar_color, text='password', fg=lighten_hex_color(bg_color), font=("Batang", 9), anchor='w', borderwidth=1, border=1).place(relheight=0.04, relwidth=0.98, rely=0.44, relx=0.01)
    password_entry_widg = tk.Entry(login_section, fg=fg_color, bg=lighten_hex_color(bg_color), font=("Courier New", 13), relief="solid", borderwidth=1)
    password_entry_widg.place(relheight=0.08, relwidth=0.98, rely=0.48, relx=0.01)
    # password_entry_widg.insert(0, '12maureen12')
    change_bg_OnHover(password_entry_widg, 'lightblue', lighten_hex_color(bg_color))

    Forgot_password_login_link = tk.Button(login_section, bg=nav_bar_color, fg='#74C365', activebackground=nav_bar_color, text='Forgot password', font=("Bradley Hand ITC", 12, 'bold'), anchor='w', borderwidth=0, border=0, command=lambda: Forgot_section.tkraise())
    Forgot_password_login_link.place(relheight=0.04, relwidth=0.5, rely=0.57, relx=0.01)
    change_fg_OnHover(Forgot_password_login_link, '#00AB66', '#A8E4A0')

    login_btn = tk.Button(login_section, bg='#1C352D', fg='white', activebackground='#8A9A5B', text='LOGIN', foreground=lighten_hex_color(bg_color), font=("Aptos", 15, 'bold'), borderwidth=1, border=0, command=lambda: login_Request(Email_entry_widg.get(), password_entry_widg.get(), login_status))
    login_btn.place(relheight=0.08, relwidth=0.98, rely=0.72, relx=0.01)
    change_bg_OnHover(login_btn, '#004830', '#1C352D')
    # password_entry_widg.bind('<Return>', lambda e: login_Request(Email_entry_widg.get(), password_entry_widg.get(), root_widget))
    # Email_entry_widg.bind('<Return>', lambda e: login_Request(Email_entry_widg.get(), password_entry_widg.get(), root_widget))

    tk.Label(login_section, bg=nav_bar_color, text="Don't have an account?", font=("Aptos Narrow", 10), fg=lighten_hex_color(bg_color), anchor='w', borderwidth=0, border=0).place(relheight=0.04, relwidth=0.4, rely=0.81, relx=0.01)
    Sign_up_login_link = tk.Button(login_section, bg=nav_bar_color, fg='#A8E4A0', activeforeground='#A8E4A0', activebackground=nav_bar_color, text="Sign up", command=lambda: sign_up_section.tkraise(), font=("Aptos Narrow", 11, 'bold'), anchor='w', borderwidth=0, border=0)
    Sign_up_login_link.place(relheight=0.04, relwidth=0.4, rely=0.81, relx=0.41)
    change_fg_OnHover(Sign_up_login_link, '#00AB66', '#A8E4A0')

    tk.Label(login_section, bg=nav_bar_color, text="Provider?", font=("Aptos Narrow", 10), fg=lighten_hex_color(bg_color), anchor='w', borderwidth=0, border=0).place(relheight=0.04, relwidth=0.4, rely=0.86, relx=0.01)
    therapist_login_link = tk.Button(login_section, bg=nav_bar_color, fg='#A8E4A0', activeforeground='#A8E4A0', activebackground=nav_bar_color, text="Log in", font=("Aptos Narrow", 11, 'bold'), anchor='w', borderwidth=0, border=0)
    therapist_login_link.place(relheight=0.04, relwidth=0.4, rely=0.86, relx=0.41)
    change_fg_OnHover(therapist_login_link, '#00AB66', '#A8E4A0')

    login_status = tk.Label(login_section, bg=nav_bar_color, fg='red', font=("Bahnschrift", 8, 'italic'))
    login_status.place(relheight=0.07, relwidth=1, relx=0, rely=0.93)
    # ------------------------------------

    img = tk.Label(Login_widget, bg=nav_bar_color, font=("Bahnschrift SemiLight Condensed", 26), borderwidth=0, border=0)
    img.place(relheight=0.9, relwidth=0.65, rely=0.05, relx=0.3)
    imagen("./Assets/login_img 1.png", int(screen_width * 0.65), int(screen_height * 0.5 * 0.9), img)
    # imagen('./login_pic.png', int(screen_width * 1 * 0.65), int(screen_height * 2 * 0.3 * 0.9), img)

    # Login_widget.place(relheight=0.5, relwidth=1, rely=0.1, relx=0)
    return Login_widget


def Main_Page(widget):
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor
    global Recording_paused, font_size, transcribed_text_widget

    def font_change(widget1, widget2, widget3):
        global defalt_font_style, defalt_font_size, closed

        defalt_font_style = 'Times New Roman'
        defalt_font_size = 13

        while not closed:
            try:
                font_style = widget1.cget("text")
                font_size = widget2.get()
                font_size = font_size.strip()
                font_style = font_style.strip()
                if font_size == '':
                    font_size = '8'
                if int(font_size) < 0:
                    font_size = '8'
                if int(font_size) > 100:
                    font_size = '100'

                if defalt_font_style != font_style.strip() or defalt_font_size != int(font_size):
                    try:
                        for i in widget3:
                            i.config(font=(font_style, font_size))
                        defalt_font_style = font_style.strip()
                        defalt_font_size = int(font_size)
                        print('changed')
                    except Exception as e:
                        print('font_change error :', e)

                time.sleep(1)
            except Exception as e:
                print(e)

    def font_style(widget):
        widg_text = widget.cget("text")
        if widg_text == "Times New Roman":
            f_style = "Bahnschrift"
            widget.config(text=f_style)
        elif widg_text == "Bahnschrift":
            f_style = "Courier New"
            widget.config(text=f_style)
        elif widg_text == "Courier New":
            f_style = "Calibri"
            widget.config(text=f_style)
        elif widg_text == "Calibri":
            f_style = "Arial Narrow"
            widget.config(text=f_style)
        elif widg_text == "Arial Narrow":
            f_style = "Blackadder ITC"
            widget.config(text=f_style)
        elif widg_text == "Blackadder ITC":
            f_style = "Candara"
            widget.config(text=f_style)
        elif widg_text == "Candara":
            f_style = "Georgia"
            widget.config(text=f_style)
        elif widg_text == "Georgia":
            f_style = "Times New Roman"
            widget.config(text=f_style)

    defalt_font_style = 'Times New Roman'
    defalt_font_size = 13
    nav_bar_bg_color = bg_color

    chatbot_widget = tk.Frame(widget, bg=bg_color, borderwidth=0, border=0)
    chatbot_widget.place(relheight=1, relwidth=1, rely=0, relx=0)

    # ================================ Navbar ==============================================================================================================================================================

    navbar = tk.Frame(chatbot_widget, bg=nav_bar_bg_color, borderwidth=0, border=0)
    navbar.place(relheight=0.03, relwidth=1, rely=0, relx=0)

    font_ = tk.Frame(navbar, bg=nav_bar_bg_color, borderwidth=2, border=0)
    font_.place(relheight=0.70, relwidth=0.2, rely=0.15, relx=0.02)

    font_style_btn0 = tk.Button(font_, bg=nav_bar_bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color, text="Times New Roman", relief=tk.GROOVE, font=("Times New Roman", 10), borderwidth=0, border=1, command=lambda: font_style(font_style_btn0))
    font_style_btn0.place(relheight=0.8, relwidth=0.7, rely=0.1, relx=0)

    font_style_btn = tk.Button(font_, text='v', bg=nav_bar_bg_color, activebackground=nav_bar_bg_color, fg=fg_color, relief=tk.GROOVE, font=("Times New Roman", 13, 'bold'), borderwidth=0, border=1)
    font_style_btn.place(relheight=0.8, relwidth=0.09, rely=0.1, relx=0.7)

    font_size_entry = tk.Entry(font_, bg=nav_bar_bg_color, fg=fg_color, relief=tk.GROOVE, font=("Times New Roman", 10), borderwidth=0, border=1)
    font_size_entry.place(relheight=0.8, relwidth=0.19, rely=0.1, relx=0.8)

    # ======================================================================================================================================================================================================

    paned_window = tk.PanedWindow(chatbot_widget, bg=bg_color, orient=tk.VERTICAL, sashwidth=8, sashrelief=tk.FLAT)
    paned_window.place(relheight=0.96, relwidth=0.75, rely=0.03, relx=0.0253)

    t1 = tk.Text(paned_window, bg=bg_color, fg='gray', relief=tk.SUNKEN, wrap="word", font=("Times New Roman", 13), borderwidth=2, border=1)  # t4.place(relheight=0.70, relwidth=0.75, rely=0.03, relx=0.0253)
    t1.tag_configure("ASR", foreground="gray")
    t2 = tk.Text(paned_window, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, wrap="word", font=("Times New Roman", 13), borderwidth=4, border=1)
    t2.tag_configure("error_config", foreground="#CD5C5C", justify=tk.LEFT)  # t2.place(relheight=0.25, relwidth=0.75, rely=0.74, relx=0.0253)
    t3 = tk.Text(paned_window, bg=darken_hex_color(bg_color), fg=fg_color, relief=tk.SUNKEN, wrap="word", font=("Times New Roman", 13), borderwidth=4, border=1)
    t3.tag_configure("ASR", foreground="gray", font=("Broadway"))
    text_list_widget.append(t3)

    paned_window.add(t1)
    paned_window.add(t2)
    paned_window.add(t3)

    threading.Thread(target=font_change, args=(font_style_btn0, font_size_entry, [t1, t2, t3])).start()

    entity_section = tk.Frame(chatbot_widget, bg='brown', borderwidth=0, border=0)
    entity_section.place(relheight=0.72, relwidth=0.21, rely=0.03, relx=0.78)

    title = tk.Frame(entity_section, bg=bg_color, borderwidth=2, border=1)
    title.place(relheight=0.036, relwidth=1, rely=0, relx=0)
    tk.Label(title, text="Field Name", bg=bg_color, fg=fg_color, borderwidth=0, border=0, font=("Georgia", 11, 'bold')).place(relx=0.01, rely=0.04, relwidth=0.5, relheight=1)
    tk.Label(title, text="Type", bg=bg_color, fg=fg_color, borderwidth=0, border=0, font=("Georgia", 11, 'bold')).place(relx=0.52, rely=0.04, relwidth=0.2, relheight=1)

    fr = tk.Frame(entity_section, bg=bg_color, borderwidth=0, border=0)
    fr.place(relheight=0.97, relwidth=1, rely=0.036, relx=0)
    user_page_widget, user_page_canvas = attach_scroll(fr, bg_color)
    fr2 = tk.Frame(user_page_widget, bg=bg_color, borderwidth=0, border=0, height=4000, width=int(screen_width * 0.9747 * 0.21))
    fr2.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    def add(widget):
        global entity_type, entity_widg_list

        def delet_widget(widget):
            widget.destroy()
            for i in entity_widg_list:
                if i[0] == widget:
                    entity_widg_list.remove(i)

        def change_type(widget):
            widg_text = widget.cget("text")
            if widg_text == "STRING":
                entity_type = "NUMBER"
                widget.config(text=entity_type)
            elif widg_text == "NUMBER":
                entity_type = "BOOLEAN"
                widget.config(text=entity_type)
            else:
                entity_type = "STRING"
                widget.config(text=entity_type)

        chk_var = tk.BooleanVar(value=False)

        new_entity = tk.Frame(widget, bg=bg_color, borderwidth=2, border=1, height=50, width=int(screen_width * 0.9747 * 0.21 - 3))
        new_entity.pack(side=tk.TOP, fill=tk.X)

        entity_name = tk.Entry(new_entity, bg=bg_color, fg=fg_color, borderwidth=0, border=1, font=("Times New Roman", 11))
        entity_name.place(relx=0.01, rely=0, relwidth=0.5, relheight=0.9)
        entity_type = tk.Button(new_entity, bg=bg_color, fg=fg_color, activeforeground=fg_color, text="STRING", font=("Times New Roman", 10, 'bold'), relief=tk.SUNKEN, activebackground=bg_color, borderwidth=0, border=1)
        entity_type.config(command=lambda k=entity_type: change_type(k))
        entity_type.place(relx=0.52, rely=0, relwidth=0.2, relheight=0.9)
        entity_requred = tk.Checkbutton(new_entity, background=bg_color, activebackground=bg_color, variable=chk_var, onvalue=True, offvalue=False)
        entity_requred.place(relx=0.8, rely=0, relwidth=0.1, relheight=1)
        close_widg = tk.Button(new_entity, bg=bg_color, fg=fg_color, activebackground=bg_color, text="X", borderwidth=0, border=0, font=("Bauhaus 93", 10), command=lambda: delet_widget(new_entity))
        close_widg.place(relx=0.95, rely=0, relwidth=0.05, relheight=1)
        change_fg_OnHover(close_widg, 'red', 'black')

        new_entity.bind("<MouseWheel>", lambda e: on_mouse_wheel(user_page_canvas, e))
        children = new_entity.winfo_children()
        for child in children:
            child.bind("<MouseWheel>", lambda e: on_mouse_wheel(user_page_canvas, e))

        entity_widg_list.append((new_entity, entity_name, entity_type, chk_var))

        return entity_name, entity_type, chk_var

    def custom_add(widget):
        defalt_entities_list = [('Symptom', 'STRING'), ('Diagnosis', 'STRING')]
        for i in defalt_entities_list:
            e_name, e_type, chk_var = add(fr2)
            e_name.insert(0, i[0])
            e_type.config(text=i[1])
            chk_var.set(False)

    def pause(wid):
        global pause_output_live

        if pause_output_live:
            wid.config(text="Pause")
            pause_output_live = False

        else:
            wid.config(text="Continue")
            pause_output_live = True






    custom_add(fr2)

    Add_new_entity = tk.Button(entity_section, text='+ Add new entity', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", font_size - 5), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: add(fr2))
    Add_new_entity.place(relheight=0.03, relwidth=0.4, rely=0.97, relx=0)
    change_fg_OnHover(Add_new_entity, 'red', fg_color)

    Record_btn = tk.Button(chatbot_widget, text='🎙', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", 25), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: RUN_OFFLINE_speech_recognition(t1, t2, t3, Record_btn, clock_lb, Conversation_Name_entry))
    Record_btn.place(relheight=0.03, relwidth=0.02, rely=0.751, relx=0.78)

    play_pause_btn = tk.Button(chatbot_widget, text='⏯', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", 15), anchor='s', activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: set_recording_paused(play_pause_btn))
    play_pause_btn.place(relheight=0.03, relwidth=0.02, rely=0.751, relx=0.8)

    clock_lb = tk.Label(chatbot_widget, text='', fg=fg_color, font=("Bauhaus 93", 13), bg=bg_color, borderwidth=0, border=0)
    clock_lb.place(relheight=0.03, relwidth=0.06, rely=0.751, relx=0.82)

    download_audio_btn = tk.Button(chatbot_widget, text='⤓', fg=fg_color, activeforeground=fg_color, activebackground=bg_color, font=("Bauhaus 93", 22), bg=bg_color, borderwidth=0, border=0, command=lambda: download_transcribed_audio(download_audio_btn))
    download_audio_btn.place(relheight=0.03, relwidth=0.02, rely=0.751, relx=0.881)

    upload_audio_wid_btn = tk.Button(chatbot_widget, text='⤒', fg=fg_color, activeforeground=fg_color, activebackground=bg_color, font=("Georgia", 22), bg=bg_color, borderwidth=0, border=0, command=lambda: upload_audio_file(t1, upload_audio_wid_btn))
    upload_audio_wid_btn.place(relheight=0.03, relwidth=0.02, rely=0.751, relx=0.902)

    Export_Conv = tk.Button(chatbot_widget, text='EXPORT', fg=fg_color, activeforeground=fg_color, activebackground=bg_color, font=("Georgia", 12), bg=bg_color, borderwidth=0, border=0, command=lambda: Export_to_TXT_file(t2, "Conversation.txt"))
    Export_Conv.place(relheight=0.03, relwidth=0.04, rely=0.751, relx=0.9221)

    extract_wid = tk.Button(chatbot_widget, text='⎋ Extract', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", font_size - 5), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: Entity_Extraction(t2, t3))
    extract_wid.place(relheight=0.02, relwidth=0.04, rely=0.79, relx=0.78)
    change_fg_OnHover(extract_wid, 'red', fg_color)

    Summary_wid = tk.Button(chatbot_widget, text='≅Summarize', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", font_size - 5), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: D_Summary(t2, t3))
    Summary_wid.place(relheight=0.02, relwidth=0.041, rely=0.79, relx=0.821)
    change_fg_OnHover(Summary_wid, 'red', fg_color)

    Medical_Info = tk.Button(chatbot_widget, text='≅Medical_Info', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", font_size - 5), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: Medical_Information(t2, t3))
    Medical_Info.place(relheight=0.02, relwidth=0.05, rely=0.79, relx=0.863)
    change_fg_OnHover(Summary_wid, 'red', fg_color)


    Patient_Info_widget = tk.Frame(chatbot_widget, bg=bg_color, borderwidth=1, relief=tk.RAISED, border=1)
    Patient_Info_widget.place(relheight=0.13, relwidth=0.21, rely=0.81, relx=0.78)

    tk.Label(Patient_Info_widget, text="Patient Info", anchor="w", font=("Georgia", font_size - 5), fg=darken_hex_color(bg_color), bg=bg_color).place(relwidth=1, relheight=0.11, relx=0, rely=0)

    Conversation_Name = tk.Label(Patient_Info_widget, text='Patient_Name:', fg=fg_color, activeforeground=fg_color, bg=bg_color, anchor="w", font=("Calibri Light", font_size-5), activebackground="blue", borderwidth=0, border=0)
    Conversation_Name.place(relheight=0.15, relwidth=0.3, rely=0.11, relx=0)

    Conversation_Name_entry = tk.Entry(Patient_Info_widget, fg=fg_color, font=("Times New Roman", font_size - 2), bg=bg_color, borderwidth=0, border=1)
    Conversation_Name_entry.place(relheight=0.15, relwidth=0.69, rely=0.11, relx=0.3)



    Analysis = tk.Button(chatbot_widget, text='Analysis', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", font_size - 5), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: create_floating_frame(t2))
    Analysis.place(relheight=0.03, relwidth=0.05, rely=0.95, relx=0.78)

    CLEAR_t_1_2 = tk.Button(chatbot_widget, text='Clear IN', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", font_size - 5), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: (t1.delete(1.0, tk.END), t2.delete(1.0, tk.END)))
    CLEAR_t_1_2.place(relheight=0.03, relwidth=0.05, rely=0.95, relx=0.83)

    CLEAR_t3 = tk.Button(chatbot_widget, text='Clear OUT', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", font_size - 5), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda:  t3.delete(1.0, tk.END))
    CLEAR_t3.place(relheight=0.03, relwidth=0.05, rely=0.95, relx=0.88)

    Pause_t3 = tk.Button(chatbot_widget, text='Pause', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", font_size - 5), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: pause(Pause_t3))
    Pause_t3.place(relheight=0.03, relwidth=0.05, rely=0.95, relx=0.93)

    #REDO_t2 = tk.Button(chatbot_widget, text='Redo', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", font_size - 5), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: redo(t2))
    #REDO_t2.place(relheight=0.03, relwidth=0.05, rely=0.95, relx=0.98)

    # change_fg_OnHover(upload_audio_wid, 'red', fg_color)

    return chatbot_widget


def call(widget):
    global t1_list

    def on_entry_click(widget, event):
        if widget.get() == "Search or start a new call" or widget.get().isspace():
            widget.delete(0, tk.END)
            widget.config(fg='black')  # Change text color to black

    def on_focusout(widget, event):
        if not widget.get() or widget.get().isspace():
            widget.delete(0, tk.END)
            widget.insert(0, "Search or start a new call")
            widget.config(fg='gray')  # Change text color to gray

    def display_contacts(widget):
        pass
        """
        global t1_list

        def tab_widget(widget, pos,  info_):
            t1_list = []
            def change_1(widget):  # leave color
                widget.config(bg=widgets_bg_color)
                children = widget.winfo_children()
                for child in children:
                    child.config(bg=widgets_bg_color)

            def change_2(widget):  # hover color
                widget.config(bg="#F3DECA")
                children = widget.winfo_children()
                for child in children:
                    child.config(bg="#F3DECA")

            def active(widget):
                global t1_list
                for i in t1_list:
                    if i != widget:
                        i.config(borderwidth=0, border=0)
                    else:
                        i.config(borderwidth=0, border=2)

            t1 = tk.Frame(widget, bg=widgets_bg_color, relief="solid", borderwidth=0, border=0)
            t1.place(relheight=0.106, relwidth=1, rely=pos, relx=0)
            t1.bind("<Button-1>", lambda m=t1: active(t1))
            t1.bind("<Enter>", func=lambda e: change_2(t1))
            t1.bind("<Leave>", func=lambda e: change_1(t1))
            t1_list.append(t1)

            t2 = tk.Label(t1, bg="blue", text='👤', font=("Calibri", 40, "bold"), activebackground=widgets_bg_color, borderwidth=0, border=0)
            t2.place(relheight=0.8, relwidth=0.3, rely=0.1, relx=0.05)
            t2.bind("<Button-1>", lambda m=t1: active(t1))
            img = info_[2][2:]
            img = img.encode('utf-8')  # Convert the content to bytes
            imagen(img, int(screen_width * 0.9747 * 0.2 * 1 * 0.3), int(screen_height * 0.96 * 0.9 * 0.959 * 0.106 * 0.8), t2)

            t3 = tk.Label(t1, bg=widgets_bg_color, text=info_[1], font=("Calibri", 12, "bold"), activebackground=widgets_bg_color, anchor="w", borderwidth=0, border=0)
            t3.place(relheight=0.3, relwidth=0.6, rely=0.1, relx=0.36)
            t3.bind("<Button-1>", lambda m=t1: active(t1))

        def tab_widget_2(widget):
            def ac():
                global connection_status
                while True:
                    time.sleep(2)
                    print("connection_status", connection_status)
                    if connection_status:
                        list_m = fetch_info()
                        i = j = 0
                        pos = 0
                        while True:
                            if j < len(list_m):
                                print("breaking ", j)
                                tab_widget(widget, pos, list_m[j])

                                pos += 0.106
                                i += 1
                                j += 1
                            else:
                                print("breaking")
                                break
                        break
                print("list_m: ", list_m)
            threading.Thread(target=ac).start()
            #root.after(500, lambda: (tab_widget_2(widget)))

        tab_widget_2(widget)
        """

    widgets_bg_color = '#DFDFD5'
    call_widget = tk.Frame(widget, bg="#F2F7FD", borderwidth=0, border=0)
    call_widget.place(relheight=1, relwidth=1, rely=0, relx=0)

    # ===========================  Display contacts ================================

    display_contacts_widget = tk.Frame(call_widget, bg=widgets_bg_color, borderwidth=0, border=0)
    display_contacts_widget.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.05)

    tk.Label(display_contacts_widget, bg=widgets_bg_color, text="🔍", font=("Courier New", 22), anchor="e", relief="solid", borderwidth=0, border=0).place(relheight=0.04, relwidth=0.2, rely=0, relx=0)

    contact_search_entry_widg = tk.Entry(display_contacts_widget, bg=widgets_bg_color, fg="gray", insertbackground="blue", font=('Georgia', 12), relief="solid", borderwidth=0, border=0)
    contact_search_entry_widg.place(relheight=0.04, relwidth=0.79, rely=0.0, relx=0.2)
    contact_search_entry_widg.insert(0, 'Search or start a new call')
    contact_search_entry_widg.bind("<FocusIn>", lambda e: on_entry_click(contact_search_entry_widg, e))
    contact_search_entry_widg.bind("<FocusOut>", lambda e: on_focusout(contact_search_entry_widg, e))

    contacts_hold_widget = tk.Frame(display_contacts_widget, bg=widgets_bg_color, borderwidth=0, border=0)
    contacts_hold_widget.place(relheight=0.959, relwidth=1, rely=0.041, relx=0)

    # display_contacts(contacts_hold_widget)

    # ===========================  Display selected contact ================================

    display_selected_contact = tk.Frame(call_widget, bg=widgets_bg_color, relief="solid", borderwidth=0, border=0)
    display_selected_contact.place(relheight=0.9, relwidth=0.7, rely=0.05, relx=0.26)

    bar = tk.Frame(display_selected_contact, bg=widgets_bg_color, relief="solid", borderwidth=0, border=0)
    bar.place(relheight=0.05, relwidth=1, rely=0, relx=0)

    tk.Label(bar, bg=widgets_bg_color, text="👤", font=("Courier New", 22), relief="solid", borderwidth=0, border=0).place(relheight=1, relwidth=0.051, rely=0, relx=0)

    tk.Label(bar, bg=widgets_bg_color, fg="gray", text="Dr. Hezron Wekesa Nangulu", anchor="w", font=("Calibri", 12),
             borderwidth=0, border=0).place(relheight=0.5, relwidth=0.3, rely=0, relx=0.051)

    tk.Button(bar, bg=widgets_bg_color, text="📞", font=("Courier New", 17), borderwidth=0, border=0).place(
        relheight=0.6, relwidth=0.035, rely=0.2, relx=0.92)
    tk.Button(bar, bg=widgets_bg_color, text="🎥", font=("Courier New", 17), borderwidth=0, border=0).place(
        relheight=0.6, relwidth=0.035, rely=0.2, relx=0.96)

    return call_widget


def RAG_page(widget):
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor, screen_width

    conversation_widget = tk.Frame(widget, bg=bg_color, borderwidth=0, border=0)
    conversation_widget.place(relheight=1, relwidth=1, rely=0, relx=0)

    paned_window = tk.PanedWindow(conversation_widget, bg=bg_color, orient=tk.HORIZONTAL, sashwidth=8, sashrelief=tk.FLAT)
    paned_window.place(relheight=1, relwidth=1, rely=0, relx=0)

    frame_view1 = tk.Frame(paned_window, bg=bg_color, relief=tk.FLAT, width=int(screen_width / 4), borderwidth=0, border=0)
    pdf_view_frame = WebView2(frame_view1, 500, 500)
    pdf_view_frame.place(relheight=1, relwidth=1, relx=0, rely=0)
    pdf_view_frame.load_url('file:///' + path_exe + "/html/LoadFile_Animation.html")

    # t1.place(relheight=0.60, relwidth=0.485, rely=0.03, relx=0.01)
    frame_view2 = tk.Frame(paned_window, bg=bg_color, relief=tk.FLAT, borderwidth=0, border=0)

    """
    t2.tag_configure("user_config", foreground="gray", justify=tk.LEFT)  # user queries  config's
    t2.tag_configure("llm_config", foreground="black", justify=tk.LEFT)  # llm responses config's
    t2.tag_configure("error_config", foreground="red",  justify=tk.LEFT)  # llm responses config's
    t2.config(state=tk.DISABLED)
    """
    paned_window.add(frame_view1)
    paned_window.add(frame_view2)

    tk.Button(frame_view2, text="Upload", bg=bg_color, activebackground=bg_color, fg=fg_color, font=("Times New Roman", 8), borderwidth=2, border=3, command=lambda: Upload_rag_file(pdf_view_frame)).place(relheight=0.03, relwidth=0.07, rely=0.0, relx=0.01)
    tk.Button(frame_view2, text="clear", bg=bg_color, activebackground=bg_color, fg=fg_color, font=("Times New Roman", 8), borderwidth=2, border=3, command=lambda: clear_rag_file(pdf_view_frame)).place(relheight=0.03, relwidth=0.07, rely=0.0, relx=0.08)

    # tk.Button(conversation_widget, text="Audio File", bg=bg_color, activebackground=bg_color, fg=fg_color, font=("Times New Roman", 13), borderwidth=2, border=3).place(relheight=0.03, relwidth=0.07, rely=0.65, relx=0.081)
    # tk.Button(conversation_widget, text="Record", bg=bg_color, activebackground=bg_color, fg=fg_color, font=("Times New Roman", 13), borderwidth=2, border=3, command=lambda: RUN_OFFLINE_speech_recognition(t1)).place(relheight=0.03, relwidth=0.07, rely=0.65, relx=0.152)

    chat_display_widget = tk.Text(frame_view2, bg=bg_color, fg=fg_color, font=("Times New Roman", 13), wrap='word', borderwidth=0, border=0)
    chat_display_widget.place(relheight=0.8, relwidth=0.98, rely=0.1, relx=0.01)
    chat_display_widget.tag_configure("error_config", foreground="red", font=('Baskerville Old Face', 7, 'italic'), justify=tk.LEFT)  # llm responses config's

    # status_widg = tk.Label(t2, text="𝕤𝕥𝕒𝕥𝕦𝕤", anchor='sw', bg=bg_color, activebackground=bg_color, fg=fg_color, font=("Times New Roman", 20), borderwidth=2, border=3)
    # status_widg.place(relheight=0.03, relwidth=0.07, rely=0.63, relx=0.505)

    input_widget_ = tk.Text(frame_view2, bg=darken_hex_color(bg_color), insertbackground="lightblue", fg=fg_color, relief=tk.SUNKEN, wrap="word", font=("Times New Roman", 13), borderwidth=2, border=1)
    input_widget_.place(relheight=0.05, relwidth=0.96, rely=0.945, relx=0.01)
    text_list_widget.append(input_widget_)

    bng = tk.Button(frame_view2, text="▶", activebackground=bg_color, bg=bg_color, fg=fg_color, font=("Arial Black", 15), borderwidth=0, border=0, command=lambda: rag_chat(input_widget_, chat_display_widget, bng))
    bng.place(relheight=0.06, relwidth=0.02, rely=0.945, relx=0.973)

    return conversation_widget


def chat_me(widget):
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor, current_theme
    global num_y, num_height, current, path_exe
    num_y = 0.9
    num_height = 0.05
    current = 130
    previous = 0

    chatbot_widget = WebView2(widget, 500, 500)
    chatbot_widget.place(relheight=1, relwidth=1, rely=0, relx=0)

    chatbot_widget.load_url('file:///' + path_exe + "/html/MedBot.html")

    return chatbot_widget


def Clinical_Image(widget):
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor, current_theme
    global clinical_Note_upload_btn
    global view_track
    view_track = 0

    def Analyzed_Output_(display_frame):
        global view_track
        if view_track == 0:
            display_frame.load_url('file:///' + path_exe + "/html/Analyzed_Output_.html")
            view_track = 1
        else:
            display_frame.load_url('file:///' + path_exe + "/temp_files/extraced_img.jpg")
            view_track = 0

    def clear_dd(web_widg, text_tk_widg):
        web_widg.load_url('file:///' + path_exe + "/html/Load_img_request.html")
        text_tk_widg.delete(1.0, tk.END)

    Clinical_widg_page = tk.Frame(widget, bg=bg_color, borderwidth=0, border=0)
    Clinical_widg_page.place(relheight=1, relwidth=1, rely=0, relx=0)

    display_img = WebView2(Clinical_widg_page, 500, 500)
    display_img.place(relheight=0.6, relwidth=1, rely=0.02, relx=0)
    display_img.load_url('file:///' + path_exe + "/html/Load_img_request.html")

    Display_text_ = tk.Text(Clinical_widg_page, bg=darken_hex_color(bg_color), fg=fg_color, font=("Georgia", 12))
    Display_text_.place(relheight=0.3, relwidth=1, rely=0.62, relx=0)
    text_list_widget.append(Display_text_)

    clinical_Note_upload_btn = tk.Button(Clinical_widg_page, text="clinical Note+", command=lambda: image_text_extract_Handwriten(display_img, Display_text_))
    clinical_Note_upload_btn.place(relheight=0.02, relwidth=0.05, rely=0, relx=0.)
    tk.Button(Clinical_widg_page, text="Change View", command=lambda: Analyzed_Output_(display_img)).place(relheight=0.02, relwidth=0.05, rely=0, relx=0.05)
    tk.Button(Clinical_widg_page, text="Clear", command=lambda: clear_dd(display_img, Display_text_)).place(relheight=0.02, relwidth=0.05, rely=0, relx=0.1)
    tk.Button(Clinical_widg_page, text="Export txt", command=lambda: Export_to_TXT_file(Display_text_, "clinical_Note_export.txt")).place(relheight=0.02, relwidth=0.05, rely=0, relx=0.15)

    return Clinical_widg_page


def Recodes_Page(widget):
    global bg_color, fg_color, screen_height, screen_width
    global sound_widgets, active_sound_widget, font_size, ref_btn
    global llm_chain3, llm_chain4, text_list_widget

    sound_widgets = []
    active_sound_widget = None

    Recodes_Page = tk.Frame(widget, bg=bg_color, borderwidth=0, border=0)
    Recodes_Page.place(relheight=1, relwidth=1, rely=0, relx=0)

    x = tk.Frame(Recodes_Page, bg=bg_color, borderwidth=0, highlightbackground=fg_color, highlightthickness=0.5, border=0)
    x.place(relheight=0.9, relwidth=0.64, rely=0.05, relx=0.35)

    x2 = tk.Text(x, bg=bg_color, borderwidth=0, highlightbackground=fg_color, fg=fg_color, wrap='word', relief=tk.SUNKEN, border=1)
    x2.place(relheight=0.5, relwidth=1, rely=0, relx=0)

    tk.Button(x, text="Contextual AI", borderwidth=0, border=0, bg=bg_color, fg='gray', activeforeground=fg_color, activebackground=bg_color, font=("Calibri", font_size - 3), command=lambda: context_assistant(x2, x3)).place(relheight=0.02, relwidth=0.1, rely=0.51, relx=0)
    tk.Button(x, text="Summarize", borderwidth=0, border=0, bg=bg_color, fg='gray', activeforeground=fg_color, activebackground=bg_color, font=("Calibri", font_size - 3), command=lambda: D_Summary(x2, x3, False)).place(relheight=0.02, relwidth=0.1, rely=0.51, relx=0.1)
    tk.Button(x, text="Entity_Extract", borderwidth=0, border=0, bg=bg_color, fg='gray', activeforeground=fg_color, activebackground=bg_color, font=("Calibri", font_size - 3), command=lambda: Entity_Extraction(x2, x3, False)).place(relheight=0.02, relwidth=0.1, rely=0.51, relx=0.2)
    tk.Button(x, text="follow-up ", borderwidth=0, border=0, bg=bg_color, fg='gray', activeforeground=fg_color, activebackground=bg_color, font=("Calibri", font_size - 3), command=lambda: AI_doctor_assistant(x2, x3)).place(relheight=0.02, relwidth=0.1, rely=0.51, relx=0.3)
    tk.Button(x, text="Medical Info", borderwidth=0, border=0, bg=bg_color, fg='gray', activeforeground=fg_color, activebackground=bg_color, font=("Calibri", font_size - 3), command=lambda: Medical_Information(x2, x3)).place(relheight=0.02, relwidth=0.1, rely=0.51, relx=0.4)

    btn_widget = tk.Button(x, text="Save", borderwidth=0, border=0, bg=bg_color, fg='gray', activeforeground=fg_color, activebackground=bg_color, font=("Calibri", font_size - 3), command=lambda: text_pdf_save(btn_widget, [x2, x3]))
    btn_widget.place(relheight=0.02, relwidth=0.1, rely=0.51, relx=0.5)
    # tk.Button(x, text="Contextual AI", borderwidth=0, border=0, bg=bg_color, fg='gray', activeforeground=fg_color, activebackground=bg_color, font=("Calibri", font_size - 3)).place(relheight=0.02, relwidth=0.1, rely=0.51, relx=0.5)
    # tk.Button(x, text="Contextual AI", borderwidth=0, border=0, bg=bg_color, fg='gray', activeforeground=fg_color, activebackground=bg_color, font=("Calibri", font_size - 3)).place(relheight=0.02, relwidth=0.1, rely=0.51, relx=0.6)
    # tk.Button(x, text="Contextual AI", borderwidth=0, border=0, bg=bg_color, fg='gray', activeforeground=fg_color, activebackground=bg_color, font=("Calibri", font_size - 3)).place(relheight=0.02, relwidth=0.1, rely=0.51, relx=0.7)
    # tk.Button(x, text="Contextual AI", borderwidth=0, border=0, bg=bg_color, fg='gray', activeforeground=fg_color, activebackground=bg_color, font=("Calibri", font_size - 3)).place(relheight=0.02, relwidth=0.1, rely=0.51, relx=0.8)
    # tk.Button(x, text="Contextual AI", borderwidth=0, border=0, bg=bg_color, fg='gray', activeforeground=fg_color, activebackground=bg_color, font=("Calibri", font_size - 3)).place(relheight=0.02, relwidth=0.1, rely=0.51, relx=0.9)

    x3 = tk.Text(x, bg=darken_hex_color(bg_color), borderwidth=0, highlightbackground=fg_color, fg=fg_color, wrap='word', relief=tk.SUNKEN, border=1)
    x3.place(relheight=0.4, relwidth=1, rely=0.6, relx=0)
    x3.tag_configure("ASR", foreground="gray", font=("Broadway"))
    text_list_widget.append(x3)

    def context_assistant(text_widget, display_widget):
        def context_assistant_run(text_widget=text_widget, display_widget=display_widget):
            global llm_chain3
            text = text_widget.get("6.0", "end")

            AI_response = llm_chain3.invoke(input=text)
            display_widget.insert(tk.END, "\n\n------------ AI context-aware suggestions ----------------------------------\n\n", 'ASR')
            display_widget.insert(tk.END, AI_response['text'])
            display_widget.insert(tk.END, "\n\n-----------------------------------------------------------------------------\n", 'ASR')

            display_widget.see(tk.END)  # Scroll to the end of the text widget

        threading.Thread(target=context_assistant_run).start()

    def AI_doctor_assistant(text_widget, display_widget):
        def AI_doctor_assistant_run(text_widget=text_widget, display_widget=display_widget):
            global llm_chain4
            text = text_widget.get("6.0", "end")
            AI_response = llm_chain4.invoke(input=text)
            display_widget.insert(tk.END, "\n\n------------ Follow Up Analysis ------------------------------------------ \n\n", 'ASR')
            display_widget.insert(tk.END, AI_response['text'])
            display_widget.insert(tk.END, "\n\n---------------------------------------------------------------------------\n", 'ASR')
            display_widget.see(tk.END)  # Scroll to the end of the text widget

        threading.Thread(target=AI_doctor_assistant_run).start()

    def analyse_recoding(audio_path, an_widget, x2=x2, x3=x3):
        global downloading_audio
        downloading_audio = True

        def visual_analyse_recoding_run(bt_widget=an_widget):
            global downloading_audio
            global fg_color
            color = 'yellow'
            while downloading_audio:
                if color == 'yellow':
                    bt_widget.config(fg=color)
                    color = 'gold'
                else:
                    bt_widget.config(fg=color)
                    color = 'yellow'
                time.sleep(0.1)
            bt_widget.config(fg=fg_color)

        def analyse_recoding_run(audio_path=audio_path, x2=x2, x3=x3):
            global wisper_model_tiny, path_exe, llm_chain3
            global downloading_audio
            if llm_chain3 is None:
                llm_inference_initializ()
            try:
                threading.Thread(target=visual_analyse_recoding_run).start()

                audio_path_full = path_exe + '\\Audio_Records\\' + audio_path
                result = wisper_model_tiny.transcribe(audio_path_full)
                x2.delete(1.0, tk.END)
                x2.insert(tk.END, "\n File Name : " + audio_path + "\n\n")
                x2.insert(tk.END, "\n Conversation : \n\n" + result["text"])
                downloading_audio = False

                x3.delete(1.0, tk.END)
                AI_response = llm_chain3.invoke(input=result["text"])
                x3.insert(tk.END, AI_response['text'])
            except Exception as e:
                print(e)
                downloading_audio = False

        threading.Thread(target=analyse_recoding_run).start()

    def refresh_recodings(frame, Audio_recodes_canvas):
        global sound_widgets, active_sound_widget
        active_sound_widget = None
        for wid in sound_widgets:
            wid.destroy()

        audio_recodings(frame, Audio_recodes_canvas)

        frame.update_idletasks()
        Audio_recodes_canvas.configure(scrollregion=Audio_recodes_canvas.bbox("all"))

    def audio_recodings(frame_widget, cavas_widget):
        global font_size, screen_height, bg_color, fg_color
        global path_exe

        def create_audio_widget(audio_file):
            global playing, path_exe, sound_widgets

            playing = 0

            def Play_Recoding(audio_file_name, widget):
                global playing, active_sound_widget, path_exe
                file_path = path_exe + '\\Audio_Records\\' + audio_file_name
                if active_sound_widget != None:
                    if active_sound_widget != widget:
                        pygame.mixer.music.stop()
                        active_sound_widget.config(text="▶")
                        playing = 0

                active_sound_widget = widget

                if playing == 0:
                    pygame.mixer.music.load(file_path)
                    pygame.mixer.music.play()
                    playing = 1
                    widget.config(text="||")
                elif playing == 1:
                    pygame.mixer.music.pause()
                    widget.config(text="≜")
                    playing = 2
                elif playing == 2:
                    pygame.mixer.music.unpause()
                    widget.config(text="||")
                    playing = 1

            def stop():
                global playing, active_sound_widget
                playing = 0
                active_sound_widget.config(text="▶")
                pygame.mixer.music.stop()
                active_sound_widget = None

            audio_wid = tk.Frame(frame_widget, bg=bg_color, height=int((screen_height - 20) * 0.9 * 0.05), highlightbackground=fg_color, highlightthickness=0, borderwidth=0, border=0)
            audio_wid.pack(expand=True, fill=tk.X)  # .place(rel height=0.04, relwidth=1, rely=rely, relx=0)
            audio_Lable = tk.Label(audio_wid, text="  " + audio_file, bg=bg_color, fg=fg_color, anchor=tk.W, font=("Calibri", font_size - 2, 'italic'), borderwidth=0, border=0)
            audio_Lable.place(relheight=1, relwidth=0.7, rely=0, relx=0.)
            audio_play_btn = tk.Button(audio_wid, text="▶", bg=bg_color, fg=fg_color, activeforeground='green', activebackground=bg_color, command=lambda k=audio_file: Play_Recoding(k, audio_play_btn), font=("Arial Rounded MT Bold", font_size), borderwidth=0, border=0)
            audio_play_btn.place(relheight=1, relwidth=0.1, rely=0, relx=0.7)
            audio_download_btn = tk.Button(audio_wid, text="🛑", bg=bg_color, fg=fg_color, activeforeground='red', activebackground=bg_color, command=lambda: stop(), font=("Arial Rounded MT Bold", font_size), borderwidth=0, border=0)
            audio_download_btn.place(relheight=1, relwidth=0.1, rely=0, relx=0.8)
            audio_push_btn = tk.Button(audio_wid, text="⌥", bg=bg_color, fg=fg_color, activeforeground=fg_color, activebackground=bg_color, command=lambda k=audio_file: analyse_recoding(k, audio_push_btn), font=("Arial Rounded MT Bold", font_size + 5), borderwidth=0, border=0)
            audio_push_btn.place(relheight=1, relwidth=0.1, rely=0, relx=0.9)
            sound_widgets.append(audio_wid)

            audio_wid.bind("<MouseWheel>", lambda e: cavas_widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))
            audio_Lable.bind("<MouseWheel>", lambda e: cavas_widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))
            audio_play_btn.bind("<MouseWheel>", lambda e: cavas_widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))
            audio_download_btn.bind("<MouseWheel>", lambda e: cavas_widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))
            audio_push_btn.bind("<MouseWheel>", lambda e: cavas_widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        folder_path = path_exe + "\\Audio_Records"
        file_list = []
        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    file_list.append(file_name)

            for audio_file in file_list:
                create_audio_widget(audio_file)

            frame_widget.update_idletasks()
            cavas_widget.configure(scrollregion=Audio_recodes_canvas.bbox("all"))

        else:
            print("Folder not found.")

        return file_list



    tk.Label(Recodes_Page, text="Conversations Recordings", bg=bg_color, fg=fg_color, font=("Book Antiqua", font_size, 'bold'), anchor=tk.SW, borderwidth=0, border=0).place(relheight=0.05, relwidth=0.3, rely=0, relx=0.02)
    refresh_btn = tk.Button(Recodes_Page, text="↺", bg=bg_color, activebackground=bg_color, activeforeground="green", command=lambda: refresh_recodings(frame, Audio_recodes_canvas), fg=fg_color, font=("Book Antiqua", font_size, 'bold'), anchor=tk.S, borderwidth=0, border=0)
    refresh_btn.place(relheight=0.05, relwidth=0.1, rely=0, relx=0.22)
    ref_btn = refresh_btn
    Audio_recodes_frame = tk.Frame(Recodes_Page, bg=bg_color, borderwidth=0, highlightbackground=fg_color, highlightthickness=0.5, border=0)
    Audio_recodes_frame.place(relheight=0.9, relwidth=0.3, rely=0.05, relx=0.02)
    Audio_recodes_canvas = tk.Canvas(Audio_recodes_frame, highlightthickness=0, bg=bg_color, borderwidth=0, border=0)
    Audio_recodes_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(Audio_recodes_frame, orient=tk.VERTICAL)
    Audio_recodes_canvas.configure(yscrollcommand=scrollbar.set)
    frame = tk.Frame(Audio_recodes_canvas, bg=bg_color, borderwidth=0, border=0)
    Audio_recodes_canvas.create_window((0, 0), window=frame, width=int(screen_width * 0.9747 * 0.3), anchor=tk.NW)
    Audio_recodes_canvas.bind("<MouseWheel>", lambda e: Audio_recodes_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    audio_recodings(frame, Audio_recodes_canvas)

    return Recodes_Page


def Profile_Page(widget):
    global bg_color, fg_color
    global screen_width, screen_height, font_size
    global User_Name, User_Pass, User_Image, User_Email, User_Phone
    global gradient_ai_workspace_id, assemblyai_access_key, gradient_ai_access_key, gradient_ai_finetuned_id, gradient_ai_base_model_id, keys, Gem_Key

    profile_page_container = tk.Frame(widget, bg=bg_color, borderwidth=0, border=0)
    profile_page_container.place(relheight=1, relwidth=1, rely=0, relx=0)

    sign_out_widget = tk.Button(profile_page_container, bg=bg_color, activeforeground=fg_color, activebackground=bg_color, fg=darken_hex_color(bg_color), text="sign out", font=("Calibri", font_size - 6, 'italic'), borderwidth=0, border=0, command=lambda: sign_out_request())
    sign_out_widget.place(relheight=0.03, relwidth=0.05, relx=0.95, rely=0)
    change_fg_OnHover(sign_out_widget, fg_color, darken_hex_color(bg_color))

    User_imag_widget = tk.Button(profile_page_container, bg=bg_color, fg=fg_color, text="👤", font=("Forte", 100), borderwidth=0, border=0)
    User_imag_widget.place(relheight=0.17, relwidth=0.12, relx=0.05, rely=0.05)
    imagen('./Assets/img.png', int(screen_width * 0.9747 * 0.12), int((screen_height - 20) * 0.13), User_imag_widget)

    User_Name_widget_lable = tk.Label(profile_page_container, text="Email     : ", anchor=tk.W, bg=bg_color, fg=fg_color, font=('Georgia', font_size - 5, 'bold'))
    User_Name_widget_lable.place(relheight=0.03, relwidth=0.05, relx=0.05, rely=0.23)
    User_Name_widget_entry = tk.Label(profile_page_container, bg=bg_color, text=User_Email, fg='gray', font=('Calibri', font_size - 3), borderwidth=0, border=0)
    User_Name_widget_entry.place(relheight=0.029, relwidth=0.13, relx=0.1, rely=0.23)

    User_EMAIL_widget = tk.Label(profile_page_container, text="PassWord    : ", anchor=tk.W, bg=bg_color, fg=fg_color, font=('Georgia', font_size - 5, 'bold'))
    User_EMAIL_widget.place(relheight=0.03, relwidth=0.05, relx=0.05, rely=0.261)
    User_EMAIL_widget_entry = tk.Label(profile_page_container, bg=bg_color, text="  *  *  *  *  *  *  *  * ", fg='gray', font=('Calibri', font_size - 3), borderwidth=0, border=0)
    User_EMAIL_widget_entry.place(relheight=0.029, relwidth=0.13, relx=0.1, rely=0.2615)

    User_PHONE_widget = tk.Button(profile_page_container, text="Change Password", anchor=tk.W, activebackground=bg_color, activeforeground='green', borderwidth=0, border=0, bg=bg_color, fg=fg_color, font=('Courier New', font_size - 6, 'italic'))
    User_PHONE_widget.place(relheight=0.03, relwidth=0.1, relx=0.05, rely=0.292)

    # ======================================================= Section 1 ===========================================================================================================================================

    g1 = tk.Frame(profile_page_container, bg=bg_color, relief=tk.RAISED, borderwidth=0, border=2)
    g1.place(relheight=0.4, relwidth=0.41, rely=0.5, relx=0.0253)

    # tk.Label(g1, bg='blue', fg=fg_color, borderwidth=7, border=7).place(relheight=1, relwidth=1, rely=0, relx=0)

    tk.Label(g1, text="ACCESS KEYS ", fg=darken_hex_color(bg_color), bg=bg_color, font=("Georgia", 12, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.6, rely=0, relx=0)
    tk.Label(g1, text="  G_ACCESS_TOKEN :", bg=bg_color, fg=darken_hex_color(bg_color), font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.071, relx=0)
    gradient_access_widget = tk.Entry(g1, bg=bg_color, fg=darken_hex_color(bg_color), borderwidth=0, border=1, font=("Courier New", 10))
    gradient_access_widget.place(relheight=0.07, relwidth=0.74, rely=0.071, relx=0.25)
    gradient_access_widget.insert(0, gradient_ai_access_key)
    change_bg_OnHover(gradient_access_widget, bg_hovercolor)

    tk.Label(g1, text="  G_WORKSPACE_ID :", bg=bg_color, fg=darken_hex_color(bg_color), font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.142, relx=0)
    gradient_work_widget = tk.Entry(g1, bg=bg_color, fg=darken_hex_color(bg_color), borderwidth=0, border=1, font=("Courier New", 10))
    gradient_work_widget.place(relheight=0.07, relwidth=0.74, rely=0.142, relx=0.25)
    gradient_work_widget.insert(0, gradient_ai_workspace_id)
    change_bg_OnHover(gradient_work_widget, bg_hovercolor)

    tk.Label(g1, text="  NLP_adapter_ID :", bg=bg_color, fg=darken_hex_color(bg_color), font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.213, relx=0)
    gradient_finetuned_model_id = tk.Entry(g1, bg=bg_color, fg=darken_hex_color(bg_color), borderwidth=0, border=1, font=("Courier New", 10))
    gradient_finetuned_model_id.place(relheight=0.07, relwidth=0.74, rely=0.213, relx=0.25)
    gradient_finetuned_model_id.insert(0, gradient_ai_finetuned_id)
    change_bg_OnHover(gradient_finetuned_model_id, bg_hovercolor)

    tk.Label(g1, text="  B_Model_ID :", bg=bg_color, fg=darken_hex_color(bg_color), font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.284, relx=0)
    gradient_base_model_id = tk.Entry(g1, bg=bg_color, fg=darken_hex_color(bg_color), borderwidth=0, border=1, font=("Courier New", 10))
    gradient_base_model_id.place(relheight=0.07, relwidth=0.74, rely=0.284, relx=0.25)
    gradient_base_model_id.insert(0, gradient_ai_base_model_id)
    change_bg_OnHover(gradient_base_model_id, bg_hovercolor)

    # tk.Label(g1, text="ASSEMBLY-AI  ", bg=bg_color, fg=fg_color, font=("Georgia", 12, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.6, rely=0.363, relx=0)
    tk.Label(g1, text="  A_AI  key:", bg=bg_color, fg=darken_hex_color(bg_color), font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.432, relx=0)
    assembly_widget = tk.Entry(g1, bg=bg_color, fg=darken_hex_color(bg_color), borderwidth=0, border=1, font=("Courier New", 10))
    assembly_widget.place(relheight=0.07, relwidth=0.74, rely=0.432, relx=0.25)
    assembly_widget.insert(0, assemblyai_access_key)
    change_bg_OnHover(assembly_widget, bg_hovercolor)

    tk.Label(g1, text="  GEM_AI  key:", bg=bg_color, fg=darken_hex_color(bg_color), font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.502, relx=0)
    gemini_widget = tk.Entry(g1, bg=bg_color, fg=darken_hex_color(bg_color), borderwidth=0, border=1, font=("Courier New", 10))
    gemini_widget.place(relheight=0.07, relwidth=0.74, rely=0.502, relx=0.25)
    gemini_widget.insert(0, Gem_Key)
    change_bg_OnHover(gemini_widget, bg_hovercolor)

    # ======================================================= Section 2 ===========================================================================================================================================

    g2 = tk.Frame(profile_page_container, bg=bg_color, relief=tk.RAISED, borderwidth=0, border=2)
    g2.place(relheight=0.4, relwidth=0.41, rely=0.02, relx=0.5)

    tk.Label(g2, text="PERSONALIZATION ", bg=bg_color, fg=darken_hex_color(bg_color), font=("Georgia", 12, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.6, rely=0, relx=0)
    tk.Label(g2, text="  current theme :", bg=bg_color, fg=darken_hex_color(bg_color), font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.071, relx=0)
    themes_change = tk.Button(g2, text=current_theme, bg=bg_color, anchor="w", fg=darken_hex_color(bg_color), borderwidth=0, border=0, font=("Courier New", 10), command=lambda: change_color(root, themes_change))
    themes_change.place(relheight=0.07, relwidth=0.3, rely=0.071, relx=0.25)
    change_fg_OnHover(themes_change, darken_hex_color(bg_color))

    tk.Label(g2, text="Font_Size:", bg=bg_color, fg=darken_hex_color(bg_color), font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.142, relx=0)
    Font_Size_set_widget = tk.Label(g2, bg=bg_color, text='12', anchor="w", fg=darken_hex_color(bg_color), borderwidth=0, border=0, font=("Courier New", 10))
    Font_Size_set_widget.place(relheight=0.07, relwidth=0.74, rely=0.142, relx=0.25)

    tk.Label(g2, text="Font_Name :", bg=bg_color, fg=darken_hex_color(bg_color), font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.213, relx=0)
    Font_Name_set_widget = tk.Label(g2, bg=bg_color, text='Calibri', anchor="w", fg=darken_hex_color(bg_color), borderwidth=0, border=0, font=("Courier New", 10))
    Font_Name_set_widget.place(relheight=0.07, relwidth=0.74, rely=0.213, relx=0.25)

    # ======================================================= Section 3 ===========================================================================================================================================

    g4 = tk.Frame(profile_page_container, bg=bg_color, relief=tk.RAISED, borderwidth=0, border=2)
    g4.place(relheight=0.4, relwidth=0.41, rely=0.5, relx=0.5)
    # ======================================================= ====== ===========================================================================================================================================

    return profile_page_container


def Document_Management_page(widget):
    global bg_color, fg_color
    global screen_width, screen_height, font_size
    global User_Name, User_Pass, User_Image, User_Email, User_Phone
    global chang_status, ERH_Systems

    DOCUMENT_PATH = './Document_Managment'  # File system path for storing documents

    def load_documents(tree):
        for folder, _, files in os.walk(DOCUMENT_PATH):
            for file in files:
                file_path = os.path.join(folder, file)
                file_size = os.path.getsize(file_path)
                file_date = os.path.getmtime(file_path)
                tree.insert("", "end", text=file, values=(file, format_file_size(file_size), format_date(file_date)))

    def format_file_size(size):
        if size < 1024:
            return f"{size} B"
        elif size < 1024 ** 2:
            return f"{size // 1024} KB"
        elif size < 1024 ** 3:
            return f"{size // (1024 ** 2)} MB"
        else:
            return f"{size // (1024 ** 3)} GB"

    def format_date(timestamp):
        import datetime
        return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    def add_document(tree):
        file_path = filedialog.askopenfilename(title="Select Document")
        if file_path:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(DOCUMENT_PATH, file_name)
            shutil.copy(file_path, dest_path)
            file_size = os.path.getsize(dest_path)
            file_date = os.path.getmtime(dest_path)
            tree.insert("", "end", text=file_name, values=(file_name, format_file_size(file_size), format_date(file_date)))

    def delete_document(tree):
        selected_item = tree.selection()
        if selected_item:
            file_name = tree.item(selected_item, "text")
            file_path = os.path.join(DOCUMENT_PATH, file_name)
            answer = messagebox.askyesno("Delete Document", f"Are you sure you want to delete '{file_name}'?")
            if answer:
                os.remove(file_path)
                tree.delete(selected_item)

    def upload_document(tree):
        file_path = filedialog.askopenfilename(title="Select Document to Upload")
        if file_path:
            # Implement your logic to upload the document to a server or cloud storage
            pass

    Document_Managemen_container = tk.Frame(widget, bg=bg_color, borderwidth=0, border=0)
    Document_Managemen_container.place(relheight=1, relwidth=1, rely=0, relx=0)

    # Create a frame to hold the document list
    document_frame = tk.Frame(Document_Managemen_container, bg=bg_color)
    document_frame.place(relheight=0.95, relwidth=1, rely=0, relx=0)

    # Create a style object
    style = ttk.Style()

    # Configure the Treeview style
    #style.configure("Treeview", background=bg_color, foreground=fg_color, fieldbackground=bg_color, )
    #style.map("Treeview", background=[("selected", "blue")])

    # Create a scrollable treeview to display the documents
    document_tree = ttk.Treeview(document_frame)
    document_tree["columns"] = ("name", "size", "date")
    document_tree.column("#0", width=200)
    document_tree.column("name", width=200, anchor="w")
    document_tree.column("size", width=100, anchor="w")
    document_tree.column("date", width=150, anchor="w")
    document_tree.heading("#0", text="Name", anchor="w")
    document_tree.heading("name", text="Name", anchor="w")
    document_tree.heading("size", text="Size", anchor="w")
    document_tree.heading("date", text="Date Modified", anchor="w")
    document_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a vertical scrollbar to the treeview
    document_scrollbar = ttk.Scrollbar(document_frame, orient=tk.VERTICAL, command=document_tree.yview)
    document_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    document_tree.configure(yscrollcommand=document_scrollbar.set)

    # Load documents from the file system
    load_documents(document_tree)

    # Create buttons for adding, deleting, and uploading documents
    button_frame = tk.Frame(Document_Managemen_container, bg=bg_color)
    button_frame.place(relheight=0.05, relwidth=1, rely=0.95, relx=0)

    add_button = ttk.Button(button_frame, text="Add Document", command=lambda: add_document(document_tree))
    add_button.place(relheight=1, relwidth=0.2, rely=0, relx=0)

    delete_button = ttk.Button(button_frame, text="Delete Document", command=lambda: delete_document(document_tree))
    delete_button.place(relheight=1, relwidth=0.2, rely=0, relx=0.2)

    upload_button = ttk.Button(button_frame, text="Upload Document", command=lambda: upload_document(document_tree))
    upload_button.place(relheight=1, relwidth=0.2, rely=0, relx=0.4)

    return Document_Managemen_container


def EHR_integration_page(widget):
    global bg_color, fg_color
    global screen_width, screen_height, font_size
    global User_Name, User_Pass, User_Image, User_Email, User_Phone
    global chang_status, ERH_Systems

    ERH_Systems = """
# Define a dictionary to store EHR system configurations
{
    "Epic": {
        "api_base_url": "https://example.com/epic/api",
        "api_key": "your_epic_api_key",
        "api_secret": "your_epic_api_secret"
    },
    "Cerner": {
        "api_base_url": "https://example.com/cerner/api",
        "api_key": "your_cerner_api_key",
        "api_secret": "your_cerner_api_secret"
    },
    # Add more EHR systems as needed
}
    """

    def MySQL_CONNECTION(h_name, u_name, p_key, d_name, port):
        global host_name, user_name, password_key, database_name
        host_name = host_name
        user_name = user_namem
        password_key = password_key
        database_name = database_name

        mydb = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=password_key,
            database=database_name
        )
        mycursor = mydb.cursor()

    def visual_connection_status(widget):
        global closed
        DBM_status = False
        color = 'yellow'
        while True:
            if closed:
                break
            if DBM_status == True:
                if color == "yellow":
                    widget.config(fg="green")
                    color = 'green'
                    time.sleep(1)
                else:
                    widget.config(fg="yellow")
                    color = 'yellow'
                    time.sleep(1)
            else:
                if color == "yellow":
                    widget.config(fg="red")
                    color = 'red'
                    time.sleep(1)
                else:
                    widget.config(fg="yellow")
                    color = 'yellow'
                    time.sleep(1)

    def ehr_run(widget):
        global ERH_Systems
        string_code = widget.get(1.0, tk.END)
        dict_obj = eval(string_code)

        print(dict_obj)
        print(type(dict_obj))

    EHR_page_container = tk.Frame(widget, bg=bg_color, borderwidth=0, border=0)
    EHR_page_container.place(relheight=1, relwidth=1, rely=0, relx=0)

    tk.Label(EHR_page_container, text="Data Base Connection Point ", bg=bg_color, fg='gray', font=("Georgia", font_size, 'bold')).place(relheight=0.02, relwidth=0.2, rely=0, relx=0.03)
    tk.Label(EHR_page_container, text="D_Name :", bg=bg_color, fg='gray', font=("Georgia", font_size), anchor="w").place(relheight=0.02, relwidth=0.1, rely=0.025, relx=0.03)
    tk.Label(EHR_page_container, text="H_Name :", bg=bg_color, fg='gray', font=("Georgia", font_size), anchor="w").place(relheight=0.02, relwidth=0.1, rely=0.046, relx=0.03)
    tk.Label(EHR_page_container, text="P_Key :", bg=bg_color, fg='gray', font=("Georgia", font_size), anchor="w").place(relheight=0.02, relwidth=0.1, rely=0.067, relx=0.03)
    tk.Label(EHR_page_container, text="Port CCN :", bg=bg_color, fg='gray', font=("Georgia", font_size), anchor="w").place(relheight=0.02, relwidth=0.1, rely=0.088, relx=0.03)
    tk.Label(EHR_page_container, text="DBMS :", bg=bg_color, fg='gray', font=("Georgia", font_size), anchor="w").place(relheight=0.02, relwidth=0.1, rely=0.11, relx=0.03)

    tk.Entry(EHR_page_container, bg=bg_color, fg=fg_color, font=("Times New Roman", font_size - 2), borderwidth=1, border=1).place(relheight=0.02, relwidth=0.1, rely=0.025, relx=0.13)
    tk.Entry(EHR_page_container, bg=bg_color, fg=fg_color, font=("Times New Roman", font_size - 2), borderwidth=1, border=1).place(relheight=0.02, relwidth=0.1, rely=0.046, relx=0.13)
    tk.Entry(EHR_page_container, bg=bg_color, fg=fg_color, font=("Times New Roman", font_size - 2), borderwidth=1, border=1).place(relheight=0.02, relwidth=0.1, rely=0.067, relx=0.13)
    tk.Entry(EHR_page_container, bg=bg_color, fg=fg_color, font=("Times New Roman", font_size - 2), borderwidth=1, border=1).place(relheight=0.02, relwidth=0.1, rely=0.088, relx=0.13)
    tk.Button(EHR_page_container, text="DBMS :", bg=bg_color, activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, font=("Georgia", font_size), anchor="w").place(relheight=0.02, relwidth=0.1, rely=0.11, relx=0.13)

    CON_btn = tk.Label(EHR_page_container, text="connect", bg=bg_color, fg='gray', font=("Georgia", font_size - 6))
    CON_btn.place(relheight=0.02, relwidth=0.05, rely=0.14, relx=0.03)
    change_fg_OnHover(CON_btn, 'yellow', "gray")

    DISCON_btn = tk.Label(EHR_page_container, text="disconnect", bg=bg_color, fg='gray', font=("Georgia", font_size - 6))
    DISCON_btn.place(relheight=0.02, relwidth=0.05, rely=0.14, relx=0.09)
    change_fg_OnHover(DISCON_btn, 'yellow', "gray")

    tk.Label(EHR_page_container, text="Connection Status :", bg=bg_color, fg=fg_color, font=("Georgia", font_size - 3), anchor="w").place(relheight=0.02, relwidth=0.1, rely=0.2, relx=0.03)
    status_widg = tk.Label(EHR_page_container, text="⊙", bg=bg_color, fg=fg_color, font=("Broadway", font_size), anchor="w")
    status_widg.place(relheight=0.02, relwidth=0.05, rely=0.2, relx=0.13)
    threading.Thread(target=visual_connection_status, args=(status_widg,)).start()

    info_ehr = """
Welcome! Follow these steps to connect our system to your Electronic Health Record (EHR) system.
Configure Connection Settings:
        - Go to the Settings section of our system.
        - Navigate to EHR Integration.
        - Enter the access credentials provided by your EHR system administrator.
    
Test the Connection:
        - After entering the credentials, click on the Run Connection button.
        - Ensure that the connection is successful. If you encounter any errors, double-check the entered credentials and try again.
    
Enable Data Sync:
        - Once the connection is successful, enable data synchronization by toggling the Data Sync option.
        - Select the data types you wish to sync (e.g., patient records, appointments, medical histories).
        
Schedule Automatic Sync:
        
        - Set up a schedule for automatic data synchronization.
        - Choose the frequency (e.g., hourly, daily) and the time when the sync should occur.
Review and Confirm:
        - Review the connection settings and synchronization options.
        - Click Save to confirm and activate the connection.
    """

    info_ehr_wid = tk.Text(EHR_page_container, relief=tk.RAISED, bg=bg_color, fg=darken_hex_color(bg_color),  borderwidth=0, border=1, font=("Courier New", 11))
    info_ehr_wid.place(relheight=0.6, relwidth=0.5, rely=0.3, relx=0.03)
    info_ehr_wid.insert(tk.END, info_ehr)
    info_ehr_wid.config(state=tk.DISABLED)

    E_nav = tk.Frame(EHR_page_container, bg=bg_color)
    E_nav.place(relheight=0.02, relwidth=0.4, rely=0.03, relx=0.59)

    coning_terminal = tk.Text(EHR_page_container, bg="Black", fg=fg_color, highlightthickness=1, highlightbackground=lighten_hex_color(bg_color))
    coning_terminal.place(relheight=0.9, relwidth=0.4, relx=0.59, rely=0.05)
    coning_terminal.insert(tk.END, ERH_Systems)
    tk.Button(E_nav, text="❗", font=("Georgia", font_size), bg=bg_color, borderwidth=0, border=0, fg='gray', activeforeground='green', activebackground=bg_color, command=lambda: ehr_run(coning_terminal)).place(relheight=1, relwidth=0.07, relx=0.86)
    tk.Button(E_nav, text="▶", font=("Georgia", font_size), bg=bg_color, borderwidth=0, border=0, fg='green', activeforeground='green', activebackground=bg_color, command=lambda: ehr_run(coning_terminal)).place(relheight=1, relwidth=0.07, relx=0.93)
    tk.Label(E_nav, text="ERH_system Terminal", font=("Courier New ", font_size - 5, "bold"), anchor='w', fg='gray', bg=bg_color).place(relheight=1, relwidth=0.2, relx=0)

    return EHR_page_container


def User_Home_page(widget):
    global user_id, side_bar_widget_list, side_bar_widget_list2, Home_page_frame
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor, nav_bg
    global root, screen_width, screen_height, nav_widg, font_size

    def change_Widget_Attribute_OnHover(widget_bn, pop_side_bar, solid_side_bat):  # Color change bg on Mouse Hover
        def show(pop_side_bar=pop_side_bar, solid_side_bat=solid_side_bat):
            global nav_bg, bg_color, side_bar_widget_list2
            color = darken_hex_color(bg_color)
            for i in side_bar_widget_list2:
                i.config(bg=color)
            pop_side_bar.config(bg=color)
            pop_side_bar.place(rely=0, relx=0.025, width=int(screen_width * 0.1), height=int((screen_height * 1) - 20))

        def hide(pop_side_bar=pop_side_bar, solid_side_bat=solid_side_bat):
            global nav_bg

            def enter():
                pop_side_bar.after_cancel(id)

            def leave():
                pop_side_bar.config(bg=nav_bg)
                pop_side_bar.place_forget()

            id = pop_side_bar.after(300, pop_side_bar.place_forget)
            pop_side_bar.bind("<Enter>", func=lambda e: enter())
            pop_side_bar.bind("<Leave>", func=lambda e: leave())

        widget_bn.bind("<Enter>", func=lambda e: show())
        widget_bn.bind("<Leave>", func=lambda e: hide())

    Home_page_frame = tk.Frame(widget, bg=fg_color, width=screen_width, height=screen_height)
    Home_page_frame.place(relx=0, rely=0)

    container1 = tk.Frame(Home_page_frame, bg=bg_color)
    container1.place(rely=0, relx=0, width=int(screen_width * 0.025), height=int((screen_height * 1) - 20))

    container2 = tk.Frame(Home_page_frame, bg=bg_color)
    container2.place(rely=0, relx=0.0253, width=int(screen_width * 0.9747), height=int((screen_height * 1) - 20))  # place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253, )

    # PROFILE_widget = profile(Home_page_frame)

    Profile_Widget = Profile_Page(container2)
    # CALL_Widget = call(container2)
    chat_me_Widget = chat_me(container2)
    CHAT_Widget = Main_Page(container2)
    rag_widget = RAG_page(container2)
    img_extract = Clinical_Image(container2)
    patient_recods = Recodes_Page(container2)
    integration_page = EHR_integration_page(container2)
    DManagment_page = Document_Management_page(container2)

    # sidebar  widgets ------------------------------------------------------------------------------------------------------------------------------------

    def active(widget):
        global side_bar_widget_list, fg_hovercolor, nav_bg, bg_color
        for i in side_bar_widget_list:
            if i != widget:
                try:
                    i.config(relief=tk.FLAT, border=0, fg=fg_color, bg=bg_color)
                    # change_bg_OnHover_light(st2_bt)
                except:

                    side_bar_widget_list.remove(i)
            else:

                i.config(relief=tk.FLAT, border=0, fg="yellow", bg=lighten_hex_color(bg_color))
                # change_bg_OnHover(widget, lighten_hex_color(bg_color), lighten_hex_color(bg_color))

    def duplicate_widget(widget, dest_frame, text=""):
        def run_func(widget=widget, dest_frame=dest_frame, text=text):
            global fg_color, bg_color, side_bar_widget_list2
            relx = widget.place_info()["relx"]
            rely = widget.place_info()["rely"]
            relwidth = widget.place_info()["relwidth"]
            relheight = widget.place_info()["relheight"]

            widget_type = type(widget)
            widget_geometry = widget.winfo_geometry()
            widget_text = text
            widget_state = widget.cget("state")

            duplicate = widget_type(dest_frame)
            side_bar_widget_list2.append(duplicate)
            if isinstance(duplicate, tk.Label):
                font = ("Broadway", font_size)
                duplicate.config(text=widget_text, font=font, state=widget_state, bg=darken_hex_color(bg_color), fg=fg_color, anchor=tk.W, borderwidth=0, border=0)

            elif isinstance(duplicate, tk.Button):
                font = ("Bahnschrift Light Condensed", font_size - 3)
                widget_command = widget.cget("command")
                duplicate.config(text=widget_text, command=widget_command, font=font, state=widget_state, bg=darken_hex_color(bg_color), fg=fg_color, anchor=tk.W, borderwidth=0, border=0)
                # change_bg_OnHover_light(duplicate)
                change_bg_OnHover_dark(duplicate, widget)

            duplicate.place(relheight=relheight, relwidth=relwidth, rely=rely, relx=relx)

        threading.Thread(target=run_func).start()

    side_bar = tk.Frame(container1, bg=nav_bg, borderwidth=0, border=0)
    side_bar.place(relheight=1, relwidth=1, rely=0, relx=0)
    side_bar_full = tk.Frame(Home_page_frame, bg=nav_bg, borderwidth=0, border=0)
    nav_widg = (side_bar, side_bar_full)
    # side_bar.bind("<Configure>", lambda e: resize(side_bar, side_wdg_width, side_wdg_height))

    profile_widget = tk.Label(side_bar, bg=nav_bg, activebackground=bg_color, activeforeground=fg_color, text='⍲', font=("Calibri", font_size), fg=fg_color, anchor='center', borderwidth=0, border=0)  # ,command=lambda: (PROFILE_widget.tkraise(), active(profile_widget)))
    profile_widget.place(relheight=0.03, relwidth=1, rely=0.01, relx=0)

    side_bar_widget_list.append(profile_widget)
    change_Widget_Attribute_OnHover(profile_widget, side_bar_full, side_bar)
    duplicate_widget(profile_widget, side_bar_full, text="Digital Scribe")

    st1_bt = tk.Button(side_bar, bg=nav_bg, activebackground=bg_color, activeforeground=fg_color, text='≣', font=("Calibri", font_size), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (Profile_Widget.tkraise(), active(st1_bt)))
    st1_bt.place(relheight=0.03, relwidth=1, rely=0.05, relx=0)
    change_bg_OnHover_light(st1_bt)
    side_bar_widget_list.append(st1_bt)
    duplicate_widget(st1_bt, side_bar_full, text="Account")

    st2_bt = tk.Button(side_bar, bg=nav_bg, activebackground=bg_color, activeforeground=fg_color, text='⧮', font=("Calibri", font_size), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (CHAT_Widget.tkraise(), active(st2_bt)))
    st2_bt.place(relheight=0.03, relwidth=1, rely=0.09, relx=0)
    change_bg_OnHover_light(st2_bt)
    side_bar_widget_list.append(st2_bt)
    duplicate_widget(st2_bt, side_bar_full, text="Live Entity extract")

    st3_bt = tk.Button(side_bar, bg=nav_bg, activebackground=bg_color, activeforeground=fg_color, text='🗐', font=("Calibri", font_size), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (rag_widget.tkraise(), active(st3_bt)))
    st3_bt.place(relheight=0.03, relwidth=1, rely=0.13, relx=0)
    change_bg_OnHover_light(st3_bt)
    side_bar_widget_list.append(st3_bt)
    duplicate_widget(st3_bt, side_bar_full, text="RAG clinical Documents")

    st4_bt = tk.Button(side_bar, bg=nav_bg, activebackground=bg_color, activeforeground=fg_color, text='⧉', font=("Calibri", font_size), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (chat_me_Widget.tkraise(), active(st4_bt)))
    st4_bt.place(relheight=0.03, relwidth=1, rely=0.17, relx=0)
    change_bg_OnHover_light(st4_bt)
    side_bar_widget_list.append(st4_bt)
    duplicate_widget(st4_bt, side_bar_full, text="AI-powered Assistance")

    st5_bt = tk.Button(side_bar, bg=nav_bg, activebackground=bg_color, activeforeground=fg_color, text='🕮', font=("Calibri", font_size), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (img_extract.tkraise(), active(st5_bt)))
    st5_bt.place(relheight=0.03, relwidth=1, rely=0.21, relx=0)
    change_bg_OnHover_light(st5_bt)
    side_bar_widget_list.append(st5_bt)
    duplicate_widget(st5_bt, side_bar_full, text="OCR clinical img Notes ")

    st6_bt = tk.Button(side_bar, bg=nav_bg, activebackground=bg_color, activeforeground=fg_color, text='✎', font=("Calibri", font_size), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (patient_recods.tkraise(), active(st6_bt)))
    st6_bt.place(relheight=0.03, relwidth=1, rely=0.25, relx=0)
    change_bg_OnHover_light(st6_bt)
    side_bar_widget_list.append(st6_bt)
    duplicate_widget(st6_bt, side_bar_full, text="Patient Records")

    st9_bt = tk.Button(side_bar, bg=nav_bg, activebackground=bg_color, activeforeground=fg_color, text='🗁', font=("Calibri", font_size), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (DManagment_page.tkraise(), active(st9_bt)))
    st9_bt.place(relheight=0.03, relwidth=1, rely=0.29, relx=0)
    change_bg_OnHover_light(st9_bt)
    side_bar_widget_list.append(st9_bt)
    duplicate_widget(st9_bt, side_bar_full, text="Document Management")

    st7_bt = tk.Button(side_bar, bg=nav_bg, activebackground=bg_color, activeforeground=fg_color, text='≎', font=("Calibri", font_size), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (integration_page.tkraise(), active(st7_bt)))
    st7_bt.place(relheight=0.03, relwidth=1, rely=0.97, relx=0)
    change_bg_OnHover_light(st7_bt)
    side_bar_widget_list.append(st7_bt)
    duplicate_widget(st7_bt, side_bar_full, text="EHR integration")

    CHAT_Widget.tkraise()
    active(st2_bt)


def Welcome_Page(wiget):
    global screen_width, screen_height, bg_color, fg_color

    def change_Widget_Attribute_OnHover(widget, Text_On_Hover, Text_On_Leave, function):  # Color change bg on Mouse Hover
        def show(widg):
            widg.place(relheight=0.5, relwidth=1, rely=0.1, relx=0)

        def hide(widg):
            def enter():
                widg.after_cancel(id)

            def leave():
                widg.place_forget()
                return

            id = widg.after(300, widg.place_forget)
            widg.bind("<Enter>", func=lambda e: enter())
            widg.bind("<Leave>", func=lambda e: leave())

        widget.bind("<Enter>", func=lambda e: (widget.config(text=Text_On_Hover, background=lighten_hex_color(bg_color)), show(function)))
        widget.bind("<Leave>", func=lambda e: (widget.config(text=Text_On_Leave, background=lighten_hex_color(bg_color)), hide(function)))

    welcome_page_frame = tk.Frame(wiget, bg=bg_color, width=screen_width)
    welcome_page_frame.pack(fill=tk.BOTH, expand=True)

    App_title = "Digital ScriBe"
    nav_bar_color = "white"
    nav_bar_btn_hover_color = '#F5F5F5'

    img1 = tk.Label(welcome_page_frame, bg=bg_color)
    img1.place(relheight=0.35, relwidth=0.4, rely=0.05, relx=0)
    imagen("./Assets/home_img_2.png", int(screen_width * 0.4), int(screen_height * 0.35), img1)

    section1 = tk.Frame(welcome_page_frame, bg=bg_color)
    section1.place(relheight=0.35, relwidth=0.4, rely=0.05, relx=0.4)
    tk.Label(section1, text="Responsibilities of Digital Scribe", bg=bg_color, fg=fg_color, font=("Bauhaus 93", 20), anchor="w").place(relwidth=1, relheight=0.2, rely=0, relx=0)
    tk.Label(section1, text=" * Transcribe during appointment", bg=bg_color, fg=fg_color, font=("Times New Roman", 20), anchor="w").place(relwidth=1, relheight=0.1, rely=0.2, relx=0)
    tk.Label(section1, text=" * Update and maintain Medical Conversation", bg=bg_color, fg=fg_color, font=("Times New Roman", 20), anchor="w").place(relwidth=1, relheight=0.1, rely=0.3, relx=0)
    tk.Label(section1, text=" * Administrative Duties ", bg=bg_color, fg=fg_color, font=("Times New Roman", 20), anchor="w").place(relwidth=1, relheight=0.1, rely=0.4, relx=0)
    tk.Label(section1, text=" * AI Assistant", bg=bg_color, fg=fg_color, font=("Times New Roman", 20), anchor="w").place(relwidth=1, relheight=0.1, rely=0.5, relx=0)
    tk.Label(section1, text=" * Analyze clinical notes", bg=bg_color, fg=fg_color, font=("Times New Roman", 20), anchor="w").place(relwidth=1, relheight=0.1, rely=0.6, relx=0)
    tk.Label(section1, text=" * Summarize Clinical 'info'", bg=bg_color, fg=fg_color, font=("Times New Roman", 20), anchor="w").place(relwidth=1, relheight=0.1, rely=0.7, relx=0)
    tk.Label(section1, text=" * Extract Clinical data from conversations", bg=bg_color, fg=fg_color, font=("Times New Roman", 20), anchor="w").place(relwidth=1, relheight=0.1, rely=0.8, relx=0)
    tk.Label(section1, text=" * ", bg=bg_color, fg=fg_color, font=("Times New Roman", 20), anchor="w").place(relwidth=1, relheight=0.1, rely=0.9, relx=0)

    img3 = tk.Label(welcome_page_frame, bg=bg_color)
    img3.place(relheight=0.35, relwidth=0.2, rely=0.05, relx=0.8)
    imagen("./Assets/home_img_1.png", int(screen_width * 0.4), int(screen_height * 0.35), img3)

    img2 = tk.Label(welcome_page_frame, bg=bg_color)
    img2.place(relheight=0.5, relwidth=1, rely=0.4, relx=0)
    imagen("./Assets/home_img_3.png", int(screen_width), int(screen_height * 0.5), img2)

    nav_bar = tk.Frame(welcome_page_frame, bg=lighten_hex_color(bg_color))
    nav_bar.place(relheight=0.05, relwidth=1, rely=0, relx=0)

    nav_bar_title_widget = tk.Label(nav_bar, bg=lighten_hex_color(bg_color), fg=darken_hex_color(bg_color), text=App_title, justify=tk.LEFT, anchor="w", font=("Forte", 20), borderwidth=0, border=0)
    nav_bar_title_widget.place(relheight=1, relwidth=0.1, rely=0, relx=0)

    """
    nav_bar_bt1_widget = tk.Button(nav_bar, bg=nav_bar_color, text='Services ∨', justify=tk.LEFT, anchor="center", font=("Calibri", 12), borderwidth=0, border=0)
    nav_bar_bt1_widget.place(relheight=0.6, relwidth=0.08, rely=0.2, relx=0.6)
    change_Widget_Attribute_OnHover(nav_bar_bt1_widget, 'Services ∧', 'Services ∨', nav_bar_btn_hover_color, nav_bar_color, Service_Section(welcome_page_frame))

    nav_bar_bt2_widget = tk.Button(nav_bar, bg=nav_bar_color, text='For Clinicians ∨', justify=tk.LEFT, anchor="center", font=("Calibri", 12), borderwidth=0, border=0)
    nav_bar_bt2_widget.place(relheight=0.6, relwidth=0.08, rely=0.2, relx=0.69)
    change_Widget_Attribute_OnHover(nav_bar_bt2_widget, 'For Clinicians ∧', 'For Clinicians ∨', nav_bar_btn_hover_color, nav_bar_color, Service_Section(welcome_page_frame))

    nav_bar_bt3_widget = tk.Button(nav_bar, bg=nav_bar_color, text='For Business ∨', justify=tk.LEFT, anchor="center", font=("Calibri", 12), borderwidth=0, border=0)
    nav_bar_bt3_widget.place(relheight=0.6, relwidth=0.08, rely=0.2, relx=0.78)
    change_Widget_Attribute_OnHover(nav_bar_bt3_widget, 'For Business ∧', 'For Business ∨', nav_bar_btn_hover_color, nav_bar_color, Service_Section(welcome_page_frame))
    """

    nav_bar_bt4_widget = tk.Button(nav_bar, bg=lighten_hex_color(bg_color), fg=darken_hex_color(bg_color), text='Log in ∨', activebackground=lighten_hex_color(bg_color), activeforeground=fg_color, justify=tk.LEFT, anchor="center", font=("Calibri", 12), borderwidth=0, border=0)
    nav_bar_bt4_widget.place(relheight=0.6, relwidth=0.05, rely=0.2, relx=0.87)

    change_Widget_Attribute_OnHover(nav_bar_bt4_widget, 'Log in ∧', 'Log in ∨', Login_Section_widget(welcome_page_frame))

    nav_bar_bt5_widget = tk.Button(nav_bar, bg=lighten_hex_color(bg_color), fg=darken_hex_color(bg_color), text='Get started', activebackground=lighten_hex_color(bg_color), activeforeground=fg_color, justify=tk.LEFT, anchor="center", font=("Calibri", 12), borderwidth=0, border=0)
    nav_bar_bt5_widget.place(relheight=0.6, relwidth=0.06, rely=0.2, relx=0.935)


# =============================== Main Function definition ============================================================
# =====================================================================================================================
def main():
    global root, screen_width, screen_height, session, client_socket, server_IP4v_address, Server_listening_port
    global user_id, user_Photo, First_name, Second_Name, Last_Name, Email
    global gradient_ai_workspace_id, assemblyai_access_key, gradient_ai_access_key, keys
    global bg_color, User_Email, User_Pass

    Set_Configuration()
    run_server()
    themes_configurations()

    root = tk.Tk()

    scale = tk.Scale(root, from_=0, to=256, orient=tk.HORIZONTAL)
    scale.set(100)  # Set the default value to 100
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # For Windows 8.1 and above

    root.title("")
    root.state('zoomed')  # this creates a window that takes over the screen
    root.minsize(600, 500)
    root.geometry("1920x1280")
    screen_width = root.winfo_screenwidth()  # Get the screen width dimensions
    screen_height = root.winfo_screenheight()  # Get the screen height dimensions

    title_bar_color(root, bg_color)

    Welcome_Page(root)


    try:
        with open('./Data_Raw/CUR_user.json', 'r') as openfile:  # Reading from json file
            cur_detail = json.load(openfile)
        cridentials_age = cur_detail["_CERT_DT_"]

        cridentials_age = cridentials_age.split(',')
        cur_date = now_date.strftime("%Y,%m,%d")
        cur_date = cur_date.split(',')

        y = int(cur_date[0]) - int(cridentials_age[0])
        m = int(cur_date[1]) - int(cridentials_age[1])
        d = int(cur_date[2]) - int(cridentials_age[2])

        if y == 0:
            m = m * 30
            aged = m + d
            if aged < 30:
                print("aged: ", aged)
                User_Email = decrypt_data(cur_detail['_E_token_'])
                User_Pass = decrypt_data(cur_detail['_P_token_'])
                User_Home_page(root)

    except Exception as e:
        print(e)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


def go():
    try:
        main()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    #main()

    #"""
        t = System_Thread(ThreadStart(go))
        t.ApartmentState = ApartmentState.STA
        t.Start()
        t.Join()
    # """
