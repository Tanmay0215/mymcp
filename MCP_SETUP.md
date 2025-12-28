# MCP Configuration Guide

This guide helps you configure the MCP server for use with Cursor IDE or Claude Desktop.

## Quick Setup

1. **Find your project path:**
   ```bash
   cd /path/to/mymcp
   pwd
   ```
   Copy the output path.

2. **Update `mcp.json`:**
   
   Replace all instances of `/path/to/your/mymcp` with your actual project path.

3. **Add to your MCP client** (see below for specific instructions)

## Platform-Specific Paths

### macOS/Linux
```json
{
  "command": "/Users/yourname/projects/mymcp/venv/bin/python",
  "args": ["/Users/yourname/projects/mymcp/run_server.py"]
}
```

### Windows
```json
{
  "command": "C:/Users/yourname/projects/mymcp/venv/Scripts/python.exe",
  "args": ["C:/Users/yourname/projects/mymcp/run_server.py"]
}
```

**Note:** Use forward slashes (`/`) or escaped backslashes (`\\\\`) in JSON.

## Cursor IDE Setup

1. Open Cursor Settings
   - Mac: `Cmd + ,`
   - Windows/Linux: `Ctrl + ,`

2. Search for "MCP" or navigate to:
   - Features → Model Context Protocol

3. Click "Edit Config"

4. Paste your updated `mcp.json` content

5. Save and restart Cursor completely
   - Mac: `Cmd + Q` then reopen
   - Windows/Linux: Close all windows and reopen

## Claude Desktop Setup

1. Open Claude Desktop

2. Go to Settings → Developer → Model Context Protocol

3. Add your server configuration from `mcp.json`

4. Restart Claude Desktop

## Troubleshooting

### Server not connecting?

1. **Verify Python path:**
   ```bash
   /path/to/your/mymcp/venv/bin/python --version
   ```
   Should show Python 3.10+

2. **Test server manually:**
   ```bash
   /path/to/your/mymcp/venv/bin/python /path/to/your/mymcp/run_server.py
   ```

3. **Check logs:**
   - Cursor: Check the MCP logs in settings
   - Claude: Check application logs

### Common Issues

- **Path errors:** Make sure all paths are absolute (start with `/` on Unix or `C:/` on Windows)
- **Python not found:** Verify virtual environment is activated and dependencies installed
- **Permission denied:** Ensure `run_server.py` is executable or use Python to run it

## Environment Variables

If you need email functionality, make sure your `.env` file is configured:

```bash
cp .env.example .env
# Edit .env with your Gmail credentials
```

See [EMAIL_SETUP.md](EMAIL_SETUP.md) for details.
