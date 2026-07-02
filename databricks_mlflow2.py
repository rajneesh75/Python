import sys


# Reload the agent module to pick up the updated configuration
import importlib
if 'agent' in sys.modules:
    importlib.reload(sys.modules['agent'])
    from agent import AGENT
else:
    from agent import AGENT

# Correct request format
request_example = "Give me the information about john21@example.net"
answer = AGENT.predict({"input":[{"role": "user", "content": request_example}]})