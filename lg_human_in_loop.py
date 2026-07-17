import os
from typing import (TypedDict, Annotated)
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import (StateGraph, START, END)
import logging

logging.basicConfig(level=logging.DEBUG)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-5.6", temperature=0, api_key=api_key, reasoning_effort="none", )


class AgentState(TypedDict):
    request: str
    email: str
    approved: bool


def write_email(state: AgentState):
    prompt = f"""
    Write a professional email for:

    {state["request"]}
    """

    response = llm.invoke(prompt)
    return {"email": response.content}


def human_review(state: AgentState):
    print("\nGenerated Email\n")
    print(state["email"])
    answer = input("\nApprove? (yes/no): ")
    return {"approved": answer.lower() == "yes"}


def review_router(state: AgentState):
    if state["approved"]:
        return "send_email"
    return "rewrite_email"


def send_email(state):
    print("\nEmail sent!")
    return {}


def rewrite_email(state):
    prompt = f"""
    Rewrite this email.

    Previous version:

    {state["email"]}

    Make it friendlier.
    """

    response = llm.invoke(prompt)
    return {"email": response.content}


builder = StateGraph(AgentState)
builder.add_node("write_email", write_email)
builder.add_node("human_review", human_review)
builder.add_node("rewrite_email", rewrite_email)
builder.add_node("send_email", send_email)
builder.add_edge(START, "write_email")
builder.add_edge("write_email", "human_review")
builder.add_conditional_edges("human_review", review_router,
                              {
                                  "send_email": "send_email",
                                  "rewrite_email": "rewrite_email"
                              })
builder.add_edge("rewrite_email", "human_review")
builder.add_edge("send_email", END)
graph = builder.compile()

graph.invoke({
    "request": "Tell your girlfriend to meet tomorrow."
})
