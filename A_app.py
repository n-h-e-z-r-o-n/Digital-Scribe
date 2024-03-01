import tkinter as tk

def get_button_text():
    button_text = button.cget("text")
    print("Button Text:", button_text)

# Create the main window
root = tk.Tk()
root.title("Get Button Text Example")

# Create a Button widget
button = tk.Button(root, text="Click Me", command=get_button_text)
button.pack(padx=20, pady=20)

# Run the Tkinter event loop
root.mainloop()
