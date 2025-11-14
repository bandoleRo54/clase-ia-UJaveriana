# 📚 Technical Documentation Generator API

Un sistema automatizado que genera documentación técnica profesional (README, API docs, class documentation) a partir de código fuente Python o JavaScript.

## 🎯 Características Core (Obligatorias)

- ✅ **Análisis de código fuente** - Extrae funciones, clases y módulos
- ✅ **Generación de README** - Crea documentación de proyecto con secciones estándar
- ✅ **Documentación de API** - Genera docs para endpoints y funciones
- ✅ **Exportación a Markdown** - Genera Markdown bien formateado

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+** - Lenguaje base
- **Flask** - Framework web para los endpoints
- **OpenAI API** (GitHub Models) - Para mejorar descripciones con IA
- **AST** - Para análisis de código Python
- **Regex** - Para análisis de código JavaScript

## 📋 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes Python)
- Token de GitHub para usar GitHub Models (opcional, para LLM)

### Pasos de Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/doc-generator.git
cd doc-generator

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno (opcional)
export GITHUB_TOKEN="tu_token_aqui"  # Para usar LLM enhancement
```

## 🚀 Inicio Rápido

### Ejecutar el servidor

```bash
python api_server.py
```

El servidor estará disponible en `http://localhost:5000`

### Usar el cliente de ejemplo

```bash
python example_client.py
```

## 📡 API Endpoints

### 1. Health Check
Verificar que el API está funcionando.

```
GET /health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "Technical Documentation Generator",
  "version": "1.0.0",
  "supported_formats": [".py", ".js"]
}
```

### 2. Analizar Código
Extraer estructura del código fuente.

```
POST /api/v1/analyze
```

**Body:**
```json
{
  "file_path": "/path/to/file.py"
}
```

**Respuesta:**
```json
{
  "status": "success",
  "file": "/path/to/file.py",
  "analysis": {
    "functions": [...],
    "classes": [...],
    "imports": [...],
    "endpoints": [...],
    "summary": {...}
  }
}
```

### 3. Generar README
Crear documentación README del proyecto.

```
POST /api/v1/generate/readme
```

**Body:**
```json
{
  "file_path": "/path/to/file.py",
  "project_name": "Mi Proyecto",
  "use_llm": true
}
```

**Respuesta:**
```json
{
  "status": "success",
  "file": "/path/to/file.py",
  "project_name": "Mi Proyecto",
  "content": "# 🚀 Mi Proyecto\n\n## Descripción\n...",
  "format": "markdown"
}
```

### 4. Generar Documentación de API
Crear documentación de endpoints REST.

```
POST /api/v1/generate/api-docs
```

**Body:**
```json
{
  "file_path": "/path/to/api.js",
  "use_llm": true
}
```

**Respuesta:**
```json
{
  "status": "success",
  "file": "/path/to/api.js",
  "endpoints_count": 5,
  "content": "# 📡 API Documentation\n\n## 🚀 Endpoints\n...",
  "format": "markdown"
}
```

### 5. Generar Documentación de Clases
Crear documentación detallada de una clase.

```
POST /api/v1/generate/class-docs
```

**Body:**
```json
{
  "file_path": "/path/to/file.py",
  "class_name": "MyClass",
  "use_llm": true
}
```

**Respuesta:**
```json
{
  "status": "success",
  "file": "/path/to/file.py",
  "class_name": "MyClass",
  "methods_count": 5,
  "content": "# 🏗️ MyClass\n...",
  "format": "markdown"
}
```

### 6. Generar Documentación de Funciones
Crear documentación detallada de una función.

```
POST /api/v1/generate/function-docs
```

**Body:**
```json
{
  "file_path": "/path/to/file.py",
  "function_name": "my_function",
  "use_llm": true
}
```

**Respuesta:**
```json
{
  "status": "success",
  "file": "/path/to/file.py",
  "function_name": "my_function",
  "args_count": 2,
  "content": "### `my_function(arg1, arg2)`\n...",
  "format": "markdown"
}
```

### 7. Generar Documentación Completa
Generar README + API Docs + Class Docs en una sola llamada.

```
POST /api/v1/generate/complete
```

**Body:**
```json
{
  "file_path": "/path/to/file.py",
  "project_name": "Mi Proyecto",
  "use_llm": true
}
```

**Respuesta:**
```json
{
  "status": "success",
  "file": "/path/to/file.py",
  "project_name": "Mi Proyecto",
  "documentation": {
    "readme": "# 🚀 Mi Proyecto\n...",
    "api_docs": "# 📡 API Documentation\n...",
    "classes": [
      {
        "class_name": "MyClass",
        "content": "# 🏗️ MyClass\n..."
      }
    ]
  },
  "summary": {
    "functions": 5,
    "classes": 2,
    "endpoints": 3
  }
}
```

## 🏗️ Arquitectura

### Módulos

```
├── code_analyzer.py       # Análisis de código fuente
│   ├── PythonAnalyzer     # Parser Python (AST)
│   ├── JavaScriptAnalyzer # Parser JavaScript (Regex)
│   └── CodeAnalyzer       # Coordinator
│
├── doc_generator.py       # Generación de documentación
│   ├── LLMClient          # Cliente OpenAI/GitHub Models
│   └── MarkdownGenerator  # Templates y generación
│
├── api_server.py          # Servidor Flask con endpoints
│
└── example_client.py      # Cliente de ejemplo
```

### Flujo de Procesamiento

```
Código Fuente (.py/.js)
         ↓
    [CodeAnalyzer]
         ↓
  ┌─────────────┐
  │ Funciones   │
  │ Clases      │ ← AST/Regex Parsing
  │ Endpoints   │
  │ Imports     │
  └─────────────┘
         ↓
  [LLMClient - Opcional]
    Enhance descriptions
         ↓
  [MarkdownGenerator]
    Apply templates
         ↓
   Markdown Output
```

## 💻 Ejemplos de Uso

### Ejemplo 1: Analizar archivo Python

```bash
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"file_path": "/path/to/example_fastapi.py"}'
```

### Ejemplo 2: Generar README

```bash
curl -X POST http://localhost:5000/api/v1/generate/readme \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/path/to/example_fastapi.py",
    "project_name": "User Management API",
    "use_llm": false
  }'
```

### Ejemplo 3: Generar API Docs

```bash
curl -X POST http://localhost:5000/api/v1/generate/api-docs \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/path/to/example_fastapi.py",
    "use_llm": false
  }'
```

### Ejemplo 4: Generar todo

```bash
curl -X POST http://localhost:5000/api/v1/generate/complete \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/path/to/example_fastapi.py",
    "project_name": "User Management API",
    "use_llm": false
  }' | python -m json.tool
```

## 📦 Usar con n8n

### Workflow Básico

1. **Nodo HTTP Request** (POST) → `/api/v1/generate/readme`
2. **Nodo Set** → Configurar payload con file_path y project_name
3. **Nodo HTTP Request** → Enviar a `/api/v1/generate/readme`
4. **Nodo Write to File** → Guardar contenido del README

### Configuración en n8n

```json
{
  "workflows": [
    {
      "name": "Generate Documentation",
      "nodes": [
        {
          "name": "Trigger",
          "type": "webhook"
        },
        {
          "name": "Analyze Code",
          "type": "httpRequest",
          "url": "http://localhost:5000/api/v1/analyze"
        },
        {
          "name": "Generate README",
          "type": "httpRequest",
          "url": "http://localhost:5000/api/v1/generate/readme"
        },
        {
          "name": "Save Documentation",
          "type": "writeFile"
        }
      ]
    }
  ]
}
```

## 🔧 Configuración Avanzada

### Usar GitHub Models API

Para usar mejoras con IA, configura tu token:

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
python api_server.py
```

### Desactivar LLM

En las peticiones, usa `"use_llm": false`:

```json
{
  "file_path": "/path/to/file.py",
  "project_name": "Mi Proyecto",
  "use_llm": false
}
```

## 📝 Formatos Soportados

### Input
- ✅ Python (.py) - AST parsing completo
- ✅ JavaScript (.js) - Regex parsing

### Output
- ✅ Markdown (.md) - Formato único de salida

## 🧪 Testing

Prueba el sistema con los archivos de ejemplo:

```bash
# Analizar ejemplo FastAPI
python -c "from code_analyzer import CodeAnalyzer; print(CodeAnalyzer.analyze('./example_fastapi.py'))"

# Generar README
python -c "
from code_analyzer import CodeAnalyzer
from doc_generator import MarkdownGenerator
analysis = CodeAnalyzer.analyze('./example_fastapi.py')
readme = MarkdownGenerator.generate_readme(analysis, 'FastAPI Example', use_llm=False)
print(readme)
"
```

## 🚨 Manejo de Errores

El API devuelve códigos de estado HTTP apropiados:

- `200 OK` - Éxito
- `400 Bad Request` - Parámetros inválidos
- `404 Not Found` - Archivo o recurso no encontrado
- `500 Internal Server Error` - Error del servidor

Ejemplo de respuesta de error:

```json
{
  "error": "File not found: /path/to/missing.py",
  "status": 404
}
```

## 📊 Casos de Uso Soportados

### 1. Documentación de API REST
✅ Extrae endpoints (GET, POST, PUT, DELETE, etc.)
✅ Genera ejemplos con curl
✅ Documenta parámetros y respuestas

### 2. Documentación de Proyecto
✅ README con descripción del proyecto
✅ Secciones estándar (instalación, uso, etc.)
✅ Estructura del proyecto

### 3. Documentación de Clases
✅ Descripción de clases
✅ Métodos y propiedades
✅ Ejemplos de uso

### 4. Documentación de Funciones
✅ Parámetros y tipos
✅ Retorno y excepciones
✅ Ejemplos de uso

## 🎓 Ejemplos de Salida

### README Generado

```markdown
# 🚀 User Management API

## 📋 Descripción
Sistema de gestión de usuarios construido con FastAPI que proporciona 
operaciones CRUD completas con validaciones.

## 🛠️ Tecnologías Utilizadas
- **FastAPI** - Framework moderno para APIs
- **Pydantic** - Validación de datos

## 📁 Estructura del Proyecto
### Clases
- **User** - Modelo de usuario para requests
- **UserResponse** - Modelo de usuario para responses

### Funciones principales
- **create_user(user: User)** - Crea un nuevo usuario
- **get_user(user_id: int)** - Obtiene información de usuario
```

### API Docs Generado

```markdown
# 📡 API Documentation

## 🚀 Endpoints

### POST /users/
Crea un nuevo usuario en el sistema.

**Parámetros:** No hay parámetros de ruta

**Response:**
```json
{
  "status": "success",
  "data": {}
}
```

**Ejemplo de uso:**
```bash
curl -X POST http://localhost:8000/users/
```
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

---

**Última actualización:** 2024
**Estado:** ✅ Funcional - Core features implementadas
