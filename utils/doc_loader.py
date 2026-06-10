## DocLoader
from langchain_community.document_loaders import PyMuPDFLoader

def resume_loader(file_path):
    loader = PyMuPDFLoader(file_path)
    doc_list =  loader.load()
    return '\n'.join([i.page_content for i in doc_list if i.page_content])

def text_loader(file_path):
    with open(file_path, 'r') as f:
        return f.read()
    

