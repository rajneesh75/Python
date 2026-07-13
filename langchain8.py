from langchain_classic.agents import initialize_agent, AgentType
from langchain_core.tools import Tool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",   # or gpt-4.1, etc.
    api_key=os.getenv("OPENAI_API_KEY"),
)



# Wikipedia tool
wiki = WikipediaAPIWrapper(
    top_k_results=1,
    doc_content_chars_max=1500
)

wikipedia_tool = Tool(
    name="Wikipedia",
    func=wiki.run,
    description="Useful for fetching info from Wikipedia about people, places, concepts, events."
)

# Google Search tool (SerpAPI)
google_search = GoogleSearchAPIWrapper(
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    google_cx=os.getenv("GOOGLE_CX"),   # your custom search engine ID
)

google_tool = Tool(
    name="GoogleSearch",
    func=google_search.run,
    description="Useful for searching the web when Wikipedia is not enough."
)

# -----------------------
# Agent Setup
# -----------------------

tools = [wikipedia_tool, google_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# -----------------------
# Run a Query
# -----------------------
if __name__ == "__main__":
    question = "Who is Sundar Pichai and what were the key milestones in his career?"

    answer = agent.run(question)
    print("\nFINAL ANSWER:")
    print(answer)
