import tkinter as tk
from tkinter import filedialog

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            file_content = file.read()
            text_area.delete('1.0', tk.END)  # Clear previous content
            text_area.insert(tk.END, file_content)

# Create the main application window
root = tk.Tk()
root.title("File Upload Example")

# Create a button to open the file dialog
open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack(pady=10)

# Create a text area to display the file content
text_area = tk.Text(root, height=20, width=50)
text_area.pack(fill=tk.BOTH, expand=True)

root.mainloop()
