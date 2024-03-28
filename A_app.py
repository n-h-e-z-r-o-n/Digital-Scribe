import tkinter as tk

def on_drag(event):
    # Update the size of the panes based on the drag event
    paned_window.sash_place(1, event.x, event.y)

root = tk.Tk()
root.title("Resizable Widget Demo")

# Create a PanedWindow

F = tk.Frame(root)
F.place(relheight=0.5, relwidth=0.5, relx=0.1, rely=0.1)
paned_window = tk.PanedWindow(F, orient=tk.VERTICAL, sashwidth=8, sashrelief=tk.RAISED)
paned_window.pack(fill=tk.BOTH, expand=True)

# Add widgets to the PanedWindow
widget1 = tk.Label(paned_window, text="Resizable Widget 1", bg="lightblue")
widget2 = tk.Label(paned_window, text="Resizable Widget 2", bg="lightgreen")

paned_window.add(widget1)
paned_window.add(widget2)

# Bind the motion event to the on_drag function
paned_window.bind("<B1-Motion>", on_drag)

root.mainloop()