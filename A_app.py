import tkinter as tk

def on_checkbox_click():
    if chk_var.get():
        print("Checkbox is checked")
    else:
        print("Checkbox is unchecked")

# Create the main application window
root = tk.Tk()
root.title("Checkbox Example")

# Create a Tkinter variable to hold the checkbox state
chk_var = tk.BooleanVar()

# Create the checkbox
checkbox = tk.Checkbutton(root, text="Check me", variable=chk_var, command=on_checkbox_click)
checkbox.pack()

# Run the Tkinter event loop
root.mainloop()
