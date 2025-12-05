from langchain_classic.agents import initialize_agent, AgentType
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from wikipedia import wikipedia

load_dotenv()
print("Loaded:", os.getenv("OPENAI_API_KEY"))
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Example 1 – Calculator tool
def calc_tool(query: str):
    try:
        return str(eval(query))
    except Exception as e:
        return f"Error: {e}"


# Example 2 – Wikipedia search
def wiki_search(query: str):
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception as e:
        return f"Error: {e}"


tools = [
    Tool(
        name="Calculator",
        func=calc_tool,
        description="Useful for solving math problems. Input: a math expression."
    ),
    Tool(
        name="Wikipedia",
        func=wiki_search,
        description="Useful for getting factual info on a topic."
    )
]

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
result = agent.invoke({"prompt": "what is 45 * 22?"})
print("\nFinal Answer:\n", result)
