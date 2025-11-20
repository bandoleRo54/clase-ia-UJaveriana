# 📚 Generador de Documentación Técnica

**Integrantes:**

- Juan Esteban Becerra
- Mateo Ramirez
- Alejandro Sarmiento

---

## 🎯 Objetivo

Crear un sistema automatizado que genere documentación técnica profesional a partir de código fuente, especificaciones o comentarios, produciendo README files, API docs y manuales de usuario en formato Markdown estructurado.

---

## 📝 Descripción

Esta plataforma analiza código fuente (Python/JavaScript), extrae información semántica, funcional y estructural, y genera automáticamente documentación técnica completa, bien formateada y útil para desarrolladores, incluyendo ejemplos de uso, API references y guías de instalación.

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **Flask**
- **OpenAI API (GitHub Models)**
- **AST** (análisis Python)
- **Regex** (análisis JavaScript)
- **n8n** (orquestación de flujos)
- **Docker** (opcional para n8n)

---

## ⚙️ Funcionalidades

- Análisis de código fuente para extraer funciones, clases y módulos.
- Generación de README con secciones estándar.
- Documentación de API con endpoints y parámetros.
- Exportación a Markdown bien formateado.

---

## 🚦 Guía de Uso

### 1. Iniciar n8n

Ejecuta el siguiente archivo por doble clic o desde terminal:

```bat
n8n-simple.bat
```

Esto levantará el servicio de n8n en tu máquina.

---

### 2. Preparar y levantar el servidor Python (Flask)

1. **Ejecuta el setup para dependencias:**

   ```bat
   setup.bat
   ```

2. **Define el token de GitHub Models en la terminal CMD:**

   ```cmd
   set GITHUB_TOKEN=tu_token_aqui
   ```

3. **Inicia el servidor Flask:**
   ```cmd
   python api_server.py
   ```

---

### 3. Endpoints del servidor Python (`api_server.py`)

- **GET `/health`**  
  Chequeo de estado del servicio.

  ```json
  {
    "status": "healthy",
    "service": "Technical Documentation Generator",
    "version": "1.0.0",
    "supported_formats": [".py", ".js"]
  }
  ```

- **POST `/chat`**  
  Genera documentación Markdown usando IA.

  - **Body:**
    ```json
    { "message": "Texto o prompt a documentar" }
    ```
  - **Respuesta:**
    ```json
    { "response": "Markdown generado por la IA" }
    ```

- **GET `/token`**  
  (Temporal, solo para depuración) Muestra el token actual usado.

---

### 4. Cargar, modificar y ejecutar el workflow en n8n

1. **Accede a n8n en tu navegador:**  
   La URL depende de tu IP local.  
   Ejemplo:

   ```
   http://<TU_IP_LOCAL>:5678/
   ```

   ![Verifica la IP en la barra de direcciones](URL.png)

2. **Carga el workflow:**

   - Haz clic en "Importar" y selecciona el archivo `workflow.json`.

3. **Modifica la IP del servidor Flask en el nodo HTTP Request:**

   - Edita el nodo HTTP Request y cambia la URL a la IP de tu máquina donde corre Flask, por ejemplo:
     ```
     http://192.168.1.25:5000/chat
     ```
   - Guarda los cambios.

4. **Ejecuta el workflow:**

   - Haz clic en "Ejecutar workflow" en n8n.
   - El flujo analizará archivos `.py`, generará el prompt, enviará la petición al servidor Flask y guardará el Markdown generado.

   ![Vista del workflow en n8n](WORKFLOW.png)

---

## 🏗️ Arquitectura y Flujo

```
Código Fuente (.py/.js)
         ↓
    [n8n Workflow]
         ↓
  ┌─────────────┐
  │ Análisis    │
  │ Generación  │
  │ Markdown    │
  └─────────────┘
         ↓
  [Servidor Flask + GitHub Models]
         ↓
   Markdown Output
```

---

## 💡 Notas

- Cambia la IP en el nodo HTTP Request de n8n según la IP de tu máquina.
- El endpoint `/token` es solo para depuración y debe eliminarse en producción.
- Si usas `.env`, asegúrate de que el token esté actualizado antes de iniciar el servidor.

---

## 📧 Contacto

Para dudas o soporte, contactar a cualquiera de los integrantes del equipo.

---
