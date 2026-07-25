from mcp.server.fastmcp import FastMCP
import requests
import wikipedia

mcp = FastMCP("Customer Support MCP Server", json_response=True)

@mcp.tool()
def get_order_data(customer_id: int):
    """
    Get the following information about the ordered item of the customer:
    - item name
    - delivery date
    - delivery status

    The function requires a customer_id to work and provides the above data
    for the particular customer_id. 
    """
    url = f"http://localhost:8081/delivery/{customer_id}"
    result = requests.get(url)
    if result.status_code != 200:
        return {
            "Error": "Order data not found."
        }
    else:
        return {
            "Data": result.json()
        }

@mcp.tool()
def wikipedia_search(topic: str):
    """
    Get wikipedia summary of any topic by providing
    the relevant topic name. This wikipedia search tool is limited
    to only providing a 10 line summary of the given topic.
    """
    try:
        return {
            "Data": wikipedia.summary(topic,sentences=10)
        }
    except Exception as e:
        return {
            "Error": str(e)
        }

mcp.run(transport="streamable-http")