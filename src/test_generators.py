"""
Test cases for the Documentation Generator API.
Demonstrates core functionality with real examples.
"""

import unittest
import json
from code_analyzer import CodeAnalyzer, PythonAnalyzer, JavaScriptAnalyzer
from doc_generator import MarkdownGenerator
import tempfile
import os


class TestPythonAnalyzer(unittest.TestCase):
    """Test Python code analysis."""
    
    def setUp(self):
        """Create temporary Python file for testing."""
        self.test_code = '''
"""Module docstring"""

def simple_function(x, y):
    """Add two numbers."""
    return x + y

class MyClass:
    """A simple class."""
    
    def __init__(self, name):
        """Initialize the class."""
        self.name = name
    
    def get_name(self):
        """Get the name."""
        return self.name
'''
        # Write to temp file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        self.temp_file.write(self.test_code)
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up temp file."""
        os.unlink(self.temp_file.name)
    
    def test_parse_functions(self):
        """Test extracting functions from Python code."""
        analysis = PythonAnalyzer.parse_file(self.temp_file.name)
        
        self.assertIn('functions', analysis)
        self.assertEqual(len(analysis['functions']), 1)
        self.assertEqual(analysis['functions'][0]['name'], 'simple_function')
        self.assertEqual(len(analysis['functions'][0]['args']), 2)
    
    def test_parse_classes(self):
        """Test extracting classes from Python code."""
        analysis = PythonAnalyzer.parse_file(self.temp_file.name)
        
        self.assertIn('classes', analysis)
        self.assertEqual(len(analysis['classes']), 1)
        self.assertEqual(analysis['classes'][0]['name'], 'MyClass')
        self.assertEqual(len(analysis['classes'][0]['methods']), 2)
    
    def test_parse_docstrings(self):
        """Test extracting docstrings."""
        analysis = PythonAnalyzer.parse_file(self.temp_file.name)
        
        self.assertEqual(analysis['module_docstring'], 'Module docstring')
        self.assertIn('Add two numbers', analysis['functions'][0]['docstring'])


class TestJavaScriptAnalyzer(unittest.TestCase):
    """Test JavaScript code analysis."""
    
    def setUp(self):
        """Create temporary JavaScript file for testing."""
        self.test_code = '''
// Express API
const express = require('express');
const app = express();

app.post('/api/users/', async (req, res) => {
  // Create user
  res.json({message: "User created"});
});

app.get('/api/users/{user_id}', (req, res) => {
  // Get user
  res.json({id: req.params.user_id});
});

class UserManager {
  constructor(db) {
    this.db = db;
  }
  
  async getUser(id) {
    return await this.db.query(`SELECT * FROM users WHERE id = ${id}`);
  }
}
'''
        # Write to temp file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False)
        self.temp_file.write(self.test_code)
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up temp file."""
        os.unlink(self.temp_file.name)
    
    def test_parse_endpoints(self):
        """Test extracting API endpoints from JavaScript."""
        analysis = JavaScriptAnalyzer.parse_file(self.temp_file.name)
        
        self.assertIn('endpoints', analysis)
        self.assertGreater(len(analysis['endpoints']), 0)
    
    def test_parse_imports(self):
        """Test extracting imports from JavaScript."""
        analysis = JavaScriptAnalyzer.parse_file(self.temp_file.name)
        
        self.assertIn('imports', analysis)
        self.assertIn('express', analysis['imports'])
    
    def test_parse_classes(self):
        """Test extracting classes from JavaScript."""
        analysis = JavaScriptAnalyzer.parse_file(self.temp_file.name)
        
        self.assertIn('classes', analysis)
        self.assertEqual(len(analysis['classes']), 1)
        self.assertEqual(analysis['classes'][0]['name'], 'UserManager')


class TestMarkdownGenerator(unittest.TestCase):
    """Test Markdown generation."""
    
    def setUp(self):
        """Create sample analysis data."""
        self.analysis = {
            'functions': [
                {
                    'name': 'create_user',
                    'docstring': 'Create a new user',
                    'args': ['name', 'email'],
                    'decorators': [],
                }
            ],
            'classes': [
                {
                    'name': 'UserManager',
                    'docstring': 'Manages user operations',
                    'methods': [
                        {'name': 'get_user', 'args': ['user_id'], 'is_constructor': False},
                        {'name': 'delete_user', 'args': ['user_id'], 'is_constructor': False}
                    ],
                    'properties': []
                }
            ],
            'imports': ['fastapi', 'pydantic'],
            'endpoints': [
                {'method': 'POST', 'path': '/users/', 'description': 'Create user'},
                {'method': 'GET', 'path': '/users/{user_id}', 'description': 'Get user'}
            ],
            'raw_code': 'sample code',
            'module_docstring': ''
        }
    
    def test_generate_readme(self):
        """Test README generation."""
        readme = MarkdownGenerator.generate_readme(
            self.analysis,
            'Test Project',
            use_llm=False
        )
        
        self.assertIn('Test Project', readme)
        self.assertIn('Descripción', readme)
        self.assertIn('Tecnologías', readme)
        self.assertIn('Instalación', readme)
        self.assertIn('Uso', readme)
    
    def test_generate_api_docs(self):
        """Test API documentation generation."""
        api_docs = MarkdownGenerator.generate_api_documentation(
            self.analysis,
            use_llm=False
        )
        
        self.assertIn('POST', api_docs)
        self.assertIn('GET', api_docs)
        self.assertIn('/users/', api_docs)
    
    def test_generate_class_docs(self):
        """Test class documentation generation."""
        class_doc = MarkdownGenerator.generate_class_documentation(
            self.analysis['classes'][0],
            use_llm=False
        )
        
        self.assertIn('UserManager', class_doc)
        self.assertIn('get_user', class_doc)
        self.assertIn('delete_user', class_doc)


class TestCodeAnalyzer(unittest.TestCase):
    """Test the main CodeAnalyzer coordinator."""
    
    def test_get_code_summary(self):
        """Test code summary generation."""
        analysis = {
            'functions': [1, 2, 3],
            'classes': [1, 2],
            'imports': ['a', 'b'],
            'endpoints': [1]
        }
        
        summary = CodeAnalyzer.get_code_summary(analysis)
        
        self.assertEqual(summary['num_functions'], 3)
        self.assertEqual(summary['num_classes'], 2)
        self.assertEqual(len(summary['imports']), 2)
        self.assertTrue(summary['has_api_endpoints'])
        self.assertEqual(summary['num_endpoints'], 1)


class TestIntegration(unittest.TestCase):
    """Integration tests for the full pipeline."""
    
    def setUp(self):
        """Create a sample Python file for integration testing."""
        self.test_code = '''
"""Sample API module."""

from fastapi import FastAPI

app = FastAPI()

class Database:
    """Database manager."""
    
    def connect(self):
        """Connect to database."""
        pass

@app.post("/api/data")
def create_data(data: dict):
    """Create new data entry."""
    return {"id": 1, "data": data}
'''
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        self.temp_file.write(self.test_code)
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up."""
        os.unlink(self.temp_file.name)
    
    def test_full_pipeline(self):
        """Test complete analysis to documentation generation."""
        # Step 1: Analyze code
        analysis = CodeAnalyzer.analyze(self.temp_file.name)
        
        self.assertEqual(len(analysis['functions']), 1)
        self.assertEqual(len(analysis['classes']), 1)
        
        # Step 2: Generate README
        readme = MarkdownGenerator.generate_readme(
            analysis,
            'Sample API',
            use_llm=False
        )
        
        self.assertIn('Sample API', readme)
        self.assertIsInstance(readme, str)
        self.assertGreater(len(readme), 100)
        
        # Step 3: Verify markdown format
        self.assertIn('#', readme)  # Has headers
        self.assertIn('```', readme)  # Has code blocks


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
