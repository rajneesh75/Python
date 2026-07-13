from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

llm = ChatOpenAI(
    model="meta/llama-4-maverick-17b-128e-instruct",
    api_key=NVIDIA_API_KEY,
    base_url=NVIDIA_BASE_URL,
    max_tokens=16384,
    temperature=1.0,
)

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "router-demo"


# --------------------------------------------------
# STATE DEFINITION
# --------------------------------------------------
class AgentState(TypedDict):
    messages: List[BaseMessage]
    category: str


# --------------------------------------------------
# NODE 1: CATEGORIZER
# --------------------------------------------------
def categorize_input(state: AgentState) -> dict:
    last_message = state["messages"][-1].content

    prompt = f"""
    You are a router.
    Classify the input as either Math or General.
    Return ONLY one word: Math or General.

    Input: {last_message}
    """

    response = llm.invoke(prompt)
    category = response.content.strip().capitalize()

    print("Category:", category)
    return {"category": category}


# --------------------------------------------------
# NODE 2: MATH AGENT
# --------------------------------------------------
def handle_math(state: AgentState) -> dict:
    print("--- Entering Math Node ---")

    last_message = state["messages"][-1].content
    prompt = f"You are a mathematician. Solve this simply:\n{last_message}"

    response = llm.invoke(prompt)
    return {
        "messages": state["messages"] + [AIMessage(content=response.content)]
    }


# --------------------------------------------------
# NODE 3: GENERAL AGENT
# --------------------------------------------------
def handle_general(state: AgentState) -> dict:
    print("--- Entering General Chat Node ---")

    last_message = state["messages"][-1].content
    prompt = f"You are a helpful assistant. Reply to:\n{last_message}"

    response = llm.invoke(prompt)
    return {
        "messages": state["messages"] + [AIMessage(content=response.content)]
    }


# --------------------------------------------------
# ROUTING LOGIC
# --------------------------------------------------
def routing_logic(state: AgentState):
    return "math_node" if state["category"] == "Math" else "general_node"


# --------------------------------------------------
# GRAPH DEFINITION
# --------------------------------------------------
print("Initializing Graph...")

workflow = StateGraph(AgentState)

workflow.add_node("categorizer", categorize_input)
workflow.add_node("math_node", handle_math)
workflow.add_node("general_node", handle_general)

workflow.set_entry_point("categorizer")

workflow.add_conditional_edges(
    "categorizer",
    routing_logic,
    {
        "math_node": "math_node",
        "general_node": "general_node",
    },
)

workflow.add_edge("math_node", END)
workflow.add_edge("general_node", END)

app = workflow.compile()

# --------------------------------------------------
# RUN EXAMPLES
# --------------------------------------------------
inputs = [
    "What is 55 multiplied by 10?",
    "Tell me a fun fact about history.",
    "What is square root of 2?"
]

for user_input in inputs:
    print("\nUSER:", user_input)
    state = {"messages": [HumanMessage(content=user_input)]}
    final_state = None
    for event in app.stream(state):
        for node_name, node_state in event.items():
            print(f"Finished running: {node_name}")
            final_state = node_state  # keep updating

    # After graph ends, print the last AI message
    if final_state and "messages" in final_state:
        last_msg = final_state["messages"][-1]
        print("AI:", last_msg.content)

