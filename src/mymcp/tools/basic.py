"""
Basic utility tools.
"""

import datetime
from fastmcp import Context


def register_tools(mcp):
    """Register basic utility tools with the MCP server."""
    
    @mcp.tool
    async def get_current_time(ctx: Context) -> str:
        """Get the current date and time.
        
        Returns:
            Current timestamp as a formatted string
        """
        await ctx.info("Fetching current time...")
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    @mcp.tool
    def greet(name: str, enthusiastic: bool = False) -> str:
        """Generate a greeting message.
        
        Args:
            name: Name of the person to greet
            enthusiastic: Whether to add extra enthusiasm
        
        Returns:
            A greeting message
        """
        greeting = f"Hello, {name}!"
        if enthusiastic:
            greeting += " 🎉"
        return greeting
