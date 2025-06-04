# tools/pdf_tool.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_embed_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(pages)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return FAISS.from_documents(docs, embeddings)
