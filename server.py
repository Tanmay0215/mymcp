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
import imaplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import csv
import io
import yaml
import subprocess
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


def get_gmail_imap_config():
    """Get Gmail IMAP configuration from environment variables."""
    return {
        "user": os.getenv("GMAIL_USER"),
        "password": os.getenv("GMAIL_APP_PASSWORD"),
        "imap_server": os.getenv("IMAP_SERVER", "imap.gmail.com"),
        "imap_port": int(os.getenv("IMAP_PORT", "993"))
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


@mcp.tool
async def list_emails(
    ctx: Context,
    limit: int = 10,
    folder: str = "INBOX"
) -> str:
    """List the latest emails in a mailbox folder.
    
    Args:
        limit: Maximum number of emails to return (default: 10)
        folder: Name of the folder to list (default: "INBOX")
        
    Returns:
        A formatted text list of the latest emails
    """
    try:
        config = get_gmail_imap_config()
        if not config["user"] or not config["password"]:
            return "Error: Gmail credentials not configured. Please set GMAIL_USER and GMAIL_APP_PASSWORD in .env file"
            
        await ctx.info(f"Connecting to Gmail IMAP to list latest emails in {folder}...")
        
        mail = imaplib.IMAP4_SSL(config["imap_server"], config["imap_port"])
        mail.login(config["user"], config["password"])
        
        # Select folder
        status, data = mail.select(folder)
        if status != "OK":
            mail.logout()
            return f"Error selecting folder '{folder}': {status}"
            
        # Search all emails
        status, messages = mail.search(None, "ALL")
        if status != "OK" or not messages[0]:
            mail.logout()
            return f"No messages found in folder '{folder}'"
            
        mail_ids = messages[0].split()
        await ctx.info(f"Total emails in {folder}: {len(mail_ids)}")
        
        # Get latest limit emails
        latest_ids = mail_ids[-limit:]
        latest_ids.reverse() # Newest first
        
        result = []
        result.append(f"Latest {len(latest_ids)} emails in {folder}:")
        result.append("=" * 60)
        
        for mid in latest_ids:
            status, msg_data = mail.fetch(mid, "(RFC822.HEADER)")
            if status != "OK":
                continue
                
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = _decode_mime_words(msg.get("Subject"))
                    from_ = _decode_mime_words(msg.get("From"))
                    date = msg.get("Date")
                    result.append(f"ID: {mid.decode()} | From: {from_}\nSubject: {subject}\nDate: {date}")
                    result.append("-" * 60)
                    
        mail.close()
        mail.logout()
        return "\n".join(result)
    except Exception as e:
        return f"Error listing emails: {str(e)}"


@mcp.tool
async def search_emails(
    ctx: Context,
    query: str,
    limit: int = 10,
    folder: str = "INBOX"
) -> str:
    """Search emails using IMAP search criteria (e.g. 'FROM "Indeed"', 'SUBJECT "resume"', etc.).
    
    Args:
        query: IMAP search criteria string (e.g. 'SUBJECT "hello"' or 'FROM "google"')
        limit: Maximum number of search results to return (default: 10)
        folder: Name of the folder to search in (default: "INBOX")
        
    Returns:
        A formatted text list of matching emails
    """
    try:
        config = get_gmail_imap_config()
        if not config["user"] or not config["password"]:
            return "Error: Gmail credentials not configured. Please set GMAIL_USER and GMAIL_APP_PASSWORD in .env file"
            
        await ctx.info(f"Connecting to Gmail IMAP to search {folder} with query: {query}...")
        
        mail = imaplib.IMAP4_SSL(config["imap_server"], config["imap_port"])
        mail.login(config["user"], config["password"])
        
        status, data = mail.select(folder)
        if status != "OK":
            mail.logout()
            return f"Error selecting folder '{folder}': {status}"
            
        # Perform search (query format depends on standard IMAP, e.g. FROM "Indeed")
        if '"' not in query and not any(k in query.upper() for k in ["FROM", "SUBJECT", "TO", "BODY", "TEXT"]):
            search_query = f'TEXT "{query}"'
        else:
            search_query = query
            
        status, messages = mail.search(None, search_query)
        if status != "OK" or not messages[0]:
            mail.logout()
            return f"No matching messages found for query: {search_query}"
            
        mail_ids = messages[0].split()
        await ctx.info(f"Found {len(mail_ids)} matching emails.")
        
        # Get latest limit emails
        latest_ids = mail_ids[-limit:]
        latest_ids.reverse() # Newest first
        
        result = []
        result.append(f"Found {len(mail_ids)} matching emails (showing latest {len(latest_ids)}):")
        result.append("=" * 60)
        
        for mid in latest_ids:
            status, msg_data = mail.fetch(mid, "(RFC822.HEADER)")
            if status != "OK":
                continue
                
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = _decode_mime_words(msg.get("Subject"))
                    from_ = _decode_mime_words(msg.get("From"))
                    date = msg.get("Date")
                    result.append(f"ID: {mid.decode()} | From: {from_}\nSubject: {subject}\nDate: {date}")
                    result.append("-" * 60)
                    
        mail.close()
        mail.logout()
        return "\n".join(result)
    except Exception as e:
        return f"Error searching emails: {str(e)}"


@mcp.tool
async def read_email(
    ctx: Context,
    email_id: str,
    folder: str = "INBOX"
) -> str:
    """Retrieve and read the full contents of a specific email by its ID.
    
    Args:
        email_id: The ID of the email to read (obtained from list_emails or search_emails)
        folder: Name of the folder the email belongs to (default: "INBOX")
        
    Returns:
        The full details of the email (Headers and Body)
    """
    try:
        config = get_gmail_imap_config()
        if not config["user"] or not config["password"]:
            return "Error: Gmail credentials not configured. Please set GMAIL_USER and GMAIL_APP_PASSWORD in .env file"
            
        await ctx.info(f"Connecting to Gmail IMAP to read email ID: {email_id}...")
        
        mail = imaplib.IMAP4_SSL(config["imap_server"], config["imap_port"])
        mail.login(config["user"], config["password"])
        
        status, data = mail.select(folder)
        if status != "OK":
            mail.logout()
            return f"Error selecting folder '{folder}': {status}"
            
        # Fetch full email message
        status, msg_data = mail.fetch(email_id.encode(), "(RFC822)")
        if status != "OK":
            mail.logout()
            return f"Error fetching email ID {email_id}: {status}"
            
        email_details = {}
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_details["Subject"] = _decode_mime_words(msg.get("Subject"))
                email_details["From"] = _decode_mime_words(msg.get("From"))
                email_details["To"] = _decode_mime_words(msg.get("To"))
                email_details["Date"] = msg.get("Date")
                email_details["Body"] = _get_email_body(msg)
                
        mail.close()
        mail.logout()
        
        if not email_details:
            return f"Error parsing email ID {email_id}"
            
        response = [
            f"Email Details (ID: {email_id})",
            "=" * 60,
            f"From:    {email_details.get('From')}",
            f"To:      {email_details.get('To')}",
            f"Subject: {email_details.get('Subject')}",
            f"Date:    {email_details.get('Date')}",
            "-" * 60,
            "Body:",
            email_details.get("Body"),
            "=" * 60
        ]
        return "\n".join(response)
    except Exception as e:
        return f"Error reading email: {str(e)}"


def _decode_mime_words(s: str) -> str:
    """Helper to decode MIME header words safely."""
    if not s:
        return ""
    try:
        decoded_words = decode_header(s)
        result = []
        for word, encoding in decoded_words:
            if isinstance(word, bytes):
                result.append(word.decode(encoding or 'utf-8', errors='replace'))
            else:
                result.append(word)
        return "".join(result)
    except Exception:
        return str(s)


def _get_email_body(msg: email.message.Message) -> str:
    """Helper to safely extract the readable body of an email message."""
    body = ""
    html_body = ""
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            # Extract plain text
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    payload = part.get_payload(decode=True)
                    body += payload.decode(part.get_content_charset() or 'utf-8', errors='replace')
                except Exception:
                    pass
            # Extract HTML as fallback
            elif content_type == "text/html" and "attachment" not in content_disposition:
                try:
                    payload = part.get_payload(decode=True)
                    html_body += payload.decode(part.get_content_charset() or 'utf-8', errors='replace')
                except Exception:
                    pass
    else:
        content_type = msg.get_content_type()
        try:
            payload = msg.get_payload(decode=True)
            text = payload.decode(msg.get_content_charset() or 'utf-8', errors='replace')
            if content_type == "text/html":
                html_body = text
            else:
                body = text
        except Exception:
            pass

    return body.strip() or html_body.strip() or "[No readable body found]"


# ============================================================================
# TOOLS - DATA CONVERTERS
# ============================================================================

@mcp.tool
def convert_json_to_yaml(json_string: str) -> str:
    """Convert a JSON string into a formatted YAML string.
    
    Args:
        json_string: The JSON formatted string to convert
        
    Returns:
        The converted YAML string or an error message
    """
    try:
        data = json.loads(json_string)
        return yaml.safe_dump(data, default_flow_style=False, sort_keys=False)
    except Exception as e:
        return f"Error converting JSON to YAML: {str(e)}"


@mcp.tool
def convert_yaml_to_json(yaml_string: str, indent: int = 4) -> str:
    """Convert a YAML string into a formatted JSON string.
    
    Args:
        yaml_string: The YAML formatted string to convert
        indent: JSON output indentation spaces (default: 4)
        
    Returns:
        The converted JSON string or an error message
    """
    try:
        data = yaml.safe_load(yaml_string)
        return json.dumps(data, indent=indent, ensure_ascii=False)
    except Exception as e:
        return f"Error converting YAML to JSON: {str(e)}"


@mcp.tool
def convert_csv_to_json(csv_string: str, delimiter: str = ",") -> str:
    """Convert CSV tabular data into a structured JSON array string.
    
    Args:
        csv_string: The CSV data string
        delimiter: The character used to separate fields (default: ",")
        
    Returns:
        A JSON array representation of the CSV rows or an error message
    """
    try:
        f = io.StringIO(csv_string.strip())
        reader = csv.DictReader(f, delimiter=delimiter)
        rows = list(reader)
        return json.dumps(rows, indent=4, ensure_ascii=False)
    except Exception as e:
        return f"Error converting CSV to JSON: {str(e)}"


@mcp.tool
def convert_json_to_csv(json_array_string: str, delimiter: str = ",") -> str:
    """Convert a JSON array of flat objects into a CSV string.
    
    Args:
        json_array_string: A JSON string representing an array of objects
        delimiter: The CSV column separator character (default: ",")
        
    Returns:
        The converted CSV string or an error message
    """
    try:
        data = json.loads(json_array_string)
        if not isinstance(data, list):
            return "Error: JSON input must be an array of objects."
        
        if not data:
            return ""
            
        headers = []
        for item in data:
            if isinstance(item, dict):
                for key in item.keys():
                    if key not in headers:
                        headers.append(key)
                        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=headers, delimiter=delimiter)
        writer.writeheader()
        
        for item in data:
            if isinstance(item, dict):
                writer.writerow({k: item.get(k, "") for k in headers})
                
        return output.getvalue()
    except Exception as e:
        return f"Error converting JSON to CSV: {str(e)}"


# ============================================================================
# TOOLS - MEDIA OPERATIONS (ffmpeg/ffprobe)
# ============================================================================

@mcp.tool
async def compress_image(
    ctx: Context,
    path: str,
    target_path: str = None,
    quality: int = 80,
    scale: str = None
) -> str:
    """Compress an image using ffmpeg.
    
    Args:
        path: Absolute path to the source image file
        target_path: Optional path for the compressed image (default: source_name_compressed.ext)
        quality: Quality compression level (1-100, default: 80)
        scale: Optional scale width/height (e.g., '800:-1' for width 800px maintaining aspect ratio)
        
    Returns:
        A success message with paths and sizes, or an error message
    """
    try:
        if not os.path.exists(path):
            return f"Error: Source image file not found at {path}"
            
        if not target_path:
            dir_name, file_name = os.path.split(path)
            name, ext = os.path.splitext(file_name)
            target_path = os.path.join(dir_name, f"{name}_compressed{ext}")
            
        ext = os.path.splitext(target_path)[1].lower()
        
        cmd = ["ffmpeg", "-y", "-i", path]
        
        if scale:
            cmd.extend(["-vf", f"scale={scale}"])
            
        if ext in [".webp", ".png"]:
            if ext == ".webp":
                cmd.extend(["-quality", str(max(1, min(100, quality)))])
            else:
                png_comp = max(0, min(9, int((100 - quality) * 9 / 100)))
                cmd.extend(["-compression_level", str(png_comp)])
        else:
            q_val = max(1, min(31, 31 - int(quality * 30 / 100)))
            cmd.extend(["-q:v", str(q_val)])
            
        cmd.append(target_path)
        
        await ctx.info(f"Running ffmpeg compression command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        orig_size = os.path.getsize(path) / (1024 * 1024)
        new_size = os.path.getsize(target_path) / (1024 * 1024)
        savings = (1 - (new_size / orig_size)) * 100 if orig_size > 0 else 0
        
        return (
            f"Image compressed successfully!\n"
            f"Source: {path} ({orig_size:.2f} MB)\n"
            f"Target: {target_path} ({new_size:.2f} MB)\n"
            f"File size reduced by: {savings:.1f}%"
        )
        
    except subprocess.CalledProcessError as e:
        return f"Error executing ffmpeg: {e.stderr}"
    except Exception as e:
        return f"Error compressing image: {str(e)}"


@mcp.tool
async def convert_image_format(
    ctx: Context,
    path: str,
    target_format: str = "webp",
    quality: int = 80
) -> str:
    """Convert an image to a different format (e.g., png to webp) using ffmpeg.
    
    Args:
        path: Absolute path to the source image file
        target_format: Target format extension (default: 'webp', support: 'png', 'jpg', 'jpeg')
        quality: Quality level for compression (1-100, default: 80)
        
    Returns:
        A success message with paths and sizes, or an error message
    """
    try:
        if not os.path.exists(path):
            return f"Error: Source image file not found at {path}"
            
        target_format = target_format.strip().lower().lstrip(".")
        
        dir_name, file_name = os.path.split(path)
        name, ext = os.path.splitext(file_name)
        
        target_path = os.path.join(dir_name, f"{name}.{target_format}")
        
        cmd = ["ffmpeg", "-y", "-i", path]
        
        if target_format == "webp":
            cmd.extend(["-quality", str(max(1, min(100, quality)))])
        elif target_format in ["jpg", "jpeg"]:
            q_val = max(1, min(31, 31 - int(quality * 30 / 100)))
            cmd.extend(["-q:v", str(q_val)])
        elif target_format == "png":
            png_comp = max(0, min(9, int((100 - quality) * 9 / 100)))
            cmd.extend(["-compression_level", str(png_comp)])
            
        cmd.append(target_path)
        
        await ctx.info(f"Running ffmpeg format conversion: {' '.join(cmd)}")
        
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        orig_size = os.path.getsize(path) / (1024 * 1024)
        new_size = os.path.getsize(target_path) / (1024 * 1024)
        
        return (
            f"Image converted successfully!\n"
            f"Source: {path} ({orig_size:.2f} MB)\n"
            f"Target: {target_path} ({new_size:.2f} MB)"
        )
        
    except subprocess.CalledProcessError as e:
        return f"Error executing ffmpeg: {e.stderr}"
    except Exception as e:
        return f"Error converting image format: {str(e)}"


@mcp.tool
async def get_media_metadata(
    ctx: Context,
    path: str
) -> str:
    """Get structural metadata of an image, audio, or video file using ffprobe.
    
    Args:
        path: Absolute path to the media file
        
    Returns:
        A formatted JSON summary of streams and formats
    """
    try:
        if not os.path.exists(path):
            return f"Error: Media file not found at {path}"
            
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_format",
            "-show_streams",
            "-of", "json",
            path
        ]
        
        await ctx.info(f"Running ffprobe command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        metadata = json.loads(result.stdout)
        
        summary = {
            "file_path": path,
            "file_size_mb": round(os.path.getsize(path) / (1024 * 1024), 3),
            "format_name": metadata.get("format", {}).get("format_long_name", "Unknown"),
            "duration_seconds": metadata.get("format", {}).get("duration"),
            "streams": []
        }
        
        for stream in metadata.get("streams", []):
            stream_summary = {
                "index": stream.get("index"),
                "codec_type": stream.get("codec_type"),
                "codec_name": stream.get("codec_name"),
            }
            
            if stream.get("codec_type") == "video":
                stream_summary["width"] = stream.get("width")
                stream_summary["height"] = stream.get("height")
                stream_summary["r_frame_rate"] = stream.get("r_frame_rate")
            elif stream.get("codec_type") == "audio":
                stream_summary["sample_rate"] = stream.get("sample_rate")
                stream_summary["channels"] = stream.get("channels")
                
            summary["streams"].append(stream_summary)
            
        return json.dumps(summary, indent=4, ensure_ascii=False)
        
    except subprocess.CalledProcessError as e:
        return f"Error executing ffprobe: {e.stderr}"
    except Exception as e:
        return f"Error reading media metadata: {str(e)}"


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
