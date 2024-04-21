from spire.doc import *


from spire.doc.common import *


# Create word document

document = Document()


document.LoadFromFile("C:\\Users\\Administrator\\Desktop\\input.docx")

# Save the document to PDF

document.SaveToFile("output/ToPDF.pdf", FileFormat.PDF)

document.Close()