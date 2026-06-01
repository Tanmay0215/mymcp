"""
Data format converter tools (JSON, YAML, CSV).
"""

import json
import csv
import io
import yaml

def register_tools(mcp):
    """Register data converter tools with the MCP server."""
    
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
                
            # Collect all unique keys from all objects for headers
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
                    # Write row, handling missing keys gracefully
                    writer.writerow({k: item.get(k, "") for k in headers})
                    
            return output.getvalue()
        except Exception as e:
            return f"Error converting JSON to CSV: {str(e)}"
