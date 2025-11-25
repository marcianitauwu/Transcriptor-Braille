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
            
            "¨": "⠶",
            "=": "⠶",            
                            
            "¡": "⠖",            
            "!": "⠖",       
            "+": "⠖",     
                
            "¿": "⠢",
            "?": "⠢",    
                
            # Signos comunes                                         
            ".": "⠲",
            ",": "⠂",
            ";": "⠆",
            ":": "⠒",
            "(": "⠣",
            ")": "⠜",
            "x": "⠦",
            "÷": "⠲",
            
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
        def text_to_braille(self, text):
            result = ""
            modo_numerico = False

            for ch in text:

                # 1) Manejo de dígitos
                if ch.isdigit():
                    if not modo_numerico:
                        result += self.PNUM  # activa modo numérico con ⠼
                        modo_numerico = True
                    result += self.numbers[ch]
                    continue
                
                # 2) Si aparece algo NO numérico, se apaga el modo
                if modo_numerico and not ch.isdigit():
                    modo_numerico = False

                # 3) Manejo de mayúsculas
                if ch.isalpha() and ch.isupper():
                    base = ch.lower()
                    result += self.PMAYUS + self.map.get(base, "?")
                    continue

                # 4) Letras, acentos, signos, espacio
                result += self.map.get(ch, "?")

            return result

    # Braille a texto
    def braille_to_text(self, braille):
        """Convierte una cadena en Braille a su representación en texto.
        
        Realiza la traducción Braille a texto, manejando:
        - Prefijos de mayúsculas (⠨) y números (⠼).
        - Desambiguación de signos con el mismo Braille, como "¿" / "?", "¡" / "!" / "+",
          "-" / "_", y "=" / "¨", basándose en su contexto (carácter previo y siguiente).
        
        Args:
            braille (str): Cadena de Braille a convertir.

        Returns:
            str: Cadena de texto resultante. Caracteres Braille no mapeados se convierten en '?'.
        """

        i = 0
        result = ""
        is_number = False

        while i < len(braille):

            ch = braille[i]
            prev = braille[i-1] if i > 0 else None
            next = braille[i+1] if i < len(braille)-1 else None   

            # Mayúscula
            if ch == self.PMAYUS:
                letra = self.inverse.get(braille[i+1], "?")
                result += letra.upper()
                i += 2
                continue

            # Números
            if ch == self.PNUM:
                is_number = True
                i += 1
                continue
            
            if is_number:
                # Si es un símbolo numérico válido
                if ch in self.inverse_numbers:
                    result += self.inverse_numbers[ch]
                    i += 1
                    continue
                
                # Si NO es número → se apaga modo numérico
                is_number = False
                # Y se procesa como letra/signo normal (NO continue)

            
            # Signo 1 "¿"
            if ch == "⠢":
                if prev is None: # Al inico
                    result += "¿"
                elif next is None: # Al final
                    result += "?"
                elif prev == " ":
                    result += "¿"
                elif next == " ":
                    result += "?"
                else:
                    result += "?"
                i += 1
                continue
            
            # Signo 2 "¡"
            if ch == "⠖":
                if prev is None: # Al inicio
                    result += "¡"
                elif prev == " ":
                    result += "¡"
                elif next == " ":
                    result += "!"
                elif next is None: # Al final
                    result += "!"
                elif (self._is_number(prev) and next == self.PNUM): # Entre números
                    result += "+"
                elif self._is_number(prev) and self._is_number(next): # Entre números
                    result += "+"
                else:
                    result += "!"
                i += 1
                continue
            
            # Signo 3 "-" y "_"
            if ch == "⠤":
                if self._is_number(prev) and self._is_number(next):   # Entre números
                    result += "-"
                else: # Si está al inicio, al fin o entre letras
                    result += "_"
                i += 1
                continue
            
            # Signo 4 "=" y "¨"
            if ch == "⠶":
                # Entre números
                if self._is_number(prev) and self._is_number(next):   # Entre números
                    result += "=" 
                # Entre letras
                elif self._is_letter(prev) and self._is_letter(next):   # Entre letras
                    result += "¨"
                elif prev is None or next is None: 
                    result += "¨"
                # Si está al inicio o al finl
                else:
                    result += "¨"
                i += 1
                continue

            # Letras, signos comunes, acentos, Ñ, Ü
            result += self.inverse.get(ch, "?")
            i += 1

        return result
        
    def _is_number(self, braille_char):
        """Verifica si un carácter Braille dado corresponde a un número (celda Braille de 1 a 0 sin el prefijo ⠼).
        
        Args:
            braille_char (str): Carácter Braille a evaluar.
        
        Returns:
            bool: True si el carácter es un Braille de número, False en caso contrario.
        """
        return braille_char in self.inverse_numbers
    
    def _is_letter(self, braille_char):
        """Verifica si un carácter Braille dado corresponde a una letra (minúscula, con o sin acento, o 'ñ').
        
        Excluye prefijos y signos de puntuación, centrándose solo en caracteres alfabéticos.

        Args:
            braille_char (str or None): Carácter Braille a evaluar o None.
        
        Returns:
            bool: True si el carácter es un Braille de letra, False en caso contrario o si es None.
        """
        if braille_char is None:
            return False
        decoded = self.inverse.get(braille_char)
        return decoded is not None and decoded.isalpha()