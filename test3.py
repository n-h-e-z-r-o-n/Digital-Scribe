import tkinter as tk
from tkinter import ttk

def on_scroll(*args):
    canvas.yview(*args)
    frame.yview(*args)

root = tk.Tk()
root.title("Scrollbar Example")

# Create a Canvas widget
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a scrollbar
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=on_scroll)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Link scrollbar to canvas and frame
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame within the canvas
frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

# Add some widgets to the frame (for demonstration)
for i in range(50):
    ttk.Label(frame, text="Label {}".format(i)).pack()

# Bind mousewheel scrolling (optional)
def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

# Update canvas scrolling region
frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

root.mainloop()
