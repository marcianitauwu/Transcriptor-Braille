import pytest
from src.translator import BrailleTranslator

def test_text_to_braille():
    translator = BrailleTranslator()

    # Casos básicos
    assert translator.text_to_braille("Hola") == "⠨⠓⠕⠇⠁"
    assert translator.text_to_braille("123") == "⠼⠁⠃⠉"
    assert translator.text_to_braille("1,2,3") == "⠼⠁⠂⠃⠂⠉"
    assert translator.text_to_braille("1 2 3") == "⠼⠁ ⠼⠃ ⠼⠉"
    assert translator.text_to_braille("1, 2, 3") == "⠼⠁⠂ ⠼⠃⠂ ⠼⠉"
    assert translator.text_to_braille("12a") == "⠼⠁⠃⠁"

    # Vocales acentuadas
    # á=⠷, é=⠮, í=⠌, ó=⠬, ú=⠾  (Corrección final)
    assert translator.text_to_braille("áéíóú") == "⠷⠮⠌⠬⠾"

    # Signos
    assert translator.text_to_braille("Hola, ¿cómo estás?") == \
           "⠨⠓⠕⠇⠁⠂ ⠢⠉⠬⠍⠕ ⠑⠎⠞⠷⠎⠢"
    assert translator.text_to_braille("a; b") == "⠁⠆ ⠃"

    # Espacios
    assert translator.text_to_braille("Hola Mundo") == "⠨⠓⠕⠇⠁ ⠨⠍⠥⠝⠙⠕"

def test_braille_to_text():
    translator = BrailleTranslator()

    # Casos básicos
    assert translator.braille_to_text("⠨⠓⠕⠇⠁") == "Hola"
    assert translator.braille_to_text("⠼⠁⠃⠉") == "123"
    assert translator.braille_to_text("⠼⠁⠂⠃⠂⠉") == "1,2,3"
    assert translator.braille_to_text("⠼⠁⠂ ⠼⠃⠂ ⠼⠉") == "1, 2, 3"
    assert translator.braille_to_text("⠼⠁ ⠼⠃ ⠼⠉") == "1 2 3"

    # Vocales acentuadas (consistente con text_to_braille)
    assert translator.braille_to_text("⠷⠮⠌⠬⠾") == "áéíóú"

    # Signos
    assert translator.braille_to_text("⠨⠓⠕⠇⠁⠂ ⠢⠉⠬⠍⠕ ⠑⠎⠞⠷⠎⠢") == \
           "Hola, ¿cómo estás?"

    # Espacios
    assert translator.braille_to_text("⠨⠓⠕⠇⠁ ⠨⠍⠥⠝⠙⠕") == "Hola Mundo"
