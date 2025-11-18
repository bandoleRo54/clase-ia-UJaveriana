@echo off
REM ----------------------------------------------------------------------------
REM setup.bat - Helper para Windows (cmd.exe) que replica lo esencial de setup.sh
REM Ubicación: %~dp0 (debería estar en la carpeta src)
REM Uso: doble clic o ejecutar desde cmd: setup.bat
REM ----------------------------------------------------------------------------

echo.
echo ===============================
echo  Technical Documentation Generator - Setup (Windows)
echo ===============================
echo.

REM Comprobar Python
where python >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python no encontrado en PATH. Instala Python 3.8+ y vuelve a intentarlo.
  exit /b 1
)
python --version

REM Crear virtualenv
if not exist .venv (
  echo Creando virtualenv en .venv ...
  python -m venv .venv
) else (
  echo Virtualenv .venv ya existe
)

REM Activar virtualenv
call .venv\Scripts\activate.bat
if errorlevel 1 (
  echo ERROR: No se pudo activar el virtualenv. Comprueba que .venv\Scripts\activate.bat existe.
)

REM Instalar dependencias (requirements.txt debe estar en la misma carpeta src)
if exist requirements.txt (
  echo Instalando dependencias desde requirements.txt ...
  pip install -r requirements.txt
) else (
  echo WARNING: requirements.txt no encontrado en %CD%
)

REM Validación rápida de imports
echo.
echo Ejecutando validacion rapida de dependencias (Flask, OpenAI SDK)...
python -c "import sys
try:
    from flask import Flask
    print('✅ Flask importado correctamente')
    try:
        from openai import OpenAI
        print('✅ OpenAI SDK importado correctamente')
    except Exception as e:
        print('⚠️ OpenAI SDK no disponible o error al importar:', e)
except Exception as e:
    print('❌ Error importando dependencias:', e)
    sys.exit(1)"

echo.
echo ----------------------------------
echo Quick Start (Windows)
echo ----------------------------------
echo 1) Activar el virtualenv:   .venv\Scripts\activate.bat
echo 2) Ejecutar el servidor:    python api_server.py (desde la carpeta src)
echo 3) Test rapido:             curl http://localhost:5000/health
echo 4) Levantar n8n (si usas Docker): cd ..\n8n && docker-compose up -d
echo.
pause
