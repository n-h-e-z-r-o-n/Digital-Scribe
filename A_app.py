import tkinter as tk

num_y = 0.9
num_height = 0.05
current = 150
def on_key_press(event, widget):
    global current, num_y, num_height
    text_content = entry.get("1.0", "end-1c")
    num_lines = len(text_content)  # Count the number of lines
    print("- ", num_lines)
    if num_lines > current:
        num_y  = num_y - 0.02
        num_height = num_height + 0.02
        widget.forget()
        search_lable.place(relheight=num_height, relwidth=0.4, rely=num_y, relx=0.3)
        current = current + 150
    if num_lines < current and current > 150:
        num_y = num_y + 0.02
        num_height = num_height - 0.02
        widget.forget()
        search_lable.place(relheight=num_height, relwidth=0.4, rely=num_y, relx=0.3)
        current = current - 150


root = tk.Tk()
root.geometry("300x100")

chatbot_widget = tk.Frame(root, bg='gray', borderwidth=0, border=0)
chatbot_widget.place(relheight=0.96, relwidth=0.9747, rely=0.02, relx=0.0253)

search_lable = tk.Label(chatbot_widget, text="（", bg='blue', fg='white', font=("Calibri", 10, 'bold'), anchor='w', borderwidth=0, border=0)
search_lable.place(relheight=0.05, relwidth=0.4, rely=0.9, relx=0.3)

entry = tk.Text(search_lable, wrap='word', bg='white', fg='black', font=("Calibri", 10, 'bold'), borderwidth=0, border=0)
entry.place(relheight=0.9, relwidth=0.9, rely=0.05, relx=0.05)
entry.bind("<Key>", lambda e:on_key_press(e, search_lable))


root.mainloop()
