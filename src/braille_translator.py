"""Funciones para convertir entre texto y Braille.

Se usa import relativo cuando se importa como paquete (python -m src.braille_translator).
Si se ejecuta directamente como script (python braille_translator.py) hay un fallback
que carga `utils` desde la misma carpeta.
"""

try:
    # Import relativo cuando se ejecuta como paquete
    from .utils import BRAILLE_MAP, limpiar_texto
except Exception:
    # Fallback para ejecución directa desde la carpeta src/ (python braille_translator.py)
    try:
        from utils import BRAILLE_MAP, limpiar_texto
    except Exception:
        import importlib, os, sys
        sys.path.insert(0, os.path.dirname(__file__))
        utils = importlib.import_module('utils')
        BRAILLE_MAP = getattr(utils, 'BRAILLE_MAP')
        limpiar_texto = getattr(utils, 'limpiar_texto')

def texto_a_braille(texto: str) -> str:
    """Convierte texto en español a Braille."""
    texto = limpiar_texto(texto)
    return ''.join(BRAILLE_MAP.get(ch, '?') for ch in texto)

def braille_a_texto(braille: str) -> str:
    """Convierte texto Braille a caracteres normales."""
    inverso = {v: k for k, v in BRAILLE_MAP.items()}
    return ''.join(inverso.get(ch, '?') for ch in braille)
