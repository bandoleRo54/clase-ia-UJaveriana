
# 📚 Ejercicio 5: Generador de Documentación Técnica

## 🎯 **Objetivo**
Crear un sistema automatizado que genere documentación técnica profesional a partir de código fuente, especificaciones o comentarios, produciendo README files, API docs y manuales de usuario en formato Markdown estructurado.

## 📝 **Descripción Detallada**
Desarrollar una plataforma que analice código fuente, extraiga información semántica, funcional y estructural, y genere automáticamente documentación técnica completa, bien formateada y útil para desarrolladores, incluyendo ejemplos de uso, API references y guías de instalación.

## 🛠️ **Tecnologías Requeridas**
- **Docker** - Contenedorización del sistema generador
- **n8n** - Orquestación del flujo de análisis y generación
- **GitHub Models** - IA para análisis de código y generación de texto
- **Formateo automático** - Generación de Markdown estructurado y exportación

## ⚙️ **Funcionalidades Esperadas**

### **Core (Obligatorias)**
- [ ] **Análisis de código fuente** para extraer funciones, clases y módulos
- [ ] **Generación de README** con secciones estándar
- [ ] **Documentación de API** con endpoints y parámetros
- [ ] **Exportación a Markdown** bien formateado

### **Avanzadas (Opcionales)**
- [ ] **Generación de diagramas** automáticos (arquitectura, flujo)
- [ ] **Ejemplos de código** funcionales generados por IA
- [ ] **Múltiples formatos** de salida (HTML, PDF, GitBook)
- [ ] **Documentación multi-idioma** (español, inglés)

## 📊 **Casos de Uso Ejemplo**

### **Caso 1: API REST Documentation**

#### Caso 1 - Input:
```python
# Código Input - FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users/")
async def create_user(user: User):
    """Crea un nuevo usuario en el sistema"""
    if user.age < 18:
        raise HTTPException(status_code=400, detail="Usuario menor de edad")
    return {"message": "Usuario creado", "user_id": 123}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Obtiene información de un usuario específico"""
    return {"user_id": user_id, "name": "Juan Pérez"}
```

#### Caso 1 - Output:

# 📡 API Documentation

## 🚀 Endpoints

### POST /users/
Crea un nuevo usuario en el sistema.

**Request Body:**
```json
{
  "name": "string",
  "email": "string", 
  "age": "integer"
}
```

**Response:**
```json
{
  "message": "Usuario creado",
  "user_id": 123
}
```

**Validaciones:**
- `age`: Debe ser mayor o igual a 18
- `email`: Formato de email válido

**Ejemplo de uso:**
```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Ana García", "email": "ana@email.com", "age": 25}'
```

### GET /users/{user_id}
Obtiene información de un usuario específico.

**Parámetros:**
- `user_id` (integer): ID único del usuario

**Response:**
```json
{
  "user_id": 123,
  "name": "Juan Pérez"
}
```

---

### **Caso 2: README Generation**

#### Caso 2 - Input:
```javascript
// Código Input - Node.js Project
const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

// Database connection
mongoose.connect('mongodb://localhost:27017/myapp');

// User model
const userSchema = new mongoose.Schema({
  username: String,
  password: String,
  createdAt: { type: Date, default: Date.now }
});

// Express app
const app = express();
app.use(express.json());

// Authentication endpoint
app.post('/auth/login', async (req, res) => {
  // Login logic here
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

#### Caso 2 - Output:

# 🚀 MyApp - Sistema de Autenticación

## 📋 Descripción
Sistema de autenticación construido con Node.js, Express y MongoDB que proporciona registro y login de usuarios con encriptación segura de contraseñas.

## 🛠️ Tecnologías Utilizadas
- **Node.js** - Runtime de JavaScript
- **Express** - Framework web
- **MongoDB** - Base de datos NoSQL
- **Mongoose** - ODM para MongoDB
- **bcrypt** - Encriptación de contraseñas

## ⚡ Instalación Rápida

### Prerrequisitos
- Node.js >= 14.0.0
- MongoDB >= 4.0
- npm o yarn

### Pasos de Instalación
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/myapp.git
cd myapp

# 2. Instalar dependencias
npm install

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 4. Iniciar MongoDB
mongod

# 5. Iniciar la aplicación
npm start
```

## 🌐 API Endpoints

### Autenticación
- `POST /auth/login` - Iniciar sesión

## 📁 Estructura del Proyecto
```
myapp/
├── models/
│   └── User.js
├── routes/
│   └── auth.js
├── middleware/
├── config/
└── server.js
```

## 🧪 Testing
```bash
npm test
```

## 📄 Licencia
MIT License

---

### **Caso 3: Class Documentation**

#### Caso 3 - Input:
```python
# Código Input - Python Class
class DatabaseManager:
    """Maneja conexiones y operaciones de base de datos"""
    
    def __init__(self, connection_string):
        """
        Inicializa el manager de base de datos
        
        Args:
            connection_string (str): String de conexión a la BD
        """
        self.connection = connection_string
        self.is_connected = False
    
    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            # Lógica de conexión
            self.is_connected = True
            return True
        except Exception as e:
            raise ConnectionError(f"Error conectando: {e}")
    
    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta SQL
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple, optional): Parámetros para la consulta
            
        Returns:
            list: Resultados de la consulta
            
        Raises:
            DatabaseError: Si hay error en la consulta
        """
        if not self.is_connected:
            raise ConnectionError("Base de datos no conectada")
        
        # Ejecutar consulta
        return []
```

#### Caso 3 - Output:

# 🗄️ DatabaseManager

## 📝 Descripción
Clase para manejar conexiones y operaciones de base de datos de manera segura y eficiente.

## 🏗️ Constructor

### `__init__(connection_string)`
Inicializa el manager de base de datos.

**Parámetros:**
- `connection_string` (str): String de conexión a la base de datos

**Ejemplo:**
```python
db = DatabaseManager("postgresql://user:pass@localhost:5432/mydb")
```

## 📖 Métodos

### `connect()`
Establece conexión con la base de datos.

**Returns:**
- `bool`: True si la conexión es exitosa

**Excepciones:**
- `ConnectionError`: Si no se puede establecer la conexión

**Ejemplo:**
```python
try:
    db.connect()
    print("Conectado exitosamente")
except ConnectionError as e:
    print(f"Error: {e}")
```

### `execute_query(query, params=None)`
Ejecuta una consulta SQL en la base de datos conectada.

**Parámetros:**
- `query` (str): Consulta SQL a ejecutar
- `params` (tuple, optional): Parámetros para queries parametrizadas

**Returns:**
- `list`: Lista con los resultados de la consulta

**Excepciones:**
- `ConnectionError`: Si la base de datos no está conectada
- `DatabaseError`: Si hay un error en la ejecución de la consulta

**Ejemplo:**
```python
# Query simple
results = db.execute_query("SELECT * FROM users")

# Query con parámetros
user = db.execute_query(
    "SELECT * FROM users WHERE id = %s", 
    (user_id,)
)
```

## ⚠️ Consideraciones
- Asegúrate de llamar `connect()` antes de ejecutar consultas
- Usa parámetros para evitar inyecciones SQL
- Maneja las excepciones apropiadamente

---

## 🏗️ **Arquitectura Sugerida**

```
Code Input → [AST Analysis] → [Comment Extraction] → [AI Processing] → [Template Engine] → [Markdown Generation] → [Format & Export]
```

### **Flujo Detallado:**
1. **Code Analysis**: Parsear código y extraer estructura (clases, funciones, módulos)
2. **Comment Extraction**: Extraer docstrings, comentarios y anotaciones
3. **Type Analysis**: Analizar tipos de datos, parámetros y returns
4. **AI Enhancement**: IA genera descripciones, ejemplos y mejoras
5. **Template Processing**: Aplicar templates por tipo de documentación
6. **Markdown Generation**: Generar Markdown bien estructurado
7. **Export**: Múltiples formatos de salida y distribución

## 🎯 **Criterios de Evaluación Específicos**

### **Funcionamiento (40 pts)**
- [ ] Genera documentación completa y útil
- [ ] Markdown está bien formateado y estructurado
- [ ] Ejemplos de código son funcionales y relevantes
- [ ] Maneja múltiples lenguajes de programación

### **Integración Técnica (20 pts)**
- [ ] Parser de código robusto para diferentes sintaxis
- [ ] Templates flexibles y configurables
- [ ] Pipeline de procesamiento eficiente
- [ ] Exportación a múltiples formatos

### **Calidad (15 pts)**
- [ ] Documentación es clara y profesional
- [ ] Ejemplos son prácticos y educativos
- [ ] Estructura lógica y navegación intuitiva
- [ ] Consistencia en formato y estilo

## 📚 **Entregables Específicos**

### **Código**
- Parser multi-lenguaje para código fuente
- Engine de templates para diferentes tipos de docs
- Generador de ejemplos automáticos
- Exportador a múltiples formatos

### **Documentación**
- Guía de templates disponibles
- Configuración de estilos de documentación
- Ejemplos de documentación generada
- Manual de personalización

### **Demo**
- Documentar proyecto completo en vivo
- Mostrar diferentes tipos de documentación
- Demostrar personalización de templates
- Exportar a múltiples formatos

## 💡 **Tips de Implementación**

### **Primeros Pasos**
1. Comienza con un lenguaje (Python es ideal por docstrings)
2. Implementa parser básico de funciones y clases
3. Crea templates simples de Markdown
4. Agrega gradualmente más funcionalidades

### **Parsers Sugeridos**
```python
# Python - AST parsing
import ast
import inspect

def parse_python_file(file_path):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())
    
    functions = []
    classes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                'name': node.name,
                'args': [arg.arg for arg in node.args.args],
                'docstring': ast.get_docstring(node),
                'line_number': node.lineno
            })
        elif isinstance(node, ast.ClassDef):
            classes.append({
                'name': node.name,
                'docstring': ast.get_docstring(node),
                'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            })
    
    return {'functions': functions, 'classes': classes}
```

### **Templates Sugeridos**
```yaml
templates:
  readme:
    sections:
      - title
      - description
      - installation
      - usage
      - api_reference
      - contributing
      - license
  
  api_docs:
    format: openapi_style
    sections:
      - endpoints
      - request_response
      - examples
      - error_codes
  
  class_docs:
    sections:
      - overview
      - constructor
      - methods
      - properties
      - examples
```

## 🔗 **Recursos Útiles**

- **AST Parsing**: https://docs.python.org/3/library/ast.html
- **JavaScript Parser**: https://esprima.org/
- **Markdown Generation**: https://python-markdown.github.io/
- **Template Engine**: https://jinja.palletsprojects.com/

## 🏆 **Criterios de Excelencia**

Para obtener la máxima puntuación, considera implementar:
- **Diagram Generation**: Generar diagramas UML, flujo, arquitectura automáticamente
- **Interactive Examples**: Ejemplos ejecutables en la documentación
- **Version Tracking**: Comparar cambios entre versiones de documentación
- **Integration Testing**: Verificar que ejemplos de código funcionen
- **Custom Themes**: Múltiples temas visuales para la documentación
- **Git Integration**: Actualización automática con commits

## 📊 **Tipos de Documentación Soportados**

### **README.md**
- Descripción del proyecto
- Instalación y configuración
- Ejemplos de uso básico
- Estructura del proyecto
- Contribución y licencia

### **API Documentation**
- Endpoints disponibles
- Parámetros y tipos
- Ejemplos de request/response
- Códigos de error
- Rate limiting

### **Code Documentation**
- Documentación de clases
- Métodos y funciones
- Parámetros y returns
- Excepciones posibles
- Ejemplos de uso

### **User Guide**
- Tutorial paso a paso
- Casos de uso comunes
- Troubleshooting
- FAQ
- Best practices

---
