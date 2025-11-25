from src.util import is_valid_text, is_braille

def test_is_valid_text():
    # Casos válidos
    assert is_valid_text("Hola") is True
    assert is_valid_text("áéíóú") is True  # Vocales acentuadas
    assert is_valid_text("123") is True
    assert is_valid_text("Hola, ¿cómo estás?") is True  # Signos básicos
    assert is_valid_text("Hola Mundo") is True
    assert is_valid_text("12345 Hola") is True

    # Casos inválidos
    assert is_valid_text("") is False  # Entrada vacía
    assert is_valid_text("😊") is False  # Emoji no válido
    assert is_valid_text("@#$%^&*") is False  # Caracteres especiales no válidos

def test_is_braille():
    # Casos válidos
    assert is_braille("⠓⠕⠇⠁") is True
    assert is_braille("⠼⠁⠃⠉") is True  # Números en Braille
    assert is_braille("⠨⠓⠕⠇⠁") is True  # Mayúsculas en Braille
    assert is_braille("⠨⠓⠕⠇⠁⠂ ⠦⠉⠕⠍⠕ ⠑⠎⠞⠁⠎⠦") is True  # Texto con signos

    # Casos inválidos
    assert is_braille("Hola") is False
    assert is_braille("") is False  # Entrada vacía
    assert is_braille("⠓⠕⠇⠁ Hola") is False  # Mezcla de texto y Braille