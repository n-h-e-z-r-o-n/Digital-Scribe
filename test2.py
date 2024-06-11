import tkinter as tk

def create_floating_frame():
    # Create a new Toplevel window (floating frame)
    floating_frame = tk.Toplevel(root)
    floating_frame.attributes('-toolwindow', True)
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

root.title("Main Application")

# Button to open the floating frame
open_button = tk.Button(root, text="Open Floating Frame", command=create_floating_frame)
open_button.pack(pady=50)

root.mainloop()
