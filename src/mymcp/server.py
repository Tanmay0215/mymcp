"""
Enhanced MCP Server using FastMCP

This server demonstrates comprehensive MCP features:
- Tools: 30+ functions across 6 categories
- Resources: Data sources that LLMs can read
- Prompts: Reusable templates for LLM interactions
- Email: Gmail SMTP integration for sending emails
"""

from fastmcp import FastMCP
from .tools import register_all_tools
from .resources import register_all_resources
from .prompts import register_all_prompts

# Create the MCP server instance
mcp = FastMCP(name="EnhancedServer", version="2.0.0")

# Register all tools, resources, and prompts
register_all_tools(mcp)
register_all_resources(mcp)
register_all_prompts(mcp)


def run():
    """Run the MCP server."""
    mcp.run()
