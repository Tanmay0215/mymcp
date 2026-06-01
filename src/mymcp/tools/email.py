"""
Email tools using Gmail SMTP.
"""

import os
import smtplib
import imaplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from fastmcp import Context
from ..config import get_gmail_config, get_gmail_imap_config



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

