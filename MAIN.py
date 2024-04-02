# ============================================= Used libraries ==========================================================================================

import base64
import hashlib
import time
import socket
import tkinter as tk
import ctypes as ct
import threading
from PIL import Image, ImageTk
import shelve
import io
import base64
import os
import json
import whisper

from gradientai import Gradient, SummarizeParamsLength, ExtractParamsSchemaValueType
from tkinter import filedialog
from tkinter import ttk
import docx
import ctypes
# ------------------------------
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
import whisper

# =============================== Global variable decoration  ============================================================================================
root = None
screen_width: int
screen_height: int

session = None
closed = False
user_id = None

First_name = None
Second_Name = None
Last_Name = None
Email = None
user_Photo = None
widget_list: list = []
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
Home_page_frame = None
setting_status = False
rag_data = None
rag_widget = None
sammary_data = None
Recording = False
Recording_paused = False
Recording_data = 0
audio_frames = None
# =============================== Functions definition ============================================================================================
# ================================= Themes ================================================================================================================

def title_bar_color( color):
    # import ctypes as ct
    global root
    root.update()
    if color.startswith('#'):
        blue = color[5:7]
        green = color[3:5]
        red = color[1:3]
        color = blue  + green + red
    else:
        blue = color[4:6]
        green = color[2:4]
        red = color[0:2]
        color = blue  + green + red
    print(color)
    get_parent = ct.windll.user32.GetParent
    HWND = get_parent(root.winfo_id())

    color = '0x' + color
    color = int(color, 16)

    ct.windll.dwmapi.DwmSetWindowAttribute(HWND, 35, ct.byref(ct.c_int(color)), ct.sizeof(ct.c_int))


def change_color(widget, button):
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor, current_theme
    button_text = button.cget("text")

    if button_text == 'window(light)':
        button.config(text='window(dark)')
        bg_color = '#353839'
        fg_color = 'white'
        current_theme = 'window(dark)'
        title_bar_color(bg_color)

    elif button_text == 'window(dark)':
        button.config(text='window(dark_blue)')
        bg_color = '#36454F'
        fg_color = 'white'
        current_theme = 'window(dark_blue)'
        title_bar_color(bg_color)
    elif button_text == 'window(dark_blue)':
        button.config(text='window(Blackberry)')
        bg_color = '#3A3A38'
        fg_color = 'white'
        current_theme = 'window(Blackberry)'
        title_bar_color(bg_color)
    elif button_text == 'window(Blackberry)':
        button.config(text='window(dark_green)')
        bg_color = '#555D50'
        fg_color = 'white'
        current_theme = 'window(dark_green)'
        title_bar_color(bg_color)
    elif button_text == 'window(dark_green)':
        button.config(text='window(Jacket)')
        bg_color = '#253529'
        fg_color = 'white'
        current_theme = 'window(Jacket)'
        title_bar_color(bg_color)

    elif button_text == 'window(Jacket)':
        button.config(text='window(light)')
        bg_color = '#FFFFFF'
        fg_color = 'black'
        current_theme = 'window(light)'
        title_bar_color(bg_color)
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
            "current_theme": current_theme
        }

        json_object = json.dumps(dic, indent=4)

        with open("keys.json", "w") as outfile:
            outfile.write(json_object)

    threading.Thread(target=change_all).start()


# ============================================= NLP  ==========================================================================================

def Entity_Extraction(document_widget, entity_list, widget, loop=False):
    def run(document_widget=document_widget, entity_list=entity_list, widget=widget, loop=loop):
        global Recording, Recording_paused
        mygradient = Gradient()

        while True:
            document = document_widget.get("1.0", "end")
            if len(document) < 500:
                time.sleep(5)
                continue
            if Recording_paused:
                print('entity_paused')
                continue
            if closed :
                break
            document = (document.strip())
            schema = '{'
            for i in entity_list:
                schema += '"' + i[1].get() + '": { "type": ExtractParamsSchemaValueType.' + str(i[2].cget("text")) + ', "required": ' + str(i[3].get())+ ', }, '
            schema += '}'
            dictionary = eval(schema)
            try:
                result = mygradient.extract(
                    document=document,
                    schema_=dictionary,
                )
                widget.config(state=tk.NORMAL)
                widget.delete(1.0, tk.END)
                for key, value in result["entity"].items():
                    m = key + " : " + value + "\n"
                    print()
                    widget.insert(tk.END, m)

                widget.config(state=tk.DISABLED)

            except Exception as e:
                print(type(e).__name__)
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

            if not loop:
                print("loop break")
                break
            else:
                if not Recording:
                    break
            time.sleep(10)


    threading.Thread(target=run).start()

def D_Summary(widget1, widget, loop=False):
    def run_f(widget1= widget1, widget = widget, loop=loop):
        global Recording, Recording_paused
        gradient = Gradient()
        while True:

                document = widget1.get("1.0", "end")
                document = (document.strip())


                if len(document) < 500:
                    time.sleep(5)
                    continue
                if Recording_paused:

                    continue
                if closed:
                    break

                try:
                    summary_length = SummarizeParamsLength.LONG
                    result = gradient.summarize(
                        document=document,
                        length=summary_length
                    )
                    widget.config(state=tk.NORMAL)
                    widget.delete(1.0, tk.END)

                    widget.insert(tk.END, result['summary'])
                    widget.config(state=tk.DISABLED)

                    print(" Summary result :", result['summary'])
                except Exception as e:
                    print(e)

                if not loop:
                    break
                else:
                    if not Recording:
                        break

    threading.Thread(target=run_f).start()


def rag_initialize(data = None, widget = None):
    global rag_pipeline, rag_data, rag_widget
    rag_pipeline = None

    if rag_widget == None or rag_data == None:
        return

    if data == None:
        data = rag_data
    if widget == None:
        widget = rag_widget

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
        widget.config(fg='green')
    except:
        widget.config(fg='red')
        rag_pipeline = None
        return


def rag_chat(question, widget, widget1):
    global rag_pipeline
    def run_function(question = question , widget = widget, widget1 = widget1):
        widget1.config(text='▫▫▫▫')
        question = question.strip()
        if question == '' or rag_pipeline == None:
            widget1.config(text='▶')
            return


        widget.config(state=tk.NORMAL)
        widget.insert(tk.END, f" {question}\n", 'user_config')
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
            widget.insert(tk.END, f'{result["answer_builder"]["answers"][0].data}\n\n\n', 'llm_config')
            widget.see(tk.END)  # Scroll to the end of the text widget
            widget.config(state=tk.DISABLED)
            widget1.config(text='▶')
            # return result["answer_builder"]["answers"][0].data
        except Exception as e:
            widget.config(state=tk.NORMAL)
            widget.insert(tk.END, f'ERROR: PLEASE UPLOAD FILE FIRST \n\n\n', 'error_config')
            widget1.config(text='▶')
            widget.config(state=tk.DISABLED)

            print(f"UPLOAD ERROR\n {e}")

    threading.Thread(target=run_function).start()


def Upload_file(widget, widget2):
    global rag_data, rag_widget
    widget2.config(fg='black')
    file_path = filedialog.askopenfilename()

    if file_path:
        widget.config(state=tk.NORMAL)
        widget.delete(1.0, tk.END)
        document = docx.Document(file_path)
        data = ""
        for paragraph in document.paragraphs:
            data += paragraph.text + "\n"
            if paragraph.style.name == 'List Paragraph':

                widget.insert(tk.END, f"\t •{paragraph.text}")
            elif paragraph.style.name == 'Normal':
                widget.insert(tk.END, f"{paragraph.text} \n")

        widget.config(state=tk.DISABLED)
        rag_data = data
        rag_widget = widget2
        threading.Thread(target=rag_initialize, args=(data, widget2,)).start()




    else:
        print("No file selected")


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

    template2 ="""Rewite the conversation with correct grammar
                conversation: "{conversation}"
                Chatbot:"""

    prompt2 = PromptTemplate(template=template2, input_variables=["conversation"])
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
    vosk_model = Model(model_name="vosk-model-en-us-0.22")

    wisper_model_tiny= whisper.load_model("tiny")
    wisper_model_base = whisper.load_model("base")


threading.Thread(target=Initialize_VOSK).start()


def conversation_grammar(widget, widget1):
    global llm_chain2, recording_data
    if llm_chain2 is None:
        llm_inference_initializ()
    Question = widget.get(1.0, tk.END)
    Answer = llm_chain2.invoke(input=f"{Question}")

    widget1.delete(1.0, tk.END)
    widget1.insert(tk.END, f"{Answer['text']}")
    pass


def RUN_OFFLINE_speech_recognition(widget, widget1=None, Record_btn=None, clock_wideth=None):
    global closed, Recording, Recording_paused, Recording_data, vosk_model
    global fg_color, bg_color, miniute, second, hour
    global audio_frames
    if Recording:
        miniute = second = hour = 0
        Recording = False
        Record_btn.config(fg=fg_color)
        clock_wideth.config(text='0:0:0')
        return

    def start_recording():
        global Recording
        messages.put(True)
        print("Starting...")
        Recording = True
        Record_btn.config(fg="green")

        record = Thread(target=record_microphone)
        record.start()

        transcribe = Thread(target=speech_recognition, args=(widget,))
        transcribe.start()

    def record_microphone(chunk=1024, RECORD_SECONDS=1):
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
                print('record_microphone closed')
                break
            if Recording == False:
                break
            if Recording_paused:
                continue

            data = stream.read(chunk)
            frames.append(data)
            if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
                recordings.put(frames.copy())
                frames = []

        stream.stop_stream()
        stream.close()
        p.terminate()

    import wave
    output_file = 'output.wav'

    def speech_recognition(widget=widget):
        global closed, Recording_data, Recording_paused, Recording, audio_frames
        print("scanning")
        audio_frames = []
        while not messages.empty():
            if closed :
                print('speech_recognition closed')
                break
            if Recording == False:
                break
            if Recording_paused:
                print('  paused')
                continue
            try:
                frames = recordings.get()
                audio_frames.extend(frames)
                rec.AcceptWaveform(b''.join(frames))
                result = rec.Result()
                text = json.loads(result)["text"]
                if text == "the" or text == "" :
                    continue
                #Recording_data += text
    
                #widget.config(state=tk.NORMAL)
                widget.insert(tk.END, f" {text}")
                widget.see(tk.END)
                #widget.config(state=tk.DISABLED)

                info = widget.get('1.0', tk.END)
                info = len(info)

                if widget1 is not None:
                    if info > 1000:
                       text = grammar(frames)
                       widget1.insert(tk.END, f" {text}")

                # cased = subprocess.check_output('python recasepunc/recasepunc.py predict recasepunc/checkpoint', shell=True, text=True, input=text)
                # output.append_stdout(cased)
                # time.sleep(1)
            except:
                continue

    def grammar(frames):
        global wisper_model_tiny
        # Define audio parameters
        import wave
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


    while True:
        if vosk_model == None:
            continue
        messages = Queue()
        recordings = Queue()
        FRAME_RATE = 16000
        # vosk_model = Model(model_name="vosk-model-en-us-0.22")
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


def access_keys_info():
    global gradient_ai_workspace_id, assemblyai_access_key, gradient_ai_access_key, gradient_ai_finetuned_id, gradient_ai_base_model_id, keys
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor, current_theme
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

            print('gradient_ai_workspace_id :', gradient_ai_workspace_id)
            print('gradient_ai_access_key:', gradient_ai_access_key)
            print('assemblyai_access_key :', assemblyai_access_key)

            os.environ['GRADIENT_ACCESS_TOKEN'] = gradient_ai_access_key
            os.environ['GRADIENT_WORKSPACE_ID'] = gradient_ai_workspace_id

            print(bg_color)

    except Exception as e:
        print("access_keys_info Function:", e)
        pass


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def show(widg):
    widg.place(relheight=0.3, relwidth=1, rely=0.02, relx=0)


def hide(widg):
    def enter():
        widg.after_cancel(id)

    def leave():
        widg.place_forget()
        return

    id = widg.after(300, widg.place_forget)
    widg.bind("<Enter>", func=lambda e: enter())
    widg.bind("<Leave>", func=lambda e: leave())


def change_Widget_Attribute_OnHover(widget, Text_On_Hover, Text_On_Leave, colorOnHover, colorOnLeave, function):  # Color change bg on Mouse Hover
    widget.bind("<Enter>", func=lambda e: (widget.config(text=Text_On_Hover, background=colorOnHover), show(function)))
    widget.bind("<Leave>", func=lambda e: (widget.config(text=Text_On_Leave, background=colorOnLeave), hide(function)))


def change_bg_OnHover(widget, colorOnHover, colorOnLeave):  # Color change bg on Mouse Hover
    global bg_color
    widget.bind("<Enter>", func=lambda e: widget.config(background=colorOnHover))
    widget.bind("<Leave>", func=lambda e: widget.config(background=bg_color))


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
    chatbot_widget.place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253)

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
    
    t1 = tk.Text(paned_window, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, font=("Times New Roman", 13), borderwidth=2, border=5)
    #t1.place(relheight=0.70, relwidth=0.75, rely=0.03, relx=0.0253)

    t2 = tk.Text(paned_window, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, font=("Times New Roman", 13), borderwidth=4, border=1)
    t2.tag_configure("error_config", foreground="#CD5C5C", justify=tk.LEFT)
    #t2.place(relheight=0.25, relwidth=0.75, rely=0.74, relx=0.0253)


    t3 = tk.Text(paned_window, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, font=("Times New Roman", 13), borderwidth=4, border=1)


    paned_window.add(t1)
    paned_window.add(t3)
    paned_window.add(t2)

    threading.Thread(target=font_change, args=(font_style_entry, font_size_entry, t1,)).start()
    threading.Thread(target=font_change, args=(font_style_entry, font_size_entry, t2,)).start()

    entity_section = tk.Frame(chatbot_widget, bg='brown', borderwidth=0, border=0)
    entity_section.place(relheight=0.72, relwidth=0.21, rely=0.03, relx=0.78)

    title = tk.Frame(entity_section, bg=bg_color, borderwidth=2, border=1)
    title.place(relheight=0.036, relwidth=1, rely=0, relx=0)
    tk.Label(title, text="Field Name", bg=bg_color, fg=fg_color, borderwidth=0, border=0, font=("Georgia", 11, 'bold')).place(relx=0.01, rely=0.04, relwidth=0.5, relheight=1)
    tk.Label(title, text="Type", bg=bg_color,fg=fg_color, borderwidth=0, border=0, font=("Georgia", 11, 'bold')).place(relx=0.52, rely=0.04, relwidth=0.2, relheight=1)

    fr = tk.Frame(entity_section, bg=bg_color, borderwidth=0, border=0)
    fr.place(relheight=0.97, relwidth=1, rely=0.036, relx=0)
    user_page_widget, user_page_canvas = attach_scroll(fr, bg_color)
    fr2 = tk.Frame(user_page_widget, bg=bg_color, borderwidth=0, border=0, height=4000, width=int(screen_width * 0.9747 * 0.21))
    fr2.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    global entity_widget_lists
    entity_widget_lists = []

    def add(widget):
        global entity_type, entity_widget_lists
        entity_type = "STRING"

        def delet_widget(widget):
            widget.destroy()
            for i in entity_widget_lists:
                if i[0] == widget:
                    entity_widget_lists.remove(i)

        def change_type(widget):
            global entity_type
            if entity_type == "STRING":
                entity_type = "NUMBER"
                widget.config(text=entity_type)
            elif entity_type == "NUMBER":
                entity_type = "BOOLEAN"
                widget.config(text=entity_type)
            else:
                entity_type = "STRING"
                widget.config(text=entity_type)

        #style = ttk.Style()
        #style.configure("Custom.TCheckbutton", background=bg_color, foreground="blue")
        chk_var = tk.BooleanVar(value=False)

        new_entity = tk.Frame(widget, bg=bg_color, borderwidth=2, border=1, height=50, width=int(screen_width * 0.9747 * 0.21 - 3))
        new_entity.pack(side=tk.TOP, fill=tk.X)

        entity_name = tk.Entry(new_entity, bg=bg_color, fg=fg_color, borderwidth=0, border=1, font=("Times New Roman", 11))
        entity_name.place(relx=0.01, rely=0, relwidth=0.5, relheight=0.9)
        entity_type = tk.Button(new_entity, bg=bg_color, fg=fg_color, text=entity_type, font=("Times New Roman", 10, 'bold'), relief=tk.SUNKEN, activebackground=bg_color, borderwidth=0, border=1, command=lambda: change_type(entity_type))
        entity_type.place(relx=0.52, rely=0, relwidth=0.2, relheight=0.9)
        entity_requred = tk.Checkbutton(new_entity,  background=bg_color, activebackground=bg_color, variable=chk_var, onvalue=True, offvalue=False)
        entity_requred.place(relx=0.8,  rely=0, relwidth=0.1, relheight=1)
        close_widg = tk.Button(new_entity, bg=bg_color, fg=fg_color, activebackground=bg_color, text="X", borderwidth=0, border=0, font=("Bauhaus 93", 10), command=lambda: delet_widget(new_entity))
        close_widg.place(relx=0.95, rely=0, relwidth=0.05, relheight=1)
        change_fg_OnHover(close_widg, 'red', 'black')

        new_entity.bind("<MouseWheel>", lambda e: on_mouse_wheel(user_page_canvas, e))
        children = new_entity.winfo_children()
        for child in children:
            child.bind("<MouseWheel>", lambda e: on_mouse_wheel(user_page_canvas, e))


        entity_widget_lists.append((new_entity, entity_name, entity_type, chk_var))

        return entity_name, entity_type, chk_var

    def custom_add(widget):
            defalt_entities_list = [('Symptoms', 'STRING'), ('Disease', 'STRING'), ('Treatment', 'STRING'), ('Treatment', 'STRING'), ('Diagnosis', 'STRING'), ('Medication', 'STRING')
                , ('Medical History', 'STRING'), ('Docter Name', 'STRING'), ('Patient Name', 'STRING'), ('Treatment Plan', 'STRING'), ('Allergy', 'STRING'), ('Vitals', 'STRING'), ('Lifestyle', 'STRING'), ('Patient Concerns', 'STRING')]
            for i in defalt_entities_list:
                e_name, e_type, chk_var = add(fr2)
                e_name.insert(0, i[0])
                e_type.config(text= i[1])
                chk_var.set(False)

    custom_add(fr2)

    Add_new_entity = tk.Button(entity_section, text='+ Add new entity', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", 10), activebackground=bg_color, bg='blue', borderwidth=0, border=0, command=lambda: add(fr2))
    Add_new_entity.place(relheight=0.03, relwidth=0.4, rely=0.97, relx=0)
    change_fg_OnHover(Add_new_entity, 'red', fg_color)

    Record_btn = tk.Button(chatbot_widget, text='🎙', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", 25), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: (RUN_OFFLINE_speech_recognition(t1, t3, Record_btn, clock_lb),  Entity_Extraction(t1, entity_widget_lists, t2, True), D_Summary(t1, t3,True)))
    Record_btn.place(relheight=0.03, relwidth=0.02, rely=0.751, relx=0.78)

    play_pause_btn = tk.Button(chatbot_widget, text='⏯', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", 15), anchor='s', activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: set_recording_paused(play_pause_btn))
    play_pause_btn.place(relheight=0.03, relwidth=0.02, rely=0.751, relx=0.8)

    clock_lb = tk.Label(chatbot_widget, text='', fg=fg_color, font=("Bauhaus 93", 13), bg=bg_color, borderwidth=0, border=0)
    clock_lb.place(relheight=0.03, relwidth=0.06, rely=0.751, relx=0.82)

    extract_wid = tk.Button(chatbot_widget, text='⎋ Extract', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", 10), activebackground=bg_color, bg='blue', borderwidth=0, border=0, command=lambda: Entity_Extraction(t1, entity_widget_lists, t2, False) )#D_Summary(t1, t2))
    extract_wid.place(relheight=0.02, relwidth=0.04, rely=0.78, relx=0.78)
    change_fg_OnHover(extract_wid, 'red', fg_color)

    Summary_wid = tk.Button(chatbot_widget, text='≅Summarize', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", 10), activebackground=bg_color, bg='blue', borderwidth=0, border=0, command=lambda: D_Summary(t1, t3, False))
    Summary_wid.place(relheight=0.02, relwidth=0.041, rely=0.78, relx=0.821)
    change_fg_OnHover(Summary_wid, 'red', fg_color)

    upload_audio_wid = tk.Button(chatbot_widget, text='⥣️audio', fg=fg_color, activeforeground=fg_color, font=("Bauhaus 93", 10), activebackground=bg_color, bg='blue', borderwidth=0, border=0, command=lambda: upload_audio_file(t1, upload_audio_wid))
    upload_audio_wid.place(relheight=0.02, relwidth=0.041, rely=0.78, relx=0.863)
    #change_fg_OnHover(upload_audio_wid, 'red', fg_color)





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
    call_widget.place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253)

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
    profile_widget.place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253)

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
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor

    conversation_widget = tk.Frame(widget, bg=bg_color, borderwidth=0, border=0)
    conversation_widget.place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253)

    paned_window = tk.PanedWindow(conversation_widget, bg=bg_color, orient=tk.HORIZONTAL, sashwidth=8, sashrelief=tk.FLAT)
    paned_window.place(relheight=0.60, relwidth=0.96, rely=0.03, relx=0.01)

    t1 = tk.Text(paned_window, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, wrap="word", font=("Times New Roman", 13), borderwidth=2, border=3)
    #t1.place(relheight=0.60, relwidth=0.485, rely=0.03, relx=0.01)
    t1.config(state=tk.DISABLED)

    t2 = tk.Text(paned_window, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, wrap="word", font=("Times New Roman", 13), borderwidth=2, border=3)
    #t2.place(relheight=0.60, relwidth=0.485, rely=0.03, relx=0.505)
    t2.tag_configure("user_config", foreground="gray", justify=tk.LEFT)  # user queries  config's
    t2.tag_configure("llm_config", foreground="black", justify=tk.LEFT)  # llm responses config's
    t2.tag_configure("error_config", foreground="red", justify=tk.LEFT)  # llm responses config's
    t2.config(state=tk.DISABLED)

    paned_window.add(t1)
    paned_window.add(t2)

    tk.Button(conversation_widget, text="Upload doc", bg=bg_color, activebackground=bg_color, fg=fg_color, font=("Times New Roman", 13), borderwidth=2, border=3, command=lambda: Upload_file(t1, status_widg)).place(relheight=0.03, relwidth=0.07, rely=0.65, relx=0.01)

    tk.Button(conversation_widget, text="Audio File", bg=bg_color, activebackground=bg_color, fg=fg_color, font=("Times New Roman", 13), borderwidth=2, border=3).place(relheight=0.03, relwidth=0.07, rely=0.65, relx=0.081)
    tk.Button(conversation_widget, text="Record", bg=bg_color, activebackground=bg_color, fg=fg_color, font=("Times New Roman", 13), borderwidth=2, border=3,  command=lambda: RUN_OFFLINE_speech_recognition(t1)).place(relheight=0.03, relwidth=0.07, rely=0.65, relx=0.152)

    status_widg = tk.Label(conversation_widget, text="𝕤𝕥𝕒𝕥𝕦𝕤", anchor='sw', bg=bg_color, activebackground=bg_color, fg=fg_color, font=("Times New Roman", 20), borderwidth=2, border=3)
    status_widg.place(relheight=0.03, relwidth=0.07, rely=0.63, relx=0.505)

    t3 = tk.Text(conversation_widget, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, wrap="word", font=("Times New Roman", 13), borderwidth=2, border=1)
    t3.place(relheight=0.06, relwidth=0.96, rely=0.7, relx=0.01)

    bng = tk.Button(conversation_widget, text="▶", activebackground=bg_color, bg=bg_color, fg=fg_color, font=("Arial Black", 15), borderwidth=0, border=0, command=lambda: rag_chat(t3.get("1.0", tk.END), t2, bng))
    bng.place(relheight=0.06, relwidth=0.02, rely=0.7, relx=0.973)

    return conversation_widget


def settings(widget):
    global gradient_ai_workspace_id, assemblyai_access_key, gradient_ai_access_key, gradient_ai_finetuned_id, gradient_ai_base_model_id, keys
    global root
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor, current_theme

    def save_keys(g_access, g_workkey, g_finetuned_id, g_base_model_id, Assemly_key):
        global gradient_ai_workspace_id, assemblyai_access_key, gradient_ai_access_key, keys, setting_status
        global llm_chain
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
            "current_theme": current_theme
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
    setting_widget.place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253)

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
    global num_y, num_height, current
    num_y = 0.9
    num_height = 0.05
    current = 130
    previous = 0
    def on_key_press(event, widget, widget1):
        global current, num_y, num_height, previous

        text_content = widget1.get("1.0", "end-1c")
        num_lines = len(text_content)  # Count the number of lines

        print("- ", num_lines, " - ", current)


        if num_lines > current and  num_lines > previous:
            num_y = num_y - 0.02
            num_height = num_height + 0.02
            widget.forget()
            widget.place(relheight=num_height, relwidth=0.6, rely=num_y, relx=0.2)
            current = current + 130

        elif (num_lines < current) and (num_lines > 130) and  (num_lines < previous):
            num_y = num_y + 0.02
            num_height = num_height - 0.02
            widget.forget()
            widget.place(relheight=num_height, relwidth=0.6, rely=num_y, relx=0.2)
            current = current - 130
        else:
            pass

        previous = num_lines

    chatbot_widget = tk.Frame(widget, bg=bg_color, borderwidth=0, border=0)
    chatbot_widget.place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253)

    out_put_widget = tk.Text(chatbot_widget, wrap='word', bg=bg_color, fg=fg_color, font=("Times New Roman", 14), borderwidth=0, border=0)
    out_put_widget.place(relheight=0.85, relwidth=0.62, rely=0.02, relx=0.19)
    out_put_widget.tag_configure("user_config", foreground="gray", justify=tk.LEFT)  # user queries  config's
    out_put_widget.tag_configure("llm_config", foreground="black", justify=tk.LEFT)  # llm responses config's
    out_put_widget.tag_configure("error_config", foreground="red", justify=tk.LEFT)  # llm responses config's
    out_put_widget.config(state=tk.DISABLED)

    search_lable = tk.Frame(chatbot_widget, bg=bg_color,  borderwidth=0, border=0)
    search_lable.place(relheight=0.05, relwidth=0.6, rely=0.9, relx=0.2)

    tk.Label(search_lable, text='------ ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ------ ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ', bg=bg_color,  fg=fg_color, borderwidth=0, border=0).place(relheight=0.15, relwidth=0.8, rely=0,                                                                                                                                                                                                                                                                                                                                                                                                              relx=0.1)
    tk.Label(search_lable, bg=bg_color, text='◜', fg=fg_color, anchor="nw", font=('Century Gothic', 20), borderwidth=0, border=0).place(relheight=0.5, relwidth=0.05, rely=0, relx=0)
    tk.Label(search_lable, bg=bg_color, text='◟', fg=fg_color, font=('Century Gothic', 20), anchor='sw', borderwidth=0, border=0).place(relheight=0.5, relwidth=0.05, rely=0.5, relx=0)
    tk.Label(search_lable, bg=bg_color, text='◝', fg=fg_color, font=('Century Gothic', 20), anchor='ne', borderwidth=0, border=0).place(relheight=0.5, relwidth=0.05, rely=0, relx=0.95)
    tk.Label(search_lable, bg=bg_color, text='◞', fg=fg_color, font=('Century Gothic', 20), anchor='se', borderwidth=0, border=0).place(relheight=0.5, relwidth=0.05, rely=0.5, relx=0.95)
    tk.Label(search_lable, text='------ ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ------ ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ', bg=bg_color, anchor='s', fg=fg_color, borderwidth=0, border=0).place(relheight=0.15, relwidth=0.8, rely=0.85,
                                                                                                                                                                                                                                                                                                                                                                                                                       relx=0.1)

    entry = tk.Text(search_lable, wrap='word', bg=bg_color, fg=fg_color, font=("Times New Roman", 14), borderwidth=0, border=0)
    entry.place(relheight=0.7, relwidth=0.96, rely=0.15, relx=0.02)
    entry.bind("<Key>", lambda e: on_key_press(e, search_lable, entry))
    entry.bind("<Return>", lambda e: Chat_bot_inference(entry, search_lable, out_put_widget))

    tk.Button(chatbot_widget, text='⇱', font=("Times New Roman", 14), bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color, borderwidth=0, border=0, command=lambda: Chat_bot_inference(entry, search_lable, out_put_widget)).place(relheight=0.03, relwidth=0.02, rely=0.92, relx=0.8)

    return chatbot_widget


def connect_to_server():
    pass
    """
    def connect():
        global connection_status
        global client_socket, server_IP4v_address, Server_listening_port, closed
        global user_id, user_Photo, First_name, Second_Name, Last_Name, Email
        while not closed:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
                client_socket.connect((server_IP4v_address, Server_listening_port))

                if user_id is not None:
                    user_data = f"{user_id}~{First_name} {Second_Name} {Last_Name}~{user_Photo}"
                    client_socket.send(f"active~{len(user_data)}".encode("utf-8"))
                    client_socket.send(user_data.encode("utf-8"))

                print(" Connection Established ")
                connection_status = True
                break
            except:
                pass

    threading.Thread(target=connect).start()
    """


def fetch_info():
    pass
    """
    list_hold = []  # clear the list
    global client_socket, user_id
    print("fetching")

    m = f'infoRequest~{user_id}'
    time.sleep(2)

    client_socket.send(m.encode("utf-8")[:1024])  # send message
    while True:
        print("starting")
        buffer_size = client_socket.recv(500).decode("utf-8")
        print("buffer_size, ", buffer_size)
        if buffer_size == "end":
            break
        info = client_socket.recv(int(buffer_size)).decode("utf-8")

        info = info.split("~")
        #if int(info[0]) == int(user_id):
        #    continue

        list_hold.append((info[0], info[1], info[2]))

    print("finished fetching")

    return list_hold
    """


def User_Home_page(widget):
    global user_id, widget_list, Home_page_frame
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor
    global root, screen_width, screen_height

    Home_page_frame = tk.Frame(widget, bg=fg_color, width=screen_width, height=screen_height)
    Home_page_frame.place(relx=0, rely=0)
    container1 = tk.Frame(Home_page_frame, bg=bg_color)
    container1.place(rely=0, relx=0, width=int(screen_width * 0.025), height=int((screen_height * 1)-20))
    container2 = tk.Frame(Home_page_frame, bg=bg_color)
    container2.place(rely=0, relx=0.0253, width=int(screen_width * 0.9747), height=int((screen_height * 1)-20))  # place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253, )



    
    # PROFILE_widget = profile(Home_page_frame)
 

    CALL_Widget = call(Home_page_frame)

    SETTINGS_Widget = settings(Home_page_frame)
    chat_me_Widget = chat_me(Home_page_frame)

    rag_widget = RAG_page(Home_page_frame)
    CHAT_Widget = chat(Home_page_frame)
    # sidebar  widgets ------------------------------------------------------------------------------------------------------------------------------------
 
    def active(widget):
        global widget_list, fg_hovercolor
        for i in widget_list:
            if i != widget:
                i.config(bg=bg_color, relief=tk.FLAT, border=0, fg=fg_color)
            else:
                i.config(bg=bg_color, relief=tk.RAISED, border=1, fg=fg_hovercolor)




    side_bar = tk.Frame(container1, bg=bg_color, borderwidth=0, border=0)
    side_bar.place(relheight=1, relwidth=1, rely=0, relx=0)
    #side_bar.bind("<Configure>", lambda e: resize(side_bar, side_wdg_width, side_wdg_height))

    profile_widget = tk.Button(side_bar, bg=bg_color, activebackground=bg_color, activeforeground=fg_color, text='≣', font=("Calibri", 17), fg=fg_color, anchor='center', borderwidth=0, border=0)  # ,command=lambda: (PROFILE_widget.tkraise(), active(profile_widget)))
    profile_widget.place(relheight=0.03, relwidth=1, rely=0.01, relx=0)
    change_fg_OnHover(profile_widget, fg_hovercolor, fg_color)
    widget_list.append(profile_widget)

    st1_bt = tk.Button(side_bar, bg=bg_color, activebackground=bg_color, activeforeground=fg_color, text='-', font=("Calibri", 17), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (CALL_Widget.tkraise(), active(st1_bt)))
    st1_bt.place(relheight=0.03, relwidth=1, rely=0.05, relx=0)
    change_fg_OnHover(st1_bt, fg_hovercolor, fg_color)
    widget_list.append(st1_bt)

    st2_bt = tk.Button(side_bar, bg=bg_color, activebackground=bg_color, activeforeground=fg_color, text='⧮', font=("Calibri", 17), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (CHAT_Widget.tkraise(), active(st2_bt)))
    st2_bt.place(relheight=0.03, relwidth=1, rely=0.09, relx=0)
    change_fg_OnHover(st2_bt, fg_hovercolor, fg_color)
    widget_list.append(st2_bt)

    st3_bt = tk.Button(side_bar, bg=bg_color, activebackground=bg_color, activeforeground=fg_color, text='🗐', font=("Calibri", 17), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (rag_widget.tkraise(), active(st3_bt)))
    st3_bt.place(relheight=0.03, relwidth=1, rely=0.13, relx=0)
    change_fg_OnHover(st3_bt, fg_hovercolor, fg_color)
    widget_list.append(st3_bt)

    st4_bt = tk.Button(side_bar, bg=bg_color, activebackground=bg_color, activeforeground=fg_color, text='⧉', font=("Calibri", 17), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (chat_me_Widget.tkraise(), active(st4_bt)))
    st4_bt.place(relheight=0.03, relwidth=1, rely=0.17, relx=0)
    change_fg_OnHover(st4_bt, fg_hovercolor, fg_color)
    widget_list.append(st4_bt)

    st5_bt = tk.Button(side_bar, bg=bg_color, activebackground=bg_color, activeforeground=fg_color, text='-', font=("Calibri", 17), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (rag_widget.tkraise(), active(st5_bt)))
    st5_bt.place(relheight=0.03, relwidth=1, rely=0.21, relx=0)
    change_fg_OnHover(st5_bt, fg_hovercolor, fg_color)
    widget_list.append(st5_bt)

    st6_bt = tk.Button(side_bar, bg=bg_color, activebackground=bg_color, activeforeground=fg_color, text='-', font=("Calibri", 17), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (rag_widget.tkraise(), active(st6_bt)))
    st6_bt.place(relheight=0.03, relwidth=1, rely=0.89, relx=0)
    change_fg_OnHover(st6_bt, fg_hovercolor, fg_color)
    widget_list.append(st6_bt)

    st7_bt = tk.Button(side_bar, bg=bg_color, activebackground=bg_color, activeforeground=fg_color, text='-', font=("Calibri", 17), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (rag_widget.tkraise(), active(st7_bt)))
    st7_bt.place(relheight=0.03, relwidth=1, rely=0.93, relx=0)
    change_fg_OnHover(st7_bt, fg_hovercolor, fg_color)
    widget_list.append(st7_bt)

    st8_bt = tk.Button(side_bar, bg=bg_color, activebackground=bg_color, activeforeground=fg_color, text='⚙ ', font=("Calibri", 17), fg=fg_color, anchor='center', borderwidth=0, border=0, command=lambda: (SETTINGS_Widget.tkraise(), active(st8_bt)))
    st8_bt.place(relheight=0.03, relwidth=1, rely=0.97, relx=0)
    change_fg_OnHover(st8_bt, fg_hovercolor, fg_color)
    widget_list.append(st8_bt)

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


def main():
    global root, screen_width, screen_height, session, client_socket, server_IP4v_address, Server_listening_port
    global user_id, user_Photo, First_name, Second_Name, Last_Name, Email
    global gradient_ai_workspace_id, assemblyai_access_key, gradient_ai_access_key, keys
    global bg_color
    print("main started")

    access_keys_info()

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
    content_height = root.winfo_height()

    print(str(screen_width) + "\n" + str(screen_height))

    title_bar_color(bg_color)

    User_Home_page(root)

    def on_closing():
        global session, root, closed
        closed = True
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
