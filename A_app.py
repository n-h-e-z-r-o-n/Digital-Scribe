import tkinter as tk

def disable_cursor_disappearing(entry_widget):
    # Set the insertontime attribute to a high value to prevent cursor disappearing
    entry_widget.config(insertontime=0)

root = tk.Tk()

# Create an Entry widget
entry_widget = tk.Entry(root)
entry_widget.pack()

# Call the function to disable cursor disappearing
disable_cursor_disappearing(entry_widget)

root.mainloop()
