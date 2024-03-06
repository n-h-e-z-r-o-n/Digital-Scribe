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
from gradientai import Gradient, SummarizeParamsLength, ExtractParamsSchemaValueType
from tkinter import filedialog
import docx

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
rag_pipeline = None

bg_color = None
fg_color = None
fg_hovercolor = None
bg_hovercolor = None

# =============================== Functions definition ============================================================================================
# =================================================================================================================================================


def Entity_Extraction(document, entity_list, widget):
    document = (document.strip())
    mygradient = Gradient()
    print(document)
    schema = '{'
    for i in entity_list:
        schema += '"' + i[1].get() + '": { "type": ExtractParamsSchemaValueType.' + str(i[2].cget("text")) + ', "required": False, }, '
        print(i[1].get(), '--', i[2].cget("text"))
    schema += '}'
    print(schema)
    dictionary = eval(schema)
    print(dictionary)

    try:
        result = mygradient.extract(
            document=document,
            schema_=dictionary,
        )
        widget.delete(1.0, tk.END)
        for key, value in result["entity"].items():
            m = key + " : " + value + "\n"
            print()
            widget.insert(tk.END, m)

        print(result)
        return result
    except:
        return None


def D_Summary(widget1, widget):
    document = widget1.get("1.0", "end")
    document = (document.strip())
    print(len(document))
    if len(document) == 0:
        time.sleep(2)
        return None

    gradient = Gradient()

    try:
        summary_length = SummarizeParamsLength.LONG
        result = gradient.summarize(
            document=document,
            length=summary_length
        )
        widget.delete(1.0, tk.END)
        widget.insert(tk.END, result['summary'])

        return result
    except:
        return None




def rag_initialize(data, widget):
    global rag_pipeline
    document_store = InMemoryDocumentStore()
    writer = DocumentWriter(document_store=document_store)

    document_embedder = GradientDocumentEmbedder(
        access_token=os.environ["GRADIENT_ACCESS_TOKEN"],
        workspace_id=os.environ["GRADIENT_WORKSPACE_ID"],
    )

    docs = [
        Document(content=data)
    ]

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


def rag_chat(question, widget, widget1):
    global rag_pipeline
    widget1.config(text = '▫▫▫▫')
    question = question.strip()
    if question == '':
        widget1.config(text='▶')
        return
    widget.insert(tk.END, f" {question}\n", 'user_config')
    try:
        result = rag_pipeline.run(
            {
                "text_embedder": {"text": question},
                "prompt_builder": {"query": question},
                "answer_builder": {"query": question}
            }
        )
        widget.insert(tk.END, f'{result["answer_builder"]["answers"][0].data}\n\n\n', 'llm_config')
        widget.see(tk.END)  # Scroll to the end of the text widget

        widget1.config(text='▶')
        # return result["answer_builder"]["answers"][0].data
    except Exception as e:
        widget.insert(tk.END, f'ERROR: PLEASE UPLOAD FILE FIRST \n\n\n', 'error_config')
        widget1.config(text='▶')

        print(f"UPLOAD ERROR\n {e}")


def Upload_file(widget, widget2):
    widget2.config(fg='black')
    file_path = filedialog.askopenfilename()

    if file_path:
        widget.delete(1.0, tk.END)
        document = docx.Document(file_path)
        data = ""
        for paragraph in document.paragraphs:
            data += paragraph.text + "\n"
            if paragraph.style.name == 'List Paragraph':

                widget.insert(tk.END, f"\t •{paragraph.text}")
            elif paragraph.style.name == 'Normal':
                widget.insert(tk.END, f"{paragraph.text} \n")
        print(data)
        threading.Thread(target=rag_initialize, args=(data, widget2,)).start()




    else:
        print("No file selected")


def dark_title_bar(window):
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))


# =============================== scroll Functions definition =======================================================================================

def widget_scroll_bind(widget):
    def nnn(widget, event):
        pass

    widget.bind("<Configure>", lambda e: on_frame_configure(widget, e))
    widget.bind("<MouseWheel>", lambda e: on_mouse_wheel(widget, e))


def on_mouse_wheel(widget, event):  # Function to handle mouse wheel scrolling
    # Scroll the canvas up or down based on the mouse wheel direction
    if event.delta < 0:
        widget.yview_scroll(1, "units")
    else:
        widget.yview_scroll(-1, "units")


def access_keys_info():
    global gradient_ai_workspace_id, assemblyai_access_key, gradient_ai_access_key, gradient_ai_finetuned_id, gradient_ai_base_model_id, keys
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor
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
            
            print('gradient_ai_workspace_id :', gradient_ai_workspace_id)
            print('gradient_ai_access_key:', gradient_ai_access_key)
            print('assemblyai_access_key :', assemblyai_access_key)

            os.environ['GRADIENT_ACCESS_TOKEN'] = gradient_ai_access_key
            os.environ['GRADIENT_WORKSPACE_ID'] = gradient_ai_workspace_id
    except:
        pass


def on_frame_configure(widget, event):  # Update the canvas scrolling region when the large frame changes size
    widget.configure(scrollregion=widget.bbox("all"))


def attach_scroll(widget, color='white'):
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
    widget.bind("<Enter>", func=lambda e: widget.config(fg=colorOnHover))
    widget.bind("<Leave>", func=lambda e: widget.config(fg=colorOnLeave))


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
    t3_link_btn5 = tk.Button(t3, bg=nav_bar_color, text='Teen therapy', anchor='w', borderwidth=0, border=0,
                             activebackground=nav_bar_color, font=("Calibri", 13))
    t3_link_btn5.place(relheight=0.1, relwidth=1, rely=0.56, relx=0)
    change_fg_OnHover(t3_link_btn5, 'brown', 'black')

    t4 = tk.Frame(Service_widget, bg=nav_bar_color)
    t4.place(relheight=0.4, relwidth=0.15, rely=0.02, relx=0.82)
    tk.Label(t4, bg=nav_bar_color, text='Get treatment for', anchor='w', font=("Bauhaus 93", 18)).place(relheight=0.11,
                                                                                                        relwidth=1,
                                                                                                        rely=0, relx=0)

    t4_link_btn1 = tk.Button(t4, bg=nav_bar_color, text='Depression', anchor='w', borderwidth=0, border=0,
                             activebackground=nav_bar_color, font=("Calibri", 13))
    t4_link_btn1.place(relheight=0.1, relwidth=1, rely=0.12, relx=0)
    change_fg_OnHover(t4_link_btn1, 'brown', 'black')
    t4_link_btn2 = tk.Button(t4, bg=nav_bar_color, text='Anxiety', anchor='w', borderwidth=0, border=0,
                             activebackground=nav_bar_color, font=("Calibri", 13))
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
    def font_change(widget1, widget2, widget3):
        global defalt_font_style, defalt_font_size, closed
        defalt_font_style = 'Times New Roman'
        defalt_font_size = 13

        def check(widget1=widget1, widget2=widget2, widget3=widget3):
            global defalt_font_style, defalt_font_size, closed
            while True:
                if closed:
                    break
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

        time.sleep(10)
        check()



    bg_color = 'lightgreen'
    fg_color = 'black'
    defalt_font_style = 'Times New Roman'
    defalt_font_size = 13
    nav_bar_bg_color = 'lightblue'

    chatbot_widget = tk.Frame(widget, bg="lightgreen", borderwidth=0, border=0)
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

    t1 = tk.Text(chatbot_widget, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, font=("Times New Roman", 13), borderwidth=2, border=5)
    t1.place(relheight=0.70, relwidth=0.75, rely=0.03, relx=0.0253)

    t2 = tk.Text(chatbot_widget, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, font=("Times New Roman", 13), borderwidth=4, border=1)
    t2.place(relheight=0.25, relwidth=0.75, rely=0.74, relx=0.0253)

    threading.Thread(target=font_change, args=(font_style_entry, font_size_entry, t1,)).start()
    threading.Thread(target=font_change, args=(font_style_entry, font_size_entry, t2,)).start()

    entity_section = tk.Frame(chatbot_widget, bg='brown', borderwidth=0, border=0)
    entity_section.place(relheight=0.72, relwidth=0.21, rely=0.03, relx=0.78)

    title = tk.Frame(entity_section, bg=bg_color, borderwidth=2, border=1)
    title.place(relheight=0.036, relwidth=1, rely=0, relx=0)
    tk.Label(title, text="Field Name", bg=bg_color, borderwidth=0, border=0, font=("Georgia", 11, 'bold')).place(relx=0.01, rely=0.04, relwidth=0.5, relheight=1)
    tk.Label(title, text="Type", bg=bg_color, borderwidth=0, border=0, font=("Georgia", 11, 'bold')).place(relx=0.52, rely=0.04, relwidth=0.2, relheight=1)

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

        new_entity = tk.Frame(widget, bg=bg_color, borderwidth=2, border=1, height=50, width=int(screen_width * 0.9747 * 0.21 - 3))
        new_entity.pack(side=tk.TOP, fill=tk.X)

        entity_name = tk.Entry(new_entity, bg=bg_color, borderwidth=0, border=1, font=("Times New Roman", 11))
        entity_name.place(relx=0.01, rely=0, relwidth=0.5, relheight=0.9)
        type_widget = tk.Button(new_entity, bg=bg_color, text=entity_type, font=("Times New Roman", 10, 'bold'), relief=tk.SUNKEN, activebackground=bg_color, borderwidth=0, border=1, command=lambda: change_type(type_widget))
        type_widget.place(relx=0.52, rely=0, relwidth=0.2, relheight=0.9)
        close_widg = tk.Button(new_entity, bg=bg_color, activebackground=bg_color, text="X", borderwidth=0, border=0, font=("Bauhaus 93", 10), command=lambda: delet_widget(new_entity))
        close_widg.place(relx=0.95, rely=0, relwidth=0.05, relheight=1)
        change_fg_OnHover(close_widg, 'red', 'black')

        new_entity.bind("<MouseWheel>", lambda e: on_mouse_wheel(user_page_canvas, e))

        entity_widget_lists.append((new_entity, entity_name, type_widget))

    Add_new_entity = tk.Button(entity_section, text='+ Add new entity', fg=fg_color, font=("Bauhaus 93", 10), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: add(fr2))
    Add_new_entity.place(relheight=0.03, relwidth=1, rely=0.97, relx=0)
    change_fg_OnHover(Add_new_entity, 'red', fg_color)

    Extract_entities = tk.Button(chatbot_widget, text='Extract', fg=fg_color, font=("Bauhaus 93", 10), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: Entity_Extraction(t1.get("1.0", "end"), entity_widget_lists, t2))
    Extract_entities.place(relheight=0.02, relwidth=0.21, rely=0.751, relx=0.78)
    change_fg_OnHover(Extract_entities, 'red', fg_color)

    Summary_wid = tk.Button(chatbot_widget, text='Summary', fg=fg_color, font=("Bauhaus 93", 10), activebackground=bg_color, bg=bg_color, borderwidth=0, border=0, command=lambda: D_Summary(t1, t2))
    Summary_wid.place(relheight=0.02, relwidth=0.21, rely=0.772, relx=0.78)
    change_fg_OnHover(Summary_wid, 'red', fg_color)

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


def conversation(widget):
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor


    conversation_widget = tk.Frame(widget, bg=bg_color, borderwidth=0, border=0)
    conversation_widget.place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253)

    t1 = tk.Text(conversation_widget, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, wrap="word", font=("Times New Roman", 13), borderwidth=2, border=3)
    t1.place(relheight=0.60, relwidth=0.485, rely=0.03, relx=0.01)

    t2 = tk.Text(conversation_widget, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, wrap="word", font=("Times New Roman", 13), borderwidth=2, border=3)
    t2.place(relheight=0.60, relwidth=0.485, rely=0.03, relx=0.505)
    t2.tag_configure("user_config", foreground="gray", justify=tk.LEFT)  # user queries  config's
    t2.tag_configure("llm_config", foreground="black", justify=tk.LEFT)  # llm responses config's
    t2.tag_configure("error_config", foreground="red", justify=tk.LEFT)  # llm responses config's

    tk.Button(conversation_widget, text="Upload doc", bg=bg_color, activebackground=bg_color, fg=fg_color, font=("Times New Roman", 13), borderwidth=2, border=3, command=lambda : Upload_file(t1, status_widg)).place(relheight=0.03, relwidth=0.07, rely=0.65, relx=0.01)

    tk.Button(conversation_widget, text="Audio File", bg=bg_color, activebackground=bg_color, fg=fg_color, font=("Times New Roman", 13), borderwidth=2, border=3).place(relheight=0.03, relwidth=0.07, rely=0.65, relx=0.081)

    status_widg = tk.Label(conversation_widget, text="𝕤𝕥𝕒𝕥𝕦𝕤", anchor='sw', bg=bg_color, activebackground=bg_color, fg=fg_color, font=("Times New Roman", 20), borderwidth=2, border=3)
    status_widg.place(relheight=0.03, relwidth=0.07, rely=0.63, relx=0.505)


    t3 = tk.Text(conversation_widget, bg=bg_color, fg=fg_color, relief=tk.SUNKEN, wrap="word",  font=("Times New Roman", 13), borderwidth=2, border=1)
    t3.place(relheight=0.06, relwidth=0.96, rely=0.7, relx=0.01)


    bng = tk.Button(conversation_widget, text="▶", activebackground=bg_color, bg=bg_color, fg=fg_color, font=("Arial Black", 15), borderwidth=0, border=0, command=lambda:rag_chat(t3.get("1.0", tk.END), t2, bng))
    bng.place(relheight=0.06, relwidth=0.02, rely=0.7, relx=0.973)

    return conversation_widget


def settings(widget):
    global gradient_ai_workspace_id, assemblyai_access_key, gradient_ai_access_key, gradient_ai_finetuned_id, gradient_ai_base_model_id, keys
    global root
    global bg_color, fg_color, fg_hovercolor, bg_hovercolor
    def save_keys(g_access, g_workkey, g_finetuned_id, g_base_model_id, Assemly_key):
        global gradient_ai_workspace_id, assemblyai_access_key, gradient_ai_access_key, keys

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
            '_AAI_': assemblyai_access_key
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


    setting_widget = tk.Frame(widget, bg=bg_color, borderwidth=0, border=0)
    setting_widget.place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253)

    # ======================================================= Section 1 ===========================================================================================================================================

    g1 = tk.Frame(setting_widget, bg=bg_color, relief=tk.RAISED, borderwidth=0, border=5)
    g1.place(relheight=0.4, relwidth=0.41, rely=0.02, relx=0.0253)

    # tk.Label(g1, bg='blue', fg=fg_color, borderwidth=7, border=7).place(relheight=1, relwidth=1, rely=0, relx=0)

    tk.Label(g1, text="GRADIENT AI ACCESS KEYS ", bg=bg_color, fg=fg_color, font=("Georgia", 12, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.6, rely=0, relx=0)

    tk.Label(g1, text="GRADIENT_ACCESS_TOKEN :", bg=bg_color, fg=fg_color, font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.071, relx=0)
    gradient_access_widget = tk.Entry(g1, bg=bg_color, fg=fg_color, borderwidth=0, border=1, font=("Courier New", 10))
    gradient_access_widget.place(relheight=0.07, relwidth=0.74, rely=0.071, relx=0.25)
    gradient_access_widget.insert(0, gradient_ai_access_key)
    gradient_access_widget.bind('<Return>', lambda e: save_keys(gradient_access_widget.get(), gradient_work_widget.get(), gradient_finetuned_model_id.get(), gradient_base_model_id.get(), assembly_widget.get()))
    change_bg_OnHover(gradient_access_widget, bg_hovercolor, bg_color)

    tk.Label(g1, text="GRADIENT_WORKSPACE_ID :", bg=bg_color, fg=fg_color, font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.142, relx=0)
    gradient_work_widget = tk.Entry(g1, bg=bg_color, fg=fg_color, borderwidth=0, border=1, font=("Courier New", 10))
    gradient_work_widget.place(relheight=0.07, relwidth=0.74, rely=0.142, relx=0.25)
    gradient_work_widget.insert(0, gradient_ai_workspace_id)
    gradient_work_widget.bind('<Return>', lambda e: save_keys(gradient_access_widget.get(), gradient_work_widget.get(), gradient_finetuned_model_id.get(), gradient_base_model_id.get(), assembly_widget.get()))
    change_bg_OnHover(gradient_work_widget, bg_hovercolor, bg_color)


    tk.Label(g1, text="NLP_adapter_id :", bg=bg_color, fg=fg_color, font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.213, relx=0)
    gradient_finetuned_model_id = tk.Entry(g1, bg=bg_color, fg=fg_color, borderwidth=0, border=1, font=("Courier New", 10))
    gradient_finetuned_model_id.place(relheight=0.07, relwidth=0.74, rely=0.213, relx=0.25)
    gradient_finetuned_model_id.insert(0, gradient_ai_finetuned_id)
    gradient_finetuned_model_id.bind('<Return>', lambda e: save_keys(gradient_access_widget.get(), gradient_work_widget.get(), gradient_finetuned_model_id.get(), gradient_base_model_id.get(), assembly_widget.get()))
    change_bg_OnHover(gradient_finetuned_model_id, bg_hovercolor, bg_color)

    tk.Label(g1, text="Base_Model :", bg=bg_color, fg=fg_color, font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.284, relx=0)
    gradient_base_model_id = tk.Entry(g1, bg=bg_color, fg=fg_color, borderwidth=0, border=1, font=("Courier New", 10))
    gradient_base_model_id.place(relheight=0.07, relwidth=0.74, rely=0.284, relx=0.25)
    gradient_base_model_id.insert(0, gradient_ai_base_model_id)
    gradient_base_model_id.bind('<Return>', lambda e: save_keys(gradient_access_widget.get(), gradient_work_widget.get(), gradient_finetuned_model_id.get(), gradient_base_model_id.get(), assembly_widget.get()))
    change_bg_OnHover(gradient_base_model_id, bg_hovercolor, bg_color)

    tk.Label(g1, text="ASSEMBLY-AI  ", bg=bg_color, fg=fg_color, font=("Georgia", 12, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.6, rely=0.363, relx=0)
    tk.Label(g1, text="assemblyai access key:", bg=bg_color, fg=fg_color, font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0).place(relheight=0.07, relwidth=0.24, rely=0.432, relx=0)
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

    def change_color(widget):
        global bg_color
        bg_color = 'gray'
        bg_icolor = 'gray'
        if isinstance(widget, tk.Frame):
            widget.config(bg=bg_icolor)

        elif isinstance(widget, tk.Button):
            widget.config(bg=bg_icolor, activebackground='black', fg='white', activeforeground='white')

        elif isinstance(widget, tk.Label):
            widget.config(bg=bg_icolor, fg='white')

        elif isinstance(widget, tk.Text):
            widget.config(bg=bg_icolor, fg='white')
        elif isinstance(widget, tk.Entry):
            widget.config(bg=bg_icolor, fg='white')
        else:
            #widget.config(bg=bg_icolor, fg='white')
            pass

        children = widget.winfo_children()
        for child in children:
            change_color(child)

    g2 = tk.Frame(setting_widget, bg=bg_color, relief=tk.RAISED, borderwidth=0, border=5)
    g2.place(relheight=0.4, relwidth=0.41, rely=0.5, relx=0.0253)

    theam_widget = tk.Button(g2, bg=bg_color, relief=tk.RAISED, borderwidth=0,  border=5, command=lambda: change_color(root))
    theam_widget.place(relheight=0.4, relwidth=0.41, rely=0.02, relx=0.0253)

    # ======================================================= Section 3 ===========================================================================================================================================
    g3 = tk.Frame(setting_widget, bg=bg_color, relief=tk.RAISED, borderwidth=0, border=5)
    g3.place(relheight=0.4, relwidth=0.41, rely=0.02, relx=0.5)

    # ======================================================= Section 4 ===========================================================================================================================================
    g4 = tk.Frame(setting_widget, bg=bg_color, relief=tk.RAISED, borderwidth=0, border=5)
    g4.place(relheight=0.4, relwidth=0.41, rely=0.5, relx=0.5)
    # ======================================================= Section 5 ===========================================================================================================================================

    return setting_widget


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
    global user_id, widget_list
    user_page_widget, user_page_root = attach_scroll(widget)

    Home_page_frame = tk.Frame(widget, bg='black', width=screen_width, height=screen_height)
    Home_page_frame.pack(fill=tk.BOTH, expand=True)

    nav_bar_color = 'white'
    nav_bar_btn_hover_color = '#F5F5F5'
    nav_bar = tk.Frame(Home_page_frame, bg=nav_bar_color)
    nav_bar.place(relheight=0.02, relwidth=1, rely=0, relx=0)

    nav_bar_bt5_widget = tk.Button(nav_bar, bg=nav_bar_color, activebackground=nav_bar_color, text='Sign Out', justify=tk.LEFT, anchor="center", font=("Calibri Light", 10), borderwidth=0, border=0)  # command=lambda: sign_out(user_page_root))
    nav_bar_bt5_widget.place(relheight=0.9, relwidth=0.06, rely=0.05, relx=0.935)
    change_bg_OnHover(nav_bar_bt5_widget, nav_bar_btn_hover_color, nav_bar_color)



    # PROFILE_widget = profile(Home_page_frame)


    CHAT_Widget = chat(Home_page_frame)
    #CALL_Widget = call(Home_page_frame)
    CONV_AI_Widget = conversation(Home_page_frame)
    SETTINGS_Widget = settings(Home_page_frame)


    # sidebar  widgets ------------------------------------------------------------------------------------------------------------------------------------

    side_bar_bg = "white"
    side_bar_fg = "green"
    side_bar_bg_widget_houver_color = "#FFFAFA"
    side_bar_fg_widget_houver_color = 'blue'
    active_bg_widget_color = "brown"
    active_fg_widget_color = side_bar_fg_widget_houver_color

    def active(widget):
        global widget_list
        for i in widget_list:
            if i != widget:
                i.config(bg=side_bar_bg, fg=side_bar_fg)
                change_bg_OnHover(i, side_bar_bg_widget_houver_color, side_bar_bg)
                change_fg_OnHover(i, side_bar_fg_widget_houver_color, side_bar_fg)
            else:
                i.config(bg=active_bg_widget_color, fg=active_fg_widget_color)
                change_bg_OnHover(i, active_bg_widget_color, active_bg_widget_color)
                change_fg_OnHover(i, active_fg_widget_color, active_fg_widget_color)

    side_bar = tk.Frame(Home_page_frame, bg=side_bar_bg, borderwidth=0, border=0)
    side_bar.place(relheight=0.96, relwidth=0.025, rely=0.02, relx=0)

    profile_widget = tk.Button(side_bar, bg=side_bar_bg, text='≣', font=("Calibri", 20), fg=side_bar_fg, anchor='center', borderwidth=0, border=0)  # ,command=lambda: (PROFILE_widget.tkraise(), active(profile_widget)))
    profile_widget.place(relheight=0.03, relwidth=1, rely=0.01, relx=0)
    change_bg_OnHover(profile_widget, side_bar_bg_widget_houver_color, side_bar_bg)
    change_fg_OnHover(profile_widget, side_bar_fg_widget_houver_color, side_bar_fg)
    widget_list.append(profile_widget)

    st1_bt = tk.Button(side_bar, bg=side_bar_bg, text='📞', font=("Calibri", 20), fg=side_bar_fg, anchor='center', borderwidth=0, border=0, command=lambda: (CALL_Widget.tkraise(), active(st1_bt)))
    st1_bt.place(relheight=0.03, relwidth=1, rely=0.05, relx=0)
    change_bg_OnHover(st1_bt, side_bar_bg_widget_houver_color, side_bar_bg)
    change_fg_OnHover(st1_bt, side_bar_fg_widget_houver_color, side_bar_fg)
    widget_list.append(st1_bt)

    st2_bt = tk.Button(side_bar, bg=side_bar_bg, text='🎥', font=("Calibri", 20), fg=side_bar_fg, anchor='center', borderwidth=0, border=0, command=lambda: (CHAT_Widget.tkraise(), active(st2_bt)))
    st2_bt.place(relheight=0.03, relwidth=1, rely=0.09, relx=0)
    change_bg_OnHover(st2_bt, side_bar_bg_widget_houver_color, side_bar_bg)
    change_fg_OnHover(st2_bt, side_bar_fg_widget_houver_color, side_bar_fg)
    widget_list.append(st2_bt)

    st3_bt = tk.Button(side_bar, bg=side_bar_bg, text='📩', font=("Calibri", 20), fg=side_bar_fg, anchor='center', borderwidth=0, border=0, command=lambda: (CONV_AI_Widget.tkraise(), active(st3_bt)))
    st3_bt.place(relheight=0.03, relwidth=1, rely=0.13, relx=0)
    change_bg_OnHover(st3_bt, side_bar_bg_widget_houver_color, side_bar_bg)
    change_fg_OnHover(st3_bt, side_bar_fg_widget_houver_color, side_bar_fg)
    widget_list.append(st3_bt)

    st4_bt = tk.Button(side_bar, bg=side_bar_bg, text='☏', font=("Calibri", 20), fg=side_bar_fg, anchor='center', borderwidth=0, border=0, command=lambda: (CONV_AI_Widget.tkraise(), active(st4_bt)))
    st4_bt.place(relheight=0.03, relwidth=1, rely=0.17, relx=0)
    change_bg_OnHover(st4_bt, side_bar_bg_widget_houver_color, side_bar_bg)
    change_fg_OnHover(st4_bt, side_bar_fg_widget_houver_color, side_bar_fg)
    widget_list.append(st4_bt)

    st5_bt = tk.Button(side_bar, bg=side_bar_bg, text='☏', font=("Calibri", 20), fg=side_bar_fg, anchor='center', borderwidth=0, border=0, command=lambda: (CONV_AI_Widget.tkraise(), active(st5_bt)))
    st5_bt.place(relheight=0.03, relwidth=1, rely=0.21, relx=0)
    change_bg_OnHover(st5_bt, side_bar_bg_widget_houver_color, side_bar_bg)
    change_fg_OnHover(st5_bt, side_bar_fg_widget_houver_color, side_bar_fg)
    widget_list.append(st5_bt)

    st6_bt = tk.Button(side_bar, bg=side_bar_bg, text='☏', font=("Calibri", 20), fg=side_bar_fg, anchor='center', borderwidth=0, border=0, command=lambda: (CONV_AI_Widget.tkraise(), active(st6_bt)))
    st6_bt.place(relheight=0.03, relwidth=1, rely=0.89, relx=0)
    change_bg_OnHover(st6_bt, side_bar_bg_widget_houver_color, side_bar_bg)
    change_fg_OnHover(st6_bt, side_bar_fg_widget_houver_color, side_bar_fg)
    widget_list.append(st6_bt)

    st7_bt = tk.Button(side_bar, bg=side_bar_bg, text='☏', font=("Calibri", 20), fg=side_bar_fg, anchor='center', borderwidth=0, border=0, command=lambda: (CONV_AI_Widget.tkraise(), active(st7_bt)))
    st7_bt.place(relheight=0.03, relwidth=1, rely=0.93, relx=0)
    change_bg_OnHover(st7_bt, side_bar_bg_widget_houver_color, side_bar_bg)
    change_fg_OnHover(st7_bt, side_bar_fg_widget_houver_color, side_bar_fg)
    widget_list.append(st7_bt)

    st8_bt = tk.Button(side_bar, bg=side_bar_bg, text='⚙ ', font=("Calibri", 20, 'bold'), fg=side_bar_fg, anchor='center', borderwidth=0, border=0, command=lambda: (SETTINGS_Widget.tkraise(), active(st8_bt)))
    st8_bt.place(relheight=0.03, relwidth=1, rely=0.97, relx=0)
    change_bg_OnHover(st8_bt, side_bar_bg_widget_houver_color, side_bar_bg)
    change_fg_OnHover(st8_bt, side_bar_fg_widget_houver_color, side_bar_fg)
    widget_list.append(st8_bt)

    return Home_page_frame


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

    nav_bar_title_widget = tk.Label(nav_bar, bg=nav_bar_color, text=App_title, justify=tk.LEFT, anchor="w",
                                    font=("Forte", 20), borderwidth=0, border=0)
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

def main():
    global root, screen_width, screen_height, session, client_socket, server_IP4v_address, Server_listening_port
    global user_id, user_Photo, First_name, Second_Name, Last_Name, Email
    global gradient_ai_workspace_id, assemblyai_access_key, gradient_ai_access_key, keys

    access_keys_info()

    root = tk.Tk()
    root.title("Digital Scribe")
    root.state('zoomed')  # this creates a window that takes over the screen
    root.minsize(600, 500)

    screen_width = root.winfo_screenwidth()  # Get the screen width dimensions
    screen_height = root.winfo_screenheight()  # Get the screen height dimensions
    print(str(screen_width) + "\n" + str(screen_height))

    # dark_title_bar(root)

    User_Home_page(root)

    def on_closing():
            global session, root, closed
            closed = True
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
