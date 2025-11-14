# 🔗 Integración con n8n

Guía completa para integrar el API de Generador de Documentación con n8n.

---

## 📋 Tabla de Contenidos

1. [Configuración Inicial](#configuración-inicial)
2. [Nodos Recomendados](#nodos-recomendados)
3. [Workflows de Ejemplo](#workflows-de-ejemplo)
4. [Variables y Credenciales](#variables-y-credenciales)
5. [Troubleshooting](#troubleshooting)

---

## Configuración Inicial

### 1. Iniciar el API

```bash
# Terminal 1: Servidor API
export GITHUB_TOKEN="tu_token_aqui"  # opcional
python api_server.py
# API disponible en: http://localhost:5000
```

### 2. Verificar Conectividad

```bash
# Terminal 2: Test
curl http://localhost:5000/health
# Deberías ver: {"status": "healthy", ...}
```

### 3. Configurar n8n

- Abre n8n en `http://localhost:5678`
- Crea un nuevo workflow
- Añade nodos HTTP Request

---

## Nodos Recomendados

### A. Nodo Webhook (Trigger)

```
Webhook
├─ HTTP Method: POST
├─ Path: /doc-generator
├─ Authentication: None
└─ Response Mode: Last Node Output
```

**Body de ejemplo que recibirá:**
```json
{
  "file_path": "/path/to/code.py",
  "project_name": "My Project",
  "doc_type": "readme"
}
```

---

### B. Nodo HTTP Request (Analyze)

```
HTTP Request
├─ Method: POST
├─ URL: http://localhost:5000/api/v1/analyze
├─ Authentication: None
├─ Headers:
│  └─ Content-Type: application/json
└─ Body:
   {
     "file_path": "{{ $json.file_path }}"
   }
```

---

### C. Nodo HTTP Request (Generate Documentation)

```
HTTP Request
├─ Method: POST
├─ URL: http://localhost:5000/api/v1/generate/{{ $json.doc_type }}
├─ Authentication: None
├─ Headers:
│  └─ Content-Type: application/json
└─ Body:
   {
     "file_path": "{{ $json.file_path }}",
     "project_name": "{{ $json.project_name }}",
     "use_llm": false
   }
```

---

### D. Nodo Set (Extract Data)

```
Set
├─ Keep only set fields: OFF
└─ Fields to Set:
   ├─ documentation (string): {{ $json.content }}
   └─ timestamp (date): {{ now() }}
```

---

### E. Nodo File (Write Documentation)

```
Write to File
├─ File Path: /docs/{{ $json.project_name }}_{{ now().format('YYYY-MM-DD') }}.md
├─ Data to Write: {{ $json.documentation }}
└─ Append: OFF
```

---

## Workflows de Ejemplo

### Workflow 1: Generar README Simple

```
[Webhook] 
  ↓
[HTTP Request: /api/v1/generate/readme]
  ↓
[Write to File]
  ↓
[Email Notification]
```

**Webhook Body:**
```json
{
  "file_path": "/path/to/code.py",
  "project_name": "Mi Proyecto"
}
```

---

### Workflow 2: Análisis + Generación Completa

```
[Webhook]
  ↓
[HTTP Request: /api/v1/analyze]
  ↓
[Set: Extract Summary]
  ↓
[HTTP Request: /api/v1/generate/complete]
  ↓
[Set: Parse Response]
  ↓
[Write: README]
[Write: API Docs]
[Write: Class Docs]
  ↓
[Slack Notification]
```

---

### Workflow 3: Monitorear Repositorio y Documentar

```
[Schedule: Daily at 2 AM]
  ↓
[Git: Get Changed Files]
  ↓
[Loop Through Changed Files]
  ├─ Filter: *.py files
  ├─ HTTP Request: /api/v1/analyze
  ├─ HTTP Request: /api/v1/generate/complete
  └─ Write to File: /docs/{filename}.md
  ↓
[Commit Changes to Git]
  ↓
[Push to Repository]
```

---

## Variables y Credenciales

### 1. Variables de Entorno en n8n

Crear variables para reutilizar:

```
API_URL: http://localhost:5000
GITHUB_TOKEN: tu_token_aqui
DOC_OUTPUT_PATH: /documents
```

**Uso en nodos:**
```
{{ $env.API_URL }}/api/v1/analyze
{{ $env.DOC_OUTPUT_PATH }}/readme.md
```

---

### 2. Credenciales HTTP

```
Credentials:
├─ Name: DocGenerator API
├─ Type: Generic Credentials
├─ Headers:
│  └─ Content-Type: application/json
└─ Authentication: None
```

---

## Ejemplos de Workflows en JSON

### Ejemplo 1: Simple README Generator

```json
{
  "name": "Generate README",
  "active": true,
  "nodes": [
    {
      "displayName": "Webhook",
      "name": "webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [50, 400],
      "webhookId": "unique-id",
      "method": "POST",
      "path": "doc-generator-readme"
    },
    {
      "displayName": "HTTP Request",
      "name": "http",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [250, 400],
      "method": "POST",
      "url": "http://localhost:5000/api/v1/generate/readme",
      "sendHeaders": true,
      "headers": {
        "Content-Type": "application/json"
      },
      "bodyParametersJson": "{{ JSON.stringify({file_path: $json.file_path, project_name: $json.project_name, use_llm: false}) }}"
    },
    {
      "displayName": "Write to File",
      "name": "file",
      "type": "n8n-nodes-base.writeFile",
      "typeVersion": 1,
      "position": [450, 400],
      "filePath": "/tmp/README_{{ $json.project_name }}.md",
      "dataPropertyName": "content"
    }
  ],
  "connections": {
    "webhook": {
      "main": [[{"node": "http", "branch": 0, "type": "main"}]]
    },
    "http": {
      "main": [[{"node": "file", "branch": 0, "type": "main"}]]
    }
  }
}
```

---

### Ejemplo 2: Complete Documentation Generator

```json
{
  "name": "Generate Complete Documentation",
  "active": true,
  "nodes": [
    {
      "displayName": "Webhook",
      "name": "webhook",
      "type": "n8n-nodes-base.webhook",
      "method": "POST",
      "path": "doc-complete"
    },
    {
      "displayName": "Generate Complete",
      "name": "generate",
      "type": "n8n-nodes-base.httpRequest",
      "method": "POST",
      "url": "http://localhost:5000/api/v1/generate/complete",
      "sendHeaders": true,
      "headers": {"Content-Type": "application/json"},
      "bodyParametersJson": "{{ JSON.stringify({file_path: $json.file_path, project_name: $json.project_name, use_llm: false}) }}"
    },
    {
      "displayName": "Save README",
      "name": "saveReadme",
      "type": "n8n-nodes-base.writeFile",
      "filePath": "/tmp/{{ $json.project_name }}/README.md",
      "dataPropertyName": "{{ $json.documentation.readme }}"
    },
    {
      "displayName": "Save API Docs",
      "name": "saveApiDocs",
      "type": "n8n-nodes-base.writeFile",
      "filePath": "/tmp/{{ $json.project_name }}/API_DOCS.md",
      "dataPropertyName": "{{ $json.documentation.api_docs }}"
    }
  ],
  "connections": {
    "webhook": {
      "main": [[{"node": "generate", "branch": 0, "type": "main"}]]
    },
    "generate": {
      "main": [
        [
          {"node": "saveReadme", "branch": 0, "type": "main"},
          {"node": "saveApiDocs", "branch": 0, "type": "main"}
        ]
      ]
    }
  }
}
```

---

## Casos de Uso Reales

### Caso 1: Documentar con cada Push

```bash
# .github/workflows/doc-generator.yml (GitHub Actions)
name: Generate Documentation

on:
  push:
    branches: [main, develop]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Trigger n8n Workflow
        run: |
          curl -X POST http://n8n-server/webhook/doc-generator \
            -H "Content-Type: application/json" \
            -d '{
              "file_path": "src/main.py",
              "project_name": "MyProject",
              "doc_type": "complete"
            }'
```

---

### Caso 2: Generar Documentación bajo Demanda

```javascript
// Endpoint expuesto por n8n
POST /webhook/doc-generator
{
  "file_path": "/path/to/api.js",
  "project_name": "API Project",
  "doc_type": "api-docs"
}

// Respuesta
{
  "status": "success",
  "file_saved": "/docs/API_Project_API_DOCS.md",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### Caso 3: Documentación Multi-idioma (Futuro)

```json
{
  "file_path": "/path/to/code.py",
  "project_name": "Proyecto",
  "languages": ["es", "en"],
  "doc_type": "complete"
}
```

---

## Troubleshooting

### Error: "Connection Refused"

**Problema:** n8n no puede conectar al API

```
curl: (7) Failed to connect to localhost port 5000
```

**Solución:**
1. Verifica que el API está corriendo: `curl http://localhost:5000/health`
2. Comprueba el puerto en `api_server.py`
3. Revisa firewall si estás en red remota
4. Usa IP en lugar de localhost si es remoto

---

### Error: "File Not Found"

**Problema:** El API dice que no encuentra el archivo

```json
{
  "error": "File not found: /path/to/file.py"
}
```

**Solución:**
1. Verifica que la ruta es completa (absoluta)
2. Copia el archivo a una ubicación conocida
3. Usa el nodo `Write Binary File` de n8n antes de enviar

---

### Error: "Timeout"

**Problema:** La solicitud tarda demasiado

**Solución:**
1. Aumenta el timeout del nodo HTTP (en configuración)
2. Usa `use_llm: false` para respuestas más rápidas
3. Procesa archivos pequeños primero

---

### Error: "429 Too Many Requests"

**Problema:** Demasiadas solicitudes al LLM

**Solución:**
1. Añade un nodo `Delay` entre requests
2. Usa `use_llm: false` para no usar LLM
3. Implementa rate limiting en el workflow

---

## Monitoreo y Logging

### Agregar Logging en n8n

```
Set Node:
├─ log_message: Generated docs for {{ $json.project_name }}
├─ log_time: {{ now().toISO() }}
└─ status: success
```

---

### Alertas en Caso de Error

```
Error Handler:
├─ If error: Send to Slack
├─ Channel: #documentation
└─ Message: Failed to generate docs for {{ $json.project_name }}
```

---

## Performance Tips

1. **Cacheo**: Almacena análisis anteriores
2. **Batch**: Procesa múltiples archivos en paralelo
3. **Scheduling**: Corre documentación en horarios no pico
4. **Compression**: Comprime documentación antes de guardar

---

## Recursos Adicionales

- **API OpenAPI Spec**: `openapi.json`
- **Quick Reference**: `QUICK_REFERENCE.md`
- **Documentación Completa**: `README.md`

---

**¡Disfruta automatizando tu documentación con n8n! 🎉**
