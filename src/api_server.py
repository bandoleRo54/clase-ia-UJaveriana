"""
Flask API server for the Technical Documentation Generator.
Provides REST endpoints for code analysis and documentation generation.
"""

from flask import Flask, request, jsonify
import os
import json
from typing import Dict, Any, Tuple
from code_analyzer import CodeAnalyzer
from doc_generator import MarkdownGenerator


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload


# ============================================================================
# HEALTH CHECK & INFO ENDPOINTS
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check() -> Tuple[Dict[str, Any], int]:
    """
    Health check endpoint.
    
    Returns:
        JSON with status and version information
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Technical Documentation Generator',
        'version': '1.0.0',
        'supported_formats': ['.py', '.js']
    }), 200


@app.route('/api/v1/info', methods=['GET'])
def api_info() -> Tuple[Dict[str, Any], int]:
    """
    Get API information and available endpoints.
    
    Returns:
        JSON with API documentation
    """
    return jsonify({
        'service': 'Technical Documentation Generator API',
        'version': '1.0.0',
        'endpoints': {
            'analyze': {
                'path': '/api/v1/analyze',
                'method': 'POST',
                'description': 'Analyze source code and extract structure'
            },
            'readme': {
                'path': '/api/v1/generate/readme',
                'method': 'POST',
                'description': 'Generate README documentation'
            },
            'api_docs': {
                'path': '/api/v1/generate/api-docs',
                'method': 'POST',
                'description': 'Generate API documentation'
            },
            'class_docs': {
                'path': '/api/v1/generate/class-docs',
                'method': 'POST',
                'description': 'Generate class documentation'
            }
        }
    }), 200


# ============================================================================
# CORE FUNCTIONALITY: ANALYSIS ENDPOINTS
# ============================================================================

@app.route('/api/v1/analyze', methods=['POST'])
def analyze_code() -> Tuple[Dict[str, Any], int]:
    """
    Analyze source code and extract structure (functions, classes, imports).
    
    Expected JSON:
    {
        "file_path": "/path/to/file.py or /path/to/file.js"
    }
    
    Returns:
        JSON with analysis results including functions, classes, imports
    """
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data:
            return jsonify({
                'error': 'Missing required field: file_path',
                'example': {'file_path': '/path/to/code.py'}
            }), 400
        
        file_path = data['file_path']
        
        # Validate file exists
        if not os.path.exists(file_path):
            return jsonify({
                'error': f'File not found: {file_path}'
            }), 404
        
        # Validate file extension
        if not (file_path.endswith('.py') or file_path.endswith('.js')):
            return jsonify({
                'error': 'Unsupported file type. Use .py or .js files'
            }), 400
        
        # Analyze the code
        analysis = CodeAnalyzer.analyze(file_path)
        summary = CodeAnalyzer.get_code_summary(analysis)
        
        # Remove raw_code from response (too large)
        analysis_response = {
            'functions': analysis.get('functions', []),
            'classes': analysis.get('classes', []),
            'imports': analysis.get('imports', []),
            'endpoints': analysis.get('endpoints', []),
            'summary': summary
        }
        
        return jsonify({
            'status': 'success',
            'file': file_path,
            'analysis': analysis_response
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


# ============================================================================
# DOCUMENTATION GENERATION ENDPOINTS
# ============================================================================

@app.route('/api/v1/generate/readme', methods=['POST'])
def generate_readme() -> Tuple[Dict[str, Any], int]:
    """
    Generate README documentation from source code.
    
    Expected JSON:
    {
        "file_path": "/path/to/file.py or /path/to/file.js",
        "project_name": "My Project",
        "use_llm": true  (optional, default: true)
    }
    
    Returns:
        JSON with generated README content
    """
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data:
            return jsonify({
                'error': 'Missing required field: file_path'
            }), 400
        
        file_path = data['file_path']
        project_name = data.get('project_name', 'Mi Proyecto')
        use_llm = data.get('use_llm', True)
        
        # Validate file
        if not os.path.exists(file_path):
            return jsonify({'error': f'File not found: {file_path}'}), 404
        
        if not (file_path.endswith('.py') or file_path.endswith('.js')):
            return jsonify({'error': 'Unsupported file type'}), 400
        
        # Analyze code
        analysis = CodeAnalyzer.analyze(file_path)
        
        # Generate README
        readme_content = MarkdownGenerator.generate_readme(
            analysis, 
            project_name, 
            use_llm=use_llm
        )
        
        return jsonify({
            'status': 'success',
            'file': file_path,
            'project_name': project_name,
            'content': readme_content,
            'format': 'markdown'
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/v1/generate/api-docs', methods=['POST'])
def generate_api_docs() -> Tuple[Dict[str, Any], int]:
    """
    Generate API documentation from source code endpoints.
    
    Expected JSON:
    {
        "file_path": "/path/to/file.py or /path/to/file.js",
        "use_llm": true  (optional, default: true)
    }
    
    Returns:
        JSON with generated API documentation
    """
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data:
            return jsonify({
                'error': 'Missing required field: file_path'
            }), 400
        
        file_path = data['file_path']
        use_llm = data.get('use_llm', True)
        
        # Validate file
        if not os.path.exists(file_path):
            return jsonify({'error': f'File not found: {file_path}'}), 404
        
        if not (file_path.endswith('.py') or file_path.endswith('.js')):
            return jsonify({'error': 'Unsupported file type'}), 400
        
        # Analyze code
        analysis = CodeAnalyzer.analyze(file_path)
        
        # Check if endpoints exist
        endpoints = analysis.get('endpoints', [])
        if not endpoints:
            # Fallback to functions documentation
            return jsonify({
                'status': 'no_endpoints',
                'message': 'No API endpoints found. Try using generate/function-docs instead.',
                'file': file_path,
                'functions_available': len(analysis.get('functions', []))
            }), 200
        
        # Generate API docs
        api_docs_content = MarkdownGenerator.generate_api_documentation(
            analysis,
            use_llm=use_llm
        )
        
        return jsonify({
            'status': 'success',
            'file': file_path,
            'endpoints_count': len(endpoints),
            'content': api_docs_content,
            'format': 'markdown'
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/v1/generate/class-docs', methods=['POST'])
def generate_class_docs() -> Tuple[Dict[str, Any], int]:
    """
    Generate class documentation.
    
    Expected JSON:
    {
        "file_path": "/path/to/file.py or /path/to/file.js",
        "class_name": "MyClass",  (optional, documents first if not specified)
        "use_llm": true  (optional, default: true)
    }
    
    Returns:
        JSON with generated class documentation
    """
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data:
            return jsonify({
                'error': 'Missing required field: file_path'
            }), 400
        
        file_path = data['file_path']
        class_name = data.get('class_name')
        use_llm = data.get('use_llm', True)
        
        # Validate file
        if not os.path.exists(file_path):
            return jsonify({'error': f'File not found: {file_path}'}), 404
        
        if not (file_path.endswith('.py') or file_path.endswith('.js')):
            return jsonify({'error': 'Unsupported file type'}), 400
        
        # Analyze code
        analysis = CodeAnalyzer.analyze(file_path)
        
        classes = analysis.get('classes', [])
        if not classes:
            return jsonify({
                'status': 'no_classes',
                'message': 'No classes found in the file',
                'file': file_path
            }), 200
        
        # Find target class
        target_class = None
        if class_name:
            target_class = next((c for c in classes if c['name'] == class_name), None)
            if not target_class:
                return jsonify({
                    'error': f'Class not found: {class_name}',
                    'available_classes': [c['name'] for c in classes]
                }), 404
        else:
            target_class = classes[0]
        
        # Generate class docs
        class_docs_content = MarkdownGenerator.generate_class_documentation(
            target_class,
            use_llm=use_llm
        )
        
        return jsonify({
            'status': 'success',
            'file': file_path,
            'class_name': target_class['name'],
            'methods_count': len(target_class.get('methods', [])),
            'content': class_docs_content,
            'format': 'markdown'
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/v1/generate/function-docs', methods=['POST'])
def generate_function_docs() -> Tuple[Dict[str, Any], int]:
    """
    Generate function documentation.
    
    Expected JSON:
    {
        "file_path": "/path/to/file.py or /path/to/file.js",
        "function_name": "my_function",  (optional, documents first if not specified)
        "use_llm": true  (optional, default: true)
    }
    
    Returns:
        JSON with generated function documentation
    """
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data:
            return jsonify({
                'error': 'Missing required field: file_path'
            }), 400
        
        file_path = data['file_path']
        function_name = data.get('function_name')
        use_llm = data.get('use_llm', True)
        
        # Validate file
        if not os.path.exists(file_path):
            return jsonify({'error': f'File not found: {file_path}'}), 404
        
        if not (file_path.endswith('.py') or file_path.endswith('.js')):
            return jsonify({'error': 'Unsupported file type'}), 400
        
        # Analyze code
        analysis = CodeAnalyzer.analyze(file_path)
        
        functions = analysis.get('functions', [])
        if not functions:
            return jsonify({
                'status': 'no_functions',
                'message': 'No functions found in the file',
                'file': file_path
            }), 200
        
        # Find target function
        target_func = None
        if function_name:
            target_func = next((f for f in functions if f['name'] == function_name), None)
            if not target_func:
                return jsonify({
                    'error': f'Function not found: {function_name}',
                    'available_functions': [f['name'] for f in functions]
                }), 404
        else:
            target_func = functions[0]
        
        # Generate function docs
        from doc_generator import MarkdownGenerator as MG
        func_docs_content = MG.generate_function_documentation(
            target_func,
            use_llm=use_llm
        )
        
        return jsonify({
            'status': 'success',
            'file': file_path,
            'function_name': target_func['name'],
            'args_count': len(target_func.get('args', [])),
            'content': func_docs_content,
            'format': 'markdown'
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


# ============================================================================
# COMBINED DOCUMENTATION ENDPOINT
# ============================================================================

@app.route('/api/v1/generate/complete', methods=['POST'])
def generate_complete_documentation() -> Tuple[Dict[str, Any], int]:
    """
    Generate complete documentation (README + API + Classes).
    
    Expected JSON:
    {
        "file_path": "/path/to/file.py or /path/to/file.js",
        "project_name": "My Project",
        "use_llm": true  (optional, default: true)
    }
    
    Returns:
        JSON with all generated documentation
    """
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data:
            return jsonify({
                'error': 'Missing required field: file_path'
            }), 400
        
        file_path = data['file_path']
        project_name = data.get('project_name', 'Mi Proyecto')
        use_llm = data.get('use_llm', True)
        
        # Validate file
        if not os.path.exists(file_path):
            return jsonify({'error': f'File not found: {file_path}'}), 404
        
        if not (file_path.endswith('.py') or file_path.endswith('.js')):
            return jsonify({'error': 'Unsupported file type'}), 400
        
        # Analyze code
        analysis = CodeAnalyzer.analyze(file_path)
        
        # Generate all documentations
        readme = MarkdownGenerator.generate_readme(analysis, project_name, use_llm=use_llm)
        api_docs = MarkdownGenerator.generate_api_documentation(analysis, use_llm=use_llm)
        
        # Generate class docs for all classes
        class_docs_list = []
        for cls in analysis.get('classes', []):
            class_doc = MarkdownGenerator.generate_class_documentation(cls, use_llm=use_llm)
            class_docs_list.append({
                'class_name': cls['name'],
                'content': class_doc
            })
        
        return jsonify({
            'status': 'success',
            'file': file_path,
            'project_name': project_name,
            'documentation': {
                'readme': readme,
                'api_docs': api_docs,
                'classes': class_docs_list
            },
            'summary': {
                'functions': len(analysis.get('functions', [])),
                'classes': len(analysis.get('classes', [])),
                'endpoints': len(analysis.get('endpoints', []))
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error) -> Tuple[Dict[str, Any], int]:
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 404
    }), 404


@app.errorhandler(500)
def internal_error(error) -> Tuple[Dict[str, Any], int]:
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'status': 500
    }), 500


if __name__ == '__main__':
    # Run in debug mode
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=True
    )
