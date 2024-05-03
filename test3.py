import tkinter as tk
from tkinter import ttk

def on_scroll(*args):
    Audio_recodes_canvas.yview(*args)
    #frame.yview(*args)

root = tk.Tk()
root.title("Scrollbar Example")

Audio_recodes_frame =  tk.Frame(root, bg="white", borderwidth=0, border=0)
Audio_recodes_frame.place(relheight=0.9, relwidth=0.3, rely=0.02, relx=0.02)

Audio_recodes_canvas = tk.Canvas(Audio_recodes_frame)
Audio_recodes_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=on_scroll)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

Audio_recodes_canvas.configure(yscrollcommand=scrollbar.set)
frame = ttk.Frame(Audio_recodes_canvas)
Audio_recodes_canvas.create_window((0, 0), window=frame, anchor=tk.NW)

Audio_recodes_canvas.bind_all("<MouseWheel>", lambda e: Audio_recodes_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))


Audio_recodes_canvas.configure(scrollregion=Audio_recodes_canvas.bbox("all"))


for i in range(50):
    ttk.Label(frame, text="Label {}".format(i)).pack()

# Update canvas scrolling region
frame.update_idletasks()

root.mainloop()
