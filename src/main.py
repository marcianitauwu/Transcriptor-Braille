"""Módulo principal para iniciar la aplicación Transcriptor-Braille.

Este módulo crea y arranca la interfaz gráfica BrailleApp definida en el
módulo gui. Provee una entrada clara para ejecutar la aplicación desde la
línea de comandos.

Uso:
  python src/main.py

Requisitos:
- El módulo 'gui' debe definir la clase BrailleApp.
- BrailleApp debe ser una aplicación basada en tkinter (o compatible) con un
  método mainloop() para iniciar el bucle de la interfaz.
"""

# main.py
from gui import BrailleApp

if __name__ == "__main__":
   app = BrailleApp()
   app.mainloop()
