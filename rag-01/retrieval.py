from dotenv import load_dotenv
from openai import OpenAI 
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

# SETUP THE ENVIRONMENT
load_dotenv()

client = OpenAI()

VECTOR_DB_URL = "http://localhost:6333"
COLLECTION_NAME = "product_documentation"
EMBEDDING = OpenAIEmbeddings(
    model="text-embedding-3-large")

# STEP 1: CONNECT TO EXISTING VECTOR DB AND EXISTING COLLECTION
qdrant = QdrantVectorStore.from_existing_collection(
    embedding=EMBEDDING,
    collection_name=COLLECTION_NAME,
    url=VECTOR_DB_URL,
)

# STEP 2: ASK FOR CUSTOMER QUERY
query = input("Enter Human Query: ")

# STEP 3: PERFORM SIMILARITY SEARCH
search_results = qdrant.similarity_search(
    query
)

# STEP 4: CREATE CONTEXT OUT OF CHUNKS
context_list = []

for result in search_results:
    refined_chunk = f"""
    Page Content:
    {result.page_content}
    Page Number:
    {result.metadata.get("page_label","N/A")}
    """
    context_list.append(refined_chunk)

# STEP 5: PROVIDE LLM CONTEXT

SYSTEM_PROMPT = f"""
You are an AI RAG Assistant.
You have been given extracted content from a PDF document.
Each section includes:
- The text content
- The page number

Answer the user's query using ONLY this provided information.
If the answer is available:
- Respond in a clear manner from the received data
- Mention the page number(s) from which the data was extracted

If the answer is not available:
- Clearly state to the user that your knowledge does not contain the answer

Context:
{context_list}
"""

# STEP 6: INVOKE LLM CALL
response = client.responses.create(
    model="gpt-5.4-mini",
    input=query,
    instructions=SYSTEM_PROMPT
)
print(response.output_text)