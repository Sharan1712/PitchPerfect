from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
import requests

emb_model = "sentence-transformers/all-MiniLM-L6-v2"
hf_embedding = HuggingFaceEmbeddings(model_name = emb_model) 

def pdf_loader(file):
    loader = PyPDFLoader(file)
    pages = []
    for page in loader.lazy_load():
        pages.append(page)
    
    vector_store = InMemoryVectorStore.from_documents(pages, hf_embedding)
    
    return vector_store


        
    # print(f"{pages[0].metadata}\n")
    # print(pages[0].page_content)

pdf_loader("CV.pdf")