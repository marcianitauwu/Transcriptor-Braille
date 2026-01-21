# gui.py
"""
Módulo principal de la Interfaz Gráfica de Usuario (GUI) para el Transcriptor Braille.

Este módulo maneja:
1. La inicialización de la ventana principal y la navegación entre pantallas.
2. La carga de recursos (imágenes, iconos) compatibles con PyInstaller.
3. La interacción del usuario para traducir texto a Braille.
4. La generación de reportes en PDF utilizando fuentes compatibles con caracteres Unicode Braille.
"""

import tkinter as tk
import ctypes
import sys
import os
from tkinter import messagebox
from tkinter import filedialog

# --- LIBRERÍAS DE PDF ---
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
# ------------------------

import customtkinter as ctk
from PIL import Image, ImageTk 

from translator import BrailleTranslator
from util import clean_input, is_valid_text, is_valid_braille

# --- FUNCIÓN PARA RUTAS RELATIVAS (NECESARIA PARA EL .EXE) ---
def resource_path(relative_path):
    """
    Obtiene la ruta absoluta a un recurso (imágenes, fuentes, iconos).
    
    Esta función es necesaria para que el ejecutable (.exe) generado por 
    PyInstaller pueda encontrar los archivos, ya que estos se descomprimen 
    en una carpeta temporal (_MEIPASS) durante la ejecución.

    Args:
        relative_path (str): Ruta relativa del archivo en el proyecto (ej: "src/img/logo.png").

    Returns:
        str: Ruta absoluta al archivo, ya sea en entorno de desarrollo o producción.
    """
    try:
        # PyInstaller crea una carpeta temporal en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class BrailleApp(ctk.CTk):
    """
    Clase principal de la aplicación. Hereda de customtkinter.CTk.
    
    Actúa como el controlador principal que gestiona:
    - La ventana raíz.
    - La instancia global del traductor.
    - El contenedor de pantallas (frames).
    - La navegación entre las distintas vistas.
    """
    def __init__(self):
        """Inicializa la ventana principal, configuración, icono y pantallas."""
        super().__init__()
        
        self.geometry("850x600")
        
        # Icono de la aplicación en Windows (Barra de tareas)
        if sys.platform == "win32":
            app_id = "samira.braille.transcriptor.1.0"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        try:
            icon_path = resource_path(os.path.join("src", "img", "icono.ico"))
            self.iconbitmap(icon_path)
        except:
            pass

        self.title("Transcriptor Braille")

        # Instancia del traductor que usan todas las pantallas
        self.translator = BrailleTranslator()

        # Contenedor principal donde se apilan todas las pantallas
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        # Diccionario que almacena las instancias de las pantallas
        self.frames = {}

        # Se inicializan y registran todas las pantallas disponibles
        for F in (StartScreen, MenuScreen, TextToBrailleScreen, BrailleToTextScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        # Mostrar la pantalla inicial al arrancar
        self.show_frame(StartScreen)

    def show_frame(self, screen):
        """
        Trae al frente la pantalla solicitada.

        Args:
            screen (class): La clase de la pantalla que se desea mostrar.
        """
        frame = self.frames[screen]
        frame.tkraise()

# Pantallita de inicio
class StartScreen(ctk.CTkFrame):
    """
    Pantalla de bienvenida de la aplicación.
    
    Características:
    - Fondo con imagen redimensionable.
    - Título principal.
    - Botón para iniciar la experiencia.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1e1e1e")
        self.controller = controller

        # Canvas para manejar el fondo dinámico (imagen detrás de widgets)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Intentar cargar imagen de fondo
        try:
            img_path = resource_path(os.path.join("src", "img", "fondito.png"))
            self.original_image = Image.open(img_path)
            # Evento para redimensionar la imagen si cambia el tamaño de ventana
            self.canvas.bind("<Configure>", self.resize_background)
        except Exception as e:
            pass

        # Texto "Transcriptor Braille" dibujado en el Canvas
        self.title_id = self.canvas.create_text(
            self.winfo_width()/2, 100,
            text="TRANSCRIPTOR BRAILLE",
            fill="#FFFFFF", 
            font=("Segoe UI", 82, "bold"),
            anchor="center" 
        )

        # Botón de "Comenzar" incrustado en el Canvas
        btn_comenzar = ctk.CTkButton(
            self.canvas, 
            text="Comenzar",
            font=("Segoe UI", 20, "bold"),
            fg_color="#401a63",
            bg_color="#4A61C8",
            text_color="white",
            hover_color="#5e4574",
            corner_radius=30,
            width=250,
            height=50,
            command=lambda: controller.show_frame(MenuScreen)
        )

        self.button_id = self.canvas.create_window(
            self.winfo_width()/2, 500, 
            window=btn_comenzar, 
            anchor="center"
        )

    def resize_background(self, event):
        """
        Ajusta la imagen de fondo y la posición de los elementos cuando 
        la ventana cambia de tamaño.
        """
        if hasattr(self, 'original_image') and self.original_image:
            new_width = event.width
            new_height = event.height
            
            # Redimensionar imagen con alta calidad (LANCZOS)
            resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_image)

            if hasattr(self, '_bg_image_id'):
                self.canvas.itemconfig(self._bg_image_id, image=self.bg_photo)
            else:
                self._bg_image_id = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
                self.canvas.lower(self._bg_image_id) 

            # Recentrar texto y botón
            self.canvas.coords(self.title_id, new_width / 2, new_height * 0.2)
            self.canvas.coords(self.button_id, new_width / 2, new_height * 0.8)


# Pantalla 2, menú de opciones
class MenuScreen(ctk.CTkFrame):
    """
    Pantalla de menú principal.
    
    Ofrece navegación hacia la herramienta de conversión o regreso al inicio.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#304171")
        self.controller = controller

        # Título
        ctk.CTkLabel(
            self,
            text="Selecciona una opción",
            text_color="white",
            fg_color="transparent",
            font=("Segoe UI", 30, "bold")
        ).pack(pady=(80, 40))

        # Botón Texto a Braille
        ctk.CTkButton(
            self,
            text="Texto ➜ Braille",
            font=("Segoe UI", 20, "bold"),
            fg_color="#3d79e1",
            hover_color="#2e61bb",
            corner_radius=30,
            width=350,
            height=70,
            command=lambda: controller.show_frame(TextToBrailleScreen)
        ).pack(pady=15)
        
        # Botón Braille a Texto
        ctk.CTkButton(
            self,
            text="Braille ➜ Texto",
            font=("Segoe UI", 20, "bold"),
            fg_color="#3d79e1",
            hover_color="#2e61bb",
            corner_radius=30,
            width=350,
            height=70,
            command=lambda: controller.show_frame(BrailleToTextScreen)
        ).pack(pady=15)

        # Botón regresar
        ctk.CTkButton(
            self,
            text="Regresar",
            font=("Segoe UI", 20, "bold"),
            fg_color="#401a63",
            hover_color="#5e4574",
            corner_radius=30,
            width=250,
            height=50,
            command=lambda: controller.show_frame(StartScreen)
        ).pack(pady=50)


# Pantalla 3, aquí se convierte de texto a braille
class TextToBrailleScreen(ctk.CTkFrame):
    """
    Pantalla funcional para la conversión de Texto a Braille.
    
    Funcionalidades:
    - Entrada de texto (Textbox).
    - Validación y limpieza de entrada.
    - Visualización del resultado en Braille.
    - Generación de PDF descargable.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#25282E")
        self.controller = controller
        self.translator = controller.translator

        ctk.CTkLabel(
            self,
            text="Texto ➜ Braille",
            text_color="white",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(30, 20))

        # --- Entrada de texto ---
        ctk.CTkLabel(self, text="Texto de entrada:", font=("Segoe UI", 14), text_color="#cccccc").pack()
        
        self.input_text = ctk.CTkTextbox(
            self, width=600, height=100, corner_radius=10, 
            fg_color="#2d2d2d", text_color="white", font=("Segoe UI", 14)
        )
        self.input_text.pack(pady=10)

        # --- Frame de Botones de Acción ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)

        # Botón Convertir
        ctk.CTkButton(
            btn_frame,
            text="Convertir",
            font=("Segoe UI", 20, "bold"),
            fg_color="#3d79e1",
            hover_color="#2e61bb",
            corner_radius=30,
            width=200,
            height=50,
            command=self.convert
        ).pack(side="left", padx=10)

        # Botón Imprimir PDF
        ctk.CTkButton(
            btn_frame,
            text="Imprimir PDF",
            font=("Segoe UI", 20, "bold"),
            fg_color="#28a745",
            hover_color="#218838",
            corner_radius=30,
            width=200,
            height=50,
            command=self.generar_pdf
        ).pack(side="left", padx=10)

        # --- Resultado ---
        ctk.CTkLabel(self, text="Resultado:", font=("Segoe UI", 14), text_color="#cccccc").pack()

        self.output_text = ctk.CTkTextbox(
            self, width=600, height=100, corner_radius=10, 
            fg_color="#2d2d2d", text_color="white", font=("Segoe UI", 20) 
        )
        self.output_text.pack(pady=10)

        # Botón regresar
        ctk.CTkButton(
            self,
            text="Regresar",
            font=("Segoe UI", 20, "bold"),
            fg_color="#401a63",
            hover_color="#5e4574",
            corner_radius=30,
            width=250,
            height=50,
            command=lambda: controller.show_frame(MenuScreen)
        ).pack(pady=20)

    def convert(self):
        """
        Obtiene el texto del usuario, lo valida y lo traduce a Braille.
        Actualiza el cuadro de texto de salida con el resultado.
        """
        raw_text = self.input_text.get("0.0", "end").strip()
        text = clean_input(raw_text)

        if not text:
             return

        if not is_valid_text(text):
            messagebox.showerror("Error", "Texto inválido. Use solo letras y números.")
            return

        result = self.translator.text_to_braille(text)

        self.output_text.delete("0.0", "end")
        self.output_text.insert("0.0", result)

    def generar_pdf(self):
        """
        Genera un archivo PDF que contiene el texto original y su traducción.

        Lógica del proceso:
        1. Verifica que haya contenido para traducir.
        2. Abre un cuadro de diálogo para que el usuario elija dónde guardar.
        3. Configura el Canvas de ReportLab (tamaño A4).
        4. CRÍTICO: Registra una fuente TTF compatible con Braille (Segoe UI Symbol o Arial).
           Sin esto, los caracteres Braille se verían como cuadros vacíos (tofu).
        5. Escribe el contenido en el PDF.
        """
        texto_braille = self.output_text.get("0.0", "end").strip()

        if not texto_braille:
            messagebox.showwarning("Advertencia", "Primero debes convertir un texto para poder imprimirlo.")
            return

        # 1. Abrir diálogo para guardar archivo
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar PDF para Impresión Braille"
        )

        if not filename:
            return # El usuario canceló la operación

        try:
            # 2. Configuración del Canvas
            c = canvas.Canvas(filename, pagesize=A4)
            ancho, alto = A4
            
            # --- SELECCIÓN DE FUENTES PARA BRAILLE ---
            font_name = "Helvetica" # Fallback por defecto
            
            try:
                # INTENTO 1 (PRIORIDAD): Segoe UI Symbol
                # Fuente nativa de Windows 7/8/10/11 que incluye glifos Braille.
                ruta_fuente = os.path.join(os.environ['WINDIR'], 'Fonts', 'seguisym.ttf')
                pdfmetrics.registerFont(TTFont('FuenteBraille', ruta_fuente))
                font_name = 'FuenteBraille'
                
            except Exception:
                try:
                    # INTENTO 2: Arial (Backup)
                    # Si no está Segoe, intenta con Arial.
                    ruta_fuente = os.path.join(os.environ['WINDIR'], 'Fonts', 'arial.ttf')
                    pdfmetrics.registerFont(TTFont('ArialBackup', ruta_fuente))
                    font_name = 'ArialBackup'
                except:
                    print("Advertencia: No se pudo cargar ninguna fuente TTF del sistema. El Braille podría no visualizarse.")
            # -------------------------------------------
            
            # 3. Dibujar contenido en el PDF
            # Aplicar modo espejo
            c.saveState()
            c.translate(ancho, 0)
            c.scale(-1, 1)
            
            # --- DIBUJAR CONTENIDO EN ESPEJO ---            
             # --- Texto Braille en grande ---
            text_object_braille = c.beginText(50, alto - 80)
            text_object_braille.setFont(font_name, 28)
            text_object_braille.setLeading(40)
            
            lineas_braille = simpleSplit(texto_braille, font_name, 28, ancho - 100)
            
            for linea in lineas_braille:
                text_object_braille.textLine(linea)
            
            c.drawText(text_object_braille)

            # Guardar archivo
            c.save()
            messagebox.showinfo("Éxito", "PDF generado correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}")


# Pantalla 4, aquí se convierte de braille a texto
class BrailleToTextScreen(ctk.CTkFrame):
    """
    Pantalla funcional para la conversión de Braille a Texto.
    
    Funcionalidades:
    - Entrada de texto en Braille (Textbox).
    - Validación de entrada Braille.
    - Visualización del resultado en texto normal.
    - Generación de PDF descargable.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#25282E")
        self.controller = controller
        self.translator = controller.translator

        ctk.CTkLabel(
            self,
            text="Braille ➜ Texto",
            text_color="white",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(30, 20))

        # --- Entrada de Braille ---
        ctk.CTkLabel(
            self, 
            text="Texto en Braille:", 
            font=("Segoe UI", 14), 
            text_color="#cccccc"
        ).pack()
        
        self.input_braille = ctk.CTkTextbox(
            self, width=600, height=100, corner_radius=10, 
            fg_color="#2d2d2d", text_color="white", font=("Segoe UI", 20)
        )
        self.input_braille.pack(pady=10)

        # --- Frame de Botones de Acción ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)

        # Botón Convertir
        ctk.CTkButton(
            btn_frame,
            text="Convertir",
            font=("Segoe UI", 20, "bold"),
            fg_color="#3d79e1",
            hover_color="#2e61bb",
            corner_radius=30,
            width=200,
            height=50,
            command=self.convert
        ).pack(side="left", padx=10)

        # Botón Imprimir PDF
        ctk.CTkButton(
            btn_frame,
            text="Imprimir PDF",
            font=("Segoe UI", 20, "bold"),
            fg_color="#28a745",
            hover_color="#218838",
            corner_radius=30,
            width=200,
            height=50,
            command=self.generar_pdf
        ).pack(side="left", padx=10)

        # --- Resultado ---
        ctk.CTkLabel(
            self, 
            text="Resultado:", 
            font=("Segoe UI", 14), 
            text_color="#cccccc"
        ).pack()

        self.output_text = ctk.CTkTextbox(
            self, width=600, height=100, corner_radius=10, 
            fg_color="#2d2d2d", text_color="white", font=("Segoe UI", 14) 
        )
        self.output_text.pack(pady=10)

        # Botón regresar
        ctk.CTkButton(
            self,
            text="Regresar",
            font=("Segoe UI", 20, "bold"),
            fg_color="#401a63",
            hover_color="#5e4574",
            corner_radius=30,
            width=250,
            height=50,
            command=lambda: controller.show_frame(MenuScreen)
        ).pack(pady=20)

    def convert(self):
        """
        Obtiene el texto en Braille del usuario, lo valida y lo traduce a texto normal.
        Actualiza el cuadro de texto de salida con el resultado.
        """
        from util import is_valid_braille
        
        raw_braille = self.input_braille.get("0.0", "end").strip()
        braille = clean_input(raw_braille)

        if not braille:
            return

        if not is_valid_braille(braille):
            messagebox.showerror("Error", "Texto inválido. Use solo caracteres Braille.")
            return

        result = self.translator.braille_to_text(braille)

        self.output_text.delete("0.0", "end")
        self.output_text.insert("0.0", result)

    def generar_pdf(self):
        """
        Genera un archivo PDF que contiene el texto Braille original y su traducción.

        Lógica del proceso:
        1. Verifica que haya contenido para traducir.
        2. Abre un cuadro de diálogo para que el usuario elija dónde guardar.
        3. Configura el Canvas de ReportLab (tamaño A4).
        4. Registra fuentes compatibles con Braille y texto normal.
        5. Escribe el contenido en el PDF.
        """
        texto_braille = self.input_braille.get("0.0", "end").strip()
        texto_traducido = self.output_text.get("0.0", "end").strip()

        if not texto_braille or not texto_traducido:
            messagebox.showwarning("Advertencia", "Primero debes convertir un texto para poder imprimirlo.")
            return

        # 1. Abrir diálogo para guardar archivo
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar PDF"
        )

        if not filename:
            return # El usuario canceló la operación

        try:
            # 2. Configuración del Canvas
            c = canvas.Canvas(filename, pagesize=A4)
            ancho, alto = A4
            
            # --- SELECCIÓN DE FUENTES ---
            font_name = "Helvetica" # Fallback por defecto
            
            try:
                # INTENTO 1: Segoe UI Symbol (para Braille)
                ruta_fuente = os.path.join(os.environ['WINDIR'], 'Fonts', 'seguisym.ttf')
                pdfmetrics.registerFont(TTFont('FuenteBraille', ruta_fuente))
                font_name = 'FuenteBraille'
                
            except Exception:
                try:
                    # INTENTO 2: Arial (Backup)
                    ruta_fuente = os.path.join(os.environ['WINDIR'], 'Fonts', 'arial.ttf')
                    pdfmetrics.registerFont(TTFont('ArialBackup', ruta_fuente))
                    font_name = 'ArialBackup'
                except:
                    print("Advertencia: No se pudo cargar ninguna fuente TTF del sistema.")
            
            # 3. Dibujar contenido en el PDF
            
            # Título principal
            c.setFont(font_name, 24)
            c.drawCentredString(ancho / 2, alto - 50, "Transcriptor Braille")
            
            # Línea separadora
            c.setLineWidth(1)
            c.line(50, alto - 60, ancho - 50, alto - 60)

            # --- Bloque Texto Braille ---
            c.setFont(font_name, 14)
            c.drawString(50, alto - 100, "Texto en Braille:")
            
            # Configuración para word-wrap
            text_object_braille = c.beginText(50, alto - 120)
            text_object_braille.setFont(font_name, 20)
            
            lineas_braille = simpleSplit(texto_braille, font_name, 20, ancho - 100)
            for linea in lineas_braille:
                text_object_braille.textLine(linea)
            c.drawText(text_object_braille)

            # Calcular posición dinámica para el siguiente bloque
            y_pos = alto - 120 - (len(lineas_braille) * 25) - 40
            
            # --- Bloque Texto Traducido ---
            c.setFont(font_name, 14)
            c.drawString(50, y_pos, "Traducción a Texto:")
            
            text_object_traducido = c.beginText(50, y_pos - 30)
            text_object_traducido.setFont(font_name, 12)
            
            lineas_traducido = simpleSplit(texto_traducido, font_name, 12, ancho - 100)
            for linea in lineas_traducido:
                text_object_traducido.textLine(linea)
            c.drawText(text_object_traducido)

            # Pie de página
            c.setFont("Helvetica", 10)
            c.drawCentredString(ancho / 2, 30, "Generado por Transcriptor Braille - 2025")

            # Guardar archivo
            c.save()
            messagebox.showinfo("Éxito", "PDF generado correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}")