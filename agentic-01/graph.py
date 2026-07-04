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
    return {
        "intent": result.content.strip().lower()
    }

# NODE 2: PASSWORD RESET NODE

def handle_password(state: ChatSupportState):
    return {
        "response": "To reset your password, please click on forgot password on the login page."
    }

# NODE 3: ORDER TRACKING NODE

def handle_order(state: ChatSupportState):
    return {
        "response": "Please click on my orders in your profile to track your order."
    }

# NODE 4: REFUND NODE

def handle_refund(state: ChatSupportState):
    return {
        "response": "Please click on request refund under the specific order to start the refund process."
    }

# NODE 5: ROUTER NODE

def route_intent(state: ChatSupportState):
    if state['intent'] == 'account_related':
        return 'password_node'
    elif state['intent'] == 'order_related':
        return 'order_node'
    elif state['intent'] == 'refund_related':
        return 'refund_node'
    else:
        END

# BUILD THE WORKFLOW

graph = StateGraph(ChatSupportState)

graph.add_node("classifier",classify_intent)
graph.add_node("password_node",handle_password)
graph.add_node("order_node",handle_order)
graph.add_node("refund_node",handle_refund)

# STARTING POINT OF THE WORKFLOW / ENTRY POINT
graph.set_entry_point("classifier")
graph.add_conditional_edges(
    "classifier",
    route_intent
)
graph.add_edge("password_node",END)
graph.add_edge("order_node", END)
graph.add_edge("refund_node", END)

# COMPILE THE GRAPH
app = graph.compile()

# EXECUTE THE WORKFLOW

user_input = input("Customer Query: ")

result = app.invoke({
    "user_query": user_input,
    "intent": "",
    "response": ""
})

print(result['intent'])
print(result['response'])