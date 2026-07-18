from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from langchain_openai import ChatOpenAI
from neo4j import GraphDatabase
import json 
import os 

# SETUP THE ENVIRONMENT
load_dotenv()
llm = ChatOpenAI(model="gpt-5.4-mini")

# NEO4J CONNECTION VARIABLES 

NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_AUTH = (NEO4J_USER,NEO4J_PASSWORD)

NEO4J_DRIVER = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)

# DEFINE THE STATE
class ChatState(TypedDict):
    user_id: str #figured out
    user_query: str #figured out
    ai_reply: str  #figured out
    store_memory: Optional[bool] #figured out
    extracted_facts: Optional[list] #figured out

# NODE 1: CHAT NODE
def chat_node(state: ChatState):
    response = llm.invoke(state['user_query'])
    state['ai_reply'] = response.content 
    print(f"AI REPLY: \n {state['ai_reply']}")
    return state 

# NODE 2: MEMORY CLASSIFIER NODE
def memory_classifier(state: ChatState):
    prompt = f"""
    You are a user profile memory classifier.
    Determine whether this messaage contains any 
    long-term personal information about the user.

    Return the output in the following format:
    {{
        "store_memory": true or false,
        "extracted_facts": [list of extracted facts containing long term information]
    }}

    User message:
    {state['user_query']}
    """
    response = llm.invoke(prompt)
    decision = json.loads(response.content)
    state['store_memory'] = decision['store_memory']
    state['extracted_facts'] = decision['extracted_facts']
    return state 

# NODE 3: SAVE TO NEO4J
def neo4j_save(state: ChatState):
    if not state['extracted_facts']:
        return state 
    else:
        with NEO4J_DRIVER.session() as session:
            for fact in state['extracted_facts']:
                session.run(
                    """
                    MERGE (u: User {id: $user_id})
                    MERGE (m: Memory {text: $fact})
                    MERGE (u)-[:HAS_MEMORY]->(m)
                    """,
                    user_id = state['user_id'],
                    fact=fact
                )
        print("SAVED MEMORY")
        return state


# NODE 4: CONDITIONAL ROUTER
def router(state: ChatState):
    if state['store_memory']:
        return "neo4j_save"
    else:
        return END

# BUILD THE GRAPH

graph = StateGraph(ChatState)

graph.add_node("chat_node",chat_node)
graph.add_node("memory_classifier", memory_classifier)
graph.add_node("neo4j_save",neo4j_save)

graph.set_entry_point("chat_node")
graph.add_edge("chat_node","memory_classifier")
graph.add_conditional_edges("memory_classifier",
    router,
    {
        "neo4j_save": "neo4j_save",
        END: END
    })
graph.add_edge("neo4j_save", END)

# COMPILE THE GRAPH
app = graph.compile()

# EXECUTE THE GRAPH
def run_graph():
    user_id = input("Enter your email: ")
    while True:
        user_query = input("Human Question: ")
        if user_query.lower() == "exit":
            break
        app.invoke({
            "user_id": user_id,
            "user_query": user_query
        })

run_graph()