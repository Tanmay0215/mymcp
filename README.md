# Simple MCP Server

A simple Model Context Protocol (MCP) server built with FastMCP.

## What is MCP?

The Model Context Protocol (MCP) is a standardized way to connect LLMs to external data sources and tools. Think of it as an API specifically designed for LLM interactions.

## Features

This server provides **essential MCP tools** that extend LLM capabilities with real-world actions:

### 🔧 Basic Utilities
- `get_current_time()` - Get current timestamp
- `greet(name, enthusiastic)` - Generate greeting messages

### 📁 File Operations
- `read_file(path)` - Read file contents
- `write_file(path, content)` - Write content to file
- `list_directory(path)` - List directory contents
- `file_exists(path)` - Check if file/directory exists
- `get_file_size(path)` - Get file size in bytes

### 📖 Documentation & Knowledge
- `search_docs(query, directory)` - Search documentation files for query
- `summarize_file(path)` - Summarize a documentation file
- `generate_readme(directory)` - Generate README template

### ✅ Validation
- `validate_email_format(email)` - Validate email format

### 💻 System Information
- `get_system_info()` - Get OS, CPU, memory info
- `get_disk_usage(path)` - Get disk usage statistics
- `get_cpu_percent()` - Get current CPU usage
- `get_memory_info()` - Get detailed memory info

### 🌐 Web Utilities
- `fetch_url(url)` - Fetch content from URL
- `check_url_status(url)` - Check if URL is accessible
- `extract_domain(url)` - Extract domain from URL

### 📧 Email (Gmail SMTP)
- `send_email(to, subject, body, html)` - Send email via Gmail
- `send_email_with_attachment(to, subject, body, file_path)` - Send email with attachment
- `parse_email_address(email_string)` - Parse email name and address

### 📚 Resources
Data sources that LLMs can read:
- `info://server` - Server information and capabilities
- `config://settings` - Configuration settings
- `data://user/{user_id}` - User data (dynamic template)

### 💬 Prompts
Reusable templates for LLM interactions:
- `summarize_text(text)` - Generate summarization prompts
- `code_review(code, language)` - Generate code review prompts

> [!NOTE]
> This server focuses on tools that provide **real capabilities** LLMs cannot do themselves:
> - File system access
> - Documentation search and indexing
> - System information
> - Network requests
> - Email sending
> 
> Redundant tools (string manipulation, JSON parsing, base64 encoding) have been removed since LLMs can handle these natively.


## Requirements

- **Python 3.10 or higher** (FastMCP requires Python 3.10+)

You can check your Python version with:
```bash
python3 --version
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

Or using uv (recommended):
```bash
uv pip install -r requirements.txt
```

## Email Setup (Optional)

To enable email functionality via Gmail SMTP:

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Generate a Gmail App Password:**
   - Enable 2-Factor Authentication on your Google Account
   - Go to https://myaccount.google.com/apppasswords
   - Generate an app password for "Mail"
   - Copy the 16-character password

3. **Configure your `.env` file:**
   ```bash
   GMAIL_USER=your-email@gmail.com
   GMAIL_APP_PASSWORD=your-16-char-app-password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   ```

4. **See detailed instructions:** [EMAIL_SETUP.md](file:///Users/tanmay/Developer/mymcp/EMAIL_SETUP.md)

> [!IMPORTANT]
> The `.env` file is gitignored and will never be committed. Keep your credentials secure!

## Running the Server

Run the server using the entry point:

```bash
# Option 1: Direct Python execution
./venv/bin/python run_server.py

# Option 2: Make it executable and run directly
chmod +x run_server.py
./run_server.py
```

> [!IMPORTANT]
> Always use the virtual environment Python to ensure dependencies are available.

## Testing the Server

You can test the server using an MCP client like Claude Desktop or by using FastMCP's built-in testing tools.

### Using FastMCP Dev Mode

FastMCP provides a development mode for testing:
```bash
fastmcp dev server.py
```

## Using with Cursor IDE

To use this MCP server with Cursor IDE:

1. **Add to Cursor Settings:**
   - Open Cursor Settings (Cmd+,)
   - Search for "MCP" or go to Features → Model Context Protocol
   - Click "Edit Config" and add:

```json
{
  "mcpServers": {
    "simple-server": {
      "command": "/Users/tanmay/Developer/mymcp/venv/bin/python",
      "args": ["/Users/tanmay/Developer/mymcp/server.py"]
    }
  }
}
```

2. **Restart Cursor** completely (Cmd+Q, then reopen)

3. **Verify** - The server tools and resources will be available to Cursor's AI

## Project Structure

```
mymcp/
├── src/
│   └── mymcp/              # Main package
│       ├── __init__.py     # Package exports
│       ├── server.py       # Server initialization
│       ├── config.py       # Environment & settings
│       ├── tools/          # Tool modules
│       │   ├── __init__.py
│       │   ├── basic.py    # Basic utilities
│       │   ├── files.py    # File operations
│       │   ├── docs.py     # Documentation tools
│       │   ├── validation.py # Email validation
│       │   ├── system.py   # System info
│       │   ├── web.py      # Web utilities
│       │   └── email.py    # Email tools
│       ├── resources/      # Resource modules
│       │   ├── __init__.py
│       │   └── info.py     # Server info
│       └── prompts/        # Prompt modules
│           ├── __init__.py
│           └── templates.py
├── run_server.py           # Entry point
├── mcp.json                # MCP client configuration
├── requirements.txt        # Dependencies
├── .env.example           # Env template
├── .env                   # Your credentials (gitignored)
├── EMAIL_SETUP.md         # Gmail setup guide
├── MCP_SETUP.md           # MCP configuration guide
└── README.md              # This file
```

## Learn More

- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)

## Next Steps

To extend this server further, you can:
1. Add more specialized tools for your use case
2. Connect to databases or external APIs
3. Create custom prompts for specific workflows
4. Add authentication for other services (GitHub, Azure, etc.)
5. Deploy to production using FastMCP Cloud
6. Integrate with other email providers (SendGrid, Mailgun, etc.)

## Tool Categories Summary

| Category | Tools | Description |
|----------|-------|-------------|
| 🔧 Basic Utilities | 2 | Time and greetings |
| 📁 File Operations | 5 | Read, write, list files |
| 📖 Documentation | 3 | Search, summarize, generate docs |
| ✅ Validation | 1 | Email format validation |
| 💻 System Info | 4 | CPU, memory, disk usage |
| 🌐 Web Utilities | 3 | HTTP requests, URL parsing |
| 📧 Email | 3 | Gmail SMTP integration |
| **Total** | **21** | **Focused on real capabilities** |

**Philosophy**: This server provides only tools that give LLMs **real-world capabilities** they cannot achieve through text generation alone. Redundant tools for string manipulation, JSON parsing, and encoding have been removed.
