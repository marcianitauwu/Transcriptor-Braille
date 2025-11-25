from src.util import is_valid_text, is_braille

def test_is_valid_text():
    # Casos válidos
    assert is_valid_text("Hola") is True
    assert is_valid_text("áéíóú") is True
    assert is_valid_text("123") is True
    assert is_valid_text("Hola, ¿cómo estás?") is True
    assert is_valid_text("Hola Mundo") is True
    assert is_valid_text("12345 Hola") is True

    # Casos inválidos
    assert is_valid_text("") is False
    assert is_valid_text("😊") is False
    assert is_valid_text("@#$%^&*") is False
    assert is_valid_text("Hola ⠓⠕") is False  # Mezcla de Braille y texto

def test_is_braille():
    # Casos válidos
    assert is_braille("⠓⠕⠇⠁") is True
    assert is_braille("⠼⠁⠃⠉") is True  # números
    assert is_braille("⠨⠓⠕⠇⠁") is True  # mayúscula en Braille
    assert is_braille("⠨⠓⠕⠇⠁⠂ ⠦⠉⠕⠍⠕ ⠑⠎⠞⠁⠎⠦") is True

    # Casos inválidos
    assert is_braille("") is False
    assert is_braille("Hola") is False
    assert is_braille("⣿") is False  # símbolo no estándar
    assert is_braille("⠓⠕ Hola") is False  # mezcla
