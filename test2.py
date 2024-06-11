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
    global side_bar_list
    def Show_PopUp(widget0, widget, qestion):

        pop_ = tk.Frame(widget0, bg="blue")
        relx = widget.place_info()["relx"]
        rely = widget.place_info()["rely"]
        relwidth = widget.place_info()["relwidth"]

        relheight = widget.place_info()["relheight"]

        rely = float( float(rely) + float(relheight))
        relheight = float(float(relheight) + float(0.2))

        pop_.place(relheight=relheight, relwidth=relwidth, rely=rely, relx=relx)
        pop_.bind("<Leave>",  func=lambda e: pop_.destroy())


    def active_side_bar(widget):
        global side_bar_list
        for i in side_bar_list:
            if i == widget:
                i.config(fg="yellow")
            else:
                i.config(fg=fg_color)

    if floating_frame is not None:
        if floating_frame.winfo_exists():
            floating_frame.deiconify()
            return
        else:
            floating_frame = None
            side_bar_list = None

    # Create a new Toplevel window (floating frame)
    side_bar_list = []
    floating_frame = tk.Toplevel(root)
    floating_frame.attributes('-toolwindow', True)
    title_bar_color(floating_frame, bg_color)
    floating_frame.config(bg="blue")

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

    btn0  = tk.Button(side_bar, borderwidth=0, border=0, text="\tMEDICAL HISTORY", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: (container0.tkraise(), active_side_bar(btn0)))
    btn0.place(relheight=0.07, relwidth=1, relx=0,rely=0)
    btn1 = tk.Button(side_bar, borderwidth=0, border=0, text="\tALLERGIES", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: (container1.tkraise(), active_side_bar(btn1)))
    btn1.place(relheight=0.07, relwidth=1, relx=0, rely=0.07)
    btn2 = tk.Button(side_bar, borderwidth=0, border=0, text="\tEXAMINATION", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: (container2.tkraise(), active_side_bar(btn2)))
    btn2.place(relheight=0.07, relwidth=1, relx=0, rely=0.14)
    btn3 = tk.Button(side_bar, borderwidth=0, border=0, text="\tVITALS", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: (container3.tkraise(), active_side_bar(btn3)))
    btn3.place(relheight=0.07, relwidth=1, relx=0, rely=0.21)
    btn4 = tk.Button(side_bar, borderwidth=0, border=0, text="\tDIAGNOSES", bg=bg_color, fg=fg_color, anchor="w", font=("Georgia", 12, "bold"), activeforeground="yellow", activebackground=bg_color, command=lambda: (container4.tkraise(), active_side_bar(btn4)))
    btn4.place(relheight=0.07, relwidth=1, relx=0, rely=0.28)
    side_bar_list.extend([btn0, btn1, btn2, btn3, btn4])

    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container0 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container0.place(relheight=1, relwidth=0.79, relx=0.21, rely=0)

    MHL_00 = tk.Label(container0, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="History Type", anchor="sw", font=("Times New Roman", 11))
    MHL_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0)
    MHE_00 = tk.Entry(container0, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    MHE_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.05)

    pop1 = tk.Button(container0, text="V", bg=bg_color, fg= font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, borderwidth=0, border=0, command=lambda : Show_PopUp(container0, MHE_00, "Hel"))
    pop1.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.05)



    MHL_11 = tk.Label(container0, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Notes", anchor="sw", font=("Times New Roman", 11))
    MHL_11.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.11)
    MHE_11 = tk.Text(container0, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    MHE_11.place(relheight=0.8, relwidth=0.9, relx=0.05, rely=0.16)


    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container1 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container1.place(relheight=1, relwidth=0.79, relx=0.21, rely=0)

    ALl_00 = tk.Label(container1, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Allergy Category", anchor="sw", font=("Times New Roman", 11))
    ALl_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0)
    ALe_00 = tk.Entry(container1, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    ALe_00.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.05)
    pop_ALe_00 = tk.Button(container1, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container1, ALe_00, "Hel"))
    pop_ALe_00.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.05)

    ALLlB_11 = tk.Label(container1, borderwidth=0, border=0, text="Allergen", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11))
    ALLlB_11.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0)
    ALLEN_11 = tk.Entry(container1, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    ALLEN_11.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.05)
    pop_EN_11 = tk.Button(container1, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container1, ALLEN_11, "Hel"))
    pop_EN_11.place(relheight=0.05, relwidth=0.015, relx=0.95, rely=0.05)

    SElB_22 = tk.Label(container1, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Severity", anchor="sw", font=("Times New Roman", 11))
    SElB_22.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.14)
    SEEN_22 = tk.Entry(container1, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    SEEN_22.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.19)
    pop_EN_22= tk.Button(container1, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container1, SEEN_22, "Hel"))
    pop_EN_22.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.19)

    lB_44 = tk.Label(container1, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Note", anchor="sw", font=("Times New Roman", 11))
    lB_44.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.28)
    EN_44 = tk.Text(container1, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EN_44.place(relheight=0.6, relwidth=0.9, relx=0.05, rely=0.33)


    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container2 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container2.place(relheight=1, relwidth=0.79, relx=0.21, rely=0)

    EXL_00 = tk.Label(container2, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Examination Type", anchor="sw", font=("Times New Roman", 11))
    EXL_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0)
    EXE_00 = tk.Entry(container2, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EXE_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.05)
    pop_EXE_00 = tk.Button(container2, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container2, EXE_00, "Hel"))
    pop_EXE_00.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.05)

    EXL_11 = tk.Label(container2, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Notes", anchor="sw", font=("Times New Roman", 11))
    EXL_11.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.11)
    EXE_11 = tk.Text(container2, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EXE_11.place(relheight=0.8, relwidth=0.9, relx=0.05, rely=0.16)

    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container3 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container3.place(relheight=1, relwidth=0.79, relx=0.21, rely=0)

    BTlB_00 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color,fg=fg_color, text="Body Temperature ('C)", anchor="sw", font=("Times New Roman", 11))
    BTlB_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0)
    BTBEN_00 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    BTBEN_00.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.05)
    pop_DEN_00 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container3, BTBEN_00, "Hel"))
    pop_DEN_00.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.05)

    RRlB_11 = tk.Label(container3, borderwidth=0, border=0, text="Respiration Rate (BPM)", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11))
    RRlB_11.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0)
    RRREN_11 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    RRREN_11.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.05)
    pop_DEN_11 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container3, RRREN_11, "Hel"))
    pop_DEN_11.place(relheight=0.05, relwidth=0.015, relx=0.95, rely=0.05)

    HRlB_22 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Heart Rate (BPM)", anchor="sw", font=("Times New Roman", 11))
    HRlB_22.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.14)
    HREN_22 = tk.Entry(container3, borderwidth=0, border=1,  bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    HREN_22.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.19)
    pop_DEN_22 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container3, HREN_22, "Hel"))
    pop_DEN_22.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.19)

    OSlB_33 = tk.Label(container3, borderwidth=0, border=0, text="Oxygen saturation (BPM)", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11))
    OSlB_33.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0.14)
    OSEN_33 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    OSEN_33.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.19)
    pop_DEN_33 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container3, OSEN_33, "Hel"))
    pop_DEN_33.place(relheight=0.05, relwidth=0.015, relx=0.95, rely=0.19)

    SBlB_44 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color,fg=fg_color, text="Systolic Blood Pressure", anchor="sw", font=("Times New Roman", 11))
    SBlB_44.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.28)
    SBEN_44 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    SBEN_44.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.33)
    pop_DEN_55 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container3, SBEN_44, "Hel"))
    pop_DEN_55.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.33)

    DBlB_55 = tk.Label(container3, borderwidth=0, border=0, text="Diastolic Blood Pressure", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11))
    DBlB_55.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0.28)
    DBEN_55 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    DBEN_55.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.33)
    pop_DEN_66 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container3, DBEN_55, "Hel"))
    pop_DEN_66.place(relheight=0.05, relwidth=0.015, relx=0.95, rely=0.33)

    PlB_66 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color,fg=fg_color, text="Pulse Rate", anchor="sw", font=("Times New Roman", 11))
    PlB_66.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.42)
    PEN_66 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    PEN_66.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.47)
    pop_DEN_66 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container3, PEN_66, "Hel"))
    pop_DEN_66.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.47)

    HlB_77 = tk.Label(container3, borderwidth=0, border=0, text="Height (cm)", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11))
    HlB_77.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0.42)
    HEN_77 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    HEN_77.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.47)
    pop_DEN_77 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container3, HEN_77, "Hel"))
    pop_DEN_77.place(relheight=0.05, relwidth=0.015, relx=0.95, rely=0.47)

    WlB_88 = tk.Label(container3, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Weight (KG)", anchor="sw", font=("Times New Roman", 11))
    WlB_88.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.56)
    WEN_88 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    WEN_88.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.61)
    pop_DEN_88 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container3, WEN_88, "Hel"))
    pop_DEN_88.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.61)

    BMlB_11 = tk.Label(container3, borderwidth=0, border=0, text="BM", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11))
    BMlB_11.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0.56)
    BMEN_11 = tk.Entry(container3, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    BMEN_11.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.61)
    pop_DEN_00 = tk.Button(container3, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container3, BMEN_11, "Hel"))
    pop_DEN_00.place(relheight=0.05, relwidth=0.015, relx=0.95, rely=0.61)

    # --------------------------------------------------------------------------------------------------------------------------------------------------

    container4 = tk.Frame(floating_frame, borderwidth=0, border=0, bg=bg_color)
    container4.place(relheight=1, relwidth=0.795, relx=0.205, rely=0)

    DlB_00 = tk.Label(container4, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Clinical Impression Type", anchor="sw", font=("Times New Roman", 11))
    DlB_00.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0)
    DEN_00 = tk.Entry(container4, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    DEN_00.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.05)
    pop_DEN_00 = tk.Button(container4, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color, borderwidth=0, border=0, command=lambda: Show_PopUp(container4, DEN_00, "Hel"))
    pop_DEN_00.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.05)


    DlB_11 = tk.Label(container4, borderwidth=0, border=0, text="Differential Diagnoses)", bg=bg_color, fg=fg_color, anchor="sw", font=("Times New Roman", 11))
    DlB_11.place(relheight=0.05, relwidth=0.4, relx=0.55, rely=0)
    DEN_11 = tk.Entry(container4, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    DEN_11.place(relheight=0.07, relwidth=0.4, relx=0.55, rely=0.05)
    pop_DEN_11 = tk.Button(container4, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color, fg=fg_color,borderwidth=0, border=0, command=lambda: Show_PopUp(container4, DEN_11, "Hel"))
    pop_DEN_11.place(relheight=0.05, relwidth=0.015, relx=0.95, rely=0.05)

    DlB_22 = tk.Label(container4, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Co-Existing Conditions", anchor="sw", font=("Times New Roman", 11))
    DlB_22.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.14)
    DEN_22 = tk.Entry(container4, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    DEN_22.place(relheight=0.07, relwidth=0.4, relx=0.05, rely=0.19)
    pop_DEN_22 = tk.Button(container4, text="V", bg=bg_color, font=("Bauhaus 93", 11), activebackground=bg_color, activeforeground=fg_color,fg=fg_color, borderwidth=0, border=0, command=lambda : Show_PopUp(container4, DEN_22, "Hel"))
    pop_DEN_22.place(relheight=0.05, relwidth=0.015, relx=0.45, rely=0.19)

    lB_44 = tk.Label(container4, borderwidth=0, border=0, bg=bg_color, fg=fg_color, text="Notes", anchor="sw", font=("Times New Roman", 11))
    lB_44.place(relheight=0.05, relwidth=0.4, relx=0.05, rely=0.28)
    EN_44 = tk.Text(container4, borderwidth=0, border=1, bg=bg_color, fg=fg_color, font=("Times New Roman", 11))
    EN_44.place(relheight=0.6, relwidth=0.9, relx=0.05, rely=0.33)









# Main application window
root = tk.Tk()
root.geometry("400x300")
title_bar_color(root, "#344423")
root.title("Main Application")

# Button to open the floating frame
open_button = tk.Button(root, text="Open Floating Frame", command=create_floating_frame)
open_button.pack(pady=50)

root.mainloop()
