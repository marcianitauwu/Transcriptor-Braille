# Documento de Requerimientos del Sistema
## Sistema de Transcripción Español-Braille

**Versión:** 1.0  
**Fecha:** Noviembre 2025  

---

## 1. Introducción

### 1.1 Propósito
Este documento especifica los requerimientos funcionales y no funcionales para el desarrollo de una aplicación de escritorio de transcripción de textos entre español y sistema Braille, destinado a facilitar la creación de señalética accesible para personas con discapacidad visual.

### 1.2 Alcance
La aplicación de escritorio permitirá la transcripción bidireccional entre texto en español y sistema Braille, incluyendo letras, números, vocales acentuadas y signos básicos. El producto está orientado a personas sin discapacidad que deseen generar contenido Braille para mejorar la accesibilidad en diversos contextos.

### 1.3 Contexto
Según el Consejo Nacional para la Igualdad de Discapacidades (CONADIS), en Ecuador existen 55,487 personas con discapacidad visual (datos hasta 2023), de las cuales el 38.56% presenta discapacidad visual grave y ceguera. Este proyecto contribuye a la inclusión mediante la democratización de la producción de contenido accesible.

### 1.4 Objetivos del Proyecto
Desarrollar una aplicación de escritorio que genere textos en el sistema de lectoescritura Braille, permitiendo a los usuarios crear señalética y rotulación accesible de bajo costo para edificios, aparatos, juegos de mesa, prendas de vestir, medicamentos, alimentos empacados, entre otros.

---

## 2. Requerimientos Funcionales

### RF-01: Transcripción de Texto Español a Braille
**Prioridad:** Alta  
**Descripción:** La aplicación debe transcribir textos ingresados en español al sistema Braille.

**Criterios de aceptación:**
- El sistema debe convertir todas las letras del alfabeto español (a-z)
- Debe soportar letras adicionales del español (ñ, á, é, í, ó, ú, ü)
- Debe convertir números del 0 al 9
- Debe incluir signos básicos de puntuación
- Debe preservar el espaciado entre palabras
- El resultado debe mostrarse en representación visual de puntos Braille

### RF-02: Implementación del Sistema de Puntos Braille
**Prioridad:** Alta  
**Descripción:** La aplicación debe implementar correctamente el símbolo generador Braille basado en 6 puntos dispuestos en 2 columnas de 3 puntos cada una.

**Especificaciones:**

<img width="273" height="455" alt="image" src="https://github.com/user-attachments/assets/3b4247d3-d7ab-400b-a539-1f69920b54db" />


Cada carácter Braille se forma mediante la combinación específica de estos seis puntos.

### RF-03: Transcripción del Alfabeto - Primera Serie (a-j)
**Prioridad:** Alta  
**Descripción:** Implementar la primera serie matriz correspondiente a las diez primeras letras del alfabeto.

| Letra | Puntos |
|-------|--------|
| a | 1 |
| b | 1,2 |
| c | 1,4 |
| d | 1,4,5 |
| e | 1,5 |
| f | 1,2,4 |
| g | 1,2,4,5 |
| h | 1,2,5 |
| i | 2,4 |
| j | 2,4,5 |

### RF-04: Transcripción del Alfabeto - Segunda Serie (k-t)
**Prioridad:** Alta  
**Descripción:** La segunda serie resulta de añadir el punto 3 a la primera serie.

| Letra | Puntos | Descripción |
|-------|--------|-------------|
| k | 1,3 | a + punto 3 |
| l | 1,2,3 | b + punto 3 |
| m | 1,3,4 | c + punto 3 |
| n | 1,3,4,5 | d + punto 3 |
| o | 1,3,5 | e + punto 3 |
| p | 1,2,3,4 | f + punto 3 |
| q | 1,2,3,4,5 | g + punto 3 |
| r | 1,2,3,5 | h + punto 3 |
| s | 2,3,4 | i + punto 3 |
| t | 2,3,4,5 | j + punto 3 |

### RF-05: Transcripción del Alfabeto - Tercera Serie (u-z)
**Prioridad:** Alta  
**Descripción:** La tercera serie resulta de añadir los puntos 3 y 6 a la primera serie.

| Letra | Puntos | Descripción |
|-------|--------|-------------|
| u | 1,3,6 | a + puntos 3,6 |
| v | 1,2,3,6 | b + puntos 3,6 |
| x | 1,3,4,6 | c + puntos 3,6 |
| y | 1,3,4,5,6 | d + puntos 3,6 |
| z | 1,3,5,6 | e + puntos 3,6 |

### RF-06: Letras Adicionales del Español
**Prioridad:** Alta  
**Descripción:** Soporte para caracteres especiales del idioma español.

| Letra | Puntos |
|-------|--------|
| ñ | 1,2,3,4,5,6 |
| á | 1,2,3,5,6 |
| é | 2,3,4,6 |
| í | 3,4 |
| ó | 3,4,6 |
| ú | 1,2,3,6 |
| ü | 1,2,5,6 |

### RF-07: Transcripción de Números
**Prioridad:** Alta  
**Descripción:** La aplicación debe convertir números utilizando el signo de número seguido de la primera serie del alfabeto.

**Reglas:**
- **Signo de número:** puntos 3,4,5,6 (se antepone antes del primer dígito)
- Los números del 1-9 y 0 corresponden a las letras a-j de la primera serie
- Para cantidades de dos o más cifras, el signo se coloca solo al principio
- Se pueden incluir puntos y comas en los números
- Los números diferentes se separan con espacios en blanco

**Ejemplo:**
- "5" → [signo de número] + [e]
- "25" → [signo de número] + [b] + [e]
- "3.14" → [signo de número] + [c] + [punto] + [a] + [d]

### RF-08: Área de Entrada de Texto
**Prioridad:** Alta  
**Descripción:** La aplicación debe proporcionar un área de texto donde el usuario pueda ingresar el texto en español a transcribir.

**Criterios de aceptación:**
- Campo de texto multi-línea
- Validación de caracteres soportados
- Mensaje de error claro si hay caracteres no soportados
- Contador de caracteres opcional
- Opción para limpiar/borrar el texto
- Soporte para operaciones estándar (copiar, pegar, deshacer)

### RF-09: Visualización del Resultado en Braille
**Prioridad:** Alta  
**Descripción:** La aplicación debe mostrar el texto transcrito en representación visual Braille.

**Criterios de aceptación:**
- Representación gráfica clara de los puntos Braille
- Cada carácter debe mostrarse en su cuadratín (rectángulo de 6 puntos)
- Los puntos activos deben ser claramente distinguibles de los inactivos
- Espaciado apropiado entre caracteres y palabras
- Visualización adaptable al tamaño de la ventana

### RF-10: Transcripción Inversa (Braille a Español)
**Prioridad:** Alta  
**Descripción:** La aplicación debe permitir convertir representación Braille de vuelta a texto en español.

**Criterios de aceptación:**
- Interfaz para ingresar o seleccionar caracteres Braille
- Reconocimiento correcto de todas las combinaciones de puntos
- Identificación del signo de número para interpretar dígitos
- Reconstrucción del texto original con espaciado apropiado
- Manejo de errores para combinaciones inválidas

### RF-11: Copiar Resultado
**Prioridad:** Media  
**Descripción:** Permitir al usuario copiar el resultado de la transcripción.

**Criterios de aceptación:**
- Botón para copiar al portapapeles
- Confirmación visual de que se copió exitosamente
- Copiar en formato de texto cuando sea aplicable

---

## 3. Requerimientos No Funcionales

### RNF-01: Usabilidad
**Descripción:** La aplicación debe ser intuitiva y fácil de usar.

**Criterios:**
- Interfaz limpia y minimalista
- Tiempo de aprendizaje menor a 10 minutos para usuarios nuevos
- Mensajes de error claros y orientadores
- Tooltips o ayuda contextual para funciones principales
- Navegación intuitiva entre funcionalidades
- Accesibilidad: contraste adecuado, tamaño de texto legible
- Atajos de teclado para funciones comunes

### RNF-02: Performance
**Descripción:** La aplicación debe responder rápidamente a las acciones del usuario.

**Criterios:**
- Tiempo de inicio de la aplicación menor a 3 segundos
- Tiempo de respuesta de transcripción menor a 1 segundo para textos de hasta 1000 caracteres
- Tiempo de respuesta menor a 3 segundos para textos de hasta 5000 caracteres
- Sin bloqueo de la interfaz durante procesamiento
- Uso eficiente de memoria RAM (máximo 200 MB)

### RNF-03: Compatibilidad
**Descripción:** La aplicación debe funcionar en los sistemas operativos más utilizados.

**Sistemas operativos soportados:**
- Windows 10 o superior
- macOS 10.15 (Catalina) o superior
- Linux (Ubuntu 20.04 o superior, u otras distribuciones principales)

**Requisitos mínimos:**
- Procesador: 1 GHz o superior
- RAM: 2 GB mínimo
- Espacio en disco: 100 MB para instalación
- Resolución de pantalla: 1024x768 o superior

### RNF-04: Confiabilidad
**Descripción:** La aplicación debe transcribir con precisión y ser estable.

**Criterios:**
- Precisión del 100% en la transcripción según las reglas establecidas
- Validación de entrada antes de procesar
- Manejo robusto de errores y excepciones
- Sin pérdida de datos durante la transcripción
- Mensajes de error informativos cuando ocurran problemas
- No presentar cierres inesperados durante operación normal

### RNF-05: Mantenibilidad
**Descripción:** El código debe ser fácil de mantener y extender.

**Criterios:**
- Código bien estructurado y modular
- Comentarios en código complejo
- Separación clara de responsabilidades (lógica de negocio, presentación)
- Nombres de variables y funciones descriptivos
- Arquitectura que permita agregar nuevos caracteres o funcionalidades

---

## 4. Casos de Uso

### CU-01: Transcribir Texto Simple a Braille
**Actor:** Usuario  
**Precondiciones:** Usuario ha iniciado la aplicación de escritorio  
**Flujo Principal:**
1. Usuario ingresa texto en español en el área de entrada
2. Usuario hace clic en el botón "Transcribir a Braille"
3. Sistema valida que el texto contenga solo caracteres soportados
4. Sistema realiza la transcripción aplicando las reglas del alfabeto Braille
5. Sistema muestra el resultado en representación visual Braille
6. Usuario visualiza el resultado

**Flujo Alternativo:**
- 3a. Si hay caracteres no soportados:
  - Sistema muestra mensaje indicando los caracteres problemáticos
  - Sistema resalta los caracteres no válidos
  - Usuario corrige el texto y continúa desde el paso 2

**Postcondiciones:** El texto está transcrito y visible en pantalla

### CU-02: Transcribir Texto con Números
**Actor:** Usuario  
**Precondiciones:** Usuario ha iniciado la aplicación de escritorio  
**Flujo Principal:**
1. Usuario ingresa texto que incluye números (ej: "Piso 3")
2. Usuario hace clic en "Transcribir a Braille"
3. Sistema identifica los números en el texto
4. Sistema aplica el signo de número antes del primer dígito
5. Sistema transcribe los dígitos usando la primera serie del alfabeto
6. Sistema transcribe el resto del texto normalmente
7. Sistema muestra el resultado completo

**Postcondiciones:** El texto con números está correctamente transcrito

### CU-03: Transcribir Braille a Español
**Actor:** Usuario  
**Precondiciones:** Usuario ha iniciado la aplicación de escritorio  
**Flujo Principal:**
1. Usuario hace clic en "Traducir de Braille a Español"
2. Sistema muestra interfaz para ingresar caracteres Braille
3. Usuario ingresa o selecciona los puntos Braille para cada carácter
4. Usuario hace clic en "Transcribir a Español"
5. Sistema reconoce las combinaciones de puntos
6. Sistema identifica signos especiales (números, acentos)
7. Sistema reconstruye el texto en español
8. Sistema muestra el resultado

**Flujo Alternativo:**
- 6a. Si hay combinación de puntos inválida:
  - Sistema muestra mensaje de error
  - Sistema indica qué carácter es inválido
  - Usuario corrige y continúa desde el paso 4

**Postcondiciones:** Texto en español mostrado correctamente

### CU-04: Copiar Resultado de Transcripción
**Actor:** Usuario  
**Precondiciones:** Usuario ha realizado una transcripción exitosa  
**Flujo Principal:**
1. Usuario visualiza resultado de transcripción
2. Usuario hace clic en botón "Copiar"
3. Sistema copia el resultado al portapapeles
4. Sistema muestra notificación "Copiado exitosamente"
5. Usuario puede pegar el contenido en otra aplicación

**Postcondiciones:** Contenido disponible en portapapeles del usuario

### CU-05: Limpiar Área de Trabajo
**Actor:** Usuario  
**Precondiciones:** Hay texto en el área de entrada o resultado  
**Flujo Principal:**
1. Usuario hace clic en botón "Limpiar"
2. Sistema solicita confirmación
3. Usuario confirma la acción
4. Sistema borra el contenido del área de entrada
5. Sistema borra el resultado de la transcripción
6. Sistema limpia la vista previa si existe

**Flujo Alternativo:**
- 3a. Usuario cancela:
  - Sistema mantiene el contenido actual
  - Termina el caso de uso

**Postcondiciones:** Áreas de trabajo vacías y listas para nueva transcripción

---

## 5. Restricciones y Suposiciones

### 5.1 Restricciones
- La aplicación es exclusivamente web (no requiere instalación)
- Solo soporta transcripción de español a Braille y viceversa
- Primera iteración cubre requerimientos especificados en este documento
- Desarrollo debe usar control de versiones con GitHub
- No se permite desarrollo directo en rama main

### 5.2 Suposiciones
- Usuarios tienen una computadora con sistema operativo Windows, macOS o Linux
- Usuarios tienen permisos para instalar aplicaciones en su sistema
- Usuarios comprenden el alfabeto español
- Material impreso será procesado mediante técnicas apropiadas para crear relieve táctil
- Los usuarios no videntes que utilicen el material generado tienen conocimiento del sistema Braille
