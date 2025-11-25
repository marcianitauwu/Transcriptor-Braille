from src.util import is_valid_text, is_braille

def test_is_valid_text():
    assert is_valid_text("Hola") is True
    assert is_valid_text("123") is True
    assert is_valid_text("¡Hola!") is True  # Ajustado para aceptar signos

def test_is_braille():
    assert is_braille("⠓⠕⠇⠁") is True
    assert is_braille("Hola") is False