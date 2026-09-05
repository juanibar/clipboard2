===================================================
 GESTOR DE MENSAJES RÁPIDOS (Clipboard Manager)
===================================================

Esta es una aplicación de escritorio diseñada para almacenar, organizar 
y pegar rápidamente mensajes recurrentes, respuestas prediseñadas o 
plantillas de texto en cualquier otra aplicación (como WhatsApp Web, 
Instagram, correos electrónicos, etc.).

La ventana de la aplicación se mantiene siempre al frente para 
facilitar el flujo de trabajo.

---------------------------------------------------
 REQUISITOS PREVIOS
---------------------------------------------------
1. Tener instalado Python en Windows (se recomienda versión 3.8 o superior).
   * Importante: Al instalar Python, asegurarse de marcar la casilla 
     "Add Python to PATH" o "Agregar Python al PATH".

---------------------------------------------------
 INSTALACIÓN
---------------------------------------------------
Antes de usar el programa por primera vez, es necesario instalar la librería 
que controla los atajos de teclado.

1. Abre la terminal (Símbolo del sistema o PowerShell) en esta carpeta.
2. Ejecuta el siguiente comando:
   pip install -r requirements.txt

---------------------------------------------------
 ¿CÓMO INICIAR LA APLICACIÓN?
---------------------------------------------------
Para iniciar el programa sin que se abra la molesta ventana de la consola negra:

-> Haz doble clic en el archivo "lanzador.vbs".

La aplicación se ejecutará de fondo y podrás invocarla en cualquier momento.
(Tus mensajes se guardarán automáticamente en un archivo 'mensajes_clipboard.csv').

---------------------------------------------------
 ATAJOS DE TECLADO Y USO
---------------------------------------------------
La aplicación funciona de manera global en tu computadora. Puedes estar
escribiendo en cualquier programa y utilizar estos atajos:

* Ctrl + Espacio + K : Trae la aplicación al frente instantáneamente.
* Ctrl + Espacio + P : Pega el mensaje seleccionado directamente en la 
                       aplicación que estabas usando por detrás.

Tips adicionales:
- Si estás navegando por la lista de mensajes de la aplicación, también 
  puedes simplemente presionar la tecla "Enter" o hacer "Doble Clic" sobre 
  un mensaje para pegarlo rápidamente.
- Si dejas el cursor del mouse apoyado sobre un mensaje (sin hacer clic), 
  se abrirá un cuadro emergente (tooltip) para que puedas leer el texto 
  completo en caso de que sea muy largo.