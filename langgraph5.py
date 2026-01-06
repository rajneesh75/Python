from pprint import pprint
from typing import TypedDict, List

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

# --------------------------------------------------
# ENV SETUP
# --------------------------------------------------
load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

conversation_state = {
    "messages": []
}


class StreamingCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        print(token, end="", flush=True)


llm = ChatOpenAI(
    model="meta/llama-4-maverick-17b-128e-instruct",
    api_key=NVIDIA_API_KEY,
    base_url=NVIDIA_BASE_URL,
    max_tokens=16384,
    temperature=1.0,
    streaming=True,
    callbacks=[StreamingCallbackHandler()],
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


def debug_state(label: str, state: AgentState):
    print(f"\n🔍 STATE DEBUG [{label}]")
    pprint({
        "messages": [m.content for m in state.get("messages", [])],
        "category": state.get("category")
    })


class StreamingCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        print(token, end="", flush=True)


# --------------------------------------------------
# NODE 1: CATEGORIZER
# --------------------------------------------------
def categorize_input(state: AgentState) -> dict:
    debug_state("before categorizer", state)

    last_message = state["messages"][-1].content

    prompt = f"""
    You are a router. Classify the input as either Math or General. Return ONLY one word: Math or General.
    Input: {last_message} """

    response = llm.invoke(prompt)
    category = response.content.strip().capitalize()

    print("Category:", category)
    return {"category": category}


# --------------------------------------------------
# NODE 2: MATH AGENT
# --------------------------------------------------
def handle_math(state: AgentState) -> dict:
    debug_state("before math", state)

    print("--- Entering Math Node ---")

    last_message = state["messages"][-1].content
    prompt = f"You are a mathematician. Solve this simply:\n{last_message}"

    response = llm.invoke(prompt)
    print()
    new_state = {
        "messages": state["messages"] + [AIMessage(content=response.content)]
    }

    debug_state("after math", AgentState(**new_state, category=state["category"]))
    return new_state


# --------------------------------------------------
# NODE 3: GENERAL AGENT
# --------------------------------------------------
def handle_general(state: AgentState) -> dict:
    debug_state("before general", state)
    print("--- Entering General Chat Node ---")
    print("AI:", end=" ", flush=True)

    last_message = state["messages"][-1].content
    prompt = f"You are a helpful assistant. Reply to:\n{last_message}"

    response = llm.invoke(prompt)
    print()

    new_state = {
        "messages": state["messages"] + [AIMessage(content=response.content)]
    }

    debug_state("after general", AgentState(**new_state, category=state["category"]))
    return new_state


# --------------------------------------------------
# ROUTING LOGIC
# --------------------------------------------------
def routing_logic(state: AgentState):
    return "math_node" if state["category"] == "Math" else "general_node"


def chat(user_input: str):
    global conversation_state

    # Append user message
    conversation_state["messages"].append(
        HumanMessage(content=user_input)
    )

    # Run graph
    result = app.invoke(conversation_state)

    # Persist updated messages
    conversation_state["messages"] = result["messages"]

    # Print assistant reply
    ai_msg = result["messages"][-1]
    print("AI:", ai_msg.content)


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


# ============================================================
# MEMORY STORE (SINGLE SESSION)
# ============================================================

class AgentState(TypedDict):
    messages: List[BaseMessage]
    category: str


MAX_MESSAGES = 20  # memory trim


def trim_memory(messages: List[BaseMessage]) -> List[BaseMessage]:
    return messages[-MAX_MESSAGES:]


# ============================================================
# DEMO
# ============================================================

chat("What is 55 multiplied by 10?")
# chat("Now divide that by 5")
chat("Tell me a fun fact about history")
# chat("What is square root of 2?")
