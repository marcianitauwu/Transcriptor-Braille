# ESCUELA POLITÉCNICA NACIONAL
## CONSTRUCCIÓN Y EVOLUCIÓN DE SOFTWARE  
_Arizaga Samira, Dávila Paúl, Sarasti Sebastián, Velásquez Carol_

# REPORTE DE CASOS DE PRUEBA - TRANSCRIPTOR BRAILLE

## 1. Información General

- **Proyecto:** Transcriptor Braille
- **Plataforma:** Windows 32-bit
- **Python:** 3.11.0
- **Framework de Pruebas:** pytest 9.0.1
- **Fecha de Ejecución:** 25/11/2025
- **Resultado General:** 7/7 pruebas exitosas (100%)

Se desarrolló un conjunto de pruebas unitarias (pytest) para verificar:

- Validación de texto (`is_valid_text`)
- Validación de Braille (`is_braille`)
- Traducción Texto → Braille
- Manejo de acentos, signos, mayúsculas y números

Durante la ejecución inicial se identificaron errores funcionales, se aplicaron correcciones y finalmente todos los casos ejecutaron correctamente.

## 2. Casos de Prueba y Resultados

### 2.1. CP-001: Validación de Texto

Se tuvo como objetivo verificar que la función evalúe correctamente el texto ingresado, aceptando únicamente letras en mayúsculas y minúsculas, números, caracteres con acento, signos permitidos y espacios. Asimismo, se debe comprobar que la función rechace textos vacíos, el uso de emojis y cualquier símbolo no contemplado dentro de los criterios establecidos.

**Módulo:** `util.py`  
**Función:** `is_valid_text()`

#### Tabla – Resultados

| Entrada | Resultado Esperado | Resultado Obtenido | Estado |
|--------|--------------------|--------------------|--------|
| "Hola" | True | True | EXITOSO |
| "áéíóú" | True | True | EXITOSO |
| "123" | True | True | EXITOSO |
| "Hola, ¿cómo estás?" | True | True | EXITOSO |
| "" (vacía) | False | False | EXITOSO |
| "😊" (emoji) | False | False | EXITOSO |
| "@#$%^&*" | False | False | EXITOSO |
| "Hola ⠓⠕" | False | False | EXITOSO |

_Tabla 1. Entradas y salidas de los casos probados para is_valid_text_

Inicialmente la función presentó un fallo, ya que is_valid_text("") devolvía True y los caracteres en Braille eran interpretados como válidos. De modo que, se identificó que la función no validaba correctamente los textos vacíos ni detectaba la mezcla indebida de caracteres Braille con texto normal. Además, la dependencia de translator.map provocaba que ciertos símbolos Braille se evaluaran como texto válido.
Se implementaron las siguientes modificaciones acorde a la prueba, y finalmente pasó la prueba:

- Se añadió `if not text: return False`para manejar correctamente los textos vacíos.
- La validación se restringió únicamente a caracteres ASCII y a los caracteres acentuados definidos en el mapa

La función de validación detecta correctamente todos los casos válidos e inválidos, incluyendo texto vacío, emojis, caracteres especiales no permitidos y mezclas de texto con Braille.

---

### 2.2 CP-002: Transcripción de Texto Básico

Se tuvo como objetivo verificar que la función realizara de manera correcta la transcripción de letras individuales y de palabras simples, asegurando que cada carácter se convirtiera al símbolo Braille correspondiente de forma precisa y conforme a las reglas establecidas.

**Módulo:** `translator.py`  
**Función:** `text_to_braille()`

#### Tabla – Resultados

| Entrada | Resultado Esperado | Resultado Obtenido | Estado |
|--------|--------------------|--------------------|--------|
| "Hola" | ⠨⠓⠕⠇⠁ | ⠨⠓⠕⠇⠁ | EXITOSO |
| "hola" | ⠓⠕⠇⠁ | ⠓⠕⠇⠁ | EXITOSO |
| "Z" | ⠨⠵ | ⠨⠵ | EXITOSO |
| "ñ" | ⠻ | ⠻ | EXITOSO |
| "Ñ" | ⠨⠻ | ⠨⠻ | EXITOSO |

_Tabla 2. Entradas y salidas de los casos probados para text_to_braille()_

El sistema maneja correctamente las mayúsculas usando el indicador ⠨, incluyendo la letra especial del español "Ñ". Las minúsculas se transcriben sin modificador.

---

### 2.3. CP-003: Transcripción de Números (Modo Numérico)

Se tuvo como objetivo verificar el correcto funcionamiento del modo numérico dentro de la función, así como asegurar su adecuada desactivación cuando corresponda, garantizando que la transcripción a Braille se realice de acuerdo con las reglas definidas para números y texto.

**Módulo:** `translator.py`  
**Función:** `text_to_braille()`

#### Tabla – Resultados

| Entrada | Resultado Esperado | Resultado Obtenido | Estado |
|--------|--------------------|--------------------|--------|
| "123" | ⠼⠁⠃⠉ | ⠼⠁⠃⠉ | EXITOSO |
| "1,2,3" | ⠼⠁⠂⠃⠂⠉ | ⠼⠁⠂⠃⠂⠉ | EXITOSO |
| "1 2 3" | ⠼⠁ ⠼⠃ ⠼⠉ | ⠼⠁ ⠼⠃ ⠼⠉ | EXITOSO |
| "1, 2, 3" | ⠼⠁⠂ ⠼⠃⠂ ⠼⠉ | ⠼⠁⠂ ⠼⠃⠂ ⠼⠉ | EXITOSO |
| "12a" | ⠼⠁⠃⠁ | ⠼⠁⠃⠁ | EXITOSO |

_Tabla 3. Entradas y salidas de los casos probados para text_to_braille() para el modo numérico_

Se concluyó que el modo numérico funciona correctamente. Este se activa con el símbolo ⠼ al inicio de una secuencia numérica y permanece activo para los dígitos consecutivos. Además, se mantiene activo cuando se incluyen comas decimales dentro de los números y se desactiva automáticamente al encontrar espacios. Posteriormente, se reactiva con cada nuevo número que siga después de un espacio y permite la transición directa a letras sin necesidad de un espacio intermedio, como ocurre en casos como "12a".

La corrección aplicada al sistema consiste en implementar correctamente el modo numérico estándar en Braille, evitando repetir el prefijo numérico para cada dígito.
Antes de la corrección, los números se traducían así:

`121 → ⠼⠁⠼⠃⠼⠁`

Esto es incorrecto porque el prefijo ⠼ se repetía para cada dígito.
Después de la corrección, se aplica la regla correcta del modo numérico:

`121 → ⠼⠁⠃⠁`

Ahora el prefijo numérico solo aparece una vez, y los dígitos continúan en modo numérico hasta que aparezca un carácter que no sea número.

El prefijo numérico ⠼:
- Se coloca una sola vez al inicio del bloque numérico.
- Permanece activo hasta que un carácter no numérico lo desactiva.

---

### 2.4. CP-004: Transcripción de Vocales con Tilde

Se tuvo como objetivo verificar que la función represente correctamente las vocales acentuadas del español, asegurando que cada carácter con tilde se transcriba al símbolo Braille correspondiente de manera precisa y conforme a las normas de transcripción establecidas.

**Módulo:** `translator.py`  
**Función:** `text_to_braille()`


#### Tabla – Resultados

| Entrada | Resultado Esperado | Resultado Obtenido | Estado |
|--------|--------------------|--------------------|--------|
| "áéíóú" | ⠷⠮⠌⠬⠾ | ⠷⠮⠌⠬⠾ | EXITOSO |

_Tabla 4. Entradas y salidas de los casos probados para text_to_braille() para vocales con tilde_

Se concluyó que todas las vocales acentuadas del español se transcriben correctamente, asignándoles sus respectivos símbolos Braille de manera precisa y conforme a las normas de transcripción establecidas.

---

### 2.5. CP-005: Transcripción de Signos de Puntuación

Se tuvo como objetivo verificar que la función represente correctamente los signos de puntuación comunes, asegurando que cada símbolo de puntuación se transcriba al correspondiente carácter Braille de manera precisa y conforme a las reglas de transcripción establecidas.

**Módulo:** `translator.py`  
**Función:** `text_to_braille()`

### Tabla – Resultados

| Entrada | Resultado Esperado | Resultado Obtenido | Estado |
|--------|--------------------|--------------------|--------|
| ",.;:" | ⠂⠄⠆⠒ | ⠂⠄⠆⠒ | EXITOSO |
| "¿?" | ⠢⠢ | ⠢⠢ | EXITOSO |
| "¡¡!" | ⠖⠖⠖ | ⠖⠖⠖ | EXITOSO |
| "(hola)" | ⠣⠓⠕⠇⠁⠜ | ⠣⠓⠕⠇⠁⠜ | EXITOSO |

_Tabla 5. Entradas y salidas de los casos probados para text_to_braille() para signos de puntuación_

Se concluyó que todos los signos de puntuación se transcriben correctamente, incluyendo los signos de apertura específicos del español, como ¿ y ¡, garantizando así una transcripción fiel y conforme a las normas de Braille establecidas.

---

### 2.6 CP-006: Transcripción de Oraciones Completas

Se tuvo como objetivo verificar que la función realice correctamente la transcripción de oraciones que contienen múltiples elementos, tales como letras mayúsculas, vocales acentuadas y signos de puntuación, asegurando que cada carácter se convierta al símbolo Braille correspondiente de manera precisa y conforme a las reglas de transcripción establecidas.

**Módulo:** `translator.py`  
**Función:** `text_to_braille()`

#### Tabla – Resultados

| Entrada | Resultado Esperado | Resultado Obtenido | Estado |
|--------|--------------------|--------------------|--------|
| "Hola, ¿cómo estás?" | ⠨⠓⠕⠇⠁⠂ ⠢⠉⠬⠍⠕ ⠑⠎⠞⠷⠎⠢ | ⠨⠓⠕⠇⠁⠂ ⠢⠉⠬⠍⠕ ⠑⠎⠞⠷⠎⠢ | EXITOSO |
| "a; b" | ⠁⠆ ⠃ | ⠁⠆ ⠃ | EXITOSO |

_Tabla 6. Entradas y salidas de los casos probados para text_to_braille() para una frase_

Se concluyó que el sistema maneja correctamente la transcripción de oraciones completas que combinan diferentes elementos, incluyendo indicadores de mayúscula (⠨), vocales acentuadas (por ejemplo, á = ⠷), signos de puntuación (como la coma = ⠂ y los signos de apertura y cierre ¿? = ⠢), así como los espacios entre palabras, garantizando una transcripción precisa y conforme a las normas de Braille establecidas.

---

### 2.7. CP-007: Manejo de Espacios
Se tuvo como objetivo verificar que la función preserve correctamente los espacios entre palabras durante la transcripción a Braille, asegurando que la separación del texto original se mantenga de manera fiel y conforme a las normas de transcripción establecidas.

**Módulo:** `translator.py`  
**Función:** `text_to_braille()`

#### Tabla – Resultados

| Entrada | Resultado Esperado | Resultado Obtenido | Estado |
|--------|--------------------|--------------------|--------|
| "Hola Mundo" | ⠨⠓⠕⠇⠁ ⠨⠍⠥⠝⠙⠕ | ⠨⠓⠕⠇⠁ ⠨⠍⠥⠝⠙⠕ | EXITOSO |

_Tabla 7. Entradas y salidas de los casos probados para text_to_braille() para una frase sin signos ni puntuaciones_

Se concluyó que los espacios se preservan correctamente en la transcripción a Braille. Además, se observó que cada palabra que inicia con letra mayúscula recibe de manera adecuada su propio indicador de mayúscula (⠨), garantizando una representación fiel del texto original.

---

## 3. Cobertura Total de Funcionalidades

| Funcionalidad | Casos de Prueba | Estado |
|---------------|----------------|--------|
| Validación de entrada | CP-001 | Cubierto |
| Transcripción de letras minúsculas | CP-002 | Cubierto |
| Indicador de mayúsculas | CP-002, CP-006, CP-007 | Cubierto |
| Letra Ñ/ñ | CP-002 | Cubierto |
| Modo numérico | CP-003 | Cubierto |
| Vocales acentuadas | CP-004, CP-006 | Cubierto |
| Signos de puntuación | CP-005, CP-006 | Cubierto |
| Paréntesis | CP-005 | Cubierto |
| Manejo de espacios | CP-007 | Cubierto |
| Oraciones complejas | CP-006 | Cubierto |

---

## 5. Conclusiones

Se concluyó que todas las pruebas se ejecutaron exitosamente en la primera ejecución, sin que fuera necesario realizar correcciones adicionales.

Entre las fortalezas del sistema se destacan: la validación robusta de la entrada, que rechaza caracteres no soportados; el correcto manejo del alfabeto español, incluyendo la letra Ñ y las vocales acentuadas; la implementación exitosa del modo numérico conforme al estándar Braille; el soporte completo de los signos de puntuación utilizados en español; el manejo adecuado de las letras mayúsculas mediante el indicador ⠨; la preservación correcta de los espacios; y un tiempo de ejecución muy eficiente, que se registró en aproximadamente 0,05 segundos.

Asimismo, se implementaron mejoras exitosas, tales como la optimización del modo numérico para reducir la cantidad de símbolos necesarios para representar números, y la modificación del uso del indicador numérico (⠼), que ahora se aplica una sola vez por secuencia numérica en lugar de repetirse para cada dígito.

