# test_translator.py
import pytest
from translator import BrailleTranslator


# ---------- FIXTURE ----------
@pytest.fixture
def translator():
    """Instancia del traductor Braille."""
    return BrailleTranslator()


# ---------- PRUEBAS DE TEXTO BÁSICO ----------
def test_text_to_braille_lowercase(translator):
    assert translator.text_to_braille("hola") == "⠓⠕⠇⠁"


def test_text_to_braille_uppercase(translator):
    assert translator.text_to_braille("Hola") == "⠨⠓⠕⠇⠁"


def test_text_to_braille_single_uppercase(translator):
    assert translator.text_to_braille("Z") == "⠨⠵"


def test_text_to_braille_enye(translator):
    assert translator.text_to_braille("ñ") == "⠻"
    assert translator.text_to_braille("Ñ") == "⠨⠻"


# ---------- PRUEBAS DE VOCALES CON TILDE ----------
def test_text_to_braille_accented_vowels(translator):
    assert translator.text_to_braille("áéíóú") == "⠷⠮⠌⠬⠾"


def test_text_to_braille_umlaut(translator):
    assert translator.text_to_braille("ü") == "⠳"


# ---------- PRUEBAS DE MODO NUMÉRICO ----------
def test_text_to_braille_numbers_simple(translator):
    assert translator.text_to_braille("123") == "⠼⠁⠃⠉"


def test_text_to_braille_numbers_with_commas(translator):
    assert translator.text_to_braille("1,2,3") == "⠼⠁⠂⠃⠂⠉"


def test_text_to_braille_numbers_separated_by_space(translator):
    assert translator.text_to_braille("1 2 3") == "⠼⠁ ⠼⠃ ⠼⠉"


def test_text_to_braille_number_then_letter(translator):
    assert translator.text_to_braille("12a") == "⠼⠁⠃⠁"


def test_text_to_braille_number_mode_resets(translator):
    assert translator.text_to_braille("1a2") == "⠼⠁⠁⠼⠃"


# ---------- PRUEBAS DE SIGNOS DE PUNTUACIÓN ----------
def test_text_to_braille_punctuation(translator):
    assert translator.text_to_braille(",.;:") == "⠂⠄⠆⠒"


def test_text_to_braille_question_marks(translator):
    assert translator.text_to_braille("¿?") == "⠢⠢"


def test_text_to_braille_exclamation_marks(translator):
    assert translator.text_to_braille("¡¡!") == "⠖⠖⠖"


def test_text_to_braille_parentheses(translator):
    assert translator.text_to_braille("(hola)") == "⠣⠓⠕⠇⠁⠜"


# ---------- PRUEBAS DE FRASES COMPLETAS ----------
def test_text_to_braille_full_sentence(translator):
    text = "Hola, ¿cómo estás?"
    expected = "⠨⠓⠕⠇⠁⠂ ⠢⠉⠬⠍⠕ ⠑⠎⠞⠷⠎⠢"
    assert translator.text_to_braille(text) == expected


def test_text_to_braille_spaces(translator):
    assert translator.text_to_braille("Hola Mundo") == "⠨⠓⠕⠇⠁ ⠨⠍⠥⠝⠙⠕"


# ---------- PRUEBAS DE CARACTERES NO SOPORTADOS ----------
def test_text_to_braille_unknown_character(translator):
    assert translator.text_to_braille("@") == "?"
