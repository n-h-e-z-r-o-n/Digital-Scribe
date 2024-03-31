import tkinter as tk

def count_lines():
    # Get the index of the last line
    last_index = text_widget.index("end")
    print("Last index:", last_index)
    # Parse the last index to get the line number
    line_number = last_index.split('.')[0]
    print("Number of lines:", line_number)

# Create a tkinter window
root = tk.Tk()
root.title("Count Lines Example")

# Create a Text widget
text_widget = tk.Text(root)
text_widget.pack()

# Insert some text into the Text widget
text_widget.insert("1.0", "Line 1\nLine 2\nLine 3\nLine 4\nLine 5")

# Button to count the number of lines
count_lines_button = tk.Button(root, text="Count Lines", command=count_lines)
count_lines_button.pack()

# Run the tkinter event loop
root.mainloop()
