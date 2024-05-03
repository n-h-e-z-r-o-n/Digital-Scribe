# ============================================= Used libraries ==========================================================================================
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

from gradientai import Gradient, SummarizeParamsLength, ExtractParamsSchemaValueType
from tkinter import filedialog
# import docx
import ctypes
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

# ------------------------------- img-to-text --------------------------------------------------------------------------------------------
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from paddleocr import PaddleOCR, draw_ocr

ocr_model = PaddleOCR(lang='en', use_gpu=False)  # You can enable GPU by setting use_gpu=True

# -------------------------------  --------------------------------------------------------------------------------------------

from docx2pdf import convert  # pip install docx2pdf
import pdfplumber  # used for extracting data from pdf
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

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
keys = None
vosk_model = None
wisper_model_base = None
wisper_model_tiny = None
rag_pipeline = None
llm_chain = None
llm_chain2 = None
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

clinical_Note_upload_btn = None
proccessed_img_url = None
font_size = 15
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
            print("Data received from HTML:", received_data)

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
def title_bar_color(color):
    # import ctypes as ct
    global root
    root.update()
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
    print(color)
    get_parent = ct.windll.user32.GetParent
    HWND = get_parent(root.winfo_id())

    color = '0x' + color
    color = int(color, 16)

    ct.windll.dwmapi.DwmSetWindowAttribute(HWND, 35, ct.byref(ct.c_int(color)), ct.sizeof(ct.c_int))


def change_color(widget, button):
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor, current_theme, nav_bg, nav_widg

    button_text = button.cget("text")
    print("color_change: ", button_text)
    if button_text == 'window(light)':
        button.config(text='window(dark_gray)')
        bg_color = '#353839'
        fg_color = 'white'
        current_theme = 'window(dark_gray)'
        title_bar_color(bg_color)
        nav_bg = bg_color

    elif button_text == 'window(dark_gray)':
        button.config(text='window(dark_blue)')
        bg_color = '#36454F'
        fg_color = 'white'
        current_theme = 'window(dark_blue)'
        title_bar_color(bg_color)
        nav_bg = bg_color

    elif button_text == 'window(dark_blue)':
        button.config(text='window(Blackberry)')
        bg_color = '#3A3A38'
        fg_color = 'white'
        current_theme = 'window(Blackberry)'
        title_bar_color(bg_color)
        nav_bg = bg_color

    elif button_text == 'window(Blackberry)':
        button.config(text='window(dark_green)')
        bg_color = '#555D50'
        fg_color = 'white'
        current_theme = 'window(dark_green)'
        title_bar_color(bg_color)
        nav_bg = bg_color

    elif button_text == 'window(dark_green)':
        button.config(text='window(Jacket)')
        bg_color = '#253529'
        fg_color = 'white'
        current_theme = 'window(Jacket)'
        title_bar_color(bg_color)
        nav_bg = bg_color

    elif button_text == 'window(Jacket)':
        button.config(text='window(light)')
        bg_color = '#F5F5F5'
        fg_color = 'black'
        current_theme = 'window(light)'
        title_bar_color(bg_color)
        nav_bg = bg_color

    else:
        return

    def change_all(wdget=widget):
        global bg_color, fg_color, fg_hovercolor, bg_hovercolor, current_theme, Home_page_frame

        if isinstance(wdget, tk.Frame):
            wdget.config(bg=bg_color)

        elif isinstance(wdget, tk.Button):
            wdget.config(bg=bg_color, activebackground=bg_color, fg=fg_color, activeforeground=fg_color)

        elif isinstance(wdget, tk.Label):
            wdget.config(bg=bg_color, fg=fg_color)

        elif isinstance(wdget, tk.Text):
            wdget.config(bg=bg_color, fg=fg_color)
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
        dic = {
            '_GA_': gradient_ai_access_key,
            '_GW_': gradient_ai_workspace_id,
            '_G_FT_M_': gradient_ai_finetuned_id,
            '_G_B_M_': gradient_ai_base_model_id,
            '_AAI_': assemblyai_access_key,
            "bg_color": bg_color,
            "fg_color": fg_color,
            "fg_hovercolor": fg_hovercolor,
            "bg_hovercolor": bg_hovercolor,
            "current_theme": current_theme,
            "nav_bg": nav_bg
        }

        json_object = json.dumps(dic, indent=4)

        with open("keys.json", "w") as outfile:
            outfile.write(json_object)

    modify_css()

    threading.Thread(target=change_all).start()


# --------------------------------- NLP and LLM  --------------------------------------------------------------------------------------------------------


def entity_highlight_words(widget):
    def Run():
        global found_entities, fg_color
        if fg_color == 'black':
            widget.tag_configure("highlight", background="gold")  # Configure a tag for highlighting
        else:
            widget.tag_configure("highlight", background="#737000")

        for word in found_entities:
            start = 1.0
            entites = word.split()
            if len(entites) == 1:
                while True:
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
                    if (g_word == "or") or (g_word == "OR") or (g_word == "and") or (g_word == "AND") or (g_word == "when"):
                        continue
                    while True:
                        start = widget.search(g_word, start, stopindex=tk.END)
                        if not start:
                            break
                        end = f"{start}+{len(g_word)}c"
                        widget.tag_add("highlight", start, end)
                        start = end

    threading.Thread(target=Run).start()


def Entity_Extraction(document_widget, widget=None):
    def run(document_widget=document_widget, widget=widget):
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
            widget.delete(1.0, tk.END)
            Recording_entity = '------------------------ EXTRACTED ENTITIES \n\n'
            found_entities = []
            print('result["entity"].items() :', len(result["entity"].items()))
            for key, value in result["entity"].items():
                Recording_entity += key + " : " + value + "\n"
                found_entities.append(value)

            entity_highlight_words(document_widget)

            if widget is not None:
                widget.insert(tk.END, Recording_entity)
            else:
                Recording_entity = Recording_entity

        except Exception as e:
            print(type(e).__name__)
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


def D_Summary(widget1, widget=None):
    def run_f(widget1=widget1, widget=widget):
        global Recording, Recording_paused, Recording_summary
        gradient = Gradient()

        document = widget1.get("1.0", "end")
        document = (document.strip())

        if len(document) < 5:
            return
        try:
            Recording_summary = '\n------------------------ CONVERSATION SUMMARY\n'
            summary_length = SummarizeParamsLength.LONG
            result = gradient.summarize(
                document=document,
                length=summary_length
            )

            if widget is not None:
                widget.config(state=tk.NORMAL)
                widget.delete(1.0, tk.END)
                widget.insert(tk.END, '\n------------------------ CONVERSATION SUMMARY\n' + result['summary'])
            else:
                Recording_summary += result['summary']


        except Exception as e:
            print(e)

    threading.Thread(target=run_f).start()


def rag_initialize(data=None):
    print("rag_initializ_start")
    global rag_pipeline, rag_data

    rag_pipeline = None

    if data is None and rag_data is None:
        return

    elif data is None and rag_data is not None:
        data = rag_data

    document_store = InMemoryDocumentStore()
    writer = DocumentWriter(document_store=document_store)

    document_embedder = GradientDocumentEmbedder(
        access_token=os.environ["GRADIENT_ACCESS_TOKEN"],
        workspace_id=os.environ["GRADIENT_WORKSPACE_ID"],
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
            widget1.config(text='▶')
            widget.config(state=tk.DISABLED)

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
    global llm_chain, llm_chain2
    fine_tuned_Model_Id = "d189f721-ae17-4545-a0ad-f95194e857f5_model_adapter"  # initializes a GradientLLM with our fine-tuned model by specifying our model ID.

    gradient = Gradient()
    base_model = gradient.get_base_model(base_model_slug="nous-hermes2")

    # ================================================ chat bot section
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

    # ================================================ chat bot section
    llm2 = GradientLLM(
        model=base_model.id,
        model_kwargs=dict(max_generated_token_count=510),
    )

    template2 = """You are a AI that analyzes data exacted from images and present it in a formatted way. 
    Human: {Instruction}
    Chatbot:"""

    prompt2 = PromptTemplate(template=template2, input_variables=["Instruction"])
    llm_chain2 = LLMChain(prompt=prompt2, llm=llm2)


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


def RUN_OFFLINE_speech_recognition(widget, widget1=None, widget2=None, Record_btn=None, clock_wideth=None):
    global closed, Recording, Recording_paused, Recording_data, vosk_model
    global fg_color, bg_color, miniute, second, hour
    global audio_frames
    if Recording:
        miniute = second = hour = 0
        Recording = False
        Record_btn.config(fg=fg_color)
        clock_wideth.config(text='0:0:0')
        Recording_paused = False
        return

    def start_recording():
        global Recording
        messages.put(True)
        print("Starting...")
        Recording = True
        Record_btn.config(fg="green")

        Thread(target=record_microphone).start()
        Thread(target=speech_recognition, args=(widget,)).start()

    def record_microphone(chunk=1024, RECORD_SECONDS=5):
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
        running_scribe = False
        print("scanning")
        audio_frames = []
        previous_data = ''
        pos = 0
        index = 0
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
                        end_idx = len(audio_frames) - index
                        index = end_idx
                        transcribe_audio(audio_frames[start_idx: end_idx], widget1)
                        # D_Summary(widget1)
                        widget2.delete(1.0, tk.END)
                        widget2.insert(tk.END, Recording_entity + Recording_summary)
                        pos = 0

                    pos += 1
                else:
                    pass
                    """
                    if index != len(audio_frames) - index:
                        start_idx = index
                        end_idx = len(audio_frames) - index
                        index = end_idx
                        transcribe_audio(audio_frames[start_idx: end_idx], widget1)
                    print("index new:", index)
                    """
            except Exception as e:
                print(e)

    def grammar(frames):
        global wisper_model_tiny, wisper_model_base

        # Define audio parameters
        channels = 1  # Mono
        sample_width = 2  # 16-bit audio
        sample_rate = 16000  # Sample rate (Hz)
        output_file = 'wisper_model_tiny.wav'
        # Open the output file in write mode
        with wave.open(output_file, 'wb') as output_wave:
            # Set audio parameters
            output_wave.setnchannels(channels)
            output_wave.setsampwidth(sample_width)
            output_wave.setframerate(sample_rate)

            # Write the audio frames to the file
            output_wave.writeframes(b''.join(frames))

        # print("Audio file saved successfully.")

        result = wisper_model_tiny.transcribe(output_file)

        return result["text"]

    def transcribe_audio(frames, widget):
        global running_scribe, previous_data
        global wisper_model_tiny, wisper_model_base

        if running_scribe:
            return
        running_scribe = True
        # Define audio parameters
        channels = 1  # Mono
        sample_width = 2  # 16-bit audio
        sample_rate = 16000  # Sample rate (Hz)
        output_file = 'wisper_model_tiny.wav'
        # Open the output file in write mode
        with wave.open(output_file, 'wb') as output_wave:
            # Set audio parameters
            output_wave.setnchannels(channels)
            output_wave.setsampwidth(sample_width)
            output_wave.setframerate(sample_rate)

            # Write the audio frames to the file
            output_wave.writeframes(b''.join(frames))

        # print("Audio file saved successfully.")
        result = wisper_model_tiny.transcribe(output_file)
        # widget.delete(1.0, tk.END)
        widget.insert(tk.END, result["text"] + "\n")
        widget.see(tk.END)
        Entity_Extraction(widget1)
        running_scribe = False

        # integrate_strings(previous_data, widget.get("1.0", "end"), result["text"])

    while True:
        """
        if vosk_model == None:
            continue
        """
        messages = Queue()
        recordings = Queue()
        FRAME_RATE = 16000
        rec = KaldiRecognizer(vosk_model, FRAME_RATE)
        rec.SetWords(True)
        threading.Thread(target=start_recording).start()
        speech_record_time(clock_wideth)
        break


miniute = 0
hour = 0
sec = 0


def speech_record_time(widget):
    def Run(widget=widget):
        global closed, Recording, Recording_paused
        global sec, miniute, hour
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

                # Open the output file in write mode
                with wave.open(output_file, 'wb') as output_wave:
                    # Set audio parameters
                    output_wave.setnchannels(channels)
                    output_wave.setsampwidth(sample_width)
                    output_wave.setframerate(sample_rate)
                    output_wave.writeframes(b''.join(audio_frames))
            downloading_audio = False

    threading.Thread(target=run).start()


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

    threading.Thread(target=run1).start()

    global ocr_model, extraced_img_data, llm_chain2, proccessed_img_url

    view_wid.load_url('file:///' + path_exe + "/html/load_anmation2.html")
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
        print(text)

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


def access_keys_info():
    global gradient_ai_workspace_id, assemblyai_access_key, gradient_ai_access_key, gradient_ai_finetuned_id, gradient_ai_base_model_id, keys
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor, current_theme, nav_bg
    try:
        with open('keys.json', 'r') as openfile:  # Reading from json file
            keys = json.load(openfile)

            gradient_ai_access_key = keys['_GA_']
            gradient_ai_workspace_id = keys['_GW_']
            gradient_ai_finetuned_id = keys['_G_FT_M_']
            gradient_ai_base_model_id = keys['_G_B_M_']

            assemblyai_access_key = keys['_AAI_']

            bg_color = keys['bg_color']
            fg_color = keys['fg_color']
            fg_hovercolor = keys['fg_hovercolor']
            bg_hovercolor = keys['bg_hovercolor']
            current_theme = keys['current_theme']
            nav_bg = keys['nav_bg']

            print('gradient_ai_workspace_id :', gradient_ai_workspace_id)
            print('gradient_ai_access_key:', gradient_ai_access_key)
            print('assemblyai_access_key :', assemblyai_access_key)

            os.environ['GRADIENT_ACCESS_TOKEN'] = gradient_ai_access_key
            os.environ['GRADIENT_WORKSPACE_ID'] = gradient_ai_workspace_id

            print(bg_color)
            modify_css()
    except Exception as e:
        print("access_keys_info Function:", e)
        modify_css()
        pass


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


def change_bg_OnHover(widget, colorOnHover, colorOnLeave):  # Color change bg on Mouse Hover
    global bg_color
    widget.bind("<Enter>", func=lambda e: widget.config(background=colorOnHover))
    widget.bind("<Leave>", func=lambda e: widget.config(background=bg_color))


def change_bg_OnHover_light(widget):  # Color change bg on Mouse Hover
    global bg_color
    widget.bind("<Enter>", func=lambda e: widget.config(background=lighten_hex_color(bg_color, factor=0.2)))
    widget.bind("<Leave>", func=lambda e: widget.config(background=bg_color))


def change_bg_OnHover_dark(widget1, widget2):  # Color change bg on Mouse Hover
    global bg_color
    widget1.bind("<Enter>", func=lambda e: (widget1.config(background=lighten_hex_color(bg_color, factor=0.2)), widget2.config(background=lighten_hex_color(bg_color, factor=0.2))))
    widget1.bind("<Leave>", func=lambda e: (widget1.config(background=darken_hex_color(bg_color, factor=0.2)), widget2.config(background=bg_color)))


def change_fg_OnHover(widget, colorOnHover, colorOnLeave):  # Color change fg on Mouse Hover
    global fg_color
    widget.bind("<Enter>", func=lambda e: widget.config(fg=colorOnHover))
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


# =============================== Pages Functions definition =======================================================================================
def sign_out(wig):
    global client_socket, server_IP4v_address, Server_listening_port, session, user_id
    signout_credentials = f'Sign_out_Request~{user_id}'
    try:
        client_socket.send(signout_credentials.encode("utf-8")[:1024])  # send message
        status = client_socket.recv(1024).decode("utf-8", errors="ignore")
        if status == 'signed_out_success':
            client_socket.close()
            wig.destroy()
            session.clear()
            Welcome_Page(root)
        else:
            pass
    except:
        connect_to_server()


def encrypt(string):
    salt = "5gzbella"
    string = string + salt  # Adding salt to the password
    hashed = hashlib.md5(string.encode())  # Encoding the password
    return hashed.hexdigest()  # return the Hash


def login_Request(email, passw, root_widget):
    global client_socket, server_IP4v_address, Server_listening_port, session, user_id, First_name, Second_Name, Last_Name, Email, user_Photo
    if (len(email) and len(passw)) > 3:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
        try:
            client_socket.connect((server_IP4v_address, Server_listening_port))  # connect to the server
        except:
            print('Error: Unable to connect')
        login_credentials = f'login_Request~{email}~{encrypt(passw)}'
        client_socket.send(login_credentials.encode("utf-8")[:1024])  # send message
        status = client_socket.recv(700000).decode("utf-8", errors="ignore")
        if status == 'User_Error':
            print('User_Error')
            client_socket.close()
        else:
            status = status.split('~')

            user_id = status[0]
            First_name = status[1]
            Second_Name = status[2]
            Last_Name = status[3]
            Email = status[4]
            user_Photo = status[5]

            print('User_id: ', user_id)
            session['logged_in'] = True
            session['__id__'] = user_id
            session['__FN__'] = First_name
            session['__SN__'] = Second_Name
            session['__LN__'] = Last_Name
            session['__EM__'] = Email
            session['__IMG__'] = user_Photo

            root_widget.destroy()
            User_Home_page(root)

    # root_widget.destroy()
    # User_Home_page(root)


def sign_up_Request(email, passw, root_widget):
    pass


def Login_Section_widget(widget, root_widget):
    global screen_width, screen_height
    nav_bar_color = "white"
    Login_widget = tk.Frame(widget, bg=nav_bar_color)

    # Login_widget.place(relheight=0.3, relwidth=1, rely=0.02, relx=0)

    def Forgot_pass():
        def back(widg):
            widg.place_forget()

        Forgot_password_widget = tk.Frame(Login_widget, bg=nav_bar_color, borderwidth=0, border=0)
        # Forgot_password_widget.place(relheight=0.7, relwidth=0.25, rely=0.05, relx=0.34)

        tk.Label(Forgot_password_widget, bg=nav_bar_color, text='🔎', font=("Bahnschrift SemiLight Condensed", 36),
                 borderwidth=0, border=0).place(relheight=0.1, relwidth=1, rely=0, relx=0)
        tk.Label(Forgot_password_widget, bg=nav_bar_color, text='Forgot your password?',
                 font=("Bahnschrift SemiLight Condensed", 36), borderwidth=0, border=0).place(relheight=0.1, relwidth=1,
                                                                                              rely=0.1, relx=0)
        tk.Label(Forgot_password_widget, bg=nav_bar_color,
                 text='Please enter the email address you used to register.\nWe’ll send a link with instructions to reset your password',
                 font=("Bahnschrift SemiLight Condensed", 12), borderwidth=0, border=0).place(relheight=0.12,
                                                                                              relwidth=1, rely=0.2,
                                                                                              relx=0)
        tk.Label(Forgot_password_widget, bg=nav_bar_color, text='email', anchor='w', font=("Batang", 9), borderwidth=0,
                 border=0).place(relheight=0.03, relwidth=0.8, rely=0.395, relx=0.1)

        email_password_entry_widg = tk.Entry(Forgot_password_widget, bg=nav_bar_color, font=("Courier New", 13),
                                             relief="solid", borderwidth=1, border=1)
        email_password_entry_widg.place(relheight=0.1, relwidth=0.8, rely=0.43, relx=0.1)
        change_bg_OnHover(email_password_entry_widg, '#F5F5F5', nav_bar_color)

        password_reset__btn = tk.Button(Forgot_password_widget, bg='#1C352D', fg='white', activebackground='#8A9A5B',
                                        text='Request Password reset', font=('Aptos Narrow', 11, 'bold'),
                                        relief="solid", borderwidth=0, border=0)
        password_reset__btn.place(relheight=0.1, relwidth=0.8, rely=0.6, relx=0.1)
        change_bg_OnHover(password_reset__btn, '#004830', '#1C352D')

        tk.Label(Forgot_password_widget, bg=nav_bar_color, fg='black', activebackground='#8A9A5B', text='Need help?',
                 font=('Aptos Narrow', 10), relief="solid", anchor='w', borderwidth=0, border=0).place(relheight=0.04,
                                                                                                       relwidth=0.2,
                                                                                                       rely=0.72,
                                                                                                       relx=0.1)
        Customer_support_link = tk.Button(Forgot_password_widget, bg=nav_bar_color, fg='#A8E4A0',
                                          activeforeground='#A8E4A0', activebackground=nav_bar_color,
                                          text='Customer support', font=('Aptos Narrow', 10, 'bold'), relief="solid",
                                          anchor='w', borderwidth=0, border=0)
        Customer_support_link.place(relheight=0.04, relwidth=0.3, rely=0.72, relx=0.31)
        change_fg_OnHover(Customer_support_link, '#00AB66', '#A8E4A0')

        tk.Label(Forgot_password_widget, bg=nav_bar_color, fg='black', activebackground='#8A9A5B', text='Go to Login?',
                 font=('Aptos Narrow', 10), relief="solid", anchor='w', borderwidth=0, border=0).place(relheight=0.04,
                                                                                                       relwidth=0.2,
                                                                                                       rely=0.78,
                                                                                                       relx=0.1)
        Jump_to_login_link = tk.Button(Forgot_password_widget, bg=nav_bar_color, fg='#A8E4A0',
                                       activeforeground='#A8E4A0', activebackground=nav_bar_color, text='Login',
                                       font=('Aptos Narrow', 10, 'bold'), relief="solid", anchor='w', borderwidth=0,
                                       border=0, command=lambda: back(Forgot_password_widget))
        Jump_to_login_link.place(relheight=0.04, relwidth=0.3, rely=0.78, relx=0.31)
        change_fg_OnHover(Jump_to_login_link, '#00AB66', '#A8E4A0')
        return Forgot_password_widget

    tk.Label(Login_widget, text='Log in to your account', bg=nav_bar_color,
             font=("Bahnschrift SemiLight Condensed", 26), borderwidth=0, border=0).place(relheight=0.05, relwidth=0.25,
                                                                                          rely=0.05, relx=0.03)
    tk.Label(Login_widget, text='Log in to continue your therapy journey \ntowards a happier, healthier you.',
             bg=nav_bar_color, font=("Bahnschrift SemiLight Condensed", 12), borderwidth=0, border=0).place(
        relheight=0.051, relwidth=0.25, rely=0.11, relx=0.03)

    tk.Label(Login_widget, bg=nav_bar_color, text='email', font=("Batang", 9), anchor='w', borderwidth=0, border=0).place(relheight=0.03, relwidth=0.07, rely=0.18, relx=0.05)
    Email_entry_widg = tk.Entry(Login_widget, bg=nav_bar_color, font=("Courier New", 13), relief="solid", borderwidth=1)
    Email_entry_widg.place(relheight=0.07, relwidth=0.2, rely=0.21, relx=0.05)
    change_bg_OnHover(Email_entry_widg, '#F5F5F5', nav_bar_color)
    Email_entry_widg.insert(0, 'm@gmail')

    tk.Label(Login_widget, bg=nav_bar_color, text='password', font=("Batang", 9), anchor='w', borderwidth=1, border=1).place(relheight=0.03, relwidth=0.07, rely=0.3, relx=0.05)
    password_entry_widg = tk.Entry(Login_widget, bg=nav_bar_color, font=("Courier New", 13), relief="solid", borderwidth=1)
    password_entry_widg.place(relheight=0.07, relwidth=0.2, rely=0.33, relx=0.05)

    password_entry_widg.insert(0, '12maureen12')
    change_bg_OnHover(password_entry_widg, '#F5F5F5', nav_bar_color)

    Forgot_password_login_link = tk.Button(Login_widget, bg=nav_bar_color, fg='#74C365', activebackground=nav_bar_color, text='Forgot password', font=("Bradley Hand ITC", 12, 'bold'), anchor='w', borderwidth=0, border=0, command=lambda: Forgot_pass().place(relheight=0.7, relwidth=0.25, rely=0.05,
                                                                                                                                                                                                                                                                 relx=0.03))
    Forgot_password_login_link.place(relheight=0.03, relwidth=0.1, rely=0.41, relx=0.05)
    change_fg_OnHover(Forgot_password_login_link, '#00AB66', '#A8E4A0')

    login_btn = tk.Button(Login_widget, bg='#1C352D', fg='white', activebackground='#8A9A5B', text='LOGIN', font=("Aptos", 15, 'bold'), borderwidth=1, border=0, command=lambda: login_Request(Email_entry_widg.get(), password_entry_widg.get(), root_widget))
    login_btn.place(relheight=0.06, relwidth=0.2, rely=0.5, relx=0.05)
    change_bg_OnHover(login_btn, '#004830', '#1C352D')
    password_entry_widg.bind('<Return>', lambda e: login_Request(Email_entry_widg.get(), password_entry_widg.get(), root_widget))
    Email_entry_widg.bind('<Return>', lambda e: login_Request(Email_entry_widg.get(), password_entry_widg.get(), root_widget))

    tk.Label(Login_widget, bg=nav_bar_color, text="Don't have an account?", font=("Aptos Narrow", 10), anchor='w',
             borderwidth=0, border=0).place(relheight=0.03, relwidth=0.1, rely=0.6, relx=0.05)
    Sign_up_login_link = tk.Button(Login_widget, bg=nav_bar_color, fg='#A8E4A0', activeforeground='#A8E4A0',
                                   activebackground=nav_bar_color, text="Sign up", font=("Aptos Narrow", 11, 'bold'),
                                   anchor='w', borderwidth=0, border=0)
    Sign_up_login_link.place(relheight=0.03, relwidth=0.05, rely=0.6, relx=0.15)
    change_fg_OnHover(Sign_up_login_link, '#00AB66', '#A8E4A0')

    tk.Label(Login_widget, bg=nav_bar_color, text="Therapy Provider?", font=("Aptos Narrow", 10), anchor='w',
             borderwidth=0, border=0).place(relheight=0.03, relwidth=0.1, rely=0.65, relx=0.05)
    therapist_login_link = tk.Button(Login_widget, bg=nav_bar_color, fg='#A8E4A0', activeforeground='#A8E4A0',
                                     activebackground=nav_bar_color, text="Log in", font=("Aptos Narrow", 11, 'bold'),
                                     anchor='w', borderwidth=0, border=0)
    therapist_login_link.place(relheight=0.03, relwidth=0.05, rely=0.65, relx=0.15)
    change_fg_OnHover(therapist_login_link, '#00AB66', '#A8E4A0')

    img = tk.Label(Login_widget, bg=nav_bar_color, font=("Bahnschrift SemiLight Condensed", 26), borderwidth=0,
                   border=0)
    img.place(relheight=0.9, relwidth=0.65, rely=0.05, relx=0.3)
    # imagen('./login_pic.png', int(screen_width * 1 * 0.65), int(screen_height * 2 * 0.3 * 0.9), img)

    return Login_widget


def chat(widget):
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor
    global Recording_paused

    def font_change(widget1, widget2, widget3):
        global defalt_font_style, defalt_font_size, closed

        defalt_font_style = 'Times New Roman'
        defalt_font_size = 13

        def check(widget1=widget1, widget2=widget2, widget3=widget3):
            global defalt_font_style, defalt_font_size, closed
            while True:
                if closed:
                    break
                try:
                    font_style = widget1.get()
                    font_size = widget2.get()
                    if font_size == '':
                        font_size = '1'
                    if defalt_font_style != font_style.strip() or defalt_font_size != int(font_size):
                        try:
                            widget3.config(font=(font_style, font_size))
                            defalt_font_style = font_style.strip()
                            defalt_font_size = int(font_size)
                            print('changed')
                        except:
                            pass
                    time.sleep(1)
                except:
                    pass

        time.sleep(10)
        check()

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

    font_style_entry = tk.Entry(font_, bg=nav_bar_bg_color, fg=fg_color, relief=tk.GROOVE, font=("Times New Roman", 13), borderwidth=0, border=1)
    font_style_entry.place(relheight=0.8, relwidth=0.7, rely=0.1, relx=0)
    font_style_entry.insert(0, defalt_font_style)

    font_style_btn = tk.Button(font_, text='v', bg=nav_bar_bg_color, activebackground=nav_bar_bg_color, fg=fg_color, relief=tk.GROOVE, font=("Times New Roman", 13, 'bold'), borderwidth=0, border=1)
    font_style_btn.place(relheight=0.8, relwidth=0.09, rely=0.1, relx=0.7)

    font_size_entry = tk.Entry(font_, bg=nav_bar_bg_color, fg=fg_color, relief=tk.GROOVE, font=("Times New Roman", 11), borderwidth=0, border=1)
    font_size_entry.place(relheight=0.8, relwidth=0.19, rely=0.1, relx=0.8)
    font_size_entry.insert(0, defalt_font_size)

    # ======================================================================================================================================================================================================

    paned_window = tk.PanedWindow(chatbot_widget, bg=bg_color, orient=tk.VERTICAL, sashwidth=8, sashrelief=tk.FLAT)
    paned_window.place(relheight=0.96, relwidth=0.75, rely=0.03, relx=0.0253)

    t1 = tk.Text(paned_window, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, wrap="word", font=("Times New Roman", 13), borderwidth=2, border=1)  # t4.place(relheight=0.70, relwidth=0.75, rely=0.03, relx=0.0253)
    t1.tag_configure("ASR", foreground="gray")
    t2 = tk.Text(paned_window, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, wrap="word", font=("Times New Roman", 13), borderwidth=4, border=1)
    t2.tag_configure("error_config", foreground="#CD5C5C", justify=tk.LEFT)  # t2.place(relheight=0.25, relwidth=0.75, rely=0.74, relx=0.0253)
    t3 = tk.Text(paned_window, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, wrap="word", font=("Times New Roman", 13), borderwidth=4, border=1)

    paned_window.add(t1)
    paned_window.add(t2)
    paned_window.add(t3)

    threading.Thread(target=font_change, args=(font_style_entry, font_size_entry, t1,)).start()
    threading.Thread(target=font_change, args=(font_style_entry, font_size_entry, t2,)).start()
    threading.Thread(target=font_change, args=(font_style_entry, font_size_entry, t3,)).start()

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
        defalt_entities_list = [('Symptoms', 'STRING'), ('Diagnosis', 'STRING')]
        for i in defalt_entities_list:
            e_name, e_type, chk_var = add(fr2)
            e_name.insert(0, i[0])
            e_type.config(text=i[1])
            chk_var.set(False)

    custom_add(fr2)

    Add_new_entity = tk.Button(entity_section, text='+ Add new entity', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", 10), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: add(fr2))
    Add_new_entity.place(relheight=0.03, relwidth=0.4, rely=0.97, relx=0)
    change_fg_OnHover(Add_new_entity, 'red', fg_color)

    Record_btn = tk.Button(chatbot_widget, text='🎙', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", 25), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: RUN_OFFLINE_speech_recognition(t1, t2, t3, Record_btn, clock_lb))
    Record_btn.place(relheight=0.03, relwidth=0.02, rely=0.751, relx=0.78)

    play_pause_btn = tk.Button(chatbot_widget, text='⏯', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", 15), anchor='s', activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: set_recording_paused(play_pause_btn))
    play_pause_btn.place(relheight=0.03, relwidth=0.02, rely=0.751, relx=0.8)

    clock_lb = tk.Label(chatbot_widget, text='', fg=fg_color, font=("Bauhaus 93", 13), bg=bg_color, borderwidth=0, border=0)
    clock_lb.place(relheight=0.03, relwidth=0.06, rely=0.751, relx=0.82)

    download_audio_btn = tk.Button(chatbot_widget, text='⤓', fg=fg_color, activeforeground=fg_color, activebackground=bg_color, font=("Bauhaus 93", 22), bg=bg_color, borderwidth=0, border=0, command=lambda: download_transcribed_audio(download_audio_btn))
    download_audio_btn.place(relheight=0.03, relwidth=0.02, rely=0.751, relx=0.881)

    upload_audio_wid_btn = tk.Button(chatbot_widget, text='⤒', fg=fg_color, activeforeground=fg_color, activebackground=bg_color, font=("Georgia", 22), bg=bg_color, borderwidth=0, border=0, command=lambda: upload_audio_file(t1, upload_audio_wid_btn))
    upload_audio_wid_btn.place(relheight=0.03, relwidth=0.02, rely=0.751, relx=0.902)

    extract_wid = tk.Button(chatbot_widget, text='⎋ Extract', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", 10), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: Entity_Extraction(t2, t3))
    extract_wid.place(relheight=0.02, relwidth=0.04, rely=0.79, relx=0.78)
    change_fg_OnHover(extract_wid, 'red', fg_color)

    Summary_wid = tk.Button(chatbot_widget, text='≅Summarize', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", 10), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: D_Summary(t2, t3))
    Summary_wid.place(relheight=0.02, relwidth=0.041, rely=0.79, relx=0.821)
    change_fg_OnHover(Summary_wid, 'red', fg_color)

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


def profile(widget):
    global screen_width, screen_height, user_id, First_name, Second_Name, Last_Name, Email, user_Photo
    back_ground_color = "#F5FEFD"
    for_ground_color = "black"
    profile_widget = tk.Frame(widget, bg=back_ground_color, borderwidth=0, border=0)
    profile_widget.place(relheight=1, relwidth=1, rely=0, relx=0)

    user_profile_widget = tk.Label(profile_widget, bg=back_ground_color, fg=for_ground_color)
    user_profile_widget.place(relheight=0.11, relwidth=0.09, relx=0.02, rely=0.02)
    user_Photo = user_Photo[2:]
    user_Photo = user_Photo.encode('utf-8')  # Convert the content to bytes
    imagen(user_Photo, int(screen_width * 0.9747 * 0.09), int(screen_height * 0.96 * 0.11), user_profile_widget)

    tk.Label(profile_widget, text=f" {First_name} {Second_Name} {Last_Name}", bg=back_ground_color, fg=for_ground_color,
             anchor="w", font=("Calibri", 12)).place(relheight=0.03, relwidth=0.14, relx=0.111, rely=0.02)
    tk.Label(profile_widget, text=f" user_id:{user_id}", bg=back_ground_color, fg=for_ground_color, anchor="w",
             font=("Calibri", 13)).place(relheight=0.03, relwidth=0.14, relx=0.111, rely=0.06)

    return profile_widget


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

    input_widget_ = tk.Text(frame_view2, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, wrap="word", font=("Times New Roman", 13), borderwidth=2, border=1)
    input_widget_.place(relheight=0.05, relwidth=0.96, rely=0.945, relx=0.01)

    bng = tk.Button(frame_view2, text="▶", activebackground=bg_color, bg=bg_color, fg=fg_color, font=("Arial Black", 15), borderwidth=0, border=0, command=lambda: rag_chat(input_widget_, chat_display_widget, bng))
    bng.place(relheight=0.06, relwidth=0.02, rely=0.945, relx=0.973)

    return conversation_widget


def settings(widget):
    global gradient_ai_workspace_id, assemblyai_access_key, gradient_ai_access_key, gradient_ai_finetuned_id, gradient_ai_base_model_id, keys
    global root
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor, current_theme

    def save_keys(g_access, g_workkey, g_finetuned_id, g_base_model_id, Assemly_key):
        global gradient_ai_workspace_id, assemblyai_access_key, gradient_ai_access_key, keys, setting_status
        global llm_chain
        global bg_color, fg_color, fg_hovercolor, bg_hovercolor, current_theme, nav_bg
        setting_status = True
        gradient_ai_access_key = str(g_access).strip()
        gradient_ai_workspace_id = str(g_workkey).strip()
        gradient_ai_finetuned_id = str(g_finetuned_id).strip()
        gradient_ai_base_model_id = str(g_base_model_id).strip()

        assemblyai_access_key = str(Assemly_key).strip()

        dic = {
            '_GA_': gradient_ai_access_key,
            '_GW_': gradient_ai_workspace_id,
            '_G_FT_M_': gradient_ai_finetuned_id,
            '_G_B_M_': gradient_ai_base_model_id,
            '_AAI_': assemblyai_access_key,
            "bg_color": bg_color,
            "fg_color": fg_color,
            "fg_hovercolor": fg_hovercolor,
            "bg_hovercolor": bg_hovercolor,
            "current_theme": current_theme,
            "nav_bg": nav_bg
        }

        json_object = json.dumps(dic, indent=4)

        with open("keys.json", "w") as outfile:
            outfile.write(json_object)

        os.environ['GRADIENT_ACCESS_TOKEN'] = gradient_ai_access_key
        os.environ['GRADIENT_WORKSPACE_ID'] = gradient_ai_workspace_id

        print("saved")
        print("gradient_ai_access_key", gradient_ai_access_key)
        print("gradient_ai_workspace_id", gradient_ai_workspace_id)
        print("assemblyai_access_key", assemblyai_access_key)
        llm_chain = None
        rag_initialize()

    setting_widget = tk.Frame(widget, bg=bg_color, borderwidth=0, border=0)
    setting_widget.place(relheight=1, relwidth=1, rely=0, relx=0)

    # ======================================================= Section 1 ===========================================================================================================================================

    g1 = tk.Frame(setting_widget, bg=bg_color, relief=tk.RAISED, borderwidth=0, border=5)
    g1.place(relheight=0.4, relwidth=0.41, rely=0.02, relx=0.0253)

    # tk.Label(g1, bg='blue', fg=fg_color, borderwidth=7, border=7).place(relheight=1, relwidth=1, rely=0, relx=0)

    tk.Label(g1, text="GRADIENT AI ACCESS KEYS ", bg=bg_color, fg=fg_color, font=("Georgia", 12, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.6, rely=0, relx=0)

    tk.Label(g1, text="  GRADIENT_ACCESS_TOKEN :", bg=bg_color, fg=fg_color, font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.071, relx=0)
    gradient_access_widget = tk.Entry(g1, bg=bg_color, fg=fg_color, borderwidth=0, border=1, font=("Courier New", 10))
    gradient_access_widget.place(relheight=0.07, relwidth=0.74, rely=0.071, relx=0.25)
    gradient_access_widget.insert(0, gradient_ai_access_key)
    gradient_access_widget.bind('<Return>', lambda e: save_keys(gradient_access_widget.get(), gradient_work_widget.get(), gradient_finetuned_model_id.get(), gradient_base_model_id.get(), assembly_widget.get()))
    change_bg_OnHover(gradient_access_widget, bg_hovercolor, bg_color)

    tk.Label(g1, text="  GRADIENT_WORKSPACE_ID :", bg=bg_color, fg=fg_color, font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.142, relx=0)
    gradient_work_widget = tk.Entry(g1, bg=bg_color, fg=fg_color, borderwidth=0, border=1, font=("Courier New", 10))
    gradient_work_widget.place(relheight=0.07, relwidth=0.74, rely=0.142, relx=0.25)
    gradient_work_widget.insert(0, gradient_ai_workspace_id)
    gradient_work_widget.bind('<Return>', lambda e: save_keys(gradient_access_widget.get(), gradient_work_widget.get(), gradient_finetuned_model_id.get(), gradient_base_model_id.get(), assembly_widget.get()))
    change_bg_OnHover(gradient_work_widget, bg_hovercolor, bg_color)

    tk.Label(g1, text="  NLP_adapter_id :", bg=bg_color, fg=fg_color, font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.213, relx=0)
    gradient_finetuned_model_id = tk.Entry(g1, bg=bg_color, fg=fg_color, borderwidth=0, border=1, font=("Courier New", 10))
    gradient_finetuned_model_id.place(relheight=0.07, relwidth=0.74, rely=0.213, relx=0.25)
    gradient_finetuned_model_id.insert(0, gradient_ai_finetuned_id)
    gradient_finetuned_model_id.bind('<Return>', lambda e: save_keys(gradient_access_widget.get(), gradient_work_widget.get(), gradient_finetuned_model_id.get(), gradient_base_model_id.get(), assembly_widget.get()))
    change_bg_OnHover(gradient_finetuned_model_id, bg_hovercolor, bg_color)

    tk.Label(g1, text="  Base_Model :", bg=bg_color, fg=fg_color, font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.284, relx=0)
    gradient_base_model_id = tk.Entry(g1, bg=bg_color, fg=fg_color, borderwidth=0, border=1, font=("Courier New", 10))
    gradient_base_model_id.place(relheight=0.07, relwidth=0.74, rely=0.284, relx=0.25)
    gradient_base_model_id.insert(0, gradient_ai_base_model_id)
    gradient_base_model_id.bind('<Return>', lambda e: save_keys(gradient_access_widget.get(), gradient_work_widget.get(), gradient_finetuned_model_id.get(), gradient_base_model_id.get(), assembly_widget.get()))
    change_bg_OnHover(gradient_base_model_id, bg_hovercolor, bg_color)

    tk.Label(g1, text="ASSEMBLY-AI  ", bg=bg_color, fg=fg_color, font=("Georgia", 12, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.6, rely=0.363, relx=0)
    tk.Label(g1, text="  assemblyai access key:", bg=bg_color, fg=fg_color, font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.432, relx=0)
    assembly_widget = tk.Entry(g1, bg=bg_color, fg=fg_color, borderwidth=0, border=1, font=("Courier New", 10))
    assembly_widget.place(relheight=0.07, relwidth=0.74, rely=0.432, relx=0.25)
    assembly_widget.insert(0, assemblyai_access_key)
    assembly_widget.bind('<Return>', lambda e: save_keys(gradient_access_widget.get(), gradient_work_widget.get(), gradient_finetuned_model_id.get(), gradient_base_model_id.get(), assembly_widget.get()))
    change_bg_OnHover(assembly_widget, bg_hovercolor, bg_color)

    save = tk.Button(g1, text="save ", bg=bg_color, fg=fg_color, font=("Calibri", 12, 'bold'), activebackground=bg_color, activeforeground=fg_hovercolor, borderwidth=0, border=0, command=lambda: save_keys(gradient_access_widget.get(), gradient_work_widget.get(), gradient_finetuned_model_id.get(), gradient_base_model_id.get(), assembly_widget.get()))
    save.place(relheight=0.05, relwidth=0.07, rely=0.94, relx=0.92)
    # change_bg_OnHover(save, 'lightgreen', bg_color)
    change_fg_OnHover(save, fg_hovercolor, fg_color)

    # ======================================================= Section 2 ===========================================================================================================================================

    g2 = tk.Frame(setting_widget, bg=bg_color, relief=tk.RAISED, borderwidth=0, border=5)
    g2.place(relheight=0.4, relwidth=0.41, rely=0.5, relx=0.0253)

    tk.Label(g2, text="PERSONALIZATION ", bg=bg_color, fg=fg_color, font=("Georgia", 12, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.6, rely=0, relx=0)
    tk.Label(g2, text="  current theme :", bg=bg_color, fg=fg_color, font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.071, relx=0)
    themes_change = tk.Button(g2, text=current_theme, bg=bg_color, fg=fg_color, borderwidth=0, border=0, font=("Courier New", 10), command=lambda: change_color(root, themes_change))
    themes_change.place(relheight=0.07, relwidth=0.3, rely=0.071, relx=0.25)
    change_fg_OnHover(themes_change, fg_hovercolor, fg_color)

    # ======================================================= Section 3 ===========================================================================================================================================
    g3 = tk.Frame(setting_widget, bg=bg_color, relief=tk.RAISED, borderwidth=0, border=5)
    g3.place(relheight=0.4, relwidth=0.41, rely=0.02, relx=0.5)

    # ======================================================= Section 4 ===========================================================================================================================================
    g4 = tk.Frame(setting_widget, bg=bg_color, relief=tk.RAISED, borderwidth=0, border=5)
    g4.place(relheight=0.4, relwidth=0.41, rely=0.5, relx=0.5)
    # ======================================================= Section 5 ===========================================================================================================================================

    return setting_widget


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

    Display_text_ = tk.Text(Clinical_widg_page, bg=bg_color, fg=fg_color, font=("Georgia", 12))
    Display_text_.place(relheight=0.3, relwidth=1, rely=0.62, relx=0)

    clinical_Note_upload_btn = tk.Button(Clinical_widg_page, text="clinical Note+", command=lambda: image_text_extract_Handwriten(display_img, Display_text_))
    clinical_Note_upload_btn.place(relheight=0.02, relwidth=0.05, rely=0, relx=0.)
    tk.Button(Clinical_widg_page, text="Change View", command=lambda: Analyzed_Output_(display_img)).place(relheight=0.02, relwidth=0.05, rely=0, relx=0.05)
    tk.Button(Clinical_widg_page, text="Clear", command=lambda: clear_dd(display_img, Display_text_)).place(relheight=0.02, relwidth=0.05, rely=0, relx=0.1)

    return Clinical_widg_page


def Recodes_Page(widget):
    global bg_color, fg_color, screen_height, screen_width
    global active_sound_widget_file, active_sound_widget, font_size

    active_sound_widget_file = None
    active_sound_widget = None

    Recodes_Page = tk.Frame(widget, bg=bg_color, borderwidth=0, border=0)
    Recodes_Page.place(relheight=1, relwidth=1, rely=0, relx=0)


    #def sound_play_stop(play_widget, pause_widget, stop_widget, file_name):


    def audio_recodings(frame_widget, cavas_widget):
        global font_size, screen_height, bg_color, fg_color
        global active_sound_widget_file


        def create_audio_widget(audio_file):
             global playing, active_sound_widget_file

             playing = 0

             def Play_Recoding(file_path, widget):
                global playing, active_sound_widget_file, active_sound_widget

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
                elif playing == 1 :
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


             audio_file_path = folder_path + "/" + audio_file

             audio_wid = tk.Frame(frame_widget, bg=bg_color, height=int((screen_height - 20) * 0.9 * 0.05), highlightbackground=fg_color, highlightthickness=0, borderwidth=0, border=0)

             audio_Lable = tk.Label(audio_wid, text="  "+audio_file, bg=bg_color, fg=fg_color,  anchor=tk.W, font=("Calibri", font_size-2, 'italic'), borderwidth=0, border=0)
             audio_Lable.place(relheight=1, relwidth=0.7, rely=0, relx=0.)
             audio_play_btn = tk.Button(audio_wid, text="▶", bg=bg_color, fg=fg_color, activeforeground=fg_color, activebackground=bg_color, command=lambda k = audio_file_path: Play_Recoding(k, audio_play_btn), font=("Arial Rounded MT Bold", font_size), borderwidth=0, border=0)
             audio_play_btn.place(relheight=1, relwidth=0.1, rely=0, relx=0.7)
             audio_download_btn = tk.Button(audio_wid, text="⍊", bg=bg_color, fg=fg_color, activeforeground=fg_color, activebackground=bg_color, command=lambda: stop(), font=("Arial Rounded MT Bold", font_size), borderwidth=0, border=0)
             audio_download_btn.place(relheight=1, relwidth=0.1, rely=0, relx=0.8)
             audio_push_btn = tk.Button(audio_wid, text="⌥", bg=bg_color, fg=fg_color, activeforeground=fg_color, activebackground=bg_color, font=("Arial Rounded MT Bold", font_size), borderwidth=0, border=0)
             audio_push_btn.place(relheight=1, relwidth=0.1, rely=0, relx=0.9)

             audio_wid.pack(expand=True, fill=tk.X)  # .place(rel height=0.04, relwidth=1, rely=rely, relx=0)
             audio_wid.bind("<MouseWheel>", lambda e: cavas_widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))
             audio_Lable.bind("<MouseWheel>", lambda e: cavas_widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))
             audio_play_btn.bind("<MouseWheel>", lambda e: cavas_widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))
             audio_download_btn.bind("<MouseWheel>", lambda e: cavas_widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))
             audio_push_btn.bind("<MouseWheel>", lambda e: cavas_widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))


        folder_path = r"C:\Users\HEZRON WEKESA\OneDrive\Music"
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

    tk.Label(Recodes_Page, text="Conversations Recordings", bg=bg_color,  fg=fg_color, font=("Book Antiqua", font_size, 'bold'), anchor=tk.SW, borderwidth=0, border=0).place(relheight=0.05, relwidth=0.3, rely=0, relx=0.02)
    Audio_recodes_frame = tk.Frame(Recodes_Page, bg=bg_color, borderwidth=0,  highlightbackground=fg_color, highlightthickness=0.5, border=0)
    Audio_recodes_frame.place(relheight=0.9, relwidth=0.3, rely=0.05, relx=0.02)
    Audio_recodes_canvas = tk.Canvas(Audio_recodes_frame,  highlightthickness=0, bg=bg_color, borderwidth=0, border=0)
    Audio_recodes_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(Audio_recodes_frame, orient=tk.VERTICAL)
    Audio_recodes_canvas.configure(yscrollcommand=scrollbar.set)
    frame = tk.Frame(Audio_recodes_canvas, bg=bg_color,  borderwidth=0, border=0)
    Audio_recodes_canvas.create_window((0, 0), window=frame, width=int(screen_width * 0.9747 * 0.3), anchor=tk.NW)
    Audio_recodes_canvas.bind("<MouseWheel>", lambda e: Audio_recodes_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    audio_recodings(frame, Audio_recodes_canvas)

    x = tk.Frame(Recodes_Page, bg=bg_color, borderwidth=0, highlightbackground=fg_color, highlightthickness=0.5, border=0)
    x.place(relheight=0.9, relwidth=0.64, rely=0.05, relx=0.35)

    x2 = tk.Text(x, bg=bg_color, borderwidth=0, highlightbackground=fg_color, highlightthickness=0.5, border=0)
    x2.place(relheight=0.5, relwidth=1, rely=0, relx=0)



    return Recodes_Page


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

    CALL_Widget = call(container2)
    SETTINGS_Widget = settings(container2)
    chat_me_Widget = chat_me(container2)
    CHAT_Widget = chat(container2)
    rag_widget = RAG_page(container2)
    img_extract = Clinical_Image(container2)
    patient_recods = Recodes_Page(container2)

    # sidebar  widgets ------------------------------------------------------------------------------------------------------------------------------------

    def active(widget):
        global side_bar_widget_list, fg_hovercolor, nav_bg, bg_color
        for i in side_bar_widget_list:
            if i != widget:
                i.config(bg=nav_bg, relief=tk.FLAT, border=0, fg=fg_color)
            else:
                i.config(bg=nav_bg, relief=tk.FLAT, border=0, fg="red")

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

    st1_bt = tk.Button(side_bar, bg=nav_bg, activebackground=bg_color, activeforeground=fg_color, text='-', font=("Calibri", font_size), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (CALL_Widget.tkraise(), active(st1_bt)))
    st1_bt.place(relheight=0.03, relwidth=1, rely=0.05, relx=0)
    change_bg_OnHover_light(st1_bt)
    side_bar_widget_list.append(st1_bt)
    duplicate_widget(st1_bt, side_bar_full, text="Digital Scribe")

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

    st6_bt = tk.Button(side_bar, bg=nav_bg, activebackground=bg_color, activeforeground=fg_color, text='-', font=("Calibri", font_size), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (patient_recods.tkraise(), active(st6_bt)))
    st6_bt.place(relheight=0.03, relwidth=1, rely=0.25, relx=0)
    change_bg_OnHover_light(st6_bt)
    side_bar_widget_list.append(st6_bt)
    duplicate_widget(st6_bt, side_bar_full, text="Patient Records")

    st7_bt = tk.Button(side_bar, bg=nav_bg, activebackground=bg_color, activeforeground=fg_color, text='-', font=("Calibri", font_size), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (rag_widget.tkraise(), active(st7_bt)))
    st7_bt.place(relheight=0.03, relwidth=1, rely=0.93, relx=0)
    change_bg_OnHover_light(st7_bt)
    side_bar_widget_list.append(st7_bt)
    duplicate_widget(st7_bt, side_bar_full, text="Billing & Reimbursement")

    st8_bt = tk.Button(side_bar, bg=nav_bg, activebackground=bg_color, activeforeground=fg_color, text='≣', font=("Calibri", font_size), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (SETTINGS_Widget.tkraise(), active(st8_bt)))
    st8_bt.place(relheight=0.03, relwidth=1, rely=0.97, relx=0)
    change_bg_OnHover_light(st8_bt)
    side_bar_widget_list.append(st8_bt)
    duplicate_widget(st8_bt, side_bar_full, text="Settings")

    CHAT_Widget.tkraise()
    active(st2_bt)

    return container2


def Welcome_Page(wiget):
    global screen_width, screen_height
    home_widget, welcome_page_root = attach_scroll(wiget)

    large_frame_size = screen_height * 2
    welcome_page_frame = tk.Frame(home_widget, bg='gray', width=screen_width, height=large_frame_size)
    welcome_page_frame.pack(fill=tk.BOTH, expand=True)

    App_title = "Digital ScriBe"
    nav_bar_color = "white"
    nav_bar_btn_hover_color = '#F5F5F5'

    nav_bar = tk.Frame(welcome_page_frame, bg=nav_bar_color)
    nav_bar.place(relheight=0.02, relwidth=1, rely=0, relx=0)

    nav_bar_title_widget = tk.Label(nav_bar, bg=nav_bar_color, text=App_title, justify=tk.LEFT, anchor="w", font=("Forte", 20), borderwidth=0, border=0)
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

    nav_bar_bt4_widget = tk.Button(nav_bar, bg=nav_bar_color, text='Log in ∨', justify=tk.LEFT, anchor="center",
                                   font=("Calibri", 12), borderwidth=0, border=0)
    nav_bar_bt4_widget.place(relheight=0.6, relwidth=0.05, rely=0.2, relx=0.87)
    change_Widget_Attribute_OnHover(nav_bar_bt4_widget, 'Log in ∧', 'Log in ∨', nav_bar_btn_hover_color, nav_bar_color,
                                    Login_Section_widget(welcome_page_frame, welcome_page_root))

    nav_bar_bt5_widget = tk.Button(nav_bar, bg=nav_bar_color, text='Get started', justify=tk.LEFT, anchor="center",
                                   font=("Calibri", 12), borderwidth=0, border=0)
    nav_bar_bt5_widget.place(relheight=0.6, relwidth=0.06, rely=0.2, relx=0.935)


# =============================== Main Function definition ============================================================
# =====================================================================================================================

def resize(widget, width, heigh):
    global root, screen_width, screen_height

    # Prevent resizing by setting the widget's size to its original size
    widget.config(width=width, height=heigh)
    print("resized")


def on_closing():
    global root, closed, httpd
    print("clossing")
    closed = True
    httpd.shutdown()
    httpd.server_close()
    root.destroy()

    #time.sleep(2)
    """
    while True:
        time.sleep(10)
        for thread in threading.enumerate():
            print("- ", thread.name)
    """
    sys.exit()


def main():
    global root, screen_width, screen_height, session, client_socket, server_IP4v_address, Server_listening_port
    global user_id, user_Photo, First_name, Second_Name, Last_Name, Email
    global gradient_ai_workspace_id, assemblyai_access_key, gradient_ai_access_key, keys
    global bg_color
    print("main started")

    access_keys_info()
    run_server()

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

    title_bar_color(bg_color)

    User_Home_page(root)
    # Welcome_Page(root)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


def go():
    try:
        main()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
    """
    t = System_Thread(ThreadStart(go))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()
    """
