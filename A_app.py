import tkinter as tk

def on_drag(event):
    # Update the size of the panes based on the drag event
    paned_window.sash_place(1, event.x, event.y)

root = tk.Tk()
root.title("Resizable Widget Demo")

# Create a PanedWindow

F = tk.Frame(root, bg='black')
F.place(relheight=0.5, relwidth=0.5, relx=0.1, rely=0.1)
paned_window = tk.PanedWindow(F, bg='black', orient=tk.VERTICAL, sashwidth=8, sashrelief=tk.FLAT)
paned_window.place(relheight=0.96, relwidth=0.75, rely=0.03, relx=0.0253)


# Add widgets to the PanedWindow
widget1 = tk.Text(paned_window, bg="lightblue")
widget2 = tk.Text(paned_window, bg="lightgreen")

paned_window.add(widget1)
paned_window.add(widget2)

# Bind the motion event to the on_drag function
paned_window.bind("<B1-Motion>", on_drag)

root.mainloop()