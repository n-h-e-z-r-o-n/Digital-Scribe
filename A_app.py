import tkinter as tk

root = tk.Tk()
root.title("")  # Set title to an empty string to minimize any impact on the width

total_height = root.winfo_screenheight()

# Get the height of the window content area
content_height = root.winfo_height()

# Calculate the title bar height
title_bar_height = total_height - content_height

print(f"{content_height} : {total_height} Title Bar Height:", title_bar_height)
print('root.winfo_x() = ', root.winfo_height())
print('root.winfo_y() = ', root.winfo_y())
print('root.geometry() = ', root.geometry())

root.mainloop()
