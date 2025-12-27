# Simple MCP Server

A simple Model Context Protocol (MCP) server built with FastMCP.

## What is MCP?

The Model Context Protocol (MCP) is a standardized way to connect LLMs to external data sources and tools. Think of it as an API specifically designed for LLM interactions.

## Features

This server demonstrates the core MCP capabilities:

### 🛠️ Tools
Functions that LLMs can call to perform actions:
- `add(a, b)` - Add two numbers
- `multiply(a, b)` - Multiply two numbers
- `get_current_time()` - Get current timestamp
- `greet(name, enthusiastic)` - Generate greeting messages

### 📚 Resources
Data sources that LLMs can read:
- `info://server` - Server information
- `config://settings` - Configuration settings
- `data://user/{user_id}` - User data (dynamic template)

### 💬 Prompts
Reusable templates for LLM interactions:
- `summarize_text(text)` - Generate summarization prompts
- `code_review(code, language)` - Generate code review prompts

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

## Running the Server

**Always use the virtual environment** to run the server:

```bash
# Option 1: Use the launcher script (recommended)
./run_server.sh

# Option 2: Use virtual environment Python directly
./venv/bin/python server.py

# Option 3: Activate venv first, then run
source venv/bin/activate
python server.py
```

> [!IMPORTANT]
> Do NOT run with system Python (e.g., `python3 server.py` or `/opt/homebrew/bin/python3.13 server.py`). FastMCP is only installed in the virtual environment.

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

See [CURSOR_SETUP.md](file:///Users/tanmay/Developer/mymcp/CURSOR_SETUP.md) for detailed instructions.

## Project Structure

```
mymcp/
├── server.py           # Main MCP server implementation
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Learn More

- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)

## Next Steps

To extend this server, you can:
1. Add more tools for specific functionality
2. Connect to databases or APIs in resources
3. Create more sophisticated prompts
4. Add authentication (Google, GitHub, Azure, etc.)
5. Deploy to production using FastMCP Cloud
