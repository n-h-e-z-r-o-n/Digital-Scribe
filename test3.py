import tkinter as tk

def button_clicked():
    print("Button clicked!")

# Create a Tkinter window
root = tk.Tk()

# Create a button
button = tk.Button(root, text="Click Me", command=button_clicked)
button.pack()

# Function to programmatically trigger the button
def trigger_button():
    button.invoke()

# Create a button to trigger the first button
trigger_button = tk.Button(root, text="Trigger Button", command=trigger_button)
trigger_button.pack()

# Run the Tkinter event loop
root.mainloop()
