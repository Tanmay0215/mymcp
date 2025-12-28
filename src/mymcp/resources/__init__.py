"""
Resource registration module.
"""

from . import info


def register_all_resources(mcp):
    """Register all resources with the MCP server."""
    info.register_resources(mcp)
