import tkinter as tk

def get_text_range():
    start_index = "1.0"  # Start from the beginning of the text widget
    end_index = "7.0"    # End at line 3
    text_range = text_widget.get(start_index, end_index)
    print("Text in the range:", text_range)

# Create a tkinter window
root = tk.Tk()
root.title("Text Range Example")

# Create a Text widget
text_widget = tk.Text(root)
text_widget.pack()

# Insert some text into the Text widget
text_widget.insert("1.0", "Line 1\nLine 2\nLine 3\nLine 4\nLine 5")

# Button to retrieve text in a range
get_range_button = tk.Button(root, text="Get Text Range", command=get_text_range)
get_range_button.pack()

# Run the tkinter event loop
root.mainloop()
