import tkinter as tk
from tkinter import messagebox

def create_text_widget(root):
    text_widget = tk.Text(root, undo=True, wrap='word')
    text_widget.pack(expand=True, fill='both')
    return text_widget

def undo_action(event=None):
    try:
        text_widget.edit_undo()
    except tk.TclError:
        messagebox.showinfo("Info", "Nothing to undo")

def redo_action(event=None):
    try:
        text_widget.edit_redo()
    except tk.TclError:
        messagebox.showinfo("Info", "Nothing to redo")

def add_menu(root, text_widget):
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    edit_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Undo", command=undo_action, accelerator="Ctrl+Z")
    edit_menu.add_command(label="Redo", command=redo_action, accelerator="Ctrl+Y")

    root.bind_all("<Control-z>", undo_action)
    root.bind_all("<Control-y>", redo_action)

# Set up the main application window
root = tk.Tk()
root.title("Text Editor with Undo/Redo")

# Create the Text widget
text_widget = create_text_widget(root)

# Add the menu for undo and redo
add_menu(root, text_widget)

# Run the application
root.mainloop()
