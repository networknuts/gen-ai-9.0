from dotenv import load_dotenv
from openai import OpenAI 
import requests
import os 
import json


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

# CREATE SECOND TOOL - GET ORDER DATA

def get_order_data(user_id):
    url = f"http://localhost:8080/delivery/{user_id}"
    result = requests.get(url)
    if result.status_code != 200:
        return {"Error": "User Not Found"}
    else:
        return result.json()

# READ THE WEATHER DESCRIPTION
f = open("weather_description.txt","r")
weather_description = f.read()
f.close()

# READ THE ORDERDATA DESCRIPTION
f = open("orderdata_description.txt","r")
orderdata_description = f.read()
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
    },
    {
        "type": "function",
        "name": "get_order_data",
        "description": orderdata_description,
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "the ID of the user to get order information about"
                },
            },
            "required": ["user_id"]
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

#print(response.output)

# CREATE TOOL EXECUTION PROCESS
function_output = []

for item in response.output:
    if item.type == "function_call":
        args = json.loads(item.arguments)
        if item.name == "get_weather":
            result = get_weather(args['zipcode'])
            print("RAW FUNCTION OUTPUT")
            print(result)
            print("---------------------------")
        elif item.name == "get_order_data":
            result = get_order_data(args['user_id'])
            print("RAW FUNCTION OUTPUT")
            print(result)
            print("---------------------------")
        else:
            result = "unknown function executed"

        function_output.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps({"result": result})
            }
        )

# SECOND LLM CALL
final_response = client.responses.create(
    model="gpt-5.4-mini",
    input=function_output,
    previous_response_id=response.id
)

print("REFINED AI OUTPUT\n")
print(final_response.output_text)