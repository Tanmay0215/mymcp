"""
Prompt registration module.
"""

from . import templates


def register_all_prompts(mcp):
    """Register all prompts with the MCP server."""
    templates.register_prompts(mcp)
