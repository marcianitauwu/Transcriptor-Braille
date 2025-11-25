# util.py

#Funciones auxiliares para validación y limpieza.
from translator import BrailleTranslator

translator = BrailleTranslator()

def clean_input(text: str) -> str:
   """Limpia una cadena de texto eliminando espacios innecesarios.

   Necesaria para preparar el texto antes de la traducción.
   
   Args:
      text (str): Cadena de texto a limpiar.

   Returns:
      str: Cadena de texto limpia.
   """
   
   # Elimina espacios
   return text.strip()

def is_valid_text(text: str) -> bool:
   """Verifica si una cadena de texto contiene solo caracteres válidos.
   
   Esta función evalúa cada carácter del texto y determina si está permitido:
   - mayúsculas
   - minúsculas
   - números usando prefijos especiales.
   - carácteres acentuados.
   - letra ñ.
    
   Args:
      text (str): Cadena de texto a validar.

   Returns:
      bool: True si el texto es válido, False en caso contrario.
   """
   if not text:
        return False
     
   for ch in text:

      # Espacios permitidos
      if ch == " ":
         continue

      # Números
      if ch.isdigit():
         continue

      # Letras o acentos
      if ch in translator.map:
         continue

      # Mayúsculas (validar minúscula en map)
      if ch.isalpha() and ch.lower() in translator.map:
         continue
      
      # Carácter no válido
      return False
   return True
# --------------------------------------------------------
def is_braille(text: str) -> bool:
    """Verifica si una cadena de texto contiene únicamente caracteres Braille válidos o espacios.

    Utiliza el rango Unicode estándar para las celdas Braille (U+2800 a U+28FF, que corresponde
    a '⠀' hasta '⣿').

    Args:
        text (str): La cadena a validar.

    Returns:
        bool: True si la cadena es Braille válido (o solo espacios), False en caso contrario.
    """
    # Verifica si todos los caracteres pertenecen al rango Braille
    if not text:
        return False

    # ⣿ es Unicode Braille, pero NO se usa en Braille literario → no se incluye.
    valid = set(translator.inverse.keys()) | \
            set(translator.inverse_numbers.keys()) | \
            {translator.PNUM, translator.PMAYUS, " "}

    for ch in text:
        if ch not in valid:
            return False

    return True