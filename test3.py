import tkinter as tk

def duplicate_widget(widget):
    # Get widget properties
    widget_type = type(widget)
    widget_geometry = widget.winfo_geometry()
    widget_text = widget.cget("text")
    widget_command = widget.cget("command")
    widget_state = widget.cget("state")

    # Create a new instance of the widget with the same properties
    duplicate = widget_type(widget.master)
    duplicate.config(text=widget_text, command=widget_command, state=widget_state)

    # Place the new widget at the same position as the original
    duplicate.place(x=0, y=0)
    duplicate.geometry(widget_geometry)

    return duplicate

# Create a Tkinter window
root = tk.Tk()

# Create a button widget
button = tk.Button(root, text="Click Me", command=lambda: print("Button clicked!"))
button.pack()

# Function to duplicate the button
def duplicate_button():
    global button
    button = duplicate_widget(button)

button = tk.Frame(root)
button.place(relheight=1,relwidth=0.5, r)

button = tk.Button(root, text="Click Me", command=lambda: print("Button clicked!"))
button.pack()

root.mainloop()
