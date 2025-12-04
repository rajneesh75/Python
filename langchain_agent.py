from langchain.agents import initialize_agent, AgentType

tools = [search_code, update_jira_description]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)