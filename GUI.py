import base64
import hashlib
import time
import socket
import tkinter as tk
import ctypes as ct
import threading
from PIL import Image, ImageTk
import shelve

# =============================== Server Details ============================================================================================
"""
server_domain_name = "inspiring-frost-18221.pktriot.net"
server_IP4v_address = socket.gethostbyname(server_domain_name)
Server_listening_port = 22575  # socket server port number
#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate
client_socket = None
#client_socket.connect((server_IP4v_address, Server_listening_port))  # connect to the server
"""

server_IP4v_address = "192.168.100.9"  #"127.0.0.1"  # as both code is running on same pc
Server_listening_port = 800  # socket server port number
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
client_socket = None
# client_socket.connect((server_IP4v_address, Server_listening_port))  # connect to the server

# =============================== Global variable decoration  ============================================================================================
root = None
screen_width: int
screen_height: int
widget_list: list = []
session = None
closed = False
user_id = None

# =============================== Functions definition ============================================================================================
# =================================================================================================================================================

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
    widget.bind("<Configure>", lambda e: on_frame_configure(widget, e))
    widget.bind_all("<MouseWheel>", lambda e: on_mouse_wheel(widget, e))


def on_mouse_wheel(widget, event):  # Function to handle mouse wheel scrolling
    # Scroll the canvas up or down based on the mouse wheel direction
    if event.delta < 0:
        widget.yview_scroll(1, "units")
    else:
        widget.yview_scroll(-1, "units")


def on_frame_configure(widget, event):  # Update the canvas scrolling region when the large frame changes size
    widget.configure(scrollregion=widget.bbox("all"))


def attach_scroll(widget):
    FRAME_2 = tk.Frame(widget, bg='black')
    FRAME_2.place(relwidth=1, relheight=1, relx=0, rely=0)
    canvas_FRAME_2 = tk.Canvas(FRAME_2, highlightthickness=0)  # Create a Canvas widget to hold the frame and enable scrolling
    canvas_FRAME_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    canvas_FRAME_2_scrollbar = tk.Scrollbar(widget, command=canvas_FRAME_2.yview)  # Create a Scrollbar and connect it to the Canvas
    canvas_FRAME_2.config(yscrollcommand=canvas_FRAME_2_scrollbar.set)
    canvas_FRAME_2_frame = tk.Frame(canvas_FRAME_2)  # Create a frame to hold your content of the canvers
    canvas_FRAME_2.create_window((0, 0), window=canvas_FRAME_2_frame, anchor=tk.NW)
    widget_scroll_bind(canvas_FRAME_2)  # Bind the mouse wheel event to the canvas
    return canvas_FRAME_2_frame, FRAME_2


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
    widget.bind("<Enter>", func=lambda e: widget.config(background=colorOnHover))
    widget.bind("<Leave>", func=lambda e: widget.config(background=colorOnLeave))


def change_fg_OnHover(widget, colorOnHover, colorOnLeave):  # Color change fg on Mouse Hover
    widget.bind("<Enter>", func=lambda e: widget.config(fg=colorOnHover))
    widget.bind("<Leave>", func=lambda e: widget.config(fg=colorOnLeave))


import io


def imagen(image_path, screen_width, screen_height, widget):
    def load_image():
        try:
            image = Image.open(image_path)
        except:
            image = Image.open(io.BytesIO(image_path))

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
    imagen('TEST/Xtest/12.png', 259, 307, hh)
    tk.Label(t2, bg=nav_bar_color, text='Services', font=("Bauhaus 93", 18)).place(relheight=0.15, relwidth=0.35, rely=0.04, relx=0.1)
    tk.Label(t2, bg=nav_bar_color, text='Get accesses to therapy, \nMedication Management, \nPersonalized treatment.', font=("Calibri", 15)).place(relheight=0.6, relwidth=0.45, rely=0.21, relx=0.05)

    t3 = tk.Frame(Service_widget, bg=nav_bar_color)
    t3.place(relheight=0.4, relwidth=0.15, rely=0.02, relx=0.35)
    tk.Label(t3, bg=nav_bar_color, text='Therapy', anchor='w', font=("Bauhaus 93", 18)).place(relheight=0.11, relwidth=1, rely=0, relx=0)

    t3_link_btn1 = tk.Button(t3, bg=nav_bar_color, text='Individual therapy', anchor='w', borderwidth=0, border=0, activebackground=nav_bar_color, font=("Calibri", 13))
    t3_link_btn1.place(relheight=0.1, relwidth=1, rely=0.12, relx=0)
    change_fg_OnHover(t3_link_btn1, 'brown', 'black')
    t3_link_btn2 = tk.Button(t3, bg=nav_bar_color, text='Couples Therapy', anchor='w', borderwidth=0, border=0, activebackground=nav_bar_color, font=("Calibri", 13))
    t3_link_btn2.place(relheight=0.1, relwidth=1, rely=0.23, relx=0)
    change_fg_OnHover(t3_link_btn2, 'brown', 'black')
    t3_link_btn3 = tk.Button(t3, bg=nav_bar_color, text='Therapy For Veterans', anchor='w', borderwidth=0, border=0, activebackground=nav_bar_color, font=("Calibri", 13))
    t3_link_btn3.place(relheight=0.1, relwidth=1, rely=0.34, relx=0)
    change_fg_OnHover(t3_link_btn3, 'brown', 'black')
    t3_link_btn4 = tk.Button(t3, bg=nav_bar_color, text='Messaging therapy', anchor='w', borderwidth=0, border=0, activebackground=nav_bar_color, font=("Calibri", 13))
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
    t4_link_btn3 = tk.Button(t4, bg=nav_bar_color, text='Bipolar disorder For Veterans', anchor='w', borderwidth=0, border=0, activebackground=nav_bar_color, font=("Calibri", 13))
    t4_link_btn3.place(relheight=0.1, relwidth=1, rely=0.34, relx=0)
    change_fg_OnHover(t4_link_btn3, 'brown', 'black')
    t4_link_btn4 = tk.Button(t4, bg=nav_bar_color, text='OCD', anchor='w', borderwidth=0, border=0, activebackground=nav_bar_color, font=("Calibri", 13))
    t4_link_btn4.place(relheight=0.1, relwidth=1, rely=0.45, relx=0)
    change_fg_OnHover(t4_link_btn4, 'brown', 'black')
    t4_link_btn5 = tk.Button(t4, bg=nav_bar_color, text='PTSD', anchor='w', borderwidth=0, border=0, activebackground=nav_bar_color, font=("Calibri", 13))
    t4_link_btn5.place(relheight=0.1, relwidth=1, rely=0.56, relx=0)
    change_fg_OnHover(t4_link_btn5, 'brown', 'black')
    t4_link_btn6 = tk.Button(t4, bg=nav_bar_color, text='Post-partum depression', anchor='w', borderwidth=0, border=0, activebackground=nav_bar_color, font=("Calibri", 13))
    t4_link_btn6.place(relheight=0.1, relwidth=1, rely=0.67, relx=0)
    change_fg_OnHover(t4_link_btn6, 'brown', 'black')
    t4_link_btn7 = tk.Button(t4, bg=nav_bar_color, text='Panic disorder', anchor='w', borderwidth=0, border=0, activebackground=nav_bar_color, font=("Calibri", 13))
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
    global client_socket, server_IP4v_address, Server_listening_port, session, user_id
    if (len(email) and len(passw)) > 3:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
        try:
            client_socket.connect((server_IP4v_address, Server_listening_port))  # connect to the server
        except:
            print('Error: Unable to connect')
        login_credentials = f'login_Request~{email}~{encrypt(passw)}'
        client_socket.send(login_credentials.encode("utf-8")[:1024])  # send message
        status = client_socket.recv(1024).decode("utf-8", errors="ignore")
        if status == 'User_Error':
            print('User_Error')
            client_socket.close()
        else:
            root_widget.destroy()
            user_id = status
            print('User_id: ', user_id)
            session['logged_in'] = True
            session['__id__'] = user_id
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

        tk.Label(Forgot_password_widget, bg=nav_bar_color, text='🔎', font=("Bahnschrift SemiLight Condensed", 36), borderwidth=0, border=0).place(relheight=0.1, relwidth=1, rely=0, relx=0)
        tk.Label(Forgot_password_widget, bg=nav_bar_color, text='Forgot your password?', font=("Bahnschrift SemiLight Condensed", 36), borderwidth=0, border=0).place(relheight=0.1, relwidth=1, rely=0.1, relx=0)
        tk.Label(Forgot_password_widget, bg=nav_bar_color, text='Please enter the email address you used to register.\nWe’ll send a link with instructions to reset your password', font=("Bahnschrift SemiLight Condensed", 12), borderwidth=0, border=0).place(relheight=0.12, relwidth=1, rely=0.2, relx=0)
        tk.Label(Forgot_password_widget, bg=nav_bar_color, text='email', anchor='w', font=("Batang", 9), borderwidth=0, border=0).place(relheight=0.03, relwidth=0.8, rely=0.395, relx=0.1)

        email_password_entry_widg = tk.Entry(Forgot_password_widget, bg=nav_bar_color, font=("Courier New", 13), relief="solid", borderwidth=1, border=1)
        email_password_entry_widg.place(relheight=0.1, relwidth=0.8, rely=0.43, relx=0.1)
        change_bg_OnHover(email_password_entry_widg, '#F5F5F5', nav_bar_color)

        password_reset__btn = tk.Button(Forgot_password_widget, bg='#1C352D', fg='white', activebackground='#8A9A5B', text='Request Password reset', font=('Aptos Narrow', 11, 'bold'), relief="solid", borderwidth=0, border=0)
        password_reset__btn.place(relheight=0.1, relwidth=0.8, rely=0.6, relx=0.1)
        change_bg_OnHover(password_reset__btn, '#004830', '#1C352D')

        tk.Label(Forgot_password_widget, bg=nav_bar_color, fg='black', activebackground='#8A9A5B', text='Need help?', font=('Aptos Narrow', 10), relief="solid", anchor='w', borderwidth=0, border=0).place(relheight=0.04, relwidth=0.2, rely=0.72, relx=0.1)
        Customer_support_link = tk.Button(Forgot_password_widget, bg=nav_bar_color, fg='#A8E4A0', activeforeground='#A8E4A0', activebackground=nav_bar_color, text='Customer support', font=('Aptos Narrow', 10, 'bold'), relief="solid", anchor='w', borderwidth=0, border=0)
        Customer_support_link.place(relheight=0.04, relwidth=0.3, rely=0.72, relx=0.31)
        change_fg_OnHover(Customer_support_link, '#00AB66', '#A8E4A0')

        tk.Label(Forgot_password_widget, bg=nav_bar_color, fg='black', activebackground='#8A9A5B', text='Go to Login?', font=('Aptos Narrow', 10), relief="solid", anchor='w', borderwidth=0, border=0).place(relheight=0.04, relwidth=0.2, rely=0.78, relx=0.1)
        Jump_to_login_link = tk.Button(Forgot_password_widget, bg=nav_bar_color, fg='#A8E4A0', activeforeground='#A8E4A0', activebackground=nav_bar_color, text='Login', font=('Aptos Narrow', 10, 'bold'), relief="solid", anchor='w', borderwidth=0, border=0, command=lambda: back(Forgot_password_widget))
        Jump_to_login_link.place(relheight=0.04, relwidth=0.3, rely=0.78, relx=0.31)
        change_fg_OnHover(Jump_to_login_link, '#00AB66', '#A8E4A0')
        return Forgot_password_widget

    tk.Label(Login_widget, text='Log in to your account', bg=nav_bar_color, font=("Bahnschrift SemiLight Condensed", 26), borderwidth=0, border=0).place(relheight=0.05, relwidth=0.25, rely=0.05, relx=0.03)
    tk.Label(Login_widget, text='Log in to continue your therapy journey \ntowards a happier, healthier you.', bg=nav_bar_color, font=("Bahnschrift SemiLight Condensed", 12), borderwidth=0, border=0).place(relheight=0.051, relwidth=0.25, rely=0.11, relx=0.03)

    tk.Label(Login_widget, bg=nav_bar_color, text='email', font=("Batang", 9), anchor='w', borderwidth=0, border=0).place(relheight=0.03, relwidth=0.07, rely=0.18, relx=0.05)
    Email_entry_widg = tk.Entry(Login_widget, bg=nav_bar_color, font=("Courier New", 13), relief="solid", borderwidth=1)
    Email_entry_widg.place(relheight=0.07, relwidth=0.2, rely=0.21, relx=0.05)
    change_bg_OnHover(Email_entry_widg, '#F5F5F5', nav_bar_color)

    tk.Label(Login_widget, bg=nav_bar_color, text='password', font=("Batang", 9), anchor='w', borderwidth=1, border=1).place(relheight=0.03, relwidth=0.07, rely=0.3, relx=0.05)
    password_entry_widg = tk.Entry(Login_widget, bg=nav_bar_color, font=("Courier New", 13), relief="solid", borderwidth=1)
    password_entry_widg.place(relheight=0.07, relwidth=0.2, rely=0.33, relx=0.05)
    change_bg_OnHover(password_entry_widg, '#F5F5F5', nav_bar_color)

    Forgot_password_login_link = tk.Button(Login_widget, bg=nav_bar_color, fg='#74C365', activebackground=nav_bar_color, text='Forgot password', font=("Bradley Hand ITC", 12, 'bold'), anchor='w', borderwidth=0, border=0, command=lambda: Forgot_pass().place(relheight=0.7, relwidth=0.25, rely=0.05, relx=0.03))
    Forgot_password_login_link.place(relheight=0.03, relwidth=0.1, rely=0.41, relx=0.05)
    change_fg_OnHover(Forgot_password_login_link, '#00AB66', '#A8E4A0')

    login_btn = tk.Button(Login_widget, bg='#1C352D', fg='white', activebackground='#8A9A5B', text='LOGIN', font=("Aptos", 15, 'bold'), borderwidth=1, border=0, command=lambda: login_Request(Email_entry_widg.get(), password_entry_widg.get(), root_widget))
    login_btn.place(relheight=0.06, relwidth=0.2, rely=0.5, relx=0.05)
    change_bg_OnHover(login_btn, '#004830', '#1C352D')

    tk.Label(Login_widget, bg=nav_bar_color, text="Don't have an account?", font=("Aptos Narrow", 10), anchor='w', borderwidth=0, border=0).place(relheight=0.03, relwidth=0.1, rely=0.6, relx=0.05)
    Sign_up_login_link = tk.Button(Login_widget, bg=nav_bar_color, fg='#A8E4A0', activeforeground='#A8E4A0', activebackground=nav_bar_color, text="Sign up", font=("Aptos Narrow", 11, 'bold'), anchor='w', borderwidth=0, border=0)
    Sign_up_login_link.place(relheight=0.03, relwidth=0.05, rely=0.6, relx=0.15)
    change_fg_OnHover(Sign_up_login_link, '#00AB66', '#A8E4A0')

    tk.Label(Login_widget, bg=nav_bar_color, text="Therapy Provider?", font=("Aptos Narrow", 10), anchor='w', borderwidth=0, border=0).place(relheight=0.03, relwidth=0.1, rely=0.65, relx=0.05)
    therapist_login_link = tk.Button(Login_widget, bg=nav_bar_color, fg='#A8E4A0', activeforeground='#A8E4A0', activebackground=nav_bar_color, text="Log in", font=("Aptos Narrow", 11, 'bold'), anchor='w', borderwidth=0, border=0)
    therapist_login_link.place(relheight=0.03, relwidth=0.05, rely=0.65, relx=0.15)
    change_fg_OnHover(therapist_login_link, '#00AB66', '#A8E4A0')

    img = tk.Label(Login_widget, bg=nav_bar_color, font=("Bahnschrift SemiLight Condensed", 26), borderwidth=0, border=0)
    img.place(relheight=0.9, relwidth=0.65, rely=0.05, relx=0.3)
    imagen('./login_pic.png', int(screen_width * 1 * 0.65), int(screen_height * 2 * 0.3 * 0.9), img)

    return Login_widget


def chat(widget):
    chatbot_widget = tk.Label(widget, bg="blue", font=("Calibri", 20, "bold"), anchor='center', borderwidth=0, border=0)
    chatbot_widget.place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253)
    tk.Entry(chatbot_widget).pack()
    return chatbot_widget


def call(widget):


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
        global t1_list

        def tab_widget(widget):
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

            t1 = tk.Frame(widget, bg=widgets_bg_color, relief="solid", borderwidth=0, border=0)
            t1.place(relheight=0.106, relwidth=1, rely=pos, relx=0)
            t1.bind("<Button-1>", lambda m=t1: active(t1))
            t1.bind("<Enter>", func=lambda e: change_2(t1))
            t1.bind("<Leave>", func=lambda e: change_1(t1))
            t1_list.append(t1)

            t2 = tk.Label(t1, bg=widgets_bg_color, text='👤', font=("Calibri", 40, "bold"), activebackground=widgets_bg_color, borderwidth=0, border=0)
            t2.place(relheight=0.8, relwidth=0.3, rely=0.1, relx=0.05)
            t2.bind("<Button-1>", lambda m=t1: active(t1))

            t3 = tk.Label(t1, bg=widgets_bg_color, text='Dr. Hezron Wekesa', font=("Calibri", 12, "bold"), activebackground=widgets_bg_color, anchor="w", borderwidth=0, border=0)
            t3.place(relheight=0.3, relwidth=0.6, rely=0.1, relx=0.36)
            t3.bind("<Button-1>", lambda m=t1: active(t1))


        i = 0
        pos = 0
        t1_list = []
        while i < 9:
            tab_widget(widget)
            pos += 0.106
            i += 1

    def active(widget):
        global t1_list
        for i in t1_list:
            if i != widget:
                i.config( borderwidth=0, border=0)
            else:
                i.config(borderwidth=0, border=2)



    widgets_bg_color = '#DFDFD5'
    call_widget = tk.Label(widget, bg="#F2F7FD", font=("Calibri", 20, "bold"), anchor='center', borderwidth=0, border=0)
    call_widget.place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253)

    # ===========================  Display contacts ================================

    display_contacts_widget = tk.Frame(call_widget, bg=widgets_bg_color, borderwidth=0, border=0)
    display_contacts_widget.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.05)

    tk.Label(display_contacts_widget, bg=widgets_bg_color, text="🔍", font=("Courier New", 22), anchor="e" , relief="solid", borderwidth=0, border=0).place(relheight=0.04, relwidth=0.2, rely=0, relx=0)

    contact_search_entry_widg = tk.Entry(display_contacts_widget, bg=widgets_bg_color, fg="gray", insertbackground="blue", font=('Georgia', 12), relief="solid", borderwidth=0, border=0)
    contact_search_entry_widg.place(relheight=0.04, relwidth=0.79, rely=0.0, relx=0.2)
    contact_search_entry_widg.insert(0, 'Search or start a new call')
    contact_search_entry_widg.bind("<FocusIn>", lambda e: on_entry_click(contact_search_entry_widg, e))
    contact_search_entry_widg.bind("<FocusOut>", lambda e: on_focusout(contact_search_entry_widg, e))

    contacts_hold_widget = tk.Frame(display_contacts_widget, bg=widgets_bg_color, borderwidth=0, border=0)
    contacts_hold_widget.place(relheight=0.959, relwidth=1, rely=0.041, relx=0)

    display_contacts(contacts_hold_widget)

    # ===========================  Display selected contact ================================

    display_selected_contact = tk.Frame(call_widget, bg=widgets_bg_color, relief="solid", borderwidth=0, border=0)
    display_selected_contact.place(relheight=0.9, relwidth=0.7, rely=0.05, relx=0.26)

    bar = tk.Frame(display_selected_contact, bg=widgets_bg_color, relief="solid", borderwidth=0, border=0)
    bar.place(relheight=0.05, relwidth=1, rely=0, relx=0)

    tk.Label(bar, bg=widgets_bg_color, text="👤", font=("Courier New", 22),  relief="solid", borderwidth=0, border=0).place(relheight=1, relwidth=0.051, rely=0, relx=0)

    tk.Label(bar, bg=widgets_bg_color, fg="gray", text="Dr. Hezron Wekesa Nangulu", anchor="w", font=("Calibri", 12),  borderwidth=0, border=0).place(relheight=0.5, relwidth=0.3, rely=0, relx=0.051)

    tk.Button(bar, bg=widgets_bg_color, text="📞", font=("Courier New", 17),  borderwidth=0, border=0).place(relheight=0.6, relwidth=0.035, rely=0.2, relx=0.92)
    tk.Button(bar, bg=widgets_bg_color, text="🎥", font=("Courier New", 17),  borderwidth=0, border=0).place(relheight=0.6, relwidth=0.035, rely=0.2, relx=0.96)







    return call_widget


def profile(widget):
    profile_widget = tk.Label(widget, bg="brown", font=("Calibri", 20, "bold"), anchor='center', borderwidth=0, border=0)
    profile_widget.place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253)
    tk.Entry(profile_widget).pack()
    return profile_widget


def conversation(widget):
    conversation_widget = tk.Label(widget, bg="yellow", font=("Calibri", 20, "bold"), anchor='center', borderwidth=0, border=0)
    conversation_widget.place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253)
    tk.Entry(conversation_widget).pack()
    return conversation_widget


def settings(widget):
    setting_widget = tk.Label(widget, bg="lightblue", font=("Calibri", 20, "bold"), anchor='center', borderwidth=0, border=0)
    setting_widget.place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253)
    return setting_widget


def connect_to_server():
    def connect():
        global client_socket, server_IP4v_address, Server_listening_port, closed
        while not closed:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
                client_socket.connect((server_IP4v_address, Server_listening_port))
                print(" Connection Established ")
                break
            except:
                pass
    threading.Thread(target=connect).start()


def fetch_info():
    global client_socket, user_id
    sign_up_credentials = f'active~{user_id}'
    client_socket.send(sign_up_credentials.encode("utf-8")[:1024])  # send message



def User_Home_page(widget):
    global user_id
    user_page_widget, user_page_root = attach_scroll(widget)
    Home_page_frame = tk.Frame(user_page_widget, bg='black', width=screen_width, height=screen_height)
    Home_page_frame.pack(fill=tk.BOTH, expand=True)

    nav_bar_color = 'white'
    nav_bar_btn_hover_color = '#F5F5F5'
    nav_bar = tk.Frame(Home_page_frame, bg=nav_bar_color)
    nav_bar.place(relheight=0.02, relwidth=1, rely=0, relx=0)

    nav_bar_bt5_widget = tk.Button(nav_bar, bg=nav_bar_color, activebackground=nav_bar_color, text='Sign Out', justify=tk.LEFT, anchor="center", font=("Calibri", 12), command=lambda: sign_out(user_page_root), borderwidth=0, border=0)
    nav_bar_bt5_widget.place(relheight=0.8, relwidth=0.06, rely=0.1, relx=0.935)
    change_bg_OnHover(nav_bar_bt5_widget, nav_bar_btn_hover_color, nav_bar_color)


    profile_widget = tk.Label(Home_page_frame, bg=nav_bar_color, text='Profile', font=("Calibri", 12), anchor='center', borderwidth=0, border=0)
    profile_widget.place(relheight=0.055, relwidth=0.055, rely=0.022, relx=0.94)
    #imagen(binary_data, int(screen_width * 1 * 0.055), int(screen_height * 1 * 0.055), profile_widget)

    side_bar_bg = "#F5F5F5"
    side_bar_fg = "Black"
    side_bar_houver_color = "#FFFAFA"
    side_bar = tk.Label(Home_page_frame, bg=side_bar_bg, font=("Calibri", 20, "bold"), anchor='center', borderwidth=0, border=0)
    side_bar.place(relheight=0.96, relwidth=0.025, rely=0.02, relx=0)

    def active(widget):
        print(len(widget_list))
        for i in widget_list:
            if i != widget:
                print(' not found')
                i.config(bg=side_bar_bg)
                change_bg_OnHover(i, side_bar_houver_color, side_bar_bg)
            else:
                print('found')
                i.config(bg="#F3DECA")
                change_bg_OnHover(i, '#F3DECA', '#F3DECA')

    PROFILE_widget = profile(Home_page_frame)

    CHAT_Widget = chat(Home_page_frame)
    CONV_AI_Widget = conversation(Home_page_frame)
    SETTINGS_Widget = settings(Home_page_frame)
    CALL_Widget = call(Home_page_frame)

    profile_widget = tk.Button(side_bar, bg=side_bar_bg, text='👤', font=("Calibri", 20), anchor='center', borderwidth=0, border=0, command=lambda: (PROFILE_widget.tkraise(), active(profile_widget)))
    profile_widget.place(relheight=0.03, relwidth=1, rely=0.01, relx=0)
    change_bg_OnHover(profile_widget, side_bar_houver_color, side_bar_bg)
    widget_list.append(profile_widget)

    st1_bt = tk.Button(side_bar, bg=side_bar_bg, text='📞', font=("Calibri", 20), anchor='center', borderwidth=0, border=0, command=lambda: (CALL_Widget.tkraise(), active(st1_bt)))
    st1_bt.place(relheight=0.03, relwidth=1, rely=0.05, relx=0)
    change_bg_OnHover(st1_bt, side_bar_houver_color, side_bar_bg)
    widget_list.append(st1_bt)
    st2_bt = tk.Button(side_bar, bg=side_bar_bg, text='🎥', font=("Calibri", 20), anchor='center', borderwidth=0, border=0, command=lambda: (CHAT_Widget.tkraise(), active(st2_bt)))
    st2_bt.place(relheight=0.03, relwidth=1, rely=0.09, relx=0)
    change_bg_OnHover(st2_bt, side_bar_houver_color, side_bar_bg)
    widget_list.append(st2_bt)
    st3_bt = tk.Button(side_bar, bg=side_bar_bg, text='📩', font=("Calibri", 20), anchor='center', borderwidth=0, border=0, command=lambda: (CONV_AI_Widget.tkraise(), active(st3_bt)))
    st3_bt.place(relheight=0.03, relwidth=1, rely=0.13, relx=0)
    change_bg_OnHover(st3_bt, side_bar_houver_color, side_bar_bg)
    widget_list.append(st3_bt)
    st4_bt = tk.Button(side_bar, bg=side_bar_bg, text='☏', font=("Calibri", 20), anchor='center', borderwidth=0, border=0, command=lambda: (CONV_AI_Widget.tkraise(), active(st4_bt)))
    st4_bt.place(relheight=0.03, relwidth=1, rely=0.17, relx=0)
    change_bg_OnHover(st4_bt, side_bar_houver_color, side_bar_bg)
    widget_list.append(st4_bt)
    st5_bt = tk.Button(side_bar, bg=side_bar_bg, text='☏', font=("Calibri", 20), anchor='center', borderwidth=0, border=0, command=lambda: (CONV_AI_Widget.tkraise(), active(st5_bt)))
    st5_bt.place(relheight=0.03, relwidth=1, rely=0.21, relx=0)
    change_bg_OnHover(st5_bt, side_bar_houver_color, side_bar_bg)
    widget_list.append(st5_bt)

    st6_bt = tk.Button(side_bar, bg=side_bar_bg, text='☏', font=("Calibri", 20), anchor='center', borderwidth=0, border=0, command=lambda: (CONV_AI_Widget.tkraise(), active(st6_bt)))
    st6_bt.place(relheight=0.03, relwidth=1, rely=0.89, relx=0)
    change_bg_OnHover(st6_bt, side_bar_houver_color, side_bar_bg)
    widget_list.append(st6_bt)
    st7_bt = tk.Button(side_bar, bg=side_bar_bg, text='☏', font=("Calibri", 20), anchor='center', borderwidth=0, border=0, command=lambda: (CONV_AI_Widget.tkraise(), active(st7_bt)))
    st7_bt.place(relheight=0.03, relwidth=1, rely=0.93, relx=0)
    change_bg_OnHover(st7_bt, side_bar_houver_color, side_bar_bg)
    widget_list.append(st7_bt)
    st8_bt = tk.Button(side_bar, bg=side_bar_bg, text='⚙', font=("Calibri", 17), anchor='center', borderwidth=0, border=0, command=lambda: (SETTINGS_Widget.tkraise(), active(st8_bt)))
    st8_bt.place(relheight=0.03, relwidth=1, rely=0.97, relx=0)
    change_bg_OnHover(st8_bt, side_bar_houver_color, side_bar_bg)
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

    nav_bar_bt4_widget = tk.Button(nav_bar, bg=nav_bar_color, text='Log in ∨', justify=tk.LEFT, anchor="center", font=("Calibri", 12), borderwidth=0, border=0)
    nav_bar_bt4_widget.place(relheight=0.6, relwidth=0.05, rely=0.2, relx=0.87)
    change_Widget_Attribute_OnHover(nav_bar_bt4_widget, 'Log in ∧', 'Log in ∨', nav_bar_btn_hover_color, nav_bar_color, Login_Section_widget(welcome_page_frame, welcome_page_root))

    nav_bar_bt5_widget = tk.Button(nav_bar, bg=nav_bar_color, text='Get started', justify=tk.LEFT, anchor="center", font=("Calibri", 12), borderwidth=0, border=0)
    nav_bar_bt5_widget.place(relheight=0.6, relwidth=0.06, rely=0.2, relx=0.935)


# =============================== Main Function definition =========================================================================================
# ==================================================================================================================================================

def main():
    global root, screen_width, screen_height, session, client_socket, server_IP4v_address, Server_listening_port, user_id
    root = tk.Tk()
    root.title("Digital Scribe")
    root.state('zoomed')  # this creates a window that takes over the screen
    root.minsize(1500, 500)
    root.config(bg="green")

    screen_width = root.winfo_screenwidth()  # Get the screen width dimensions
    screen_height = root.winfo_screenheight()  # Get the screen height dimensions
    print(str(screen_width) + "\n" + str(screen_height))

    # dark_title_bar(root)

    session = shelve.open("session.db")
    try:
        if session['logged_in']:
            user_id = session['__id__']
            User_Home_page(root)
        else:
            Welcome_Page(root)
    except Exception as e:
        session['logged_in'] = False
        Welcome_Page(root)

    connect_to_server()

    def on_closing():
        global session, client_socket, root , closed
        closed = True
        session.close()
        client_socket.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
