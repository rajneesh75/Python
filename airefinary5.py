import asyncio
import os
from air import DistillerClient
from dotenv import load_dotenv

load_dotenv()

api_key = str(os.getenv("AIREFINARY"))

print(repr(api_key))
PROJECT_NAME = "cricket_team"
CONFIG_PATH = "selection.yaml"


# -----------------------------------------------------------------------
# Custom executor for "captain agent"
# This function is called whenever the orchestrator invokes the captain agent.
# You can plug in any logic here — an LLM call, a rules engine, etc.
# -----------------------------------------------------------------------
async def captain_agent_executor(query: str) -> str:
    """
    Simulates an experienced ODI captain making tactical decisions.
    Replace the body with real logic or an LLM call as needed.
    """
    return (
        f"Captain Agent responding to: '{query}'\n\n"
        "Tactical assessment:\n"
        "- Toss decision will depend on pitch report and dew factor.\n"
        "- Opening bowlers to target top-order with swing in the first 10 overs.\n"
        "- Spin duo to be introduced in the middle overs (15-40) to stem run flow.\n"
        "- Field placements will shift to attacking positions in the death overs.\n"
        "- Batting order flexible — finishers held back based on match situation."
    )


# -----------------------------------------------------------------------
# Map agent_name -> executor for every CustomAgent in your YAML
# PlannerAgent does NOT need an entry here — it is handled internally
# -----------------------------------------------------------------------
EXECUTOR_DICT = {
    "captain agent": captain_agent_executor,
}


# -----------------------------------------------------------------------
# One-time project setup — safe to call every run because
# create_project is idempotent on most Distiller versions.
# -----------------------------------------------------------------------
def setup_project(distiller_client: DistillerClient) -> bool:
    print("Validating config...")
    if not distiller_client.validate_config(config_path=CONFIG_PATH):
        print("❌ Configuration validation failed. Aborting.")
        return False

    print("Registering project...")
    distiller_client.create_project(
        config_path=CONFIG_PATH,
        project=PROJECT_NAME,
    )
    print(f"✅ Project '{PROJECT_NAME}' ready.\n")
    return True


# -----------------------------------------------------------------------
# Main agent session
# -----------------------------------------------------------------------
async def run_cricket_agents():
    distiller_client = DistillerClient(api_key=api_key)

    if not setup_project(distiller_client):
        return

    async with distiller_client(
            project=PROJECT_NAME,
            uuid="rajneesh",  # unique session/user identifier
            executor_dict=EXECUTOR_DICT,
    ) as dc:

        queries = [
            # Query 1 — triggers PlannerAgent (team selection)
            (
                "Pick a 17 member Indian squad from early 1990s era for a 5-match ODI series in Australia. "
                "Include a mix of experienced players and young talent. "
                "Ensure 2 wicket-keepers and a balanced bowling attack. "
                "Justify each selection."
            ),
            # Query 2 — triggers captain agent (tactical planning)
            (
                "We won the toss at the MCG. The pitch looks dry and the outfield is fast. "
                "Dew is expected in the second innings. "
                "Should we bat or bowl first? "
                "What is your game plan in each case?"
            ),
        ]

        for i, query in enumerate(queries, start=1):
            print(f"{'=' * 60}")
            print(f"Query {i}: {query}\n")

            responses = await dc.query(query=query)

            async for response in responses:
                # response dict typically contains 'content' and 'agent_name'
                agent_label = response.get("agent_name", "Agent")
                content = response.get("content", "")
                print(f"[{agent_label}]:\n{content}\n")


# -----------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(run_cricket_agents())
