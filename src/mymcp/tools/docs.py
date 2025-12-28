"""
Documentation and knowledge tools.
"""

import os
import glob
from pathlib import Path
from typing import List


def register_tools(mcp):
    """Register documentation and knowledge tools with the MCP server."""
    
    @mcp.tool
    def search_docs(query: str, directory: str = ".") -> str:
        """Search for documentation files containing the query.
        
        Args:
            query: Search term to look for
            directory: Directory to search in (default: current directory)
        
        Returns:
            List of matching files with snippets
        """
        try:
            doc_extensions = ['.md', '.txt', '.rst', '.adoc']
            matches = []
            
            for ext in doc_extensions:
                pattern = os.path.join(directory, f'**/*{ext}')
                for filepath in glob.glob(pattern, recursive=True):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if query.lower() in content.lower():
                                # Find the line containing the query
                                lines = content.split('\n')
                                matching_lines = [
                                    (i+1, line) for i, line in enumerate(lines)
                                    if query.lower() in line.lower()
                                ]
                                
                                if matching_lines:
                                    snippet = matching_lines[0][1][:100]
                                    matches.append(
                                        f"{filepath}:{matching_lines[0][0]} - {snippet}..."
                                    )
                    except Exception:
                        continue
            
            if matches:
                return "\n".join(matches[:10])  # Limit to 10 results
            else:
                return f"No documentation found containing '{query}'"
        except Exception as e:
            return f"Error searching docs: {str(e)}"

    @mcp.tool
    def summarize_file(path: str) -> str:
        """Summarize a documentation file.
        
        Args:
            path: Path to the file to summarize
        
        Returns:
            Summary of the file including headers and key sections
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            summary_parts = []
            
            # Extract title (first non-empty line or first header)
            for line in lines:
                if line.strip():
                    summary_parts.append(f"Title: {line.strip('# ')}")
                    break
            
            # Extract headers
            headers = [
                line.strip('# ').strip() 
                for line in lines 
                if line.startswith('#')
            ]
            
            if headers:
                summary_parts.append(f"\nSections ({len(headers)}):")
                summary_parts.extend([f"  - {h}" for h in headers[:10]])
            
            # File stats
            word_count = len(content.split())
            line_count = len(lines)
            summary_parts.append(f"\nStats: {line_count} lines, ~{word_count} words")
            
            return "\n".join(summary_parts)
        except Exception as e:
            return f"Error summarizing file: {str(e)}"

    @mcp.tool
    def generate_readme(directory: str = ".") -> str:
        """Generate a README.md template for a directory.
        
        Args:
            directory: Directory to generate README for (default: current directory)
        
        Returns:
            Generated README content
        """
        try:
            dir_path = Path(directory)
            dir_name = dir_path.name if dir_path.name else "Project"
            
            # Scan directory for files
            files = []
            dirs = []
            
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path) and not item.startswith('.'):
                    files.append(item)
                elif os.path.isdir(item_path) and not item.startswith('.'):
                    dirs.append(item)
            
            # Detect project type
            project_type = "Project"
            if "package.json" in files:
                project_type = "Node.js Project"
            elif "requirements.txt" in files or "setup.py" in files:
                project_type = "Python Project"
            elif "Cargo.toml" in files:
                project_type = "Rust Project"
            elif "go.mod" in files:
                project_type = "Go Project"
            
            readme = f"""# {dir_name}

{project_type} - Add a brief description here.

## Overview

Describe what this project does and its main purpose.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
# Add installation instructions here
```

## Usage

```bash
# Add usage examples here
```

## Project Structure

```
{dir_name}/
"""
            
            # Add directory structure
            for d in sorted(dirs)[:5]:
                readme += f"├── {d}/\n"
            for f in sorted(files)[:10]:
                readme += f"├── {f}\n"
            
            readme += """```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Specify your license here.
"""
            
            return readme
        except Exception as e:
            return f"Error generating README: {str(e)}"
