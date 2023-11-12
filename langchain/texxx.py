import tkinter as tk

def on_enter_pressed(event):
    # Event handler for the Enter key
    entered_text = entry.get()
    print("Text entered:", entered_text)

# Create the main window
root = tk.Tk()
root.title("Enter Key Example")

# Create an Entry widget
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Bind the Enter key to the on_enter_pressed function
entry.bind('<Return>', lambda e: on_enter_pressed(e))

# Run the Tkinter event loop
root.mainloop()

