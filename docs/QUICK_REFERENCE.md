# 🚀 Quick Reference - Documentation Generator API

## Inicio Rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar servidor
python api_server.py

# 3. Verificar estado
curl http://localhost:5000/health
```

---

## 📡 Endpoints Principales

### 1. Analizar Código
**POST** `/api/v1/analyze`

```bash
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"file_path": "/path/to/file.py"}'
```

---

### 2. Generar README
**POST** `/api/v1/generate/readme`

```bash
curl -X POST http://localhost:5000/api/v1/generate/readme \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/path/to/file.py",
    "project_name": "Mi Proyecto",
    "use_llm": false
  }' > README.md
```

---

### 3. Generar API Docs
**POST** `/api/v1/generate/api-docs`

```bash
curl -X POST http://localhost:5000/api/v1/generate/api-docs \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/path/to/api.js",
    "use_llm": false
  }' > API_DOCS.md
```

---

### 4. Generar Documentación de Clases
**POST** `/api/v1/generate/class-docs`

```bash
curl -X POST http://localhost:5000/api/v1/generate/class-docs \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/path/to/file.py",
    "class_name": "MyClass",
    "use_llm": false
  }' > CLASS_DOCS.md
```

---

### 5. Generar Todo de una Vez
**POST** `/api/v1/generate/complete`

```bash
curl -X POST http://localhost:5000/api/v1/generate/complete \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/path/to/file.py",
    "project_name": "Proyecto",
    "use_llm": false
  }' > complete_docs.json
```

---

## 🔧 Uso Programático (Python)

```python
from code_analyzer import CodeAnalyzer
from doc_generator import MarkdownGenerator

# Analizar código
analysis = CodeAnalyzer.analyze('./example.py')

# Generar README
readme = MarkdownGenerator.generate_readme(
    analysis,
    project_name="Mi Proyecto",
    use_llm=False
)

# Generar API docs
api_docs = MarkdownGenerator.generate_api_documentation(
    analysis,
    use_llm=False
)

# Generar documentación de clase
class_doc = MarkdownGenerator.generate_class_documentation(
    analysis['classes'][0],
    use_llm=False
)

print(readme)
print(api_docs)
print(class_doc)
```

---

## 🔗 Uso con n8n

### Configuración de Nodo HTTP

```
URL: http://localhost:5000/api/v1/generate/readme
Method: POST
Authentication: None

Body:
{
  "file_path": "{{ $json.filepath }}",
  "project_name": "{{ $json.project }}",
  "use_llm": false
}

Headers:
Content-Type: application/json
```

### Workflow Básico

1. **Webhook** → Recibir solicitud con filepath
2. **HTTP Request** → POST a `/api/v1/generate/readme`
3. **Set** → Extraer content del response
4. **Write File** → Guardar README.md
5. **Email** → Notificar cuando esté listo

---

## 📊 Formatos Soportados

| Entrada | Salida | Status |
|---------|--------|--------|
| .py | Markdown | ✅ |
| .js | Markdown | ✅ |

---

## 🎯 Casos de Uso

### Caso 1: API REST (JavaScript/Express)
```javascript
// input: api.js
app.post('/api/users/', (req, res) => {
  // código...
});
```
```bash
# comando
curl -X POST http://localhost:5000/api/v1/generate/api-docs \
  -H "Content-Type: application/json" \
  -d '{"file_path": "api.js", "use_llm": false}'
```

---

### Caso 2: Proyecto Python
```python
# input: main.py
class DatabaseManager:
    def connect(self): pass
    def query(self, sql): pass
```
```bash
# comando
curl -X POST http://localhost:5000/api/v1/generate/complete \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "main.py",
    "project_name": "DB Manager",
    "use_llm": false
  }'
```

---

## ⚙️ Variables de Entorno

```bash
# Token para LLM (GitHub Models)
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"

# Puerto (opcional)
export PORT=5000

# Ejecutar
python api_server.py
```

---

## 🐛 Troubleshooting

### Error: "File not found"
- Verifica que la ruta es absoluta o relativa correcta
- Asegúrate que el archivo existe

### Error: "Unsupported file type"
- Solo soporta `.py` (Python) y `.js` (JavaScript)
- Verifica la extensión del archivo

### Error: "GITHUB_TOKEN not set"
- Usa `use_llm: false` en tu request
- O configura la variable de entorno

### API no responde
- Verifica que el servidor está corriendo: `curl http://localhost:5000/health`
- Revisa si el puerto 5000 está disponible

---

## 📝 Parámetros de Request

### Requeridos
- `file_path` (string) - Ruta al archivo

### Opcionales
- `project_name` (string) - Nombre del proyecto [default: "Mi Proyecto"]
- `class_name` (string) - Nombre de clase específica [default: primera]
- `function_name` (string) - Nombre de función específica [default: primera]
- `use_llm` (boolean) - Usar LLM para mejoras [default: true]

---

## 🎨 Formato de Salida Markdown

### README
```markdown
# 🚀 Nombre del Proyecto
## 📋 Descripción
## 🛠️ Tecnologías Utilizadas
## 📁 Estructura del Proyecto
## ⚡ Instalación Rápida
## 🌐 Uso
## 🔌 API Endpoints
## 📄 Licencia
```

### API Docs
```markdown
# 📡 API Documentation
## 🚀 Endpoints
### METHOD /path
Description
**Parámetros:**
**Response:**
**Ejemplo de uso:**
```

### Class Docs
```markdown
# 🏗️ ClassName
## 📝 Descripción
## 🏗️ Constructor
## 📖 Métodos
```

---

## 🧪 Testing

```bash
# Ejecutar tests
python -m pytest test_generators.py -v

# O con unittest
python test_generators.py
```

---

## 🐳 Con Docker

```bash
# Construir imagen
docker build -t doc-generator .

# Ejecutar contenedor
docker run -p 5000:5000 -e GITHUB_TOKEN="$GITHUB_TOKEN" doc-generator

# O con docker-compose
docker-compose up
```

---

## 📚 Recursos

- **OpenAPI Spec**: `openapi.json`
- **Ejemplos**: `example_fastapi.py`, `example_client.py`
- **Tests**: `test_generators.py`
- **Documentación completa**: `README.md`

---

## 💡 Tips

1. **Sin LLM**: Usa `use_llm: false` para respuestas más rápidas
2. **Batch**: Genera documentación completa con `/generate/complete`
3. **Integraciones**: Usa con n8n, Make, Zapier, etc.
4. **Guardado**: Guarda la salida directamente a archivo con redirección
5. **Automatización**: CronJob + API para documentación automática

---

## 📞 Soporte

Para issues o sugerencias, consulta la documentación completa en `README.md`

---

**Versión**: 1.0.0 | **Última actualización**: 2024
