from openai import OpenAI
from dotenv import load_dotenv

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

# ASK FOR USER QUERY
query = input("Human Query: ")

# MAKE THE LLM CALL
response = client.responses.create(
    model="gpt-5.4-mini",
    input=[
        {
            "role": "user",
            "content": "hello, my name is aryan."
        },
        {
            "role": "assistant",
            "content": "Hi Aryan — nice to meet you! What can I help you with today?"
        },
        {
            "role": "user",
            "content": query
        }
    ]
)

# PRINT THE RESPONSE
print(response.output_text)