import tkinter as tk

def show_popup():
    # Create a new window for the pop-up list
    popup_window = tk.Toplevel(root)

    # Create a list of options
    options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]

    # Create a variable to store the selected option
    selected_option = tk.StringVar()

    # Set a default value for the variable
    selected_option.set(options[0])

    # Create a dropdown menu with the options
    dropdown = tk.OptionMenu(popup_window, selected_option, *options)
    dropdown.pack(padx=10, pady=10)

# Create the main window
root = tk.Tk()
root.title("Pop-up List Example")

# Create a button to show the pop-up list
popup_button = tk.Button(root, text="Show Pop-up List", command=show_popup)
popup_button.pack(padx=20, pady=20)

# Run the Tkinter event loop
root.mainloop()
