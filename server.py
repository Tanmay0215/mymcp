"""
Simple MCP Server using FastMCP

This server demonstrates the core features of FastMCP:
- Tools: Functions that LLMs can call to perform actions
- Resources: Data sources that LLMs can read
- Prompts: Reusable templates for LLM interactions
"""

from fastmcp import FastMCP, Context
import datetime

# Create the MCP server instance
mcp = FastMCP(name="SimpleServer", version="1.0.0")


# ============================================================================
# TOOLS - Functions that LLMs can call to perform actions
# ============================================================================

@mcp.tool
def add(a: float, b: float) -> float:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The sum of a and b
    """
    return a + b


@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The product of a and b
    """
    return a * b


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


# ============================================================================
# RESOURCES - Data sources that LLMs can read
# ============================================================================

@mcp.resource("info://server")
def get_server_info():
    """Get information about this MCP server."""
    return {
        "name": "SimpleServer",
        "version": "1.0.0",
        "description": "A simple MCP server demonstrating FastMCP features",
        "capabilities": ["tools", "resources", "prompts"]
    }


@mcp.resource("config://settings")
def get_settings():
    """Get server configuration settings."""
    return {
        "max_connections": 10,
        "timeout": 30,
        "debug_mode": False
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


# ============================================================================
# PROMPTS - Reusable templates for LLM interactions
# ============================================================================

@mcp.prompt
def summarize_text(text: str) -> str:
    """Generate a prompt asking the LLM to summarize text.
    
    Args:
        text: The text to summarize
    """
    return f"""Please provide a concise summary of the following text:

{text}

Summary:"""


@mcp.prompt
def code_review(code: str, language: str = "python") -> str:
    """Generate a prompt for code review.
    
    Args:
        code: The code to review
        language: Programming language of the code
    """
    return f"""Please review the following {language} code and provide feedback on:
1. Code quality and best practices
2. Potential bugs or issues
3. Suggestions for improvement

Code:
```{language}
{code}
```

Review:"""


# ============================================================================
# MAIN - Run the server
# ============================================================================

if __name__ == "__main__":
    # Run the server
    # The server will be available for MCP clients to connect to
    mcp.run()
