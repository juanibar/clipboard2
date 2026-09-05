Set WshShell = CreateObject("WScript.Shell")
' Ejecuta el archivo iniciar.bat de forma completamente oculta (0)
WshShell.Run chr(34) & "iniciar.bat" & Chr(34), 0
Set WshShell = Nothing