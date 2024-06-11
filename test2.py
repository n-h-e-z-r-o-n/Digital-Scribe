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
    fg_color = "white"
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

    # --------------------------------------------------------------------------------------------------------------------------------------------------
    side_bar = tk.Frame(floating_frame, bg=bg_color)
    side_bar.place(relwidth=0.2, relheight=1, rely=0, relx=0)

    btn0  = tk.Button(side_bar, borderwidth=0, border=0, text="\tMEDICAL HISTORY", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: container0.tkraise())
    btn0.place(relheight=0.07, relwidth=1, relx=0,rely=0)
    btn1 = tk.Button(side_bar, borderwidth=0, border=0, text="\tALLERGIES", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: container1.tkraise())
    btn1.place(relheight=0.07, relwidth=1, relx=0, rely=0.07)
    btn2 = tk.Button(side_bar, borderwidth=0, border=0, text="\tEXAMINATION", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: container2.tkraise())
    btn2.place(relheight=0.07, relwidth=1, relx=0, rely=0.14)
    btn3 = tk.Button(side_bar, borderwidth=0, border=0, text="\tVITALS", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: container3.tkraise())
    btn3.place(relheight=0.07, relwidth=1, relx=0, rely=0.21)
    btn4 = tk.Button(side_bar, borderwidth=0, border=0, text="\tFOLLOW UPS", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: container4.tkraise())
    btn4.place(relheight=0.07, relwidth=1, relx=0, rely=0.28)

    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container0 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container0.place(relheight=1, relwidth=0.8, relx=0.2,rely=0)

    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container1 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container1.place(relheight=1, relwidth=0.8, relx=0.2, rely=0)

    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container2 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container2.place(relheight=1, relwidth=0.8, relx=0.2, rely=0)

    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container3 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container3.place(relheight=1, relwidth=0.8, relx=0.2, rely=0)

    lB_00 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color, text="BODY TEMPERATURE ('C)", anchor="sw", font=("Times New Roman", 11))
    lB_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0)
    EN_00 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EN_00.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.05)

    lB_11 = tk.Label(container3, borderwidth=0, border=0, text="Respiration Rate (BPM)", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11))
    lB_11.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0)
    EN_11 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EN_11.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.05)

    lB_00 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color, text="BODY TEMPERATURE", anchor="sw", font=("Times New Roman", 11))
    lB_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.14)
    EN_00 = tk.Entry(container3, borderwidth=0, border=1,  bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EN_00.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.19)

    lB_11 = tk.Label(container3, borderwidth=0, border=0, text="Respiration Rate (BPM)", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11))
    lB_11.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0.14)
    EN_11 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EN_11.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.19)

    lB_00 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color, text="BODY TEMPERATURE", anchor="sw", font=("Times New Roman", 11))
    lB_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.28)
    EN_00 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EN_00.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.33)

    lB_11 = tk.Label(container3, borderwidth=0, border=0, text="Respiration Rate (BPM)", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11))
    lB_11.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0.28)
    EN_11 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EN_11.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.33)

    lB_00 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color, text="BODY TEMPERATURE", anchor="sw", font=("Times New Roman", 11))
    lB_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.42)
    EN_00 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EN_00.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.47)

    lB_11 = tk.Label(container3, borderwidth=0, border=0, text="Respiration Rate (BPM)", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11))
    lB_11.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0.42)
    EN_11 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EN_11.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.47)

    lB_00 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color, text="BODY TEMPERATURE", anchor="sw", font=("Times New Roman", 11))
    lB_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.56)
    EN_00 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EN_00.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.61)

    lB_11 = tk.Label(container3, borderwidth=0, border=0, text="Respiration Rate (BPM)", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11))
    lB_11.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0.56)
    EN_11 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EN_11.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.61)

    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container4 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container4.place(relheight=1, relwidth=0.8, relx=0.2, rely=0)









# Main application window
root = tk.Tk()
root.geometry("400x300")
title_bar_color(root, "#344423")
root.title("Main Application")

# Button to open the floating frame
open_button = tk.Button(root, text="Open Floating Frame", command=create_floating_frame)
open_button.pack(pady=50)

root.mainloop()
