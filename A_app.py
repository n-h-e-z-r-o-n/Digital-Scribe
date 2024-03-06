import tkinter as tk

def change_color(widget):

    if isinstance(widget, tk.Frame):
         widget.config(bg="black")

    if isinstance(widget, tk.Button):
        widget.config(bg="black", activebackground='black', fg='white', activeforeground='white')

    if isinstance(widget, tk.Label):
        widget.config(bg="black",  fg='white')

    if isinstance(widget, tk.Label):
        widget.config(bg="black", fg='white')
        

    children = widget.winfo_children()
    for child in children:
        change_color(child)




def get_parent_children():
    root = tk.Tk()
    root.title("Parent Children Relationship")

    parent_frame = tk.Frame(root)
    parent_frame.pack()

    child_label1 = tk.Label(parent_frame, text="Child Label 1")
    child_label1.pack()

    child_label2 = tk.Button(parent_frame, text="Child Label 2", command=lambda: change_color(root))
    child_label2.pack()



    root.mainloop()
get_parent_children()