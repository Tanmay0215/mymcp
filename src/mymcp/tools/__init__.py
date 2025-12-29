"""
Tool registration module.
"""

from . import basic, files, validation, system, web, email, docs, code


def register_all_tools(mcp):
    """Register all tools with the MCP server."""
    basic.register_tools(mcp)
    files.register_tools(mcp)
    validation.register_tools(mcp)
    system.register_tools(mcp)
    web.register_tools(mcp)
    email.register_tools(mcp)
    docs.register_tools(mcp)
    code.register_tools(mcp)
