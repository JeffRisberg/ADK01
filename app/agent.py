from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
import yfinance as yf
from typing import Dict, Any, Optional

def get_stock_price(ticker: str, tool_context: ToolContext):
    stock = yf.Ticker(ticker)
    price = stock.info.get("currentPrice", "Price not available")

    # Initialize recent_searches if it doesn't exist
    if "recent_searches" not in tool_context.state:
        tool_context.state["recent_searches"] = []

    recent_searches = tool_context.state["recent_searches"]
    if ticker not in recent_searches:
        recent_searches.append(ticker)
        tool_context.state["recent_searches"] = recent_searches

    return {"price": price, "ticker": ticker}

def get_stock_info(ticker: str):
    stock = yf.Ticker(ticker)
    company_name = stock.info.get("shortName", "Name not available")
    sector = stock.info.get("sector", "Sector not available")
    return {
        "ticker": ticker,
        "company_name": company_name,
        "sector": sector
    }

multi_tool_agent = Agent(
    name="multi_tool_agent",
    model="gemini-2.0-flash",
    description="An agent with multiple stock information tools",
    instruction="""
    You are a stock information assistant. You have two tools:
    - get_stock_price: For prices
    - get_stock_info: For company name and sector
    """,
    tools=[get_stock_price, get_stock_info],
)

def before_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
    # Initialize tool_usage if it doesn't exist
    if "tool_usage" not in tool_context.state:
        tool_context.state["tool_usage"] = {}

    # Track tool usage count
    tool_usage = tool_context.state["tool_usage"]
    tool_name = tool.name
    tool_usage[tool_name] = tool_usage.get(tool_name, 0) + 1
    tool_context.state["tool_usage"] = tool_usage

    print(f"[LOG] Running tool: {tool_name}")
    return None

def after_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict) -> Optional[Dict]:
    print(f"[LOG] Tool {tool.name} completed")
    return None

# Initialize state before creating the agent
initial_state = {"tool_usage": {}}

callback_agent = Agent(
    name="callback_agent",
    model="gemini-2.0-flash",
    description="An agent with callbacks",
    instruction="""
    You are a stock assistant. Use get_stock_data tool to check stock prices.
    This agent keeps track of how many times tools have been used.
    """,
    tools=[get_stock_price, get_stock_info],
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)

root_agent = callback_agent  # ADK requires the main agent to be named root_agent

