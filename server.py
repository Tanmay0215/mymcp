"""
Enhanced MCP Server using FastMCP

This server demonstrates comprehensive MCP features:
- Tools: 30+ functions across 6 categories
- Resources: Data sources that LLMs can read
- Prompts: Reusable templates for LLM interactions
- Email: Gmail SMTP integration for sending emails
"""

from fastmcp import FastMCP, Context
import datetime
import os
import json
import base64
import uuid
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import requests
import psutil

# Load environment variables from .env file
load_dotenv()

# Create the MCP server instance
mcp = FastMCP(name="EnhancedServer", version="2.0.0")


# ============================================================================
# CONFIGURATION
# ============================================================================

def get_gmail_config():
    """Get Gmail SMTP configuration from environment variables."""
    return {
        "user": os.getenv("GMAIL_USER"),
        "password": os.getenv("GMAIL_APP_PASSWORD"),
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", "587"))
    }


# ============================================================================
# TOOLS - BASIC MATH (Original)
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
# TOOLS - FILE OPERATIONS
# ============================================================================

@mcp.tool
def read_file(path: str) -> str:
    """Read the contents of a file.
    
    Args:
        path: Path to the file to read
    
    Returns:
        File contents as a string
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


@mcp.tool
def write_file(path: str, content: str) -> str:
    """Write content to a file.
    
    Args:
        path: Path to the file to write
        content: Content to write to the file
    
    Returns:
        Success message or error
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


@mcp.tool
def list_directory(path: str = ".") -> str:
    """List contents of a directory.
    
    Args:
        path: Path to the directory (default: current directory)
    
    Returns:
        List of files and directories
    """
    try:
        items = os.listdir(path)
        return "\n".join(sorted(items))
    except Exception as e:
        return f"Error listing directory: {str(e)}"


@mcp.tool
def file_exists(path: str) -> bool:
    """Check if a file or directory exists.
    
    Args:
        path: Path to check
    
    Returns:
        True if exists, False otherwise
    """
    return os.path.exists(path)


@mcp.tool
def get_file_size(path: str) -> str:
    """Get the size of a file in bytes.
    
    Args:
        path: Path to the file
    
    Returns:
        File size in bytes or error message
    """
    try:
        size = os.path.getsize(path)
        return f"{size} bytes"
    except Exception as e:
        return f"Error getting file size: {str(e)}"


# ============================================================================
# TOOLS - STRING UTILITIES
# ============================================================================

@mcp.tool
def reverse_string(text: str) -> str:
    """Reverse a string.
    
    Args:
        text: String to reverse
    
    Returns:
        Reversed string
    """
    return text[::-1]


@mcp.tool
def count_words(text: str) -> int:
    """Count the number of words in text.
    
    Args:
        text: Text to count words in
    
    Returns:
        Number of words
    """
    return len(text.split())


@mcp.tool
def to_uppercase(text: str) -> str:
    """Convert text to uppercase.
    
    Args:
        text: Text to convert
    
    Returns:
        Uppercase text
    """
    return text.upper()


@mcp.tool
def to_lowercase(text: str) -> str:
    """Convert text to lowercase.
    
    Args:
        text: Text to convert
    
    Returns:
        Lowercase text
    """
    return text.lower()


@mcp.tool
def trim_whitespace(text: str) -> str:
    """Remove leading and trailing whitespace.
    
    Args:
        text: Text to trim
    
    Returns:
        Trimmed text
    """
    return text.strip()


# ============================================================================
# TOOLS - DATA PROCESSING
# ============================================================================

@mcp.tool
def parse_json(json_string: str) -> str:
    """Parse a JSON string and return formatted output.
    
    Args:
        json_string: JSON string to parse
    
    Returns:
        Formatted JSON or error message
    """
    try:
        data = json.loads(json_string)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error parsing JSON: {str(e)}"


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


@mcp.tool
def generate_uuid() -> str:
    """Generate a random UUID v4.
    
    Returns:
        UUID string
    """
    return str(uuid.uuid4())


@mcp.tool
def encode_base64(text: str) -> str:
    """Encode text to base64.
    
    Args:
        text: Text to encode
    
    Returns:
        Base64 encoded string
    """
    return base64.b64encode(text.encode()).decode()


@mcp.tool
def decode_base64(encoded: str) -> str:
    """Decode base64 to text.
    
    Args:
        encoded: Base64 encoded string
    
    Returns:
        Decoded text or error message
    """
    try:
        return base64.b64decode(encoded.encode()).decode()
    except Exception as e:
        return f"Error decoding base64: {str(e)}"


# ============================================================================
# TOOLS - SYSTEM INFORMATION
# ============================================================================

@mcp.tool
def get_system_info() -> dict:
    """Get system information (OS, CPU, memory).
    
    Returns:
        Dictionary with system information
    """
    return {
        "platform": psutil.os.name,
        "cpu_count": psutil.cpu_count(),
        "total_memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "available_memory_gb": round(psutil.virtual_memory().available / (1024**3), 2)
    }


@mcp.tool
def get_disk_usage(path: str = "/") -> dict:
    """Get disk usage statistics for a path.
    
    Args:
        path: Path to check (default: root)
    
    Returns:
        Dictionary with disk usage info
    """
    try:
        usage = psutil.disk_usage(path)
        return {
            "total_gb": round(usage.total / (1024**3), 2),
            "used_gb": round(usage.used / (1024**3), 2),
            "free_gb": round(usage.free / (1024**3), 2),
            "percent_used": usage.percent
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool
def get_cpu_percent() -> float:
    """Get current CPU usage percentage.
    
    Returns:
        CPU usage percentage
    """
    return psutil.cpu_percent(interval=1)


@mcp.tool
def get_memory_info() -> dict:
    """Get detailed memory usage information.
    
    Returns:
        Dictionary with memory info
    """
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / (1024**3), 2),
        "available_gb": round(mem.available / (1024**3), 2),
        "used_gb": round(mem.used / (1024**3), 2),
        "percent_used": mem.percent
    }


# ============================================================================
# TOOLS - WEB UTILITIES
# ============================================================================

@mcp.tool
def fetch_url(url: str) -> str:
    """Fetch content from a URL.
    
    Args:
        url: URL to fetch
    
    Returns:
        Response text or error message
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text[:1000]  # Limit to first 1000 chars
    except Exception as e:
        return f"Error fetching URL: {str(e)}"


@mcp.tool
def check_url_status(url: str) -> dict:
    """Check if a URL is accessible and get status code.
    
    Args:
        url: URL to check
    
    Returns:
        Dictionary with status info
    """
    try:
        response = requests.head(url, timeout=5)
        return {
            "url": url,
            "status_code": response.status_code,
            "accessible": response.status_code < 400
        }
    except Exception as e:
        return {
            "url": url,
            "error": str(e),
            "accessible": False
        }


@mcp.tool
def extract_domain(url: str) -> str:
    """Extract domain from a URL.
    
    Args:
        url: URL to extract domain from
    
    Returns:
        Domain name
    """
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc or parsed.path
    except Exception as e:
        return f"Error extracting domain: {str(e)}"


# ============================================================================
# TOOLS - EMAIL (Gmail SMTP)
# ============================================================================

@mcp.tool
async def send_email(
    ctx: Context,
    to: str,
    subject: str,
    body: str,
    html: bool = False
) -> str:
    """Send an email via Gmail SMTP.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content
        html: Whether body is HTML (default: False for plain text)
    
    Returns:
        Success message or error
    """
    try:
        config = get_gmail_config()
        
        if not config["user"] or not config["password"]:
            return "Error: Gmail credentials not configured. Please set GMAIL_USER and GMAIL_APP_PASSWORD in .env file"
        
        await ctx.info(f"Sending email to {to}...")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = config["user"]
        msg['To'] = to
        msg['Subject'] = subject
        
        # Attach body
        mime_type = 'html' if html else 'plain'
        msg.attach(MIMEText(body, mime_type))
        
        # Send email
        with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
            server.starttls()
            server.login(config["user"], config["password"])
            server.send_message(msg)
        
        return f"Email sent successfully to {to}"
    except Exception as e:
        return f"Error sending email: {str(e)}"


@mcp.tool
async def send_email_with_attachment(
    ctx: Context,
    to: str,
    subject: str,
    body: str,
    file_path: str
) -> str:
    """Send an email with an attachment via Gmail SMTP.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content
        file_path: Path to file to attach
    
    Returns:
        Success message or error
    """
    try:
        config = get_gmail_config()
        
        if not config["user"] or not config["password"]:
            return "Error: Gmail credentials not configured. Please set GMAIL_USER and GMAIL_APP_PASSWORD in .env file"
        
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"
        
        await ctx.info(f"Sending email with attachment to {to}...")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = config["user"]
        msg['To'] = to
        msg['Subject'] = subject
        
        # Attach body
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach file
        with open(file_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        filename = os.path.basename(file_path)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(part)
        
        # Send email
        with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
            server.starttls()
            server.login(config["user"], config["password"])
            server.send_message(msg)
        
        return f"Email with attachment sent successfully to {to}"
    except Exception as e:
        return f"Error sending email with attachment: {str(e)}"


@mcp.tool
def parse_email_address(email_string: str) -> dict:
    """Parse an email address string into name and address components.
    
    Args:
        email_string: Email string (e.g., "John Doe <john@example.com>")
    
    Returns:
        Dictionary with name and email
    """
    try:
        from email.utils import parseaddr
        name, email = parseaddr(email_string)
        return {
            "name": name or "Unknown",
            "email": email
        }
    except Exception as e:
        return {
            "error": str(e)
        }


# ============================================================================
# RESOURCES - Data sources that LLMs can read
# ============================================================================

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
