from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_openai import ChatOpenAI

# SETUP THE ENVIRONMENT
load_dotenv()
llm = ChatOpenAI(
    model="gpt-5.4-nano"
)

# DEFINE THE STATE
class ChatSupportState(TypedDict):
    user_query: str 
    intent: str 
    response: str 

# DEFINE THE FIRST NODE
def classify_intent(state: ChatSupportState):
    prompt = f"""
    Classify the user query into one of these 3 categories:
    - account_related
    - order_related
    - refund_related

    Only return the category name.
    User Query: {state['user_query']}
    """
    result = llm.invoke(prompt)
    return result.content
