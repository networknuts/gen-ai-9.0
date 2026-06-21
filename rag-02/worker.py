import redis
import ast 
from dotenv import load_dotenv
from openai import OpenAI 
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

# SETUP THE AI ENVIRONMENT
load_dotenv()

client = OpenAI()

VECTOR_DB_URL = "http://localhost:6333"
COLLECTION_NAME = "product_documentation"
EMBEDDING = OpenAIEmbeddings(
    model="text-embedding-3-large")

# REDIS CONNECTION SETUP
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

# VECTOR DATABASE CONNECTION
qdrant = QdrantVectorStore.from_existing_collection(
    embedding=EMBEDDING,
    collection_name=COLLECTION_NAME,
    url=VECTOR_DB_URL,
)

print("Worker Ready to Process Queries.")

while True: 
    queue_name, raw_payload = redis_client.blpop("rag:requests")
    payload = ast.literal_eval(raw_payload)
    job_id = payload['job_id']
    query = payload['query']
    print(f"Processing Query: {job_id}")
    search_results = qdrant.similarity_search(query)
    context_list = []
    for result in search_results:
        refined_chunk = f"""
        Page Content:
        {result.page_content}
        Page Number:
        {result.metadata.get("page_label","N/A")}
        """
        context_list.append(refined_chunk)
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
    response = client.responses.create(
    model="gpt-5.4-mini",
    input=query,
    instructions=SYSTEM_PROMPT
    )
    print(response.output_text)