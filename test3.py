import tkinter as tk

# Create the main Tkinter window
root = tk.Tk()
root.geometry("300x200")

# Create two frames
frame1 = tk.Frame(root, bg="lightblue")
frame1.pack(fill=tk.BOTH, expand=True)

frame2 = tk.Frame(root, bg="lightgreen")
frame2.pack(fill=tk.BOTH, expand=True)

# Create a label widget
shared_label = tk.Label(root, text="Shared Label", bg="white")

# Place the label in the first frame
shared_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER, in_=frame1)

# Place the label in the second frame
shared_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER, in_=frame2)

# Run the Tkinter event loop
root.mainloop()
