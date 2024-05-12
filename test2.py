from gradientai import Gradient

gradient = Gradient()

rag_collection = gradient.create_rag_collection(
  name="RAG with two sample text files",
  slug="bge-large",
  filepaths=[
    "samples/a.txt",
    "samples/b.txt",
  ],
)