# 📚 Índice del Proyecto - Technical Documentation Generator

## 🗂️ Estructura de Archivos

```
/workspace/
├── 📋 DOCUMENTACIÓN
│   ├── README.md                  ← Documentación completa (INICIO AQUÍ)
│   ├── QUICK_REFERENCE.md         ← Referencia rápida de API
│   ├── N8N_INTEGRATION.md         ← Guía de integración n8n
│   ├── PROJECT_SUMMARY.md         ← Resumen ejecutivo
│   └── 05_enunciado.md            ← Especificación del proyecto
│
├── 🐍 CÓDIGO PYTHON (Core)
│   ├── code_analyzer.py           ← Análisis de código fuente
│   ├── doc_generator.py           ← Generación de documentación
│   ├── api_server.py              ← Servidor Flask REST API
│   ├── example_client.py          ← Cliente HTTP de prueba
│   └── example_fastapi.py         ← Código de ejemplo para pruebas
│
├── 🧪 TESTING
│   └── test_generators.py         ← Suite de tests unitarios
│
├── 🐳 DEPLOYMENT
│   ├── Dockerfile                 ← Imagen Docker
│   ├── docker-compose.yml         ← Orquestación Docker
│   └── requirements.txt           ← Dependencias Python
│
├── 📖 ESPECIFICACIONES
│   └── openapi.json               ← Especificación OpenAPI 3.0
│
└── 📄 OTROS
    └── base.py                    ← Archivo base original
    └── .env                       ← Variables de entorno (si existe)
```

---

## 📖 Guía de Lectura

### Para Comenzar Rápido (5 minutos)
1. Lee: `QUICK_REFERENCE.md` - Resumen de endpoints
2. Ejecuta: `python api_server.py`
3. Prueba: `python example_client.py`

### Para Entender el Proyecto (20 minutos)
1. Lee: `README.md` - Documentación completa
2. Revisa: `PROJECT_SUMMARY.md` - Resumen ejecutivo
3. Explora: `code_analyzer.py` y `doc_generator.py`

### Para Integrar con n8n (30 minutos)
1. Lee: `N8N_INTEGRATION.md` - Guía completa
2. Revisa: `openapi.json` - Especificación API
3. Implementa: Los workflows de ejemplo

### Para Desarrollar/Extender (1 hora)
1. Estudia: `code_analyzer.py` - Estructura de análisis
2. Estudia: `doc_generator.py` - Generación de templates
3. Estudia: `api_server.py` - Endpoints REST
4. Lee: `test_generators.py` - Casos de test

---

## 🎯 Archivos por Propósito

### Análisis de Código
```
code_analyzer.py
├─ PythonAnalyzer      (AST parsing)
├─ JavaScriptAnalyzer  (Regex parsing)
└─ CodeAnalyzer        (Coordinator)
```

### Generación de Documentación
```
doc_generator.py
├─ LLMClient           (GitHub Models)
└─ MarkdownGenerator   (Templates)
```

### API REST
```
api_server.py
├─ 10+ Endpoints
├─ Health check
├─ Análisis
├─ README generation
├─ API docs generation
├─ Class docs generation
├─ Function docs generation
└─ Complete documentation
```

### Ejemplos y Testing
```
example_fastapi.py     ← Código para analizar
example_client.py      ← Cliente HTTP
test_generators.py     ← Tests unitarios
```

### Deployment
```
Dockerfile             ← Contenedor Docker
docker-compose.yml     ← Stack Docker
requirements.txt       ← Dependencias
```

### Documentación
```
README.md              ← Guía principal
QUICK_REFERENCE.md     ← Referencia rápida
N8N_INTEGRATION.md     ← Integración n8n
PROJECT_SUMMARY.md     ← Resumen del proyecto
```

---

## 🚀 Guía de Uso Rápido

### 1. Instalar y Ejecutar

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python api_server.py

# El servidor estará en http://localhost:5000
```

### 2. Probar API

```bash
# Verificar estado
curl http://localhost:5000/health

# Analizar código
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"file_path": "./example_fastapi.py"}'

# Generar README
curl -X POST http://localhost:5000/api/v1/generate/readme \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "./example_fastapi.py",
    "project_name": "Mi Proyecto",
    "use_llm": false
  }'
```

### 3. Usar Cliente Python

```bash
python example_client.py
```

### 4. Ejecutar Tests

```bash
python test_generators.py
```

### 5. Usar con Docker

```bash
# Build
docker build -t doc-generator .

# Run
docker run -p 5000:5000 doc-generator

# Con Docker Compose
docker-compose up
```

---

## 📋 Endpoints Principales

### Análisis
- `POST /api/v1/analyze` - Analizar código fuente

### Documentación
- `POST /api/v1/generate/readme` - Generar README
- `POST /api/v1/generate/api-docs` - Generar API docs
- `POST /api/v1/generate/class-docs` - Documentación de clase
- `POST /api/v1/generate/function-docs` - Documentación de función
- `POST /api/v1/generate/complete` - Todo completo

### Sistema
- `GET /health` - Health check
- `GET /api/v1/info` - Info del API

---

## 🔑 Funcionalidades Core

### ✅ 1. Análisis de Código Fuente
- Extrae funciones, clases y módulos
- Soporta Python (.py) con AST
- Soporta JavaScript (.js) con regex
- Extrae docstrings y comentarios

### ✅ 2. Generación de README
- Descripción del proyecto
- Tecnologías detectadas
- Estructura del proyecto
- Instalación y uso
- Endpoints de API
- Licencia

### ✅ 3. Documentación de API
- Endpoints REST
- Ejemplos con curl
- Parámetros documentados
- Estructura de respuestas

### ✅ 4. Exportación a Markdown
- Markdown bien formateado
- Emojis y estructura profesional
- Bloques de código
- Listo para usar

---

## 📊 Estadísticas

| Métrica | Valor |
|---------|-------|
| Líneas de código Python | 2200+ |
| Archivos Python | 5 |
| Endpoints REST | 10+ |
| Lenguajes soportados | 2 (Python, JavaScript) |
| Archivos de documentación | 6 |
| Tests unitarios | 15+ |
| Casos de uso demostrados | 3+ |

---

## 🎯 Próximos Pasos por Rol

### Para Usuario Final
1. Lee `QUICK_REFERENCE.md`
2. Ejecuta `python api_server.py`
3. Usa `example_client.py` o curl
4. Guarda la documentación generada

### Para DevOps
1. Lee `Dockerfile` y `docker-compose.yml`
2. Build: `docker build -t doc-generator .`
3. Deploy: `docker run ...`
4. Monitorea logs

### Para Integrador (n8n)
1. Lee `N8N_INTEGRATION.md`
2. Revisa `openapi.json`
3. Configura nodos HTTP en n8n
4. Crea workflows

### Para Desarrollador
1. Estudia `code_analyzer.py`
2. Estudia `doc_generator.py`
3. Estudia `api_server.py`
4. Lee `test_generators.py`
5. Agrega nuevas funcionalidades

---

## 🔗 Referencias Rápidas

### Documentación Oficial
- `README.md` - Documentación completa
- `openapi.json` - Especificación API
- `QUICK_REFERENCE.md` - Referencia rápida

### Ejemplos
- `example_fastapi.py` - Código para probar
- `example_client.py` - Cliente HTTP
- `test_generators.py` - Tests

### Deployment
- `Dockerfile` - Contenedorización
- `docker-compose.yml` - Orquestación
- `requirements.txt` - Dependencias

### Integración
- `N8N_INTEGRATION.md` - Guía n8n

---

## 💡 Tips Útiles

1. **Sin LLM**: Usa `use_llm: false` en requests para respuestas rápidas
2. **Token GitHub**: Configura `GITHUB_TOKEN` para mejorar descripciones
3. **Batch**: Usa `/generate/complete` para documentación completa
4. **Docker**: Usa Docker para ambiente limpio
5. **Tests**: Ejecuta `test_generators.py` para validar

---

## ⚠️ Requisitos

- Python 3.8+
- Flask
- OpenAI Python SDK
- Para LLM: Token de GitHub (gratuito)

---

## 🆘 Ayuda

### Si no sabes por dónde empezar
→ Lee `README.md`

### Si necesitas referencia rápida
→ Lee `QUICK_REFERENCE.md`

### Si necesitas integrar con n8n
→ Lee `N8N_INTEGRATION.md`

### Si necesitas información técnica
→ Lee `PROJECT_SUMMARY.md`

### Si tienes errores
→ Revisa sección Troubleshooting en `QUICK_REFERENCE.md`

---

## 📞 Más Información

Toda la documentación está contenida en este workspace. 
Comienza con `README.md` para una guía completa.

---

**¡Listo para usar! 🚀**

Versión: 1.0.0 | Estado: ✅ Completo
