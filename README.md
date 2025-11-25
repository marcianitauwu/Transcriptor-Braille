# Transcriptor-Braille

## Descripción

**Transcriptor-Braille** es una herramienta diseñada para convertir texto a Braille. Este proyecto permite a los usuarios trabajar con texto y Braille de manera eficiente, soportando caracteres especiales, números, y letras acentuadas. Además, incluye una interfaz gráfica para facilitar su uso.

---

## Características

- **Conversión de texto a Braille**: Soporta letras, números, signos de puntuación y caracteres acentuados.
- **Interfaz gráfica**: Una aplicación visual para interactuar con el transcriptor.

---

## Requisitos

- **Python**: 3.11
- **Dependencias**:
  - `customtkinter`
  - `pytest`

---

## Estructura del proyecto

```plaintext
Transcriptor-Braille/
├── .gitignore
├── .pytest_cache/
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   ├── 
│   └── v/
│       └── cache/
│           ├── lastfailed
│           └── nodeids
├── .qodo/
│   ├── agents/
│   └── workflows/
├── src/
│   ├── gui.py
│   ├── main.py
│   ├── translator.py
│   ├── util.py
│   ├── __pycache__/
│   ├── .qodo/
│   └── img/
├── tests/
│   ├── test_translator.py
│   ├── test_util.py
│   ├── __pycache__/
│   └── reportes/
│       ├── reporte_texto.txt
│       └── reporte_visual.html