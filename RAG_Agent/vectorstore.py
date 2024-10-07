import os
from langchain_chroma import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from bs4 import BeautifulSoup
import requests

# Constants
DATA_PATH = "C:/Users/acer/Documents/Accedemic_Folder_E19254/Training_02_TIEC_docs/RIS_project/RAG_Agent/data/"#"data/"
DB_PATH = "C:/Users/acer/Documents/Accedemic_Folder_E19254/Training_02_TIEC_docs/RIS_project/RAG_Agent/vectorstores/db_chroma"#"vectorstores/db_chroma"
URLS_FILE = "C:/Users/acer/Documents/Accedemic_Folder_E19254/Training_02_TIEC_docs/RIS_project/RAG_Agent/urls.txt"
BATCH_SIZE = 5000  # Adjust this as per your system's capacity

# Function to scrape the content of a given URL
def scrape_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract text content from the page
        text = soup.get_text()
        return Document(page_content=text, metadata={"url": url})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return None

# Split a list into chunks of a given size
def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

# Function to load URLs from the text file
def load_urls():
    if os.path.exists(URLS_FILE):
        with open(URLS_FILE, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

# Function to save URLs to the text file
def save_urls(urls):
    with open(URLS_FILE, "w") as f:
        for url in urls:
            f.write(url + "\n")

# Single method to load documents from local files and URLs, and add them to vector DB
def create_vectorstore(urls=None):
    # Check if Chroma DB already exists
    if os.path.exists(DB_PATH):
        print("Loading existing vector database...")
        # Initialize GPT4AllEmbeddings with CUDA
        embeddings = GPT4AllEmbeddings(model_kwargs={'device': 'cuda'})  # Enable CUDA for embeddings
        vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)  # Load the existing vectorstore
        return vectorstore.as_retriever()

    print("Creating new vector database...")

    # Load documents from the local directory
    loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    local_documents = loader.load()

    # Load URLs from the text file
    url_documents = load_urls()

    if urls:
        url_documents = [scrape_content(url) for url in urls if scrape_content(url) is not None]

    # Combine local and URL documents
    documents = local_documents + url_documents

    # Ensure all elements are Document objects
    documents = [doc if isinstance(doc, Document) else Document(page_content=doc) for doc in documents]

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=25)
    texts = text_splitter.split_documents(documents)

    # Initialize GPT4AllEmbeddings with CUDA
    embeddings = GPT4AllEmbeddings(model_kwargs={'device': 'cuda'})  # Enable CUDA for embeddings

    # Create a new vector database
    vectorstore = Chroma.from_documents(documents=texts, collection_name="rag-chroma", persist_directory=DB_PATH, embedding_function=embeddings)

    # Add documents in batches to avoid exceeding the maximum batch size
    for batch in chunked(texts, BATCH_SIZE):
        vectorstore.add_documents(batch)

    # Persist changes
    vectorstore.persist()

    return vectorstore.as_retriever()
