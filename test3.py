import tkinter as tk

def duplicate_widget(widget, dest_frame):
    # Get widget properties
    x, y = widget.winfo_x(), widget.winfo_y()

    relx = widget.place_info()["relx"]
    rely = widget.place_info()["rely"]

    
    dest_width = dest_frame.winfo_width()
    print(relx)
    print(rely)
    dest_height = dest_frame.winfo_height()


    widget_type = type(widget)
    widget_geometry = widget.winfo_geometry()
    widget_text = widget.cget("text")
    widget_command = widget.cget("command")
    widget_state = widget.cget("state")

    # Create a new instance of the widget with the same properties
    duplicate = widget_type(dest_frame)
    duplicate.config(text=widget_text, command=widget_command, state=widget_state)

    # Place the new widget at the same position as the original
    #duplicate.place(relx=0.4, rely=0.4)
    duplicate.place(x=x, y=y)
    #duplicate.geometry(widget_geometry)


# Create a Tkinter window
root = tk.Tk()


Frame1 = tk.Frame(root, bg='red')
Frame1.place(relheight=1,relwidth=0.5, rely=0, relx=0)

Frame2 = tk.Frame(root, bg='green')
Frame2.place(relheight=1,relwidth=0.5, rely=0, relx=0.5)

button = tk.Button(root, text="Click Me", command=lambda: duplicate_widget(duplicate_b, Frame2))
button.pack()


duplicate_b= tk.Button(Frame1, text="hELLO")
duplicate_b.place(relwidth=0.1, relheight=0.1, rely=0.4, relx=0.2)



root.mainloop()
