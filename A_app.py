import tkinter as tk
bgd= 
def refresh_widgets():
    root.update()

# Create the root window
root = tk.Tk()

# Your widget creation and layout code goes here

# Example button to trigger widget refresh
refresh_button = tk.Button(root, text="Refresh Widgets", command=refresh_widgets)
refresh_button.pack()

root.mainloop()