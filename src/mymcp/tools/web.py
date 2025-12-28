"""
Web utility tools.
"""

import requests


def register_tools(mcp):
    """Register web utility tools with the MCP server."""
    
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
