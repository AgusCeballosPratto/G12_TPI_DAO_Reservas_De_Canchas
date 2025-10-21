@echo off
echo Instalando dependencias para el Sistema de Reservas de Canchas...
echo.

rem Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

rem Instalar dependencias
echo Instalando dependencias desde requirements.txt...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ¡Instalación completada exitosamente!
    echo Ahora puede ejecutar la aplicación con: python app_gui.py
) else (
    echo.
    echo Error durante la instalación. Verifique su conexión a internet.
)

echo.
pause