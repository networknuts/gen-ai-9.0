from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
import asyncio
from openai import OpenAI 
from dotenv import load_dotenv
import json 

# SETUP OPENAI ENVIRONMENT
load_dotenv()
client = OpenAI()

# CREATE DYNAMIC TOOL DISCOVERY - OPENAI 
def convert_tool_to_openai_schema(tool):
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": tool.inputSchema
    }

# FUNCTION TO CONNECT TO MCP
async def main():
    query = input("Enter human query: ")
    async with streamable_http_client("http://localhost:8000/mcp") as (
        read_stream,
        write_stream,
        input_stream
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tool_list = await session.list_tools()
            openai_tools = []
            for t in tool_list.tools:
                openai_tools.append(convert_tool_to_openai_schema(t))
            response = client.responses.create(
                model="gpt-5.4-mini",
                input=query,
                tools=openai_tools
            )
            tool_call = None
            for item in response.output:
                if item.type == "function_call":
                    tool_call = item 
                    break 
            if tool_call:
                tool_name = tool_call.name 
                args = json.loads(tool_call.arguments)
                print(f"LLM SELECTED TOOL: {tool_name}")
                result = await session.call_tool(tool_name,args)
                for item in result.content:
                    print(item.text)
            else:
                print("NO TOOL SELECTED, RUNNING LLM DIRECTLY.")
                print(response.output_text)            

asyncio.run(main())