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
            ".": "⠄",
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