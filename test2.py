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

floating_frame = None

def create_floating_frame():
    global floating_frame
    bg_color = "#344423"
    if floating_frame is not None:
        if floating_frame.winfo_exists():
            floating_frame.deiconify()
            return
        else:
            floating_frame = None

    # Create a new Toplevel window (floating frame)

    floating_frame = tk.Toplevel(root)
    floating_frame.attributes('-toolwindow', True)
    title_bar_color(floating_frame, bg_color)
    floating_frame.config(bg=bg_color)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    frame_width = int(screen_width * 3 / 4)
    frame_height = int(screen_height * 3 / 4)

    # Calculate the position to center the frame on the screen

    x_position = (screen_width // 2) - (frame_width // 2)
    y_position = (screen_height // 2) - (frame_height // 2)

    floating_frame.geometry(f"{frame_width}x{frame_height}+{x_position}+{y_position}")  # Set the size of the floating frame
    floating_frame.title("Floating Frame")

    side_bar = tk.Frame(floating_frame)
    side_bar.place(relwidth=0.2, relheight=1, rel)











# Main application window
root = tk.Tk()
root.geometry("400x300")
title_bar_color(root, "#344423")
root.title("Main Application")

# Button to open the floating frame
open_button = tk.Button(root, text="Open Floating Frame", command=create_floating_frame)
open_button.pack(pady=50)

root.mainloop()
