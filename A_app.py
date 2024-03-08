import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()

    # Set the call method to "auto" for automatic scaling
    root.call('tk', 'scaling', '')

    # Alternatively, you can set a fixed DPI scaling factor
    # root.tk.call('tk', 'scaling', 2.0)  # Adjust the scaling factor as needed

    # Create widgets using ttk for better scaling
    label = ttk.Label(root, text="Hello, Tkinter!")
    label.pack(pady=10)

    button = ttk.Button(root, text="Click Me")
    button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
