import pytest
from src.translator import BrailleTranslator

def test_text_to_braille():
    translator = BrailleTranslator()

    # Casos básicos
    assert translator.text_to_braille("Hola") == "⠨⠓⠕⠇⠁", "La conversión de texto a Braille falló"
    assert translator.text_to_braille("123") == "⠼⠁⠃⠉", "La conversión de números a Braille falló"

    # Casos con vocales acentuadas
    assert translator.text_to_braille("áéíóú") == "⠷⠮⠿⠬⠾", "La conversión de vocales acentuadas falló"

    # Casos con signos de puntuación
    assert translator.text_to_braille("Hola, ¿cómo estás?") == "⠨⠓⠕⠇⠁⠂ ⠦⠉⠕⠍⠕ ⠑⠎⠞⠁⠎⠦", "La conversión con signos falló"

    # Casos con espacios
    assert translator.text_to_braille("Hola Mundo") == "⠨⠓⠕⠇⠁ ⠨⠍⠥⠝⠙⠕", "La conversión con espacios falló"

def test_braille_to_text():
    translator = BrailleTranslator()

    # Casos básicos
    assert translator.braille_to_text("⠨⠓⠕⠇⠁") == "Hola", "La conversión de Braille a texto falló"
    assert translator.braille_to_text("⠼⠁⠃⠉") == "123", "La conversión de números en Braille falló"

    # Casos con vocales acentuadas
    assert translator.braille_to_text("⠷⠮⠿⠬⠾") == "áéíóú", "La conversión de vocales acentuadas falló"

    # Casos con signos de puntuación
    assert translator.braille_to_text("⠨⠓⠕⠇⠁⠂ ⠦⠉⠕⠍⠕ ⠑⠎⠞⠁⠎⠦") == "Hola, ¿cómo estás?", "La conversión con signos falló"

    # Casos con espacios
    assert translator.braille_to_text("⠨⠓⠕⠇⠁ ⠨⠍⠥⠝⠙⠕") == "Hola Mundo", "La conversión con espacios falló"