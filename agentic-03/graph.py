from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient
import json

# SETUP THE ENVIRONMENT
load_dotenv()

llm_developer = ChatOpenAI(
    model="gpt-5.4-nano"
)

llm_qa = ChatOpenAI(
    model="gpt-5.5"
)

MAX_RETRIES = 3

client = MongoClient("mongodb://localhost:27017")
mongodb_client = MongoDBSaver(client)

# DEFINE THE STATE
class CodeState(TypedDict):
    user_request: str
    code: str 
    rating: int
    retries: int 
    status: str 
    feedback: str 


# NODE 1: DEVELOPER NODE
def developer_agent(state: CodeState):
    prompt = f"""
    You are a java developer. Write the code for an application as per the following
    request of the user:
    {state['user_request']}

    If feedback is provided, ignore the previous version of the code and make improvements to it.

    Previous Code:
    {state['code']}

    Feedback:
    {state['feedback']}

    Return only the java code. No markdown.
    """
    result = llm_developer.invoke(prompt).content.strip()
    return {
        "code": result,
        "feedback": ""
    }

# NODE 2: QA AGENT NODE
def qa_agent(state: CodeState):
    prompt = f"""
    You are a Java QA Engineer.
    Follow the following guidelines strictly to evaluate the code given to you:
    - Correctness of the code
    - Structure of the code
    - Readability of the code
    - Is the code following best industry practices
    - Error handling capability of the code
    - Scalability of the code, if needed to scale to thousands of customers

    Return the output in the following format:
    {{
        "rating": integer value between 1-10,
        "feedback": "clear explanation of the improvements that can be made to the code"
    }}

    Code: 
    {state['code']}
    """
    ai_output = llm_qa.invoke(prompt).content.strip()
    result = json.loads(ai_output)
    return {
        "rating": int(result['rating']),
        "feedback": result['feedback']
    }

# NODE 3: APPROVAL NODE
def set_approved(state: CodeState):
    return {
        "status": "approved"
    }

# NODE 4: FAILED NODE
def set_failed(state: CodeState):
    return {
        "status": "failed"
    }

# NODE 5: INCREMENTAL RETRY NODE
def incremental_retry(state: CodeState):
    return {
        "retries": state['retries']+1
    }

# NODE 6: ROUTER NODE
def check_rating(state: CodeState):
    if state['rating'] >= 7:
        return "approved"
    if state['retries'] >= MAX_RETRIES:
        return "failed"
    else:
        return "retry"

# BUILD THE GRAPH
graph = StateGraph(CodeState)

graph.add_node("developer",developer_agent)
graph.add_node("qa",qa_agent)
graph.add_node("approved_node",set_approved)
graph.add_node("failed_node",set_failed)
graph.add_node("retry_node",incremental_retry)

# STARTING POINT OF THE WORKFLOW

graph.set_entry_point("developer")
graph.add_edge("developer","qa")
graph.add_conditional_edges(
    "qa",
    check_rating,
    {
        "approved": "approved_node",
        "failed": "failed_node",
        "retry": "retry_node"
    }
)
graph.add_edge("approved_node",END)
graph.add_edge("failed_node", END)
graph.add_edge("retry_node","developer")

memory = MongoDBSaver(client)
app = graph.compile(checkpointer=memory)

# DECLARE THE UNIQUE IDENTIFIERS
user_id = "1"
session_id = "1"

thread_id = f"{user_id}_{session_id}"

existing_thread = memory.get({"configurable": {"thread_id": thread_id}})

try:
    if existing_thread:
        print("RESUMING FROM SAVED CHECKPOINTING")
        result = app.invoke({},config={"configurable": {"thread_id": thread_id}})
    else:
        user_input = input("Enter app to build: ")
        result = app.invoke({
            "user_request": user_input,
            "code": "",
            "rating": 0,
            "feedback": "",
            "retries": 0,
            "status": "running"
        },config={"configurable": {"thread_id": thread_id}})
    print("\nFINAL OUTPUT\n")
    print(f"CODE: {result['code']}")
    print(f"RATING: {result['rating']}")
    print(f"FEEDBACK: {result['feedback']}")
    print(f"RETRIES: {result['retries']}")
    print(f"STATUS: {result['status']}")
except Exception as e:
    print(f"Error: {e}")