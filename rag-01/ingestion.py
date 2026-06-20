from dotenv import load_dotenv 
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

# SETUP THE ENVIRONMENT
load_dotenv()

PDF_PATH = "large_data.pdf"

# STEP 1: LOAD THE PDF INTO TEXT
loader = PyPDFLoader(PDF_PATH)
text_pdf_data = loader.load()
print("PDF LOADED SUCCESSFULLY")

# STEP 2: CHUNKING STRATEGY
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
chunked_data = text_splitter.split_documents(text_pdf_data)
print("PDF CHUNKED SUCCESSFULLY")

# STEP 3: CHOOSE EMBEDDING MODEL
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large")
print("EMBEDDING MODEL INITIALIZED SUCCESSFULLY")

# STEP 4: STORE THE CHUNKS IN THE VECTOR DATABASE

VECTOR_DB_URL = "http://localhost:6333"
COLLECTION_NAME = "product_documentation"

qdrant = QdrantVectorStore.from_documents(
    chunked_data,
    embeddings,
    url=VECTOR_DB_URL,
    prefer_grpc=False,
    collection_name=COLLECTION_NAME,
)
print("INGESTION SUCCESSFULL")