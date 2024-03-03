import tkinter as tk
from tkinter import filedialog
import docx
import PyPDF2

def read_docx(file_path):
    doc = docx.Document(file_path)
    content = ""
    for paragraph in doc.paragraphs:
        content += paragraph.text + "\n"
    return content

def read_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        content = ""
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            content += page.extractText()
    return content

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Word files", "*.docx"), ("PDF files", "*.pdf")])
    if file_path:
        if file_path.endswith(".docx"):
            content = read_docx(file_path)
        elif file_path.endswith(".pdf"):
            content = read_pdf(file_path)
        text.delete(1.0, tk.END)
        text.insert(tk.END, content)

root = tk.Tk()
root.title("File Content Viewer")

upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack(pady=10)

text = tk.Text(root, wrap="word", height=20, width=60)
text.pack(fill="both", expand=True)

root.mainloop()
v