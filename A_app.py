import tkinter as tk

def change_insertion_color(entry_widget, color):
    # Set the insertbackground option to the desired color
    entry_widget.config(insertbackground=color)

root = tk.Tk()

# Create an Entry widget
entry_widget = tk.Entry(root)
entry_widget.pack()

# Call the function to change insertion cursor color
change_insertion_color(entry_widget, "red")

root.mainloop()
