from fastapi import FastAPI, Request

from langchain_agent import agent

app = FastAPI()


@app.post("/jira-agent")
async def jira_agent(request: Request):
    body = await request.json()

    story_key = body["issue"]["key"]
    summary = body["issue"]["fields"]["summary"]

    initial_state = {
        "jira_key": story_key,
        "story_summary": summary
    }

    agent.invoke(initial_state)

    return {"status": "AI agent executed"}
