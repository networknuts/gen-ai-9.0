from dotenv import load_dotenv
from openai import OpenAI 
import requests
import os 

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

# CREATE OUR FIRST TOOL - GET WEATHER TOOL

def get_weather(zipcode):
    weather_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    weather_country_code = "in"
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},{weather_country_code}&appid={weather_api_key}"
    result = requests.get(url)
    response = result.json()
    return response 

# READ THE WEATHER DESCRIPTION
f = open("weather_description.txt","r")
weather_description = f.read()
f.close()

# TOOL SCHEMA

tool_schema = [
    {
        "type": "function",
        "name": "get_weather",
        "description": weather_description,
        "parameters": {
            "type": "object",
            "properties": {
                "zipcode": {
                    "type": "string",
                    "description": "the zipcode of the location to get the weather of."
                },
            },
            "required": ["zipcode"],
        }
    }
]

# ASK FOR USER QUERY

user_query = input("Human Query: ")

# FIRST LLM CALL
response = client.responses.create(
    model="gpt-5.4-mini",
    input=user_query,
    tools=tool_schema
)

# CREATE TOOL EXECUTION PROCESS