from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from typing import TypedDict

load_dotenv()
llm = ChatOpenAI(model="gpt-5.5", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))


class AgentState(TypedDict):
    story_summary: str
    response: str


def call_model(state):
    return {"response": llm.invoke(state["story_summary"]).content}


workflow = StateGraph(AgentState)
workflow.add_node("process", call_model)
workflow.set_entry_point("process")
workflow.add_edge("process", END)

agent = workflow.compile()
print(agent.invoke({"story_summary": "Fix login issue"}))
