import tkinter as tk



# Create a Tkinter window
root = tk.Tk()


Frame1 = tk.Frame(root, bg='red')
Frame1.place(relheight=1,relwidth=0.5, rely=0, relx=0)

Frame2 = tk.Frame(root, bg='green')
Frame2.place(relheight=1,relwidth=0.5, rely=0, relx=0.5)

button = tk.Button(root, text="Click Me", command=lambda: duplicate_widget(duplicate_b, Frame2))
button.pack()


duplicate_b= tk.Button(Frame1, text="hELLO")
duplicate_b.place(relwidth=0.1, relheight=0.1, rely=0.4, relx=0.2)



root.mainloop()
