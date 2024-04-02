from tkinter import filedialog
file_path = filedialog.askopenfilename(filetypes='*.mp3')
print(file_path)