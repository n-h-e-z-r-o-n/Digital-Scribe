import tkinter as tk

def disable_entry():
    entry_widget.configure(state='disabled', disabledbackground='blue' )

def enable_entry():
    entry_widget.configure(state='normal')

root = tk.Tk()
root.geometry("300x100")

entry_widget = tk.Entry(root)
entry_widget.pack()

disable_button = tk.Button(root, text="Disable Entry", command=disable_entry)
disable_button.pack()

enable_button = tk.Button(root, text="Enable Entry", command=enable_entry)
enable_button.pack()

root.mainloop()
