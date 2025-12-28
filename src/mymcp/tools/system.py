"""
System information tools.
"""

import psutil


def register_tools(mcp):
    """Register system information tools with the MCP server."""
    
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
