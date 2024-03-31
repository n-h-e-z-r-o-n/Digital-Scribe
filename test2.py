import tkinter as tk
from time import strftime

def update_time():
    current_time = strftime('%H:%M:%S %p')
    print(current_time)
    label.config(text=current_time)
    label.after(1000, update_time)  # Update time every 1000 milliseconds (1 second)

# Create main window
root = tk.Tk()
root.title("Simple Clock")

# Create label to display time
label = tk.Label(root, font=('calibri', 40, 'bold'), background='purple', foreground='white')
label.pack(anchor='center')

# Call the function to update time
update_time()

root.mainloop()
