import tkinter as tk
from tkinter import ttk

def on_checkbox_click():
    if chk_var.get():
        print("Checkbox is checked")
    else:
        print("Checkbox is unchecked")

# Create the main application window
root = tk.Tk()
root.title("Custom Checkbox Example")

# Create a Tkinter variable to hold the checkbox state
chk_var = tk.BooleanVar()

# Create a custom style for the checkbox
style = ttk.Style()
style.configure("Custom.TCheckbutton", background="black", foreground="green")

# Create the custom checkbox
checkbox = ttk.Checkbutton(root, variable=chk_var, style="Custom.TCheckbutton", command=on_checkbox_click)
checkbox.place(relx=0.8,  rely=0.2, relwidth=0.1, relheight=0.1)

# Run the Tkinter event loop
root.mainloop()
