import pytest
from src.translator import BrailleTranslator

def test_text_to_braille():
    translator = BrailleTranslator()
    result = translator.text_to_braille("Hola")
    assert result == "⠨⠓⠕⠇⠁", "La conversión de texto a Braille falló"

def test_braille_to_text():
    translator = BrailleTranslator()
    result = translator.braille_to_text("⠨⠓⠕⠇⠁")
    assert result == "Hola", "La conversión de Braille a texto falló"