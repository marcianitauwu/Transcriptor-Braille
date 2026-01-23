# ESCUELA POLITÉCNICA NACIONAL

## CONSTRUCCIÓN Y EVOLUCIÓN DE SOFTWARE

*Arizaga Samira, Dávila Paúl, Sarasti Sebastián, Velásquez Carol*

# REPORTE DE CASOS DE PRUEBA – TRANSCRIPTOR BRAILLE → ESPAÑOL

## 1. Información General

* **Proyecto:** Transcriptor Braille
* **Requerimiento (2do Bimestre):** Conversión de Braille a Español
* **Plataforma:** Windows 32-bit
* **Python:** 3.11.0
* **Framework de Pruebas:** pytest 9.0.1
* **Fecha de Ejecución:** 25/01/2026
* **Resultado General:** 7/7 pruebas exitosas (100%)

Se desarrolló un conjunto de pruebas unitarias utilizando el framework **pytest** con el objetivo de validar el correcto funcionamiento del sistema de transcripción **Braille → Español**, considerando:

* Validación de entrada Braille (`is_braille`)
* Conversión de símbolos Braille a letras del alfabeto español
* Manejo de mayúsculas mediante indicador ⠨
* Interpretación del modo numérico ⠼
* Traducción de vocales acentuadas
* Reconocimiento de signos de puntuación
* Preservación de espacios y estructura del texto

Durante la fase inicial de pruebas se detectaron inconsistencias en el manejo del modo numérico y de los indicadores de mayúscula, las cuales fueron corregidas. Finalmente, todos los casos de prueba se ejecutaron correctamente.

---

## 2. Casos de Prueba y Resultados

### 2.1. CP-001: Validación de Entrada Braille

Se tuvo como objetivo verificar que la función valide correctamente cadenas de entrada en Braille, aceptando únicamente símbolos Braille definidos en el mapa de traducción y rechazando entradas vacías, texto plano, emojis o mezclas de Braille con caracteres no permitidos.

**Módulo:** `util.py`
**Función:** `is_braille()`

#### Tabla – Resultados

| Entrada    | Resultado Esperado | Resultado Obtenido | Estado  |
| ---------- | ------------------ | ------------------ | ------- |
| "⠓⠕⠇⠁"     | True               | True               | EXITOSO |
| "⠼⠁⠃⠉"     | True               | True               | EXITOSO |
| "⠨⠓⠕⠇⠁"    | True               | True               | EXITOSO |
| "" (vacía) | False              | False              | EXITOSO |
| "Hola"     | False              | False              | EXITOSO |
| "😊"       | False              | False              | EXITOSO |
| "⠓⠕A"      | False              | False              | EXITOSO |

*Tabla 1. Entradas y salidas de los casos probados para is_braille()*

Inicialmente, la función aceptaba cadenas vacías y no detectaba correctamente la mezcla de Braille con caracteres ASCII. Para corregir este comportamiento se implementaron las siguientes mejoras:

* Se añadió la validación explícita para entradas vacías.
* Se restringió la validación únicamente a los caracteres Braille definidos en el mapa del traductor.

Con estas correcciones, la función valida correctamente todas las entradas permitidas y no permitidas.

---

### 2.2. CP-002: Transcripción de Letras Básicas

Se tuvo como objetivo verificar la correcta conversión de letras individuales y palabras simples desde Braille a Español, asegurando que cada símbolo Braille se traduzca a su carácter correspondiente.

**Módulo:** `translator.py`
**Función:** `braille_to_text()`

#### Tabla – Resultados

| Entrada | Resultado Esperado | Resultado Obtenido | Estado  |
| ------- | ------------------ | ------------------ | ------- |
| "⠓⠕⠇⠁"  | hola               | hola               | EXITOSO |
| "⠨⠓⠕⠇⠁" | Hola               | Hola               | EXITOSO |
| "⠵"     | z                  | z                  | EXITOSO |
| "⠻"     | ñ                  | ñ                  | EXITOSO |
| "⠨⠻"    | Ñ                  | Ñ                  | EXITOSO |

*Tabla 2. Entradas y salidas de los casos probados para braille_to_text()*

El sistema interpreta correctamente el indicador de mayúscula ⠨, aplicándolo únicamente al carácter que lo sigue, incluyendo la letra especial Ñ.

---

### 2.3. CP-003: Transcripción de Números (Modo Numérico)

Se tuvo como objetivo verificar el correcto funcionamiento del modo numérico al convertir secuencias numéricas en Braille a su representación en texto plano, asegurando la correcta activación y desactivación del indicador numérico ⠼.

**Módulo:** `translator.py`
**Función:** `braille_to_text()`

#### Tabla – Resultados

| Entrada    | Resultado Esperado | Resultado Obtenido | Estado  |
| ---------- | ------------------ | ------------------ | ------- |
| "⠼⠁⠃⠉"     | 123                | 123                | EXITOSO |
| "⠼⠁⠂⠃⠂⠉"   | 1,2,3              | 1,2,3              | EXITOSO |
| "⠼⠁ ⠼⠃ ⠼⠉" | 1 2 3              | 1 2 3              | EXITOSO |
| "⠼⠁⠃⠁"     | 121                | 121                | EXITOSO |
| "⠼⠁⠃⠁⠁"    | 121a               | 121a               | EXITOSO |

*Tabla 3. Entradas y salidas de los casos probados para el modo numérico*

Se concluyó que el modo numérico se interpreta correctamente. El indicador ⠼ activa el modo numérico y permanece activo hasta que se detecta un carácter que no corresponde a un número, momento en el cual el sistema retorna automáticamente al modo texto.

---

### 2.4. CP-004: Transcripción de Vocales con Tilde

Se tuvo como objetivo verificar que las vocales acentuadas en Braille sean traducidas correctamente a sus equivalentes en español.

**Módulo:** `translator.py`
**Función:** `braille_to_text()`

#### Tabla – Resultados

| Entrada | Resultado Esperado | Resultado Obtenido | Estado  |
| ------- | ------------------ | ------------------ | ------- |
| "⠷⠮⠌⠬⠾" | áéíóú              | áéíóú              | EXITOSO |

*Tabla 4. Entradas y salidas de los casos probados para vocales con tilde*

El sistema reconoce correctamente todas las vocales acentuadas del español, garantizando una traducción fiel y conforme al estándar Braille.

---

### 2.5. CP-005: Transcripción de Signos de Puntuación

Se tuvo como objetivo verificar la correcta conversión de los signos de puntuación desde Braille a texto, incluyendo signos propios del idioma español.

**Módulo:** `translator.py`
**Función:** `braille_to_text()`

#### Tabla – Resultados

| Entrada  | Resultado Esperado | Resultado Obtenido | Estado  |
| -------- | ------------------ | ------------------ | ------- |
| "⠂⠄⠆⠒"   | ,.;:               | ,.;:               | EXITOSO |
| "⠢⠢"     | ¿?                 | ¿?                 | EXITOSO |
| "⠖⠖⠖"    | ¡¡¡                | ¡¡¡                | EXITOSO |
| "⠣⠓⠕⠇⠁⠜" | (hola)             | (hola)             | EXITOSO |

*Tabla 5. Entradas y salidas de los casos probados para signos de puntuación*

Se confirmó que el sistema maneja correctamente tanto signos estándar como signos de apertura y cierre propios del español.

---

### 2.6. CP-006: Transcripción de Oraciones Completas

Se tuvo como objetivo verificar la correcta traducción de oraciones completas que incluyen letras mayúsculas, vocales acentuadas, números y signos de puntuación.

**Módulo:** `translator.py`
**Función:** `braille_to_text()`

#### Tabla – Resultados

| Entrada               | Resultado Esperado | Resultado Obtenido | Estado  |
| --------------------- | ------------------ | ------------------ | ------- |
| "⠨⠓⠕⠇⠁⠂ ⠢⠉⠬⠍⠕ ⠑⠎⠞⠷⠎⠢" | Hola, ¿cómo estás? | Hola, ¿cómo estás? | EXITOSO |
| "⠁⠆ ⠃"                | a; b               | a; b               | EXITOSO |

*Tabla 6. Entradas y salidas de los casos probados para oraciones completas*

El sistema combina correctamente todos los elementos del lenguaje, manteniendo la estructura y significado del texto original.

---

### 2.7. CP-007: Manejo de Espacios

Se tuvo como objetivo verificar que los espacios entre palabras se conserven correctamente durante la transcripción desde Braille a Español.

**Módulo:** `translator.py`
**Función:** `braille_to_text()`

#### Tabla – Resultados

| Entrada        | Resultado Esperado | Resultado Obtenido | Estado  |
| -------------- | ------------------ | ------------------ | ------- |
| "⠨⠓⠕⠇⠁ ⠨⠍⠥⠝⠙⠕" | Hola Mundo         | Hola Mundo         | EXITOSO |

*Tabla 7. Entradas y salidas de los casos probados para manejo de espacios*

Se verificó que los espacios se preservan correctamente y que cada palabra mantiene su formato original, incluyendo el uso adecuado de mayúsculas.

---

## 3. Cobertura Total de Funcionalidades

| Funcionalidad                 | Casos de Prueba        | Estado   |
| ----------------------------- | ---------------------- | -------- |
| Validación de entrada Braille | CP-001                 | Cubierto |
| Transcripción de letras       | CP-002                 | Cubierto |
| Indicador de mayúsculas       | CP-002, CP-006, CP-007 | Cubierto |
| Letra Ñ/ñ                     | CP-002                 | Cubierto |
| Modo numérico                 | CP-003                 | Cubierto |
| Vocales acentuadas            | CP-004, CP-006         | Cubierto |
| Signos de puntuación          | CP-005, CP-006         | Cubierto |
| Paréntesis                    | CP-005                 | Cubierto |
| Manejo de espacios            | CP-007                 | Cubierto |
| Oraciones complejas           | CP-006                 | Cubierto |

---

## 5. Conclusiones

Se concluyó que todas las pruebas se ejecutaron exitosamente, cumpliendo en su totalidad con el requerimiento del segundo bimestre: **la correcta transcripción de Braille a Español**.

El sistema presenta una validación robusta de la entrada, interpreta correctamente los indicadores de mayúscula y modo numérico, maneja de forma precisa el alfabeto español incluyendo la letra Ñ y las vocales acentuadas, reconoce signos de puntuación estándar y propios del idioma, y preserva fielmente los espacios y la estructura del texto original.

Finalmente, se destaca el correcto funcionamiento del traductor inverso Braille → Español, así como su eficiencia en tiempo de ejecución, consolidando un sistema confiable y alineado con los estándares de transcripción Braille.

