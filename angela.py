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
    #self.controller = controller

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
    logo_label = tk.Label(Home_frame , image=logo_image)
    logo_label.image = logo_image
    logo_label.place(x=10, y=10)

    # Create a label for the title
    title_label = tk.Label(Home_frame, text="E-Government Services Prediction System",bg='white', font=('Arial Bold', 20))
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

# ======================================================================= Main function ==================================================================================
def Main():
    global widget_list
    app = tk.Tk()

    main_frame = tk.Frame(app, bg='white')
    main_frame.place(relwidth = 1, relheight = 1, relx = 0, rely = 0)
    widget_list.append(main_frame)



    #login_page(main_frame)
    Load_page(main_frame)



    #app.maxsize(1000, 500)
    app.mainloop()


if __name__ == "__main__":
    Main()


