"""
Module for generating documentation using templates and LLM enhancement.
"""

import os
from openai import OpenAI
from typing import Dict, List, Any
import json


class LLMClient:
    """Client for communicating with GitHub Models AI."""
    
    def __init__(self):
        """Initialize the LLM client."""
        token = os.environ.get("GITHUB_TOKEN", "")
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable not set")
        
        self.endpoint = "https://models.github.ai/inference"
        self.model_name = "openai/gpt-4o-mini"
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=token,
        )
    
    def enhance_description(self, code_context: str, element_type: str) -> str:
        """
        Use LLM to enhance description of a code element.
        
        Args:
            code_context: The code snippet or context
            element_type: Type of element (function, class, api, etc)
            
        Returns:
            Enhanced description
        """
        prompt = f"""Analyze this {element_type} and provide a professional, concise Spanish description suitable for documentation (2-3 sentences max):

{code_context}

Provide ONLY the description, no extra formatting."""
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a technical documentation expert. Provide clear, concise descriptions for code elements in Spanish.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_name,
                temperature=0.7,
                max_tokens=200,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Error: {e}")
            return ""
    
    def generate_readme_summary(self, analysis: Dict[str, Any], project_name: str) -> str:
        """
        Generate a professional README summary using LLM.
        
        Args:
            analysis: Code analysis result
            project_name: Name of the project
            
        Returns:
            Generated README summary
        """
        code_snippet = analysis.get('raw_code', '')[:500]  # First 500 chars
        imports = ', '.join(analysis.get('imports', [])[:5])
        
        prompt = f"""Generate a professional project description for: {project_name}

Based on:
- Technologies: {imports}
- Functions: {len(analysis.get('functions', []))}
- Classes: {len(analysis.get('classes', []))}
- Code preview: {code_snippet[:200]}...

Write a 2-3 sentence professional description in Spanish describing what this project does."""
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a technical writer. Create engaging project descriptions.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_name,
                temperature=0.8,
                max_tokens=300,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Error: {e}")
            return f"Proyecto: {project_name}"
    
    def generate_api_examples(self, endpoint_info: Dict[str, Any], language: str = "bash") -> str:
        """
        Generate API usage examples using LLM.
        
        Args:
            endpoint_info: Endpoint information (method, path, etc)
            language: Language for examples (bash, python, javascript)
            
        Returns:
            Generated example
        """
        method = endpoint_info.get('method', 'GET')
        path = endpoint_info.get('path', '/')
        description = endpoint_info.get('description', '')
        
        prompt = f"""Generate a {language} example for this API endpoint:
- Method: {method}
- Path: {path}
- Description: {description}

Provide a working {language} example with sample data."""
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an API documentation expert. Provide practical, working code examples.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_name,
                temperature=0.7,
                max_tokens=250,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Error: {e}")
            return f"# Ejemplo\n```bash\ncurl -X {method} http://localhost:8000{path}\n```"


class MarkdownGenerator:
    """Generate Markdown documentation from code analysis."""
    
    @staticmethod
    def generate_readme(analysis: Dict[str, Any], project_name: str, use_llm: bool = True) -> str:
        """
        Generate a README file.
        
        Args:
            analysis: Code analysis result
            project_name: Name of the project
            use_llm: Whether to use LLM for enhancement
            
        Returns:
            Generated README in Markdown
        """
        llm = None
        if use_llm:
            try:
                llm = LLMClient()
            except:
                llm = None
        
        readme_parts = []
        
        # Title
        readme_parts.append(f"# 🚀 {project_name}\n")
        
        # Description
        if llm:
            description = llm.generate_readme_summary(analysis, project_name)
        else:
            description = f"Proyecto: {project_name}"
        readme_parts.append(f"## 📋 Descripción\n{description}\n")
        
        # Technologies
        imports = analysis.get('imports', [])
        if imports:
            readme_parts.append("## 🛠️ Tecnologías Utilizadas\n")
            tech_list = MarkdownGenerator._detect_technologies(imports)
            for tech, description in tech_list.items():
                readme_parts.append(f"- **{tech}** - {description}")
            readme_parts.append("")
        
        # Project Structure
        functions = analysis.get('functions', [])
        classes = analysis.get('classes', [])
        
        if classes or functions:
            readme_parts.append("## 📁 Estructura del Proyecto\n")
            
            if classes:
                readme_parts.append("### Clases\n")
                for cls in classes[:5]:  # Max 5 classes
                    readme_parts.append(f"- **{cls['name']}** - {cls.get('docstring', 'Clase').split(chr(10))[0]}")
                readme_parts.append("")
            
            if functions:
                readme_parts.append("### Funciones principales\n")
                for func in functions[:5]:  # Max 5 functions
                    args = ', '.join(func.get('args', []))
                    readme_parts.append(f"- **{func['name']}({args})** - {func.get('docstring', 'Función').split(chr(10))[0]}")
                readme_parts.append("")
        
        # Installation
        readme_parts.append("## ⚡ Instalación Rápida\n")
        readme_parts.append("### Prerrequisitos\n")
        readme_parts.append("- Python 3.8+ o Node.js 14+\n")
        
        readme_parts.append("### Pasos de Instalación\n")
        readme_parts.append("```bash\n")
        readme_parts.append("# 1. Clonar el repositorio\n")
        readme_parts.append("git clone https://github.com/tu-usuario/proyecto.git\n")
        readme_parts.append("cd proyecto\n\n")
        readme_parts.append("# 2. Instalar dependencias\n")
        if 'import' in analysis.get('raw_code', '') and '.py' in str(analysis):
            readme_parts.append("pip install -r requirements.txt\n\n")
        else:
            readme_parts.append("npm install\n\n")
        readme_parts.append("# 3. Ejecutar el proyecto\n")
        readme_parts.append("python main.py  # o npm start\n")
        readme_parts.append("```\n")
        
        # Usage
        readme_parts.append("## 🌐 Uso\n")
        readme_parts.append("```python\n")
        readme_parts.append("# Ejemplo de uso básico\n")
        readme_parts.append("from proyecto import MiClase\n\n")
        readme_parts.append("obj = MiClase()\n")
        readme_parts.append("resultado = obj.procesar_datos()\n")
        readme_parts.append("```\n")
        
        # API Endpoints (if applicable)
        endpoints = analysis.get('endpoints', [])
        if endpoints:
            readme_parts.append("## 🔌 API Endpoints\n")
            for endpoint in endpoints[:5]:
                readme_parts.append(f"- `{endpoint['method']} {endpoint['path']}` - {endpoint.get('description', '')}\n")
            readme_parts.append("")
        
        # License
        readme_parts.append("## 📄 Licencia\n")
        readme_parts.append("MIT License\n")
        
        return "\n".join(readme_parts)
    
    @staticmethod
    def generate_api_documentation(analysis: Dict[str, Any], use_llm: bool = True) -> str:
        """
        Generate API documentation for endpoints.
        
        Args:
            analysis: Code analysis result
            use_llm: Whether to use LLM for examples
            
        Returns:
            Generated API documentation in Markdown
        """
        llm = None
        if use_llm:
            try:
                llm = LLMClient()
            except:
                llm = None
        
        doc_parts = ["# 📡 API Documentation\n"]
        
        endpoints = analysis.get('endpoints', [])
        
        if not endpoints:
            doc_parts.append("No API endpoints found in the code.\n")
            return "\n".join(doc_parts)
        
        doc_parts.append("## 🚀 Endpoints\n")
        
        for endpoint in endpoints:
            method = endpoint.get('method', 'GET')
            path = endpoint.get('path', '/')
            description = endpoint.get('description', f"Endpoint {method} {path}")
            
            doc_parts.append(f"### {method} {path}")
            doc_parts.append(f"{description}\n")
            
            # Request/Response
            doc_parts.append("**Parámetros:**\n")
            if '{' in path:
                # Extract path parameters
                import re
                params = re.findall(r'\{(\w+)\}', path)
                for param in params:
                    doc_parts.append(f"- `{param}` (string): Parámetro de ruta\n")
            else:
                doc_parts.append("- No hay parámetros de ruta\n")
            
            doc_parts.append("\n**Response:**\n")
            doc_parts.append("```json\n")
            doc_parts.append('{\n')
            doc_parts.append('  "status": "success",\n')
            doc_parts.append('  "data": {}\n')
            doc_parts.append('}\n')
            doc_parts.append("```\n")
            
            # Example
            if llm:
                example = llm.generate_api_examples(endpoint, "bash")
            else:
                example = f"```bash\ncurl -X {method} http://localhost:8000{path}\n```"
            
            doc_parts.append("**Ejemplo de uso:**\n")
            doc_parts.append(f"{example}\n")
            
            doc_parts.append("---\n\n")
        
        return "\n".join(doc_parts)
    
    @staticmethod
    def generate_class_documentation(class_info: Dict[str, Any], use_llm: bool = True) -> str:
        """
        Generate documentation for a specific class.
        
        Args:
            class_info: Class information from analysis
            use_llm: Whether to use LLM for enhancement
            
        Returns:
            Generated class documentation in Markdown
        """
        llm = None
        if use_llm:
            try:
                llm = LLMClient()
            except:
                llm = None
        
        doc_parts = []
        
        class_name = class_info.get('name', 'UnknownClass')
        docstring = class_info.get('docstring', '')
        
        doc_parts.append(f"# 🏗️ {class_name}\n")
        
        # Overview
        if docstring:
            doc_parts.append(f"## 📝 Descripción\n{docstring}\n")
        else:
            if llm:
                desc = llm.enhance_description(f"class {class_name}", "class")
                doc_parts.append(f"## 📝 Descripción\n{desc}\n")
        
        # Methods
        methods = class_info.get('methods', [])
        if methods:
            doc_parts.append("## 📖 Métodos\n")
            
            for method in methods:
                method_name = method.get('name', '')
                args = ', '.join(method.get('args', []))
                is_constructor = method.get('is_constructor', False)
                
                if is_constructor:
                    doc_parts.append(f"### `{class_name}({args})`\n")
                    doc_parts.append("Constructor de la clase.\n\n")
                else:
                    doc_parts.append(f"### `{method_name}({args})`\n")
                
                if method.get('docstring'):
                    doc_parts.append(f"{method['docstring']}\n\n")
                
                if args:
                    doc_parts.append("**Parámetros:**\n")
                    for arg in method.get('args', []):
                        doc_parts.append(f"- `{arg}` - Parámetro\n")
                    doc_parts.append("")
                
                doc_parts.append("")
        
        return "\n".join(doc_parts)
    
    @staticmethod
    def generate_function_documentation(func_info: Dict[str, Any], use_llm: bool = True) -> str:
        """
        Generate documentation for a specific function.
        
        Args:
            func_info: Function information from analysis
            use_llm: Whether to use LLM for enhancement
            
        Returns:
            Generated function documentation in Markdown
        """
        llm = None
        if use_llm:
            try:
                llm = LLMClient()
            except:
                llm = None
        
        doc_parts = []
        
        func_name = func_info.get('name', 'unknown')
        args = ', '.join(func_info.get('args', []))
        docstring = func_info.get('docstring', '')
        
        doc_parts.append(f"### `{func_name}({args})`\n")
        
        if docstring:
            doc_parts.append(f"{docstring}\n\n")
        else:
            if llm:
                desc = llm.enhance_description(f"function {func_name}({args})", "function")
                doc_parts.append(f"{desc}\n\n")
        
        if args:
            doc_parts.append("**Parámetros:**\n")
            for arg in func_info.get('args', []):
                doc_parts.append(f"- `{arg}` - Parámetro\n")
            doc_parts.append("")
        
        return_type = func_info.get('return_type')
        if return_type:
            doc_parts.append(f"**Returns:** {return_type}\n\n")
        
        return "\n".join(doc_parts)
    
    @staticmethod
    def _detect_technologies(imports: List[str]) -> Dict[str, str]:
        """Detect technologies from import statements."""
        tech_map = {
            'express': 'Framework web para Node.js',
            'django': 'Framework web para Python',
            'fastapi': 'Framework moderno para APIs en Python',
            'flask': 'Micro-framework web para Python',
            'react': 'Librería para UI con JavaScript',
            'vue': 'Framework JavaScript para UI',
            'angular': 'Framework completo para aplicaciones web',
            'sqlalchemy': 'ORM para Python',
            'mongoose': 'ODM para MongoDB en Node.js',
            'postgresql': 'Base de datos relacional',
            'mongodb': 'Base de datos NoSQL',
            'redis': 'Base de datos en memoria',
            'numpy': 'Librería numérica para Python',
            'pandas': 'Análisis de datos en Python',
            'scikit': 'Machine Learning en Python',
            'tensorflow': 'Framework de Machine Learning',
            'pytorch': 'Framework de Deep Learning',
        }
        
        detected = {}
        for imp in imports:
            imp_lower = imp.lower()
            for tech, desc in tech_map.items():
                if tech in imp_lower:
                    detected[tech.capitalize()] = desc
                    break
        
        return detected or {'Python/JavaScript': 'Lenguaje de programación'}
