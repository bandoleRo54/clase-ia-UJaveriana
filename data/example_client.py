"""
Example usage of the Technical Documentation Generator APIs.
Demonstrates how to use each core functionality.
"""

import json
import requests
from typing import Dict, Any


# API Base URL
BASE_URL = "http://localhost:5000"


class DocumentationAPIClient:
    """Client for interacting with the Documentation Generator API."""
    
    def __init__(self, base_url: str = BASE_URL):
        """Initialize the API client."""
        self.base_url = base_url
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the API is running."""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def analyze_code(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze source code.
        
        Args:
            file_path: Path to Python or JavaScript file
            
        Returns:
            Analysis results
        """
        payload = {"file_path": file_path}
        response = requests.post(
            f"{self.base_url}/api/v1/analyze",
            json=payload
        )
        return response.json()
    
    def generate_readme(self, file_path: str, project_name: str, use_llm: bool = True) -> Dict[str, Any]:
        """
        Generate README documentation.
        
        Args:
            file_path: Path to source file
            project_name: Name of the project
            use_llm: Whether to use LLM enhancement
            
        Returns:
            Generated README content
        """
        payload = {
            "file_path": file_path,
            "project_name": project_name,
            "use_llm": use_llm
        }
        response = requests.post(
            f"{self.base_url}/api/v1/generate/readme",
            json=payload
        )
        return response.json()
    
    def generate_api_docs(self, file_path: str, use_llm: bool = True) -> Dict[str, Any]:
        """
        Generate API documentation.
        
        Args:
            file_path: Path to source file with API endpoints
            use_llm: Whether to use LLM enhancement
            
        Returns:
            Generated API documentation
        """
        payload = {
            "file_path": file_path,
            "use_llm": use_llm
        }
        response = requests.post(
            f"{self.base_url}/api/v1/generate/api-docs",
            json=payload
        )
        return response.json()
    
    def generate_class_docs(self, file_path: str, class_name: str = None, use_llm: bool = True) -> Dict[str, Any]:
        """
        Generate class documentation.
        
        Args:
            file_path: Path to source file
            class_name: Specific class to document (optional)
            use_llm: Whether to use LLM enhancement
            
        Returns:
            Generated class documentation
        """
        payload = {
            "file_path": file_path,
            "use_llm": use_llm
        }
        if class_name:
            payload["class_name"] = class_name
        
        response = requests.post(
            f"{self.base_url}/api/v1/generate/class-docs",
            json=payload
        )
        return response.json()
    
    def generate_function_docs(self, file_path: str, function_name: str = None, use_llm: bool = True) -> Dict[str, Any]:
        """
        Generate function documentation.
        
        Args:
            file_path: Path to source file
            function_name: Specific function to document (optional)
            use_llm: Whether to use LLM enhancement
            
        Returns:
            Generated function documentation
        """
        payload = {
            "file_path": file_path,
            "use_llm": use_llm
        }
        if function_name:
            payload["function_name"] = function_name
        
        response = requests.post(
            f"{self.base_url}/api/v1/generate/function-docs",
            json=payload
        )
        return response.json()
    
    def generate_complete_documentation(self, file_path: str, project_name: str, use_llm: bool = True) -> Dict[str, Any]:
        """
        Generate all documentation at once.
        
        Args:
            file_path: Path to source file
            project_name: Name of the project
            use_llm: Whether to use LLM enhancement
            
        Returns:
            Complete documentation
        """
        payload = {
            "file_path": file_path,
            "project_name": project_name,
            "use_llm": use_llm
        }
        response = requests.post(
            f"{self.base_url}/api/v1/generate/complete",
            json=payload
        )
        return response.json()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    
    # Initialize client
    client = DocumentationAPIClient()
    
    print("=" * 70)
    print("Technical Documentation Generator - Example Usage")
    print("=" * 70)
    
    # Example 1: Health check
    print("\n[1] Health Check")
    print("-" * 70)
    try:
        health = client.health_check()
        print(json.dumps(health, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Analyze code
    print("\n[2] Analyze Code")
    print("-" * 70)
    example_file = "./example.py"  # Change this to your file
    print(f"Analyzing: {example_file}")
    try:
        analysis = client.analyze_code(example_file)
        print(json.dumps(analysis, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Generate README
    print("\n[3] Generate README")
    print("-" * 70)
    print(f"Generating README for: {example_file}")
    try:
        readme = client.generate_readme(
            file_path=example_file,
            project_name="Mi Proyecto Ejemplo",
            use_llm=False  # Set to False if GITHUB_TOKEN not available
        )
        if 'content' in readme:
            print(readme['content'][:500] + "...\n(truncated for display)")
        else:
            print(json.dumps(readme, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Generate API Documentation
    print("\n[4] Generate API Documentation")
    print("-" * 70)
    print(f"Generating API docs for: {example_file}")
    try:
        api_docs = client.generate_api_docs(
            file_path=example_file,
            use_llm=False
        )
        if 'content' in api_docs:
            print(api_docs['content'][:500] + "...\n(truncated for display)")
        else:
            print(json.dumps(api_docs, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 5: Generate Class Documentation
    print("\n[5] Generate Class Documentation")
    print("-" * 70)
    print(f"Generating class docs for: {example_file}")
    try:
        class_docs = client.generate_class_docs(
            file_path=example_file,
            use_llm=False
        )
        if 'content' in class_docs:
            print(class_docs['content'][:500] + "...\n(truncated for display)")
        else:
            print(json.dumps(class_docs, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 6: Generate Complete Documentation
    print("\n[6] Generate Complete Documentation")
    print("-" * 70)
    print(f"Generating complete documentation for: {example_file}")
    try:
        complete = client.generate_complete_documentation(
            file_path=example_file,
            project_name="Sistema Completo",
            use_llm=False
        )
        print(json.dumps({
            'status': complete.get('status'),
            'file': complete.get('file'),
            'summary': complete.get('summary'),
            'has_readme': 'readme' in complete.get('documentation', {}),
            'has_api_docs': 'api_docs' in complete.get('documentation', {}),
            'has_classes': len(complete.get('documentation', {}).get('classes', [])) > 0
        }, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)
