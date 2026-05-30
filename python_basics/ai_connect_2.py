from dotenv import load_dotenv
import os 
import requests
import json 

load_dotenv()

f = open("system_prompt.txt","r")
SYSTEM_PROMPT = f.read()
f.close()

USER_QUERY = input("Enter Human Query: ")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_URL = "https://api.openai.com/v1/responses"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

PAYLOAD = {
    "model": "gpt-5.4-mini",
    "instructions": SYSTEM_PROMPT,
    "input": USER_QUERY
}

JSON_CONVERTED_PAYLOAD = json.dumps(PAYLOAD)

response = requests.post(OPENAI_URL,data=JSON_CONVERTED_PAYLOAD,headers=HEADERS)

RAW_AI_RESPONSE = response.json()
AI_RESPONSE = RAW_AI_RESPONSE['output'][0]['content'][0]['text']
print("\nAI OUTPUT:\n")
print(AI_RESPONSE)