@echo off
REM ------------------------------------------------------------------------------
REM n8n-simple.bat - Versión para Windows (cmd.exe) del script n8n-simple.sh
REM Coloca este archivo en la carpeta n8n y ejecútalo desde ahí:
REM   n8n-simple.bat start|stop|restart|fix|logs|status|clean|ngrok <url>
REM ------------------------------------------------------------------------------

setlocal enabledelayedexpansion

if "%~1"=="" goto help

if /I "%~1"=="start" goto start
if /I "%~1"=="fix" goto fix
if /I "%~1"=="stop" goto stop
if /I "%~1"=="restart" goto restart
if /I "%~1"=="logs" goto logs
if /I "%~1"=="status" goto status
if /I "%~1"=="clean" goto clean
if /I "%~1"=="ngrok" goto ngrok

:help
echo n8n - Script simple (Windows)
echo Uso: n8n-simple.bat start^|stop^|restart^|fix^|logs^|status^|clean^|ngrok ^<url^
goto :eof

:start
echo 🚀 Iniciando n8n...

if not "%~2"=="" (
  set NGROK_URL=%~2
  echo 🌐 Configurando URL de ngrok: %NGROK_URL%
) else (
  if defined NGROK_URL (
    echo 🌐 Usando NGROK_URL desde variable de entorno: %NGROK_URL%
  ) else (
    echo 💡 Usando URL local. Para ngrok: n8n-simple.bat start https://tu-ngrok.url
  )
)

echo 📁 Preparando directorios...
if not exist .\n8n_data mkdir .\n8n_data

REM Ajustar permisos en Windows (dar control total al usuario actual)
icacls .\n8n_data /grant "%USERNAME%":(OI)(CI)F /T >nul 2>&1 || echo ℹ️ No se pudo ajustar permisos con icacls, continua...

echo 🐳 Iniciando servicios con docker-compose ...
docker-compose up -d

echo ⏳ Esperando que los servicios estén listos...
timeout /t 15 /nobreak >nul

REM Comprobar si n8n está arriba
docker-compose ps n8n | findstr /I "Up" >nul
if %errorlevel%==0 (
  echo ✅ n8n iniciado exitosamente!
  if defined NGROK_URL (
    echo 📍 Accede a n8n en: %NGROK_URL%
  ) else (
    echo 📍 Accede a n8n en: http://localhost:5678
  )
  echo 👤 Usuario: admin
  echo 🔑 Contraseña: admin123
) else (
  echo ❌ Error iniciando n8n. Ver logs: n8n-simple.bat logs
)
goto :eof

:fix
echo 🔧 Arreglando problemas comunes...
echo 🛑 Deteniendo servicios...
docker-compose down

echo 📁 Arreglando permisos...
if not exist .\n8n_data mkdir .\n8n_data
icacls .\n8n_data /grant "%USERNAME%":(OI)(CI)F /T >nul 2>&1 || echo ℹ️ icacls fallo

echo 🚀 Reiniciando servicios...
docker-compose up -d
timeout /t 15 /nobreak >nul
goto status

:stop
echo 🛑 Deteniendo n8n...
docker-compose down
echo ✅ n8n detenido!
goto :eof

:restart
echo 🔄 Reiniciando n8n...
docker-compose down
docker-compose up -d
echo ✅ n8n reiniciado!
goto :eof

:logs
if "%~2"=="" (
  echo 📋 Mostrando logs de todos los servicios (Ctrl+C para salir)...
  docker-compose logs -f
) else (
  echo 📋 Mostrando logs de %~2 (Ctrl+C para salir)...
  docker-compose logs -f %~2
)
goto :eof

:status
echo 📊 Estado de servicios:
docker-compose ps
echo.
echo 🌐 URLs disponibles:
echo    Local: http://localhost:5678
echo.
echo 👤 Credenciales: admin / admin123
goto :eof

:clean
echo ⚠️  Esto eliminará todos los workflows y configuraciones de n8n
choice /M "¿Continuar?"
if errorlevel 2 (
  echo ❌ Cancelado
  goto :eof
)

docker-compose down -v
if exist .\n8n_data (
  rmdir /s /q .\n8n_data
  echo ✅ Datos eliminados
) else (
  echo ℹ️ No habia carpeta n8n_data
)
goto :eof

:ngrok
if "%~2"=="" (
  echo ❌ Falta la URL de ngrok. Uso: n8n-simple.bat ngrok https://mi-ngrok.url
  goto :eof
)

set NGROK_URL=%~2
echo 🌐 Configurando n8n con ngrok: %NGROK_URL%

echo 🔄 Reiniciando n8n con la nueva URL...
docker-compose down
docker-compose up -d
timeout /t 15 /nobreak >nul
docker-compose ps n8n | findstr /I "Up" >nul
if %errorlevel%==0 (
  echo ✅ n8n configurado con ngrok!
  echo 🌐 Acceso web: %NGROK_URL%
) else (
  echo ❌ Error configurando n8n. Ver logs: n8n-simple.bat logs
)
goto :eof
