"""Aplicación de consola para transcribir texto en español a Braille

Este módulo permite al usuario ingresar texto, validarlo mediante funciones
auxiliares y convertirlo a Braille utilizando la clase `BrailleTranslator`.
El programa opera en un ciclo interactivo hasta que el usuario escriba 'SALIR'.  

Incluye:
- Limpieza de texto de entrada.
- Validación de caracteres permitidos.
- Traducción a Braille. 
"""

import sys
from translator import BrailleTranslator
from util import clean_input, is_valid_text

def main():
   
   """
   Ejecuta el programa interactivo de consola para traducir texto a Braille.

   El flujo del programa es:
   1. Mostrar instrucciones iniciales.
   2. Recibir entrada del usuario.
   3. Finalizar si se ingresa 'SALIR'.
   4. Limpiar y validar la entrada.
   5. Convertir la entrada validada a Braille.
   6. Mostrar el resultado y continuar.

   Solo se aceptan caracteres definidos como válidos en `is_valid_text`.
   En caso de detectar un carácter prohibido, se muestra un mensaje de error
   y se solicita nuevamente la entrada.
   """
   translator = BrailleTranslator()
    
   print("   PRUEBA DE CONSOLA - TRANSCRIPTOR (Texto a Braille)")
   print("========================================")
   print("Escribe 'SALIR' para terminar.")
    
   while True:
      entrada = input("Ingresa texto o números (Español): ")
       
      # Salir del programa 
      if entrada.strip().upper() == "SALIR":
         break
            
      # 1. Validar y Limpiar
      texto_limpio = clean_input(entrada)
        
      if not is_valid_text(texto_limpio):
         print("Error: Caracteres no válidos detectados.")
         continue
            
      # 2. Traducir a Braille
      resultado_braille = translator.text_to_braille(texto_limpio)
      print(f"Braille: {resultado_braille}")
        
if __name__ == "__main__":
   main()