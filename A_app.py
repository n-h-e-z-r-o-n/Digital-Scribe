import tkinter as tk

root = tk.Tk()
root.title("")  # Set title to an empty string to minimize any impact on the width

total_height = root.winfo_screenheight()

# Get the height of the window content area
content_height = root.winfo_height()

# Calculate the title bar height
title_bar_height = total_height - content_height

print("{content_height} : {total_height} Title Bar Height:", title_bar_height)

root.mainloop()
