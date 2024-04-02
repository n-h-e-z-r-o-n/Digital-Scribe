import tkinter as tk

def on_drag(event):
    # Update the size of the panes based on the drag event
    paned_window.sash_place(1, event.x, event.y)

root = tk.Tk()
root.title("Resizable Widget Demo")

# Create a PanedWindow
paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=8, sashrelief=tk.RAISED)
paned_window.pack(fill=tk.BOTH, expand=True)

# Add widgets to the PanedWindow
widget1 = tk.Frame(paned_window,  bg="lightblue")
widget2 = tk.Frame(paned_window,  bg="lightgreen")

paned_window.add(widget1, )
paned_window.add(widget2)

# Bind the motion event to the on_drag function
paned_window.bind("<B1-Motion>", on_drag)

root.mainloop()