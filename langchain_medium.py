from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
from pprint import pprint

load_dotenv()
llm = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))


# Define the schema for nutritional values
class NutritionValue(BaseModel):
    """Represents a specific nutritional component of a food item, including its name, value,
    and unit of measurement."""

    name: str = Field(description="The name of the nutritional component (e.g., Protein, Calories, Carbohydrates).")
    value: float = Field(description="The numerical value of the nutritional component per serving.")
    unit: str = Field(description="The unit of measurement for the nutrition value (e.g., kcal, g, mg).")


# Define the schema for food information
class FoodInformation(BaseModel):
    """Stores detailed information about a food item, including its name, nutritional values,
     and standard serving size."""

    name: str = Field(description="The name of the food item (e.g., Apple, Chicken Breast).")
    nutritions: List[NutritionValue] = Field(description="A list of nutritional values associated with the food item.")
    serving_size: float = Field(
        description="The standard serving size of the food item in grams (g) or milliliters (ml).")


# Define the response schema for API output
class ResponseSchema(BaseModel):
    """Defines the structure of the API response, including status, message, and retrieved food information."""

    status: bool = Field(description="Indicates whether the request was successful. True for success, False otherwise.")
    message: str = Field(
        description="A descriptive message providing information about the response "
                    "(e.g., 'Data retrieved successfully' or 'Invalid input').")
    data: List[FoodInformation] = Field(
        description="A list of food items containing their names, nutritional values, "
                    "and serving sizes. Returns an empty list if no data is found.")


# Create a JSON output parser using the defined response schema
food_parser = JsonOutputParser(name="food item", pydantic_object=ResponseSchema)

# Print format instructions for generating structured JSON output
# pprint(food_parser.get_format_instructions())

# Print JSON schema for validation/debugging purposes
# pprint(food_parser.get_config_jsonschema())

# Define the prompt template for generating food nutrition information
food_template = """You are a nutritionist expert. You are given a food item and you need to 
return the nutrition information of the food item.
Food: {food}.
If it is not a food item, return the proper message: "Provided item is not a food".
Format output:
{format_instructions}
"""

# Create a prompt template with input variables and formatted output instructions
food_prompt = PromptTemplate(
    input_variables=["food"],
    template=food_template,
    partial_variables={"format_instructions": food_parser.get_format_instructions()}
)

# Define a processing chain: Prompt → LLM → JSON Parser
food_chain = food_prompt | llm | food_parser

# Invoke the chain with an example input and print the structured output
output = food_chain.invoke({"food": "pizza"})
pprint(output)
