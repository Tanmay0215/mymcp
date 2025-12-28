"""
File operation tools.
"""

import os


def register_tools(mcp):
    """Register file operation tools with the MCP server."""
    
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
