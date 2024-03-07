import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import re
import mysql.connector
import pandas as pd
import numpy as np
from sklearn.preprocessing import (LabelEncoder, OrdinalEncoder, MinMaxScaler)
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from itertools import cycle
import time
import threading
import io
import base64

# =========================================================== global Variables  ======================================================================================

widget_list = []


# ============================================================= Functions =============================================================================================

# Function to validate username
def validate_username(username):
    # Define a regular expression pattern for allowed characters in the username
    username_pattern = r'^[a-zA-Z0-9_-]{3,20}$'  # Allow letters (upper and lower case), digits, underscores,
    # and hyphens. Length between 3 and 20 characters.

    # Validate the username against the defined pattern
    if re.match(username_pattern, username):
        return True  # Username is valid
    else:
        return False  # Username is invalid


def imagen(image_path, screen_width, screen_height, widget): # image processing
    def load_image():
        try:
            image = Image.open(image_path)
        except Exception as e:
            try:
                image = Image.open(io.BytesIO(image_path))
            except Exception as e:
                print(e)
                binary_data = base64.b64decode(image_path)  # Decode the string
                image = Image.open(io.BytesIO(binary_data))

        image = image.resize((screen_width, screen_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        widget.config(image=photo)
        widget.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected

    image_thread = threading.Thread(target=load_image)  # Create a thread to load the image asynchronously
    image_thread.start()



# Function to validate password
def validate_password(password):
    # Define a regular expression pattern for allowed characters in the password
    # Require at least one uppercase letter, one lowercase letter, one digit, and one special character
    password_pattern = r'^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[@$!%?&])[A-Za-z\d@$!%?&]{8}$'

    # Validate the password against the defined pattern
    if re.match(password_pattern, password):
        return True  # Password is valid
    else:
        return False  # Password is invalid

"""
# Database connection
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='01@mawiA',
    port='3306',
    database='logindb'
)
c = connection.cursor()
"""

def login_page(widget):

    Login = tk.Frame(widget, bg='white')
    Login.place(x=0, y=0, relwidth=1, relheight=1)

    Label = tk.Label(Login, text="login_page", font=('Arial Bold', 30))
    Label.place(x=230, y=230)

    border = tk.LabelFrame(Login, text="Login", bg='ivory', bd=10, font=('Arial', 20))
    border.pack(fill='both', expand='yes', padx=150, pady=150)

    L1 = tk.Label(border, text="username", font=('Arial Bold', 15), bg='ivory')
    L1.place(x=50, y=20)
    T1 = tk.Entry(border, width=30, bd=5)
    T1.place(x=180, y=20)

    L2 = tk.Label(border, text="Password", font=('Arial Bold', 15), bg='ivory')
    L2.place(x=50, y=80)
    T2 = tk.Entry(border, show="*", width=30, bd=5)
    T2.place(x=180, y=80)

    def verify():
            '''if T1.get() == "angel" and T2.get() == "pass":
                controller.show_frame(train_page)
            else:
                messagebox.showinfo("Error", "please provide correct username and password")'''
            username = T1.get()
            password = T2.get()

            # Validate username and password
            if not validate_username(username):
                messagebox.showinfo('Error',
                                    'Invalid username format. Username must be 3-15 characters long and can only contain letters, numbers, underscores, and hyphens.')
                return
            if not validate_password(password):
                messagebox.showinfo('Error',
                                    'Invalid password format. Password must be 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.')
                return

            select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
            vals = (username, password,)
            c.execute(select_query, vals)
            user = c.fetchone()
            if user is not None:
                controller.show_frame(Load_page)
            else:
                messagebox.showinfo('Error', 'Enter a valid username & Password')

    B1 = tk.Button(border, text='Submit', font=('Arial', 15), command=verify)
    B1.place(x=320, y=115)

    def register():
            window = tk.Tk()
            window.resizable(0, 0)
            window.configure(bg="deep sky blue")
            window.title = ("Register")
            l1 = tk.Label(window, text="Username", font=("Arial", 15), bg="deep sky blue")
            l1.place(x=10, y=10)
            t1 = tk.Entry(window, width=30, bd=5)
            t1.place(x=200, y=10)

            l2 = tk.Label(window, text="password", font=("Arial", 15), bg="deep sky blue")
            l2.place(x=10, y=60)
            t2 = tk.Entry(window, show="*", width=30, bd=5)
            t2.place(x=200, y=60)

            l3 = tk.Label(window, text="Confirm password", font=("Arial", 15), bg="deep sky blue")
            l3.place(x=10, y=110)
            t3 = tk.Entry(window, show="*", width=30, bd=5)
            t3.place(x=200, y=110)

            def check():
                username = t1.get()
                password = t2.get()
                if t1.get() != "" or t2.get() != "" or t3.get() != "":
                    if t2.get() == t3.get():
                        if not validate_username(username):
                            messagebox.showinfo('Error',
                                                'Invalid username format. Username must be 3-20 characters long and can only contain '
                                                'letters numbers, underscores, and hyphens.')
                            return
                        if not validate_password(password):
                            messagebox.showinfo('Error',
                                                'Invalid password format. Password must be 8 characters long and contain at least one '
                                                'uppercase letter, one lowercase letter, one digit, and one special character.')
                            return
                        else:
                            select_query = "SELECT * FROM users WHERE username = %s"
                            c.execute(select_query, (username,))
                            user = c.fetchone()
                            if user is None:
                                insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
                                c.execute(insert_query, (username, password,))
                                connection.commit()
                                messagebox.showinfo('Success', 'Account created successfully!')
                    else:
                        messagebox.showinfo("Password didn't get match")
                else:
                    messagebox.showinfo("Error", "Please fill all the fields !")

            b1 = tk.Button(window, text='Sign up', font=("Arial", 15), bg="#ffc22a", command=check)
            b1.place(x=170, y=150)
            window.geometry("470x220")
            window.mainloop()

    B2 = tk.Button(Login, text='Register', font=('Arial', 15), bg="dark orange", command=register)
    B2.place(x=650, y=20)
    # =============================================LOAD DATA PIPELINE===============================================##


class DataUploader:
    def _init_(self, master):
        self.master = master

    def upload_data(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            print("Selected file:", file_path)
            return file_path

    def preprocess(self, file_path):
        # Check the file extension
        file_extension = file_path.split('.')[-1].lower()

        # Read the data based on the file extension
        if file_extension == 'csv':
            data = pd.read_csv(file_path)
        elif file_extension in ['xls', 'xlsx']:
            data = pd.read_excel(file_path)
        else:
            print(f"Unsupported file format: {file_extension}")
            return

        # ================================= INITIALIZE PREPROCESSING PIPELINE========================================#

        label_encoder = LabelEncoder()
        encoder = OrdinalEncoder()
        scaler = MinMaxScaler()
        current_date = datetime.now()

        # Preprocessing for 'Gender'
        data["Gender"] = label_encoder.fit_transform(data["gender"])
        data["newGender"] = scaler.fit_transform(data[['Gender']])
        data = data.drop(['gender', 'Gender'], axis=1)

        # Preprocessing for 'County'
        data['County'] = encoder.fit_transform(data[['residencecounty']])
        data['newCounty'] = scaler.fit_transform(data[['County']])
        data = data.drop(["residencecounty", "County"], axis=1)

        # Preprocessing for 'Station'
        data["station"] = label_encoder.fit_transform(data["stationname"])
        data['Center'] = scaler.fit_transform(data[['station']])
        data = data.drop(["station", "stationname"], axis=1)

        # Preprocessing for 'Booking'
        data["Booking"] = label_encoder.fit_transform(data["type"])
        data['Booking_method'] = scaler.fit_transform(data[['Booking']])
        data = data.drop(["type", "Booking"], axis=1)

        # Preprocessing for 'Birthplace'
        data["birthplace"] = label_encoder.fit_transform(data["placeofbirth"])
        data['hometown'] = scaler.fit_transform(data[['birthplace']])
        data = data.drop(["placeofbirth", "birthplace"], axis=1)

        # Handling problematic date values
        problematic_rows = data['dob'].isin(['0000-00-00', '\\N'])
        problematic_data = data[problematic_rows]
        data = data[~problematic_rows]
        data['dob'] = pd.to_datetime(data['dob'])

        # Calculate age
        data["Age"] = ((current_date - data['dob']) / np.timedelta64(1, 'Y')).astype(int)
        data = data.drop("dob", axis=1)
        return data


def Load_page(widget):

    Home_frame = tk.Frame(widget, bg='white')
    Home_frame.place(relheight=1, relwidth=1, relx=0, rely=0)
    widget_list.append(Home_frame)

    # Load and display background image
    '''background_image = Image.open("img.jpg").resize((800, 500), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)
    background_image = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(self, image=background_image)
    background_label.image = background_image
    background_label.pack(fill="both", expand=True)'''

    # Load and resize the logo image
    logo_image = Image.open("./Assets/pnad bg.png").resize((100, 100), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)
    logo_image = ImageTk.PhotoImage(logo_image)

    # Create a label with the resized logo image
    logo_label = tk.Label(Home_frame, image=logo_image)
    logo_label.image = logo_image
    logo_label.place(x=10, y=10)

    # Create a label for the title
    title_label = tk.Label(Home_frame, text="E-Government Services Prediction System",bg='green', font=('Arial Bold', 20))
    title_label.place(x=120, y=10)

    # Create buttons for uploading data and exploratory data analysis
    upload_button = tk.Button(Home_frame, text="Upload Data", bg="white", font=('Arial', 10) ) #, command=self.upload_and_preprocess)
    upload_button.place(x=10, y=120)

    eda_button = tk.Button(Home_frame, text="Exploratory Data Analysis", bg="white", font=('Arial', 10) ) #, command=self.perform_eda)
    eda_button.place(x=120, y=120)

    def upload_and_preprocess(self):
        data_uploader = DataUploader(self.master)
        file_path = data_uploader.upload_data()
        if file_path:
            preprocessed_data = data_uploader.preprocess(file_path)
            if preprocessed_data is not None:
                messagebox.showinfo("Success", "Data preprocessing completed successfully.")
                # Do something with preprocessed_data, e.g., pass it to the next page
                self.controller.preprocessed_data = preprocessed_data
                self.controller.show_frame(Load_page)
            else:
                messagebox.showerror("Error", "Failed to preprocess data.")

    def perform_eda(self):
        # Code to perform exploratory data analysis on preprocessed data
        if hasattr(self.controller, 'preprocessed_data'):
            preprocessed_data = self.controller.preprocessed_data
            # Perform exploratory data analysis here
            # You can display plots, summary statistics, etc.
            messagebox.showinfo("EDA", "Exploratory Data Analysis completed.")
        else:
            messagebox.showerror("Error", "Preprocessed data not found.")


class train_page(tk.Frame):
    def _init_(self, parent, controller):
        tk.Frame._init_(self, parent)

        Label = tk.Label(self, text="Train Model", font=('Arial Bold', 30))
        Label.place(x=230, y=230)

        Button = tk.Button(self, text='Home', font=('Arial', 15), command=lambda: controller.show_frame(login_page))
        Button.place(x=650, y=450)

        Button = tk.Button(self, text='Back', font=('Arial', 15), command=lambda: controller.show_frame(Load_page))
        Button.place(x=100, y=450)

        algorithm_label = tk.Label(self, text="Select Algorithm:", font=('Arial', 15))
        algorithm_label.place(x=100, y=300)

        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("Random Forest")  # Default algorithm
        algorithm_options = ["Random Forest", "Multiple Linear Regression"]
        algorithm_dropdown = ttk.OptionMenu(self, self.algorithm_var, *algorithm_options)
        algorithm_dropdown.place(x=270, y=300)

        train_button = tk.Button(self, text='Train_model', font=("Arial", 15), command=self.train_models)
        train_button.place(x=650, y=450)

        back_button = tk.Button(self, text='Back', font=('Arial', 15), command=lambda: controller.show_frame(Load_page))
        back_button.place(x=100, y=450)

    def train_models(self):
        algorithm = self.algorithm_var.get()
        if algorithm == "Random Forest":
            # Train Random Forest model
            rf_model = RandomForestRegressor()
            # Training code here...
            messagebox.showinfo("Success", "Random Forest model trained successfully.")
        elif algorithm == "Multiple Linear Regression":
            # Train Multiple Linear Regression model
            mlr_model = LinearRegression()
            # Training code here...
            messagebox.showinfo("Success", "Multiple Linear Regression model trained successfully.")
        else:
            messagebox.showerror("Error", "Invalid algorithm selected.")


"""
class Application(tk.Tk):
    def _init_(self, *args, **kwargs):
        tk.Tk._init_(self, *args, **kwargs)

        window = tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0, minsize=500)
        window.grid_columnconfigure(0, minsize=800)

        self.frames = {}
        for F in (login_page, Load_page, train_page):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(login_page)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()"""


def change_bg_OnHover(widget, colorOnHover, colorOnLeave):  # Color change bg on Mouse Hover
    global bg_color
    widget.bind("<Enter>", func=lambda e: widget.config(background=colorOnHover))
    widget.bind("<Leave>", func=lambda e: widget.config(background=bg_color))



def change_fg_OnHover(widget, colorOnHover, colorOnLeave):  # Color change fg on Mouse Hover
    global fg_color
    widget.bind("<Enter>", func=lambda e: widget.config(fg=colorOnHover))
    widget.bind("<Leave>", func=lambda e: widget.config(fg=fg_color))



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

    #password_entry_widg.bind('<Return>', lambda e: login_Request(Email_entry_widg.get(), password_entry_widg.get(), root_widget))
    #Email_entry_widg.bind('<Return>', lambda e: login_Request(Email_entry_widg.get(), password_entry_widg.get(), root_widget))

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

def Welcome_Page(wiget):
    global screen_width, screen_height

    welcome_page_frame = tk.Frame(wiget, bg='gray')
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
    change_Widget_Attribute_OnHover(nav_bar_bt4_widget, 'Log in ∧', 'Log in ∨', nav_bar_btn_hover_color, nav_bar_color, Login_Section_widget(welcome_page_frame, nav_bar_color))

    nav_bar_bt5_widget = tk.Button(nav_bar, bg=nav_bar_color, text='Get started', justify=tk.LEFT, anchor="center",
                                   font=("Calibri", 12), borderwidth=0, border=0)
    nav_bar_bt5_widget.place(relheight=0.6, relwidth=0.06, rely=0.2, relx=0.935)

# ======================================================================= Main function ==================================================================================

def Main():
    global widget_list
    app = tk.Tk()

    main_frame = tk.Frame(app, bg='white')
    main_frame.place(relwidth = 1, relheight = 1, relx = 0, rely = 0)
    widget_list.append(main_frame)

    Welcome_Page(main_frame)

    #login_page(main_frame)
    #Load_page(main_frame)
    #app.maxsize(1000, 500)
    app.mainloop()


if __name__ == "__main__":
    Main()


