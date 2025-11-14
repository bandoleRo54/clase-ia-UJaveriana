"""
Module for analyzing source code and extracting structure.
Supports Python and JavaScript files.
"""

import ast
import re
import json
from typing import Dict, List, Any, Optional


class PythonAnalyzer:
    """Analyzes Python source code and extracts functions, classes, and modules."""
    
    @staticmethod
    def parse_file(file_path: str) -> Dict[str, Any]:
        """
        Parse a Python file and extract its structure.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            Dictionary containing functions, classes, imports, and docstrings
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            tree = ast.parse(code)
        except Exception as e:
            raise ValueError(f"Error parsing Python file: {e}")
        
        return {
            'functions': PythonAnalyzer._extract_functions(tree),
            'classes': PythonAnalyzer._extract_classes(tree),
            'imports': PythonAnalyzer._extract_imports(tree),
            'module_docstring': ast.get_docstring(tree) or '',
            'raw_code': code
        }
    
    @staticmethod
    def _extract_functions(tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract function definitions from AST."""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not PythonAnalyzer._is_method(node, tree):
                func_info = {
                    'name': node.name,
                    'docstring': ast.get_docstring(node) or '',
                    'args': [arg.arg for arg in node.args.args],
                    'decorators': [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list],
                    'line_number': node.lineno,
                }
                # Try to extract return type from docstring
                func_info['return_type'] = PythonAnalyzer._extract_return_type(func_info['docstring'])
                functions.append(func_info)
        return functions
    
    @staticmethod
    def _extract_classes(tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract class definitions from AST."""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'docstring': ast.get_docstring(node) or '',
                    'methods': [],
                    'properties': [],
                    'line_number': node.lineno,
                }
                
                # Extract methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_info = {
                            'name': item.name,
                            'docstring': ast.get_docstring(item) or '',
                            'args': [arg.arg for arg in item.args.args if arg.arg != 'self'],
                            'is_private': item.name.startswith('_'),
                        }
                        class_info['methods'].append(method_info)
                    elif isinstance(item, ast.Assign):
                        # Simple property detection
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                class_info['properties'].append(target.id)
                
                classes.append(class_info)
        return classes
    
    @staticmethod
    def _extract_imports(tree: ast.AST) -> List[str]:
        """Extract import statements from AST."""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"from {module} import {alias.name}")
        return list(set(imports))
    
    @staticmethod
    def _extract_return_type(docstring: str) -> Optional[str]:
        """Extract return type from docstring."""
        if not docstring:
            return None
        match = re.search(r'Returns?:\s*([^\n]+)', docstring, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None
    
    @staticmethod
    def _is_method(node: ast.FunctionDef, tree: ast.AST) -> bool:
        """Check if a function is a method of a class."""
        for parent in ast.walk(tree):
            if isinstance(parent, ast.ClassDef):
                for item in parent.body:
                    if isinstance(item, ast.FunctionDef) and item.name == node.name:
                        return True
        return False


class JavaScriptAnalyzer:
    """Analyzes JavaScript source code and extracts functions, classes, and modules."""
    
    @staticmethod
    def parse_file(file_path: str) -> Dict[str, Any]:
        """
        Parse a JavaScript file and extract its structure.
        Uses regex-based parsing for simplicity.
        
        Args:
            file_path: Path to the JavaScript file
            
        Returns:
            Dictionary containing functions, classes, and other structure
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            raise ValueError(f"Error reading JavaScript file: {e}")
        
        return {
            'functions': JavaScriptAnalyzer._extract_functions(code),
            'classes': JavaScriptAnalyzer._extract_classes(code),
            'imports': JavaScriptAnalyzer._extract_imports(code),
            'endpoints': JavaScriptAnalyzer._extract_endpoints(code),
            'raw_code': code
        }
    
    @staticmethod
    def _extract_functions(code: str) -> List[Dict[str, Any]]:
        """Extract function definitions using regex."""
        functions = []
        
        # Match: function name(args) or const name = (args) =>
        function_patterns = [
            r'function\s+(\w+)\s*\(\s*([^)]*)\s*\)',
            r'const\s+(\w+)\s*=\s*(?:async\s*)?\(\s*([^)]*)\s*\)\s*=>',
            r'async\s+function\s+(\w+)\s*\(\s*([^)]*)\s*\)',
        ]
        
        for pattern in function_patterns:
            for match in re.finditer(pattern, code):
                func_name = match.group(1)
                args_str = match.group(2)
                args = [arg.strip() for arg in args_str.split(',') if arg.strip()]
                
                # Extract JSDoc comment if exists
                docstring = JavaScriptAnalyzer._extract_jsdoc(code, match.start())
                
                functions.append({
                    'name': func_name,
                    'docstring': docstring,
                    'args': args,
                    'is_async': 'async' in match.group(0),
                })
        
        return functions
    
    @staticmethod
    def _extract_classes(code: str) -> List[Dict[str, Any]]:
        """Extract class definitions using regex."""
        classes = []
        
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{'
        for match in re.finditer(class_pattern, code):
            class_name = match.group(1)
            extends = match.group(2) or None
            
            # Find methods within class
            class_start = match.end()
            class_end = JavaScriptAnalyzer._find_matching_brace(code, class_start - 1)
            class_body = code[class_start:class_end]
            
            methods = []
            method_pattern = r'(?:async\s+)?(\w+)\s*\(\s*([^)]*)\s*\)\s*\{'
            for method_match in re.finditer(method_pattern, class_body):
                method_name = method_match.group(1)
                if method_name not in ['if', 'for', 'while', 'switch', 'catch']:
                    args_str = method_match.group(2)
                    args = [arg.strip() for arg in args_str.split(',') if arg.strip()]
                    methods.append({
                        'name': method_name,
                        'args': args,
                        'is_constructor': method_name == 'constructor',
                    })
            
            classes.append({
                'name': class_name,
                'extends': extends,
                'methods': methods,
            })
        
        return classes
    
    @staticmethod
    def _extract_imports(code: str) -> List[str]:
        """Extract import statements from JavaScript code."""
        imports = []
        
        import_patterns = [
            r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
            r"require\(['\"]([^'\"]+)['\"]\)",
        ]
        
        for pattern in import_patterns:
            for match in re.finditer(pattern, code):
                imports.append(match.group(1))
        
        return list(set(imports))
    
    @staticmethod
    def _extract_endpoints(code: str) -> List[Dict[str, Any]]:
        """Extract API endpoints (Express, etc.)."""
        endpoints = []
        
        endpoint_pattern = r'app\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']'
        for match in re.finditer(endpoint_pattern, code):
            method = match.group(1).upper()
            path = match.group(2)
            
            # Extract function comment if exists
            comment = JavaScriptAnalyzer._extract_jsdoc(code, match.start())
            
            endpoints.append({
                'method': method,
                'path': path,
                'description': comment,
            })
        
        return endpoints
    
    @staticmethod
    def _extract_jsdoc(code: str, position: int) -> str:
        """Extract JSDoc comment preceding a position."""
        # Search backwards for /** ... */
        start = code.rfind('/**', 0, position)
        if start == -1:
            return ''
        
        end = code.find('*/', start)
        if end == -1:
            return ''
        
        jsdoc = code[start:end+2]
        # Clean up JSDoc markers
        lines = jsdoc.split('\n')
        cleaned = []
        for line in lines:
            line = line.strip()
            if line.startswith('/**') or line.startswith('*/'):
                continue
            if line.startswith('*'):
                line = line[1:].strip()
            cleaned.append(line)
        
        return '\n'.join(cleaned).strip()
    
    @staticmethod
    def _find_matching_brace(code: str, start: int) -> int:
        """Find matching closing brace."""
        count = 1
        for i in range(start + 1, len(code)):
            if code[i] == '{':
                count += 1
            elif code[i] == '}':
                count -= 1
                if count == 0:
                    return i
        return len(code)


class CodeAnalyzer:
    """Main analyzer that delegates to language-specific analyzers."""
    
    @staticmethod
    def analyze(file_path: str) -> Dict[str, Any]:
        """
        Analyze a source code file (Python or JavaScript).
        
        Args:
            file_path: Path to the source file (.py or .js)
            
        Returns:
            Dictionary with analyzed code structure
        """
        if file_path.endswith('.py'):
            return PythonAnalyzer.parse_file(file_path)
        elif file_path.endswith('.js'):
            return JavaScriptAnalyzer.parse_file(file_path)
        else:
            raise ValueError("Unsupported file type. Use .py or .js files.")
    
    @staticmethod
    def get_code_summary(analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary of the analyzed code.
        
        Args:
            analysis: Result from analyze()
            
        Returns:
            Summary dictionary
        """
        return {
            'num_functions': len(analysis.get('functions', [])),
            'num_classes': len(analysis.get('classes', [])),
            'imports': analysis.get('imports', []),
            'has_api_endpoints': len(analysis.get('endpoints', [])) > 0,
            'num_endpoints': len(analysis.get('endpoints', [])),
        }
