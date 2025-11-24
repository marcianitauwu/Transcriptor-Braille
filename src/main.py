"""Aplicación de consola para transcribir texto en español a Braille y viceversa.

Este módulo permite al usuario interactuar con la clase BrailleTranslator.
Soporta dos modos de operación:
1. Traducción de Español a Braille.
2. Traducción de Braille a Español.

"""

import sys
from translator import BrailleTranslator
from util import clean_input, is_valid_text, is_braille

def main():
    """Ejecuta el ciclo interactivo de pruebas.
    Permite seleccionar el modo de traducción y validar las entradas correspondientes.
    
    Flujo:
    1. Inicializa BrailleTranslator.
    2. Entra en un bucle interactivo que presenta un menú.
    3. Gestiona la entrada del usuario para seleccionar el modo (Español->Braille o Braille->Español).
    4. Realiza la validación de entrada antes de la traducción.
    """
    translator = BrailleTranslator()
    
    print("========================================")
    print("     TRANSCRIPTOR BRAILLE - PRUEBA")
    print("========================================")
    
    while True:
        print("\n--- MENÚ ---")
        print("1. Español ➜ Braille")
        print("2. Braille ➜ Español")
        print("Q. Salir")
        
        opcion = input("Selecciona una opción: ").strip().upper()
        
        # Salir del programa
        if opcion == "Q" or opcion == "SALIR":
            print("Saliendo...")
            break
            
        # Texto a Braille
        if opcion == "1":
            entrada = input("\nIngresa texto (Español): ")
            texto_limpio = clean_input(entrada)
                
            if not is_valid_text(texto_limpio):
                print("Error: Caracteres no válidos detectados.")
                continue
                    
            resultado = translator.text_to_braille(texto_limpio)
            print(f"Resultado Braille: {resultado}")

        # Braille a texto
        elif opcion == "2":
            entrada = input("\nIngresa texto (Braille): ")
            texto_limpio = clean_input(entrada)
                
            # Validamos que sea Braille
            if not is_braille(texto_limpio):
                print("Error: La entrada contiene caracteres que no son Braille.")
                continue
                    
            resultado = translator.braille_to_text(texto_limpio)
            print(f"Resultado Español: {resultado}")
                
        else:
            print("Opción no reconocida, intenta de nuevo.")

if __name__ == "__main__":
    """Punto de entrada del script.
    
    Ejecuta la función principal 'main()' si el script se corre directamente.
    """
    main()