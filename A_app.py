import tkinter as tk

root = tk.Tk()
root.title("")  # Set title to an empty string to minimize any impact on the width

screen_width = root.winfo_screenwidth()
virtual_width = root.winfo_vrootwidth()

print("Screen Width:", screen_width)
print("Virtual Width:", virtual_width)

root.mainloop()
