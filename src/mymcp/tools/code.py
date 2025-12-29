"""
Code analysis and documentation tools.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List


def register_tools(mcp):
    """Register code analysis and documentation tools with the MCP server."""
    
    @mcp.tool
    def update_documentation(directory: str = ".", doc_file: str = "README.md") -> str:
        """Update existing documentation with current codebase information.
        
        Scans the codebase and updates documentation sections like API endpoints,
        installation instructions, and project structure.
        
        Args:
            directory: Directory to analyze (default: current directory)
            doc_file: Documentation file to update (default: README.md)
        
        Returns:
            Updated documentation content
        """
        try:
            doc_path = os.path.join(directory, doc_file)
            
            # Read existing documentation
            if os.path.exists(doc_path):
                with open(doc_path, 'r', encoding='utf-8') as f:
                    existing_doc = f.read()
            else:
                existing_doc = f"# {os.path.basename(directory)}\n\n"
            
            # Analyze codebase
            endpoints = []
            dependencies = []
            
            for root, dirs, files in os.walk(directory):
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__']]
                
                for file in files:
                    filepath = os.path.join(root, file)
                    
                    # Extract endpoints
                    if file.endswith('.py'):
                        endpoints.extend(_extract_python_routes(filepath))
                    elif file.endswith(('.js', '.ts')):
                        endpoints.extend(_extract_js_routes(filepath))
                    
                    # Extract dependencies
                    if file == 'requirements.txt':
                        with open(filepath, 'r') as f:
                            dependencies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    elif file == 'package.json':
                        with open(filepath, 'r') as f:
                            pkg = json.load(f)
                            dependencies = list(pkg.get('dependencies', {}).keys())
            
            # Update API endpoints section
            if endpoints:
                api_section = "\n## API Endpoints\n\n"
                for endpoint in endpoints[:20]:
                    api_section += f"- **{endpoint['method']}** `{endpoint['path']}`\n"
                
                # Replace or append API section
                if "## API Endpoints" in existing_doc:
                    existing_doc = re.sub(
                        r'## API Endpoints.*?(?=\n##|\Z)',
                        api_section,
                        existing_doc,
                        flags=re.DOTALL
                    )
                else:
                    existing_doc += f"\n{api_section}"
            
            # Update dependencies section
            if dependencies:
                dep_section = "\n## Dependencies\n\n"
                for dep in dependencies[:15]:
                    dep_section += f"- `{dep}`\n"
                
                if "## Dependencies" in existing_doc:
                    existing_doc = re.sub(
                        r'## Dependencies.*?(?=\n##|\Z)',
                        dep_section,
                        existing_doc,
                        flags=re.DOTALL
                    )
            
            # Write updated documentation
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(existing_doc)
            
            return f"Documentation updated: {doc_path}\n\nUpdated sections: API Endpoints, Dependencies"
        except Exception as e:
            return f"Error updating documentation: {str(e)}"
    
    @mcp.tool
    def generate_api_collection(directory: str = ".", format: str = "auto") -> str:
        """Generate Postman or Swagger/OpenAPI collection from codebase.
        
        Analyzes API endpoints and generates a collection file. Automatically detects
        which format to use based on existing files, or generates both if format='auto'.
        
        Args:
            directory: Directory to analyze (default: current directory)
            format: Output format - 'postman', 'swagger', or 'auto' (default: auto)
        
        Returns:
            Generated collection content and file path
        """
        try:
            # Analyze endpoints
            endpoints = []
            
            for root, dirs, files in os.walk(directory):
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__']]
                
                for file in files:
                    filepath = os.path.join(root, file)
                    
                    if file.endswith('.py'):
                        endpoints.extend(_extract_python_routes(filepath))
                    elif file.endswith(('.js', '.ts')):
                        endpoints.extend(_extract_js_routes(filepath))
            
            if not endpoints:
                return "No API endpoints found to generate collection"
            
            # Determine format
            output_format = format.lower()
            
            # Check for existing files if auto
            if output_format == "auto":
                if any(f.endswith(('.yaml', '.yml')) and 'swagger' in f.lower() 
                       for f in os.listdir(directory)):
                    output_format = "swagger"
                elif any(f.endswith('.json') and 'postman' in f.lower() 
                         for f in os.listdir(directory)):
                    output_format = "postman"
                else:
                    # Default to Swagger (OpenAPI)
                    output_format = "swagger"
            
            # Generate collection
            if output_format == "postman":
                collection = _generate_postman_collection(endpoints, directory)
                output_file = os.path.join(directory, "postman_collection.json")
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(collection, f, indent=2)
                return f"Postman collection generated: {output_file}\n\n{json.dumps(collection, indent=2)[:500]}..."
            
            else:  # swagger/openapi
                collection = _generate_swagger_spec(endpoints, directory)
                output_file = os.path.join(directory, "swagger.yaml")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(collection)
                return f"Swagger/OpenAPI spec generated: {output_file}\n\n{collection[:500]}..."
        
        except Exception as e:
            return f"Error generating API collection: {str(e)}"
    
    @mcp.tool
    def generate_integration_doc(directory: str = ".", output_file: str = "INTEGRATION.md") -> str:
        """Generate integration documentation for a codebase.
        
        Analyzes code to document APIs, endpoints, data models, and integration points
        for frontend-backend or service-to-service integration.
        
        Args:
            directory: Directory to analyze (default: current directory)
            output_file: Output file name (default: INTEGRATION.md)
        
        Returns:
            Generated integration documentation
        """
        try:
            doc_sections = {
                "endpoints": [],
                "models": [],
                "functions": [],
                "config": []
            }
            
            # Scan for different file types
            for root, dirs, files in os.walk(directory):
                # Skip common ignore directories
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__', 'dist', 'build']]
                
                for file in files:
                    filepath = os.path.join(root, file)
                    
                    # Analyze Python files
                    if file.endswith('.py'):
                        doc_sections = _analyze_python_file(filepath, doc_sections)
                    
                    # Analyze JavaScript/TypeScript files
                    elif file.endswith(('.js', '.ts', '.jsx', '.tsx')):
                        doc_sections = _analyze_js_file(filepath, doc_sections)
                    
                    # Analyze API spec files
                    elif file.endswith(('.yaml', '.yml')) and 'api' in file.lower():
                        doc_sections["config"].append(f"API Spec: {filepath}")
            
            # Generate documentation
            doc = _build_integration_doc(doc_sections, directory)
            
            # Write to file
            output_path = os.path.join(directory, output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(doc)
            
            return f"Integration documentation generated: {output_path}\n\n{doc[:500]}..."
        except Exception as e:
            return f"Error generating integration doc: {str(e)}"
    
    @mcp.tool
    def analyze_api_endpoints(directory: str = ".") -> str:
        """Analyze and list all API endpoints in the codebase.
        
        Args:
            directory: Directory to analyze (default: current directory)
        
        Returns:
            List of API endpoints with methods and paths
        """
        try:
            endpoints = []
            
            for root, dirs, files in os.walk(directory):
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__']]
                
                for file in files:
                    if file.endswith('.py'):
                        filepath = os.path.join(root, file)
                        endpoints.extend(_extract_python_routes(filepath))
                    elif file.endswith(('.js', '.ts')):
                        filepath = os.path.join(root, file)
                        endpoints.extend(_extract_js_routes(filepath))
            
            if not endpoints:
                return "No API endpoints found"
            
            # Format output
            output = "# API Endpoints\n\n"
            for endpoint in endpoints:
                output += f"- **{endpoint['method']}** `{endpoint['path']}` - {endpoint['file']}\n"
            
            return output
        except Exception as e:
            return f"Error analyzing endpoints: {str(e)}"
    
    @mcp.tool
    def extract_data_models(directory: str = ".") -> str:
        """Extract data models and schemas from the codebase.
        
        Args:
            directory: Directory to analyze (default: current directory)
        
        Returns:
            List of data models with their fields
        """
        try:
            models = []
            
            for root, dirs, files in os.walk(directory):
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__']]
                
                for file in files:
                    filepath = os.path.join(root, file)
                    
                    if file.endswith('.py'):
                        models.extend(_extract_python_models(filepath))
                    elif file.endswith(('.ts', '.tsx')):
                        models.extend(_extract_typescript_interfaces(filepath))
            
            if not models:
                return "No data models found"
            
            # Format output
            output = "# Data Models\n\n"
            for model in models:
                output += f"## {model['name']}\n"
                output += f"File: `{model['file']}`\n\n"
                if model.get('fields'):
                    output += "Fields:\n"
                    for field in model['fields']:
                        output += f"- `{field}`\n"
                output += "\n"
            
            return output
        except Exception as e:
            return f"Error extracting models: {str(e)}"
    
    @mcp.tool
    def generate_api_client_stub(directory: str = ".", language: str = "typescript") -> str:
        """Generate API client stub code based on detected endpoints.
        
        Args:
            directory: Directory to analyze (default: current directory)
            language: Target language (typescript, python, javascript)
        
        Returns:
            Generated API client stub code
        """
        try:
            endpoints = []
            
            for root, dirs, files in os.walk(directory):
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__']]
                
                for file in files:
                    if file.endswith('.py'):
                        filepath = os.path.join(root, file)
                        endpoints.extend(_extract_python_routes(filepath))
            
            if not endpoints:
                return "No endpoints found to generate client"
            
            # Generate client code
            if language.lower() == "typescript":
                return _generate_typescript_client(endpoints)
            elif language.lower() == "python":
                return _generate_python_client(endpoints)
            else:
                return _generate_javascript_client(endpoints)
        except Exception as e:
            return f"Error generating client: {str(e)}"


# Helper functions

def _analyze_python_file(filepath: str, doc_sections: Dict) -> Dict:
    """Analyze Python file for API routes and models."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find Flask/FastAPI routes
        route_patterns = [
            r'@app\.route\(["\']([^"\']+)["\'].*?methods=\[([^\]]+)\]',
            r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']',
            r'@mcp\.tool'
        ]
        
        for pattern in route_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                doc_sections["endpoints"].append({
                    "file": filepath,
                    "match": match.group(0)
                })
        
        # Find class definitions (potential models)
        class_pattern = r'class\s+(\w+).*?:'
        for match in re.finditer(class_pattern, content):
            doc_sections["models"].append({
                "name": match.group(1),
                "file": filepath
            })
    except Exception:
        pass
    
    return doc_sections


def _analyze_js_file(filepath: str, doc_sections: Dict) -> Dict:
    """Analyze JavaScript/TypeScript file for API routes."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find Express routes
        route_patterns = [
            r'router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']',
            r'app\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']',
        ]
        
        for pattern in route_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                doc_sections["endpoints"].append({
                    "method": match.group(1).upper(),
                    "path": match.group(2),
                    "file": filepath
                })
    except Exception:
        pass
    
    return doc_sections


def _extract_python_routes(filepath: str) -> List[Dict]:
    """Extract API routes from Python file."""
    routes = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Flask routes
        flask_pattern = r'@app\.route\(["\']([^"\']+)["\'].*?methods=\[([^\]]+)\]'
        for match in re.finditer(flask_pattern, content):
            methods = match.group(2).replace('"', '').replace("'", '').split(',')
            for method in methods:
                routes.append({
                    "method": method.strip(),
                    "path": match.group(1),
                    "file": filepath
                })
        
        # FastAPI routes
        fastapi_pattern = r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']'
        for match in re.finditer(fastapi_pattern, content):
            routes.append({
                "method": match.group(1).upper(),
                "path": match.group(2),
                "file": filepath
            })
    except Exception:
        pass
    
    return routes


def _extract_js_routes(filepath: str) -> List[Dict]:
    """Extract API routes from JavaScript/TypeScript file."""
    routes = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        route_pattern = r'(?:router|app)\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']'
        for match in re.finditer(route_pattern, content):
            routes.append({
                "method": match.group(1).upper(),
                "path": match.group(2),
                "file": filepath
            })
    except Exception:
        pass
    
    return routes


def _extract_python_models(filepath: str) -> List[Dict]:
    """Extract data models from Python file."""
    models = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find class definitions
        class_pattern = r'class\s+(\w+).*?:\s*(.*?)(?=\nclass|\Z)'
        for match in re.finditer(class_pattern, content, re.DOTALL):
            class_name = match.group(1)
            class_body = match.group(2)
            
            # Extract fields
            field_pattern = r'(\w+)\s*[:=]'
            fields = re.findall(field_pattern, class_body)
            
            models.append({
                "name": class_name,
                "file": filepath,
                "fields": fields[:10]  # Limit to first 10 fields
            })
    except Exception:
        pass
    
    return models


def _extract_typescript_interfaces(filepath: str) -> List[Dict]:
    """Extract TypeScript interfaces."""
    models = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find interface definitions
        interface_pattern = r'interface\s+(\w+)\s*\{([^}]+)\}'
        for match in re.finditer(interface_pattern, content):
            interface_name = match.group(1)
            interface_body = match.group(2)
            
            # Extract fields
            field_pattern = r'(\w+)\s*[?:]'
            fields = re.findall(field_pattern, interface_body)
            
            models.append({
                "name": interface_name,
                "file": filepath,
                "fields": fields
            })
    except Exception:
        pass
    
    return models


def _build_integration_doc(sections: Dict, directory: str) -> str:
    """Build integration documentation from analyzed sections."""
    doc = f"""# Integration Documentation

Generated for: `{directory}`

## Overview

This document provides integration information for connecting to this codebase.

## API Endpoints

"""
    
    if sections["endpoints"]:
        for endpoint in sections["endpoints"][:20]:  # Limit to 20
            doc += f"- {endpoint.get('method', 'N/A')} `{endpoint.get('path', 'N/A')}` ({endpoint.get('file', 'N/A')})\n"
    else:
        doc += "No API endpoints detected.\n"
    
    doc += "\n## Data Models\n\n"
    
    if sections["models"]:
        for model in sections["models"][:10]:  # Limit to 10
            doc += f"- **{model.get('name', 'N/A')}** ({model.get('file', 'N/A')})\n"
    else:
        doc += "No data models detected.\n"
    
    doc += """

## Integration Guide

### Authentication

[TODO: Add authentication details]

### Base URL

[TODO: Add base URL]

### Request/Response Format

[TODO: Add format details]

### Error Handling

[TODO: Add error handling details]

## Examples

[TODO: Add integration examples]
"""
    
    return doc


def _generate_typescript_client(endpoints: List[Dict]) -> str:
    """Generate TypeScript API client."""
    client = """// Auto-generated API Client
import axios, { AxiosInstance } from 'axios';

export class APIClient {
  private client: AxiosInstance;

  constructor(baseURL: string) {
    this.client = axios.create({ baseURL });
  }

"""
    
    for endpoint in endpoints[:10]:  # Limit to 10
        method = endpoint['method'].lower()
        path = endpoint['path']
        func_name = path.replace('/', '_').replace('-', '_').strip('_')
        
        client += f"""  async {func_name}(data?: any) {{
    return this.client.{method}('{path}', data);
  }}

"""
    
    client += "}\n"
    return client


def _generate_python_client(endpoints: List[Dict]) -> str:
    """Generate Python API client."""
    client = """# Auto-generated API Client
import requests

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

"""
    
    for endpoint in endpoints[:10]:  # Limit to 10
        method = endpoint['method'].lower()
        path = endpoint['path']
        func_name = path.replace('/', '_').replace('-', '_').strip('_')
        
        client += f"""    def {func_name}(self, data=None):
        return requests.{method}(f"{{self.base_url}}{path}", json=data)

"""
    
    return client


def _generate_javascript_client(endpoints: List[Dict]) -> str:
    """Generate JavaScript API client."""
    client = """// Auto-generated API Client
class APIClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

"""
    
    for endpoint in endpoints[:10]:  # Limit to 10
        method = endpoint['method'].lower()
        path = endpoint['path']
        func_name = path.replace('/', '_').replace('-', '_').replace('_', '')
        
        client += f"""  async {func_name}(data) {{
    const response = await fetch(`${{this.baseURL}}{path}`, {{
      method: '{method.upper()}',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify(data)
    }});
    return response.json();
  }}

"""
    
    client += "}\n"
    return client


def _generate_postman_collection(endpoints: List[Dict], directory: str) -> Dict:
    """Generate Postman collection from endpoints."""
    collection = {
        "info": {
            "name": f"{os.path.basename(directory)} API",
            "description": "Auto-generated Postman collection",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }
    
    for endpoint in endpoints:
        item = {
            "name": f"{endpoint['method']} {endpoint['path']}",
            "request": {
                "method": endpoint['method'],
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "url": {
                    "raw": "{{baseUrl}}" + endpoint['path'],
                    "host": ["{{baseUrl}}"],
                    "path": endpoint['path'].strip('/').split('/')
                }
            }
        }
        
        # Add body for POST/PUT/PATCH
        if endpoint['method'] in ['POST', 'PUT', 'PATCH']:
            item["request"]["body"] = {
                "mode": "raw",
                "raw": "{\n  \n}"
            }
        
        collection["item"].append(item)
    
    return collection


def _generate_swagger_spec(endpoints: List[Dict], directory: str) -> str:
    """Generate Swagger/OpenAPI YAML spec from endpoints."""
    spec = f"""openapi: 3.0.0
info:
  title: {os.path.basename(directory)} API
  description: Auto-generated API specification
  version: 1.0.0
servers:
  - url: http://localhost:8000
    description: Development server
paths:
"""
    
    # Group endpoints by path
    paths = {}
    for endpoint in endpoints:
        path = endpoint['path']
        method = endpoint['method'].lower()
        
        if path not in paths:
            paths[path] = {}
        
        paths[path][method] = {
            "summary": f"{endpoint['method']} {path}",
            "responses": {
                "200": {
                    "description": "Successful response",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object"
                            }
                        }
                    }
                }
            }
        }
        
        # Add request body for POST/PUT/PATCH
        if method in ['post', 'put', 'patch']:
            paths[path][method]["requestBody"] = {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object"
                        }
                    }
                }
            }
    
    # Convert to YAML
    for path, methods in paths.items():
        spec += f"  {path}:\n"
        for method, details in methods.items():
            spec += f"    {method}:\n"
            spec += f"      summary: {details['summary']}\n"
            
            if 'requestBody' in details:
                spec += "      requestBody:\n"
                spec += "        required: true\n"
                spec += "        content:\n"
                spec += "          application/json:\n"
                spec += "            schema:\n"
                spec += "              type: object\n"
            
            spec += "      responses:\n"
            spec += "        '200':\n"
            spec += "          description: Successful response\n"
            spec += "          content:\n"
            spec += "            application/json:\n"
            spec += "              schema:\n"
            spec += "                type: object\n"
    
    return spec
