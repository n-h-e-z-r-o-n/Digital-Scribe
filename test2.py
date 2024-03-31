import tkinter as tk
from time import strftime

miniute = 0
hour = 0
sec = 0
def update_time(widget):
    global sec, miniute, hour
    time = f"{hour}:{miniute}:{sec}"
    sec = sec + 1
    if sec == 60:
        sec = 0
        miniute = miniute + 1
        if miniute == 60:
            miniute = 0
            hour = hour + 1
    widget.config(text=time)
    widget.after(1000, update_time)  # Update time every 1000 milliseconds (1 second)

# Create main window
root = tk.Tk()
root.title("Simple Clock")

# Create label to display time
label = tk.Label(root, font=('calibri', 40, 'bold'), background='purple', foreground='white')
label.pack(anchor='center')

# Call the function to update time
update_time()

root.mainloop()
