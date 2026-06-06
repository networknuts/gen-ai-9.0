from openai import OpenAI
from dotenv import load_dotenv

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

# LOAD THE SYSTEM PROMPT
f = open("few_shot_prompt.txt","r")
system_prompt = f.read()
f.close()

# ASK FOR USER QUERY
query = input("Human Query: ")

# MAKE THE LLM CALL
response = client.responses.create(
    model="gpt-5.4-mini",
    instructions=system_prompt,
    input=query
)

# PRINT THE RESPONSE
print(response.output_text)