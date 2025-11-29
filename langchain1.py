from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.globals import set_debug, set_verbose
import os
from dotenv import load_dotenv

set_debug(True)
set_verbose(True)

load_dotenv()
chat = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"), verbose=True)


template_string = """Translate the text that is delimited by triple backticks \
into a style that is {style}. text: ```{text}```"""

prompt_template = ChatPromptTemplate.from_template(template_string)
print(prompt_template.messages[0].prompt)
print(prompt_template.messages[0].prompt.input_variables)

customer_style = """Hindi"""
customer_email = """Arrr, I be fuming that me blender lid flew off and splattered me kitchen walls \
with smoothie! And to make matters worse, the warranty don't cover the cost of \
cleaning up me kitchen. I need yer help right now, matey!"""

customer_messages = prompt_template.format_messages(style=customer_style, text=customer_email)
print(type(customer_messages))
print(customer_messages[0])

# Call the LLM to translate the style
customer_message = chat.invoke(customer_messages)
print(customer_message.content)

service_reply = """Hey there customer,the warranty does not cover cleaning expenses for your kitchen \
because it's your fault that you misused your blender by forgetting to put the lid on before \
starting the blender. Tough luck! See ya!"""

service_style = """Bhojpuri"""

service_messages = prompt_template.format_messages(style=service_style, text=service_reply)
print(service_messages[0].content)

service_response = chat.invoke(service_messages)
print(service_response.content)
