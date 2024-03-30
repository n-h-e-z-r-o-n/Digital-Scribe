import tkinter as tk

def get_text_range():
    start_index = "1.0"  # Start from the beginning of the text widget
    end_index = "3.0"    # End at line 3
    text_range = text_widget.get(start_index, end_index)
    print("Text in the range:", text_range)

# Create a tkinter window
root = tk.Tk()
root.title("Text Range Example")

# Create a Text widget
text_widget = tk.Text(root)
text_widget.pack()