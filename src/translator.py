# translator.py

class BrailleTranslator:
    """Clase para traducir texto a Braille y viceversa.
    
    Esta clase permite convertir letras (mayúsculas y minúsculas), números y
    algunos carácteres acentuados, a su representación en Braille.
    """         

    def __init__(self):
        """Inicializa los mapas de traducción.
        
        Atributos:
            PMAYUS (str): Prefijo para mayúsculas en Braille.
            PNUM (str): Prefijo para números en Braille.
            map (dict): Mapa de caracteres a Braille.
            numbers (dict): Mapa de números a Braille.
            inverse (dict): Mapa inverso de Braille a caracteres.
            inverse_numbers (dict): Mapa inverso de Braille a números.
        """
        
        # Prefijos
        self.PMAYUS = "⠨" 
        self.PNUM = "⠼"

        """**Mapa principal de caracteres a Braille.**
        
        Contiene el mapeo de letras minúsculas, caracteres acentuados, 'ñ', signos de puntuación,
        y mapeos duales para desambiguación.
        """
        # Letras
        self.map = {
            "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑",
            "f": "⠋", "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚",
            "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕",
            "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞",
            "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭", "y": "⠽", "z": "⠵",

            # Acentos
            "á": "⠷",
            "é": "⠮",
            "í": "⠌",
            "ó": "⠬",
            "ú": "⠾",
            "ü": "⠳",
            # Ñ
            "ñ": "⠻",
            
            # Signos con braille iguales pero diferentes usos
            "_": "⠤",            
            "-": "⠤",
            
            "x": "⠦",
            "¨": "⠦",
                            
            "¡": "⠖",            
            "!": "⠖",       
            "+": "⠖",     
                
            "¿": "⠢",
            "?": "⠢",    
                
            # Signos comunes                                         
            ".": "⠄",
            ",": "⠂",
            ";": "⠆",
            ":": "⠒",
            "(": "⠣",
            ")": "⠜",
            "÷": "⠲",
            "=": "⠶",         
                
            # Espacio
            " ": " "
        }
        # Números: prefijo ⠼
        self.numbers = {
            "0": "⠚", "1": "⠁", "2": "⠃", "3": "⠉", "4": "⠙",
            "5": "⠑", "6": "⠋", "7": "⠛", "8": "⠓", "9": "⠊"
        }
        
        # Inversos (Braille → Texto)
        self.inverse = {v: k for k, v in self.map.items()}
        self.inverse_numbers = {v: k for k, v in self.numbers.items()}
        

    def text_to_braille(self, text):
        # Texto a Braille
        """Convierte una cadena de texto en Braille.

        La traducción maneja:
        - mayúsculas
        - minúsculas
        - números usando prefijos especiales.
        - carácteres acentuados.
        - letra ñ.
        
        Cualquier carácter no mapeado se convierte en '?'.

        Args:
        text (str): Cadena de texto a convertir.

        Returns:
            str: Cadena resultante de representación en Braille del texto.
        """   
        result = ""
        modo_numerico = False

        for ch in text:

            # 1) Dígitos → activan modo numérico
            if ch.isdigit():
                if not modo_numerico:
                    result += self.PNUM
                    modo_numerico = True
                result += self.numbers[ch]
                continue

            # 2) Comas dentro del número NO rompen modo numérico
            if modo_numerico and ch == ",":
                result += self.map[ch]
                continue

            # 3) Si aparece algo que NO es digit ni coma → cerrar modo
            if modo_numerico and not ch.isdigit():
                modo_numerico = False

            # 4) Mayúsculas
            if ch.isalpha() and ch.isupper():
                base = ch.lower()
                result += self.PMAYUS + self.map.get(base, "?")
                continue

            # 5) Resto de signos, minúsculas, acentos, espacio
            result += self.map.get(ch, "?")

        return result

    def braille_to_text(self, braille):
        """
        Traduce una cadena de caracteres Braille a texto normal (ASCII/Unicode).
        
        Características principales:
        1. Manejo de estado para MODO NUMÉRICO (detecta prefijos de número).
        2. Lógica contextual para símbolos ambiguos (Ej: '⠖' puede ser '+' o '!' o '¡').
        3. Soporte para mayúsculas (prefijo '⠨').
        4. Lookahead/Lookbehind: Analiza caracteres adyacentes para decidir el significado.
        
        Args:
            braille (str): Cadena conteniendo caracteres Unicode Braille.
            
        Returns:
            str: Texto traducido y formateado.
        """
        i = 0
        result = ""
        is_number = False

        while i < len(braille):
            ch = braille[i]
            prev = braille[i-1] if i > 0 else None
            next = braille[i+1] if i < len(braille)-1 else None    

            # A. Prefijo de Mayúscula (⠨)
            if ch == self.PMAYUS:
                if next in self.inverse:
                    letra = self.inverse.get(next, "?")
                    result += letra.upper()
                    i += 2 
                    continue
                else:
                    i += 1
                    continue

            # B. Prefijo Numérico (⠼)
            if ch == self.PNUM:
                is_number = True
                i += 1
                continue
            
            # --- PROCESAMIENTO MODO NUMÉRICO ---
            if is_number:
                # Espacio rompe el número
                if ch == " ":
                    is_number = False
                    result += " "
                    i += 1
                    continue
                
                # Dígitos válidos
                numero = self.inverse_numbers.get(ch, None)
                if numero is not None:
                    result += numero
                    i += 1
                    continue
                
                # Coma decimal
                if ch == "⠂": 
                    result += ","
                    i += 1
                    continue
                
                # Caso Especial: Signos Matemáticos (+ - x = ÷)
                # Si encontramos uno, NO rompemos el modo numérico inmediatamente aquí (pass),
                # permitimos que el flujo continúe hacia la lógica contextual más abajo
                # para que se interpreten como operaciones matemáticas y no puntuación.
                if ch in ["⠖", "⠤", "⠦", "⠶", "⠲"]:
                    pass # Dejamos que la lógica de abajo procese el signo
                else:
                    is_number = False # Cualquier otra cosa rompe el número
            
            # LÓGICA DE SIGNOS CONTEXTUALES

            # Resta (-) vs Guion bajo (_) -> Símbolo (⠤)
            if ch == "⠤":
                # Si está rodeado de números o venimos de un número, es Resta (-)
                if is_number or (self._is_number_char(prev) and self._is_number_char(next)):
                    result += "-"
                    # Nota: Mantenemos is_number en True para el siguiente digito
                else:
                    result += "_"
                    is_number = False
                i += 1
                continue

            # Multiplicación (x) vs Diéresis (¨) -> Símbolo (⠦)
            if ch == "⠦":
                # Si venimos de un número, es Multiplicación (x)
                if is_number or (self._is_number_char(prev) and self._is_number_char(next)):
                    result += "x" 
                else:
                    result += "¨"
                    is_number = False
                i += 1
                continue

            # Suma (+) vs Admiración (! ¡) -> Símbolo (⠖)
            if ch == "⠖":
                # Si venimos de un número, es Suma (+)
                if is_number or (self._is_number_char(prev) and self._is_number_char(next)):
                    result += "+"
                # Si está al principio o tras espacio -> ¡
                elif prev is None or prev == " ": 
                    result += "¡"
                    is_number = False
                # En cualquier otro caso -> !
                else: 
                    result += "!"
                    is_number = False
                i += 1
                continue

            # Interrogación (¿ ?) -> Símbolo (⠢)
            if ch == "⠢":
                if prev is None or prev == " ": # Al inicio -> ¿
                    result += "¿"
                else: # Al final -> ?
                    result += "?"
                is_number = False
                i += 1
                continue
            
            # Igual (=) -> Símbolo (⠶)
            if ch == "⠶":
                result += "="
                # El igual suele mantener el contexto matemático
                i += 1
                continue

            # División (÷) -> Símbolo (⠲)
            if ch == "⠲":
                result += "÷"
                i += 1
                continue

            # Resto de caracteres (letras, etc.)
            val = self.inverse.get(ch, "?")

            if val == "mult": val = "x" 
            
            result += val
            i += 1

        return result
      
    def _is_number_char(self, braille_char):
        """
        Helper auxiliar para verificar contexto numérico.
        Determina si el caracter braille dado es un dígito válido o el prefijo numérico.
        Utilizado para mirar atrás (prev) o adelante (next).
        """
        if braille_char is None: return False
        return braille_char in self.inverse_numbers or braille_char == self.PNUM