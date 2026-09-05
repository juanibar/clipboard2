@echo off
:: Cambia el directorio actual a la carpeta donde está este archivo
cd /d "%~dp0"

:: 1. DESCARGAR CAMBIOS (Pull antes de abrir)
git pull

:: 2. EJECUTAR LA APLICACIÓN
:: (La consola invisible se quedará esperando en este paso hasta que cierres la app)
python clipboard_app.py

:: 3. SUBIR CAMBIOS AL CERRAR LA APP
:: Agrega solo el archivo de la base de datos
git add mensajes_clipboard.csv
:: Crea un commit automático
git commit -m "Auto-sync: Actualizacion de mensajes"
:: Sube los cambios
git push