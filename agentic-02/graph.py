from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_openai import ChatOpenAI

# SETUP THE ENVIRONMENT
load_dotenv()

llm_developer = ChatOpenAI(
    model="gpt-5.4-nano"
)

llm_qa = ChatOpenAI(
    model="gpt-5.5"
)

MAX_RETRIES = 3

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

    Return only the java code.
    """
    result = llm_developer.invoke(prompt)
    return {
        "code": result.content,
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
    """
    result = llm_qa.invoke(prompt)
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