"""
Server information resources.
"""

import os


def register_resources(mcp):
    """Register server resources with the MCP server."""
    
    @mcp.resource("info://server")
    def get_server_info():
        """Get information about this MCP server."""
        return {
            "name": "EnhancedServer",
            "version": "2.0.0",
            "description": "Enhanced MCP server with 30+ tools including Gmail SMTP",
            "capabilities": ["tools", "resources", "prompts", "email"],
            "tool_categories": [
                "math",
                "file_operations",
                "string_utilities",
                "data_processing",
                "system_info",
                "web_utilities",
                "email"
            ]
        }

    @mcp.resource("config://settings")
    def get_settings():
        """Get server configuration settings."""
        return {
            "max_connections": 10,
            "timeout": 30,
            "debug_mode": False,
            "email_configured": bool(os.getenv("GMAIL_USER") and os.getenv("GMAIL_APP_PASSWORD"))
        }

    @mcp.resource("data://user/{user_id}")
    def get_user_data(user_id: int):
        """Get user data by ID (dynamic resource template).
        
        Args:
            user_id: The user's ID
        """
        # In a real application, this would fetch from a database
        return {
            "id": user_id,
            "name": f"User {user_id}",
            "status": "active",
            "created_at": "2024-01-01"
        }
