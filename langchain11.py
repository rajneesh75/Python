from dotenv import load_dotenv
import os
from uuid import uuid4
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
tavily_api_key = os.getenv("TAVILY_KEY")
tool = TavilySearch(tavily_api_key=tavily_api_key, max_results=3)  # increased number of results

"""
In previous examples we've annotated the `messages` state key
with the default `operator.add` or `+` reducer, which always
appends new messages to the end of the existing messages array.

Now, to support replacing existing messages, we annotate the
`messages` key with a customer reducer function, which replaces
messages with the same `id`, and appends them otherwise.
"""


def reduce_messages(left: list[AnyMessage], right: list[AnyMessage]) -> list[AnyMessage]:
    # assign ids to messages that don't have them
    for message in right:
        if not message.id:
            message.id = str(uuid4())
    # merge the new messages with the existing messages
    merged = left.copy()
    for message in right:
        for i, existing in enumerate(merged):
            # replace any existing messages with the same id
            if existing.id == message.id:
                merged[i] = message
                break
        else:
            # append any new messages to the end
            merged.append(message)
    return merged


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], reduce_messages]


class Agent:

    def __init__(self, model, tools, checkpointer, system=""):
        print("Inside init")
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile(
            checkpointer=checkpointer,
            interrupt_before=["action"]
        )
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)
        print("Exiting init")

    def call_openai(self, state: AgentState):
        print("Inside call_openai")
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def exists_action(self, state: AgentState):
        print("Inside exists_action")
        result = state['messages'][-1]
        print(f"Exiting exists_action {len(result.tool_calls)}")
        return len(result.tool_calls) > 0

    def take_action(self, state: AgentState):
        print("Inside take_action")
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:  # check for bad tool name from LLM
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        return {'messages': results}


prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""

model = ChatOpenAI(model="gpt-4o")
memory = MemorySaver()
abot = Agent(model, [tool], system=prompt, checkpointer=memory)


messages = [HumanMessage(content="Give me govt universities located in Dwarka, Delhi. Give me their urls"
                                 "if possible. Try to keep the number of results to 3.")]
thread = {"configurable": {"thread_id": "1"}}
print("Invoking graph...")

for event in abot.graph.stream({"messages": messages}, thread):
    for v in event.values():
        print(v)

print(abot.graph.get_state(thread))
print(abot.graph.get_state(thread).next)

# ✅ Resume the interrupted graph BEFORE sending the next message
print("Resuming after interrupt...")
for event in abot.graph.stream(None, thread):
    for v in event.values():
        print(v)

print()
print()

messages = [HumanMessage(content="What about Jammu, Jammu & Kashmir?")]
print("Invoking graph...")
for event in abot.graph.stream({"messages": messages}, thread):
    for v in event.values():
        print(v)

print(abot.graph.get_state(thread))
print(abot.graph.get_state(thread).next)

# ✅ Resume again after second interrupt
print("Resuming after interrupt...")
for event in abot.graph.stream(None, thread):
    for v in event.values():
        print(v)

print()
print()

messages = [HumanMessage(content="Which has better universities with regards to placements")]
print("Invoking graph...")
for event in abot.graph.stream({"messages": messages}, thread):
    for v in event.values():
        print(v)

# ✅ Resume again
print("Resuming after interrupt...")
for event in abot.graph.stream(None, thread):
    for v in event.values():
        print(v)