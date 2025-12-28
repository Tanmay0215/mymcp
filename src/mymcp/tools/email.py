"""
Email tools using Gmail SMTP.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from fastmcp import Context
from ..config import get_gmail_config


def register_tools(mcp):
    """Register email tools with the MCP server."""
    
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
