from langgraph.graph import StateGraph
from typing import TypedDict

class MyState(TypedDict):
    message: str

def step1(state: MyState):
    print("Running step1")
    return {"message": state["message"] + " world"}

def step2(state: MyState):
    print("Running step2")
    return {"message": state["message"] + "!"}

# Build graph
graph = StateGraph(MyState)
graph.add_node("step1", step1)
graph.add_node("step2", step2)
graph.set_entry_point("step1")
graph.add_edge("step1", "step2")
graph.set_finish_point("step2")

# Compile
app = graph.compile()

# Run
result = app.invoke({"message": "hello"})
print(result)