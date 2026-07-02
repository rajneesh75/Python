import yaml
import mlflow

catalog = "main"
schema = "dbdemos_ai_agent"

rag_chain_config = {
    "config_version_name": "first_config",
    "input_example": [{"role": "user", "content": "Give me the orders for john21@example.net"}],
    "uc_tool_names": [f"{catalog}.{schema}.*"],
    "system_prompt": "Your job is to provide customer help. call the tool to answer.",
    "llm_endpoint_name": "databricks-claude-opus-4-6",
    "max_history_messages": 20,
    "retriever_config": None,
    "mcp_server_urls": []
}
try:
    with open('agent_config.yaml', 'w') as f:
        yaml.dump(rag_chain_config, f)
except:
    print('pass to work on build job')
model_config = mlflow.models.ModelConfig(development_config='agent_config.yaml')

