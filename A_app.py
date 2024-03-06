

from tkinter import filedialog

import docx

#file_path = filedialog.askopenfilename()
#print(file_path)

document = docx.Document(r"C:\Users\HEZRON WEKESA\Desktop\Dart.docx")
# Do something with the document, such as printing its content
for paragraph in document.paragraphs:
    #print(paragraph.text)
    pass

print(   document. )



