import tkinter as tk


def create_floating_frame():
    # Create a new Toplevel window (floating frame)
    floating_frame = tk.Toplevel(root)
    floating_frame.geometry("300x200x0x0")  # Set the size of the floating frame
    floating_frame.overrideredirect(True)  # Remove title bar and buttons
    floating_frame.config(highlightthickness=2)
    # Create a frame within the floating window to act as a custom title bar
    title_bar = tk.Frame(floating_frame, bg='gray', relief='raised', bd=2)
    title_bar.pack(fill='x', padx=5, pady=5)

    # Add a label to the custom title bar
    title_label = tk.Label(title_bar, text="Floating Frame", bg='gray')
    title_label.pack(side='left', padx=10)

    # Add a close button to the custom title bar
    close_button = tk.Button(title_bar, text="X", bg='red', command=floating_frame.destroy)
    close_button.pack(side='right')

    # Allow the frame to be moved by dragging the title bar
    def start_move(event):
        floating_frame.x = event.x
        floating_frame.y = event.y

    def stop_move(event):
        floating_frame.x = None
        floating_frame.y = None

    def on_motion(event):
        delta_x = event.x - floating_frame.x
        delta_y = event.y - floating_frame.y
        new_x = floating_frame.winfo_x() + delta_x
        new_y = floating_frame.winfo_y() + delta_y
        floating_frame.geometry(f"+{new_x}+{new_y}")

    title_bar.bind("<Button-1>", start_move)
    title_bar.bind("<ButtonRelease-1>", stop_move)
    title_bar.bind("<B1-Motion>", on_motion)

    # Example content for the floating frame
    content_frame = tk.Frame(floating_frame)
    content_frame.pack(fill='both', expand=True, padx=10, pady=10)

    label = tk.Label(content_frame, text="This is a floating frame", font=("Helvetica", 16))
    label.pack(pady=20)


# Main application window
root = tk.Tk()
root.geometry("400x300")
root.title("Main Application")

# Button to open the floating frame
open_button = tk.Button(root, text="Open Floating Frame", command=create_floating_frame)
open_button.pack(pady=50)

root.mainloop()
