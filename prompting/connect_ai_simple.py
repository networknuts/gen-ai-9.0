from openai import OpenAI
from dotenv import load_dotenv


# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

# ASK FOR USER QUESTION
user_query = input("Enter your query: ")

# LATEST OPENAI RESPONSE API
response = client.responses.create(
    model="gpt-5.4-mini",
    input=user_query
)

print(response.output_text)