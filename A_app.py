import tkinter as tk

def resize(event):
    # Prevent resizing by setting the widget's size to its original size
    widget.config(width=original_width)
    widget2.config(width=original_width)
    print("resized")

root = tk.Tk()
root.title("Resizable Widget Demo")
screen_width = root.winfo_screenwidth()  # Get the screen width dimensions
screen_height = root.winfo_screenheight()  # Get the screen height dimensions
# Set the original size of the widget
original_width = int(screen_width * 0.01)


# Create a frame to contain the widget
frame = tk.Frame(root)
frame.pack(expand=True, fill="both")

# Create the widget (e.g., a label)
widget = tk.Label(frame, text="Resizable Widget", bg="lightblue", width=original_width, height=screen_height)
widget.place(rely=0, relx=0.1, relheight=1)


widget2 = tk.Label(frame, text="Resizable Widget", bg="lightblue", width=original_width, height=screen_height)
widget2.place(rely=0, relx=0.2, relheight=1)

# Bind the resize event to the function that prevents resizing
root.bind("<Configure>", resize)

root.mainloop()
