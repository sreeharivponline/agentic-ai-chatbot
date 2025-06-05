# pdf_tools.py

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings 
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document

def load_and_embed_pdf(pdf_path: str) -> FAISS:
    """
    Loads a PDF, splits its content into chunks, embeds them using a SentenceTransformer model,
    and creates a FAISS vector store.

    Args:
        pdf_path (str): The file path to the PDF document.

    Returns:
        FAISS: A FAISS vector store containing the embedded document chunks.
    """
    loader = PyPDFLoader(pdf_path)
    pages: List[Document] = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs: List[Document] = splitter.split_documents(pages)
    
    # --- CHANGE START ---
    # Initialize SentenceTransformerEmbeddings
    # 'all-MiniLM-L6-v2' is a very common and efficient choice for general purpose embeddings.
    # It will download the model the first time it's used.
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    # --- CHANGE END ---
    
    return FAISS.from_documents(docs, embeddings)