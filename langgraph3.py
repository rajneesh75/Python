from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import os
from dotenv import load_dotenv
import requests
from langgraph.graph import StateGraph, END

load_dotenv()
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"


# The State dictates what data flows through the graph.
# Here, we just track the list of messages in the conversation.
class AgentState(TypedDict):
    messages: List[BaseMessage]
    category: str  # We will store the classification here (Math vs General)


# Node 1: The Categorizer
def categorize_input(state: AgentState) -> dict:
    """ Analyzes the user's last message and decides if it's 'Math' or 'General'. """
    last_message = state["messages"][-1].content

    # We ask the LLM to classify strictly.
    prompt = f"""
    You are a router. Classify the following input as either 'Math' or 'General'. 
    Return ONLY the word 'Math' or 'General'. Do not add punctuation.    
    Input: {last_message}
    """
    print(f"Prompt: {prompt}")
    headers = {"Authorization": f"Bearer {NVIDIA_API_KEY}", "Accept": "application/json",
               "Content-Type": "application/json", }

    payload = {
        "model": "meta/llama-4-maverick-17b-128e-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 16384,
        "temperature": 1.00,
        "top_p": 1.00,
        "frequency_penalty": 0.00,
        "presence_penalty": 0.00,
        "stream": False
    }

    response = requests.post(NVIDIA_URL, headers=headers, json=payload)
    json_resp = response.json()
    category = json_resp["choices"][0]["message"]["content"]
    print("Category:", category)
    # Update the state with the category
    return {"category": category}


# Node 2: The Math Expert
def handle_math(state: AgentState):
    print("--- Entering Math Node ---")
    last_message = state["messages"][-1].content

    # We ask the LLM to classify strictly.
    prompt = f"You are a mathematician. Solve this simply: {last_message}"
    print(f"Prompt: {prompt}")

    headers = {"Authorization": f"Bearer {NVIDIA_API_KEY}", "Accept": "application/json",
               "Content-Type": "application/json", }

    payload = {
        "model": "meta/llama-4-maverick-17b-128e-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 1.00,
        "top_p": 1.00,
        "frequency_penalty": 0.00,
        "presence_penalty": 0.00,
        "stream": False
    }

    response = requests.post(NVIDIA_URL, headers=headers, json=payload)
    json_resp = response.json()
    llm_output = json_resp["choices"][0]["message"]["content"]
    print("\nLLM OUTPUT:")
    print(llm_output)
    # We append the AI's response to the message history

    return {"messages": [AIMessage(content=llm_output)]}


# Node 3: The General Chat
def handle_general(state: AgentState):
    print("--- Entering General Chat Node ---")
    last_message = state["messages"][-1].content

    # We ask the LLM to classify strictly.
    prompt = f"You are a helpful assistant. Reply to: {last_message}"
    print(f"Prompt: {prompt}")

    headers = {"Authorization": f"Bearer {NVIDIA_API_KEY}", "Accept": "application/json",
               "Content-Type": "application/json", }

    payload = {
        "model": "meta/llama-4-maverick-17b-128e-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 1.00,
        "top_p": 1.00,
        "frequency_penalty": 0.00,
        "presence_penalty": 0.00,
        "stream": False
    }

    response = requests.post(NVIDIA_URL, headers=headers, json=payload)
    json_resp = response.json()
    llm_output = json_resp["choices"][0]["message"]["content"]
    print("\nLLM OUTPUT:")
    print(llm_output)
    return {"messages": [AIMessage(content=llm_output)]}


def routing_logic(state: AgentState):
    if state["category"] == "Math":
        return "math_node"
    else:
        return "general_node"


print("Initialising Graph...")

# 1. Initialize the Graph with our State structure
workflow = StateGraph(AgentState)

# 2. Add the Nodes
workflow.add_node("categorizer", categorize_input)
workflow.add_node("math_node", handle_math)
workflow.add_node("general_node", handle_general)

# 3. Set the Entry Point
# When the graph starts, the first person to touch the ball is the 'categorizer'
workflow.set_entry_point("categorizer")

# 4. Add Conditional Edges
# After 'categorizer' runs, look at 'routing_logic' to decide where to go next.
workflow.add_conditional_edges(
    "categorizer", routing_logic, {"math_node": "math_node",
                                   "general_node": "general_node"
                                   }
)

# 5. Add Normal Edges
# After math or general chat, we are done. Go to END.
workflow.add_edge("math_node", END)
workflow.add_edge("general_node", END)

# 6. Compile
app = workflow.compile()

input = {"messages": [HumanMessage(content="What is 55 multiplied by 10?")]}

# Stream the output to see the steps
for event in app.stream(input):
    for key, value in event.items():
        print(f"Finished running: {key}")

input = {"messages": [HumanMessage(content="Tell me a fun fact about history.")]}

for event in app.stream(input):
    for key, value in event.items():
        print(f"Finished running: {key}")

input = {"messages": [HumanMessage(content="What is square root of 2.")]}

for event in app.stream(input):
    for key, value in event.items():
        print(f"Finished running: {key}")
