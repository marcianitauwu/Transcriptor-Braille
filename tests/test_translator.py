import pytest
from src.translator import BrailleTranslator

@pytest.fixture
def translator():
    return BrailleTranslator()

def test_text_to_braille_texto(translator):

    # Casos básicos
    assert translator.text_to_braille("Hola") == "⠨⠓⠕⠇⠁"
    assert translator.text_to_braille("hola") == "⠓⠕⠇⠁"
    assert translator.text_to_braille("Z") == "⠨⠵"
    assert translator.text_to_braille("ñ") == "⠻"
    assert translator.text_to_braille("Ñ") == "⠨⠻"


def test_text_to_braille_numeros(translator):

    assert translator.text_to_braille("123") == "⠼⠁⠃⠉"
    assert translator.text_to_braille("1,2,3") == "⠼⠁⠂⠃⠂⠉"
    assert translator.text_to_braille("1 2 3") == "⠼⠁ ⠼⠃ ⠼⠉"
    assert translator.text_to_braille("1, 2, 3") == "⠼⠁⠂ ⠼⠃⠂ ⠼⠉"
    assert translator.text_to_braille("12a") == "⠼⠁⠃⠁"
    # Signos
    assert translator.text_to_braille("Hola, ¿cómo estás?") == \
           "⠨⠓⠕⠇⠁⠂ ⠢⠉⠬⠍⠕ ⠑⠎⠞⠷⠎⠢"
    assert translator.text_to_braille("a; b") == "⠁⠆ ⠃"

def test_text_to_braille_spaces_and_acentos(translator):
    # á=⠷, é=⠮, í=⠌, ó=⠬, ú=⠾ 
    assert translator.text_to_braille("áéíóú") == "⠷⠮⠌⠬⠾"

def test_text_to_braille_signos(translator):
    assert translator.text_to_braille(",.;:") == "⠂⠄⠆⠒"
    # ¿ y ?
    assert translator.text_to_braille("¿?") == "⠢⠢"
    # ¡ y !
    assert translator.text_to_braille("¡¡!") == "⠖⠖⠖"
    # Paréntesis
    assert translator.text_to_braille("(hola)") == "⠣⠓⠕⠇⠁⠜"

def test_text_to_braille_oracion_completa(translator):
    assert translator.text_to_braille("Hola, ¿cómo estás?") == \
        "⠨⠓⠕⠇⠁⠂ ⠢⠉⠬⠍⠕ ⠑⠎⠞⠷⠎⠢"
        
def test_text_to_braille_espacios(translator):  
    # Espacios
    assert translator.text_to_braille("Hola Mundo") == "⠨⠓⠕⠇⠁ ⠨⠍⠥⠝⠙⠕"
