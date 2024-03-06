import tkinter as tk
bgd= 'yellow'
def refresh_widgets():
    global bgd
    bgd = 'green'
    root.update()

# Create the root window
root = tk.Tk()
frame = tk.Frame(root, bg=bgd)
frame.place(relwidth = 1, relheight = 1, relx = 0, rely = 0)
# Your widget creation and layout code goes here

# Example button to trigger widget refresh
refresh_button = tk.Button(frame, text="Refresh Widgets", command=refresh_widgets)
refresh_button.pack()

root.mainloop()