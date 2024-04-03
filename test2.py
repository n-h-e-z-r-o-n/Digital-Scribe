import tkinter as tk

def highlight_words():
    text.tag_configure("highlight", background="yellow")  # Configure a tag for highlighting

    words_to_highlight = ["Python", "Tkinter"]  # List of words to highlight

    for word in words_to_highlight:
        start = 1.0
        while True:
            start = text.search(word, start, stopindex=tk.END)
            if not start:
                break
            end = f"{start}+{len(word)}c"
            text.tag_add("highlight", start, end)
            start = end

root = tk.Tk()
root.title("Text Highlighter")

text = tk.Text(root, wrap="word")
text.pack(expand=True, fill="both")

text.insert("1.0", "This is a simple Python script using Tkinter for GUI.")
text.insert(tk.END, "\n\nThis is another example of highlighting Tkinter in Python.")

highlight_button = tk.Button(root, text="Highlight Words", command=highlight_words)
highlight_button.pack()

root.mainloop()
