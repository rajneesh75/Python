from databricks.sdk import WorkspaceClient
import logging

logging.basicConfig(level=logging.DEBUG)

w = WorkspaceClient()
SPACE_ID = "01f11af19a0a1fcea21b49b146571f46"


def get_answer(msg):
    for attachment in msg.attachments:
        if attachment.text is not None:
            return attachment.text.content

    return "No text answer returned."


question = input("You: ")

msg = w.genie.start_conversation_and_wait(space_id=SPACE_ID, content=question)
conversation_id = msg.conversation_id
print("Genie:", get_answer(msg))

while True:
    question = input("\nYou: ")

    if question.lower() in ("exit", "quit"):
        break

    msg = w.genie.create_message_and_wait(
        space_id=SPACE_ID,
        conversation_id=conversation_id,
        content=question
    )

    print("Genie:", get_answer(msg))
