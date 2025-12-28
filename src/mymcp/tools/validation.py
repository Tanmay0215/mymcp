"""
Data validation tools.
"""

import re


def register_tools(mcp):
    """Register data validation tools with the MCP server."""
    
    @mcp.tool
    def validate_email_format(email: str) -> bool:
        """Validate email address format.
        
        Args:
            email: Email address to validate
        
        Returns:
            True if valid format, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
