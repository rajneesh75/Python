from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
wait = w.genie.start_conversation_and_wait(
    space_id="01f11af19a0a1fcea21b49b146571f46",
    content="How many total customers?"
)

print("\nQuestion:")
print(wait.content)

print("\nStatus:")
print(wait.status)

print("\nConversation:")
print(wait.conversation_id)

print("\nSQL:")
print(wait.attachments[0].query.query)

print("\nAnswer:")
print(wait.attachments[2].text.content)
