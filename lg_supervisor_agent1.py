import os
from typing import (TypedDict, Annotated)
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import (BaseMessage, HumanMessage)
from langchain_core.tools import tool
from langgraph.graph import (StateGraph, START, END)
from langgraph.graph.message import (add_messages)
from langgraph.prebuilt import ToolNode
import logging

logging.basicConfig(level=logging.DEBUG)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-5.6", temperature=0, api_key=api_key,reasoning_effort="none",)


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    next: str


@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply numbers.
    """

    print("\nMath tool running")
    return a * b


math_llm = (llm.bind_tools([multiply]))


def supervisor(state: AgentState):
    question = state["messages"][-1].content
    prompt = f"""
    Decide who should answer.

    Options:
    math_agent
    research_agent

    Question:
    {question}

    Return only one word.
    """

    decision = (llm.invoke(prompt).content.lower().strip())
    if "math_agent" in decision:
        decision = "math_agent"
    else:
        decision = "research_agent"
    print("\nSupervisor selected:", decision)
    return {"next": decision}


def research_agent(state: AgentState):
    print("\nResearch Agent")
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


def math_agent(state: AgentState):
    print("\nMath Agent")
    response = (math_llm.invoke(state["messages"]))
    return {"messages": [response]}


def route(state: AgentState):
    if state["next"] == "math_agent":
        return "math_agent"

    return "research_agent"


def math_router(state: AgentState):
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "math_tools"
    return END


builder = StateGraph(AgentState)
builder.add_node("supervisor", supervisor)
builder.add_node("research_agent", research_agent)
builder.add_node("math_agent", math_agent)
builder.add_node("math_tools", ToolNode([multiply]))
builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", route)
builder.add_conditional_edges("math_agent", math_router)
builder.add_edge("math_tools", "math_agent")
builder.add_edge("research_agent", END)
graph = builder.compile()


def ask(question):
    print("\nQUESTION:", question)
    result = graph.invoke({"messages": [HumanMessage(content=question)]})
    print("\nANSWER:")
    print(result["messages"][-1].content)


ask("What is 25 times 12?")
ask("Explain what Delta Lake is")
