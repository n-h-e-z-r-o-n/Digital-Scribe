import tkinter as tk
from tkinter import ttk

# Create a Tkinter window
root = tk.Tk()

# Create a Treeview widget
tree = ttk.Treeview(root, columns=("Column1", "Column2"))

# Set the background color using configure
tree.configure("Treeview", background="#F5F5F5")  # Replace with your desired color code

# Add some data (optional)
tree.heading("#0", text="Item")
tree.heading("Column1", text="Column 1")
tree.heading("Column2", text="Column 2")

tree.insert("", tk.END, values=("Item 1", "Value 1"))
tree.insert("", tk.END, values=("Item 2", "Value 2"))

# Pack the Treeview widget
tree.pack()

# Start the main loop
root.mainloop()