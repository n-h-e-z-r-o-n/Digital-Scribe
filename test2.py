import tkinter as tk

def title_bar_color(window, color):
    import ctypes as ct
    window.update()
    if color.startswith('#'):
        blue = color[5:7]
        green = color[3:5]
        red = color[1:3]
        color = blue + green + red
    else:
        blue = color[4:6]
        green = color[2:4]
        red = color[0:2]
        color = blue + green + red
    get_parent = ct.windll.user32.GetParent
    HWND = get_parent(window.winfo_id())

    color = '0x' + color
    color = int(color, 16)

    ct.windll.dwmapi.DwmSetWindowAttribute(HWND, 35, ct.byref(ct.c_int(color)), ct.sizeof(ct.c_int))

def create_floating_frame():
    # Create a new Toplevel window (floating frame)
    floating_frame = tk.Toplevel(root)
    floating_frame.attributes('-toolwindow', True)
    title_bar_color(floating_frame, "#344423")
    floating_frame.config(bg="#344423")
    floating_frame.geometry("300x200")  # Set the size of the floating frame
    floating_frame.title("Floating Frame")

    # Example content for the floating frame
    label = tk.Label(floating_frame, text="This is a floating frame", font=("Helvetica", 16))
    label.pack(pady=20)

    close_button = tk.Button(floating_frame, text="Close", command=floating_frame.destroy)
    close_button.pack(pady=10)

# Main application window
root = tk.Tk()
root.geometry("400x300")
title_bar_color(root, "#344423")
root.title("Main Application")

# Button to open the floating frame
open_button = tk.Button(root, text="Open Floating Frame", command=create_floating_frame)
open_button.pack(pady=50)

root.mainloop()
