
from langgraph.prebuilt import ToolNode

def create_tool_node(tools: list) -> dict:
    return ToolNode(tools)
