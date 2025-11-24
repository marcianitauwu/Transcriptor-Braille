# gui.py
import tkinter as tk
import ctypes
import sys
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk 

from translator import BrailleTranslator
from util import clean_input, is_valid_text, is_braille

class BrailleApp(ctk.CTk):
    """Ventana principal de la aplicación del Transcriptor Braille

    Maneja:
    - La creación de todas las pantallas (frames)
    - La navegación entre pantallas
    - La instancia global del traductor (BrailleTranslator)
    """
    def __init__(self):
        
        """Inicializa la ventana principal y configura los frames de la aplicación.
        """
        super().__init__()
        
        self.geometry("850x600")
        
        # Icono de la aplicación en Windows
        if sys.platform == "win32":
            app_id = "samira.braille.transcriptor.1.0"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        try:
            self.iconbitmap("src/img/icono.ico")
        except:
            pass

        self.title("Transcriptor Braille")

        # Instancia del traductor que usan todas las pantallas
        self.translator = BrailleTranslator()

        # Contenedor principal donde se colocan todas las pantallas
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        # Diccionario que guarda las pantallas
        self.frames = {}


        # Se inicializan y registran todas las pantallas
        for F in (StartScreen, MenuScreen, TextToBrailleScreen, BrailleToTextScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)


        # Mostrar la pantalla inicial
        self.show_frame(StartScreen)

    def show_frame(self, screen):
        """Método para mostrar en pantalla un frame específico.
        """
        frame = self.frames[screen]
        frame.tkraise()

# Pantallita de inicio
class StartScreen(ctk.CTkFrame):
    """Pantalla de bienvenidad de la aplciación

    Incluye fondo con imagen, título y botón para comenzar.
    """
    def __init__(self, parent, controller):
        """Inicializa la pantalla de bienvenida.
        """
        
        super().__init__(parent, fg_color="#1e1e1e")
        self.controller = controller

        # Canvas para manejar el fondo dinámico
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Intentar cargar imagen de fondo
        try:
            self.original_image = Image.open("src/img/fondito.png")
            self.canvas.bind("<Configure>", self.resize_background)
        except Exception as e:
            pass

        # Texto "Transcriptor Braille" 
        self.title_id = self.canvas.create_text(
            self.winfo_width()/2, 100,
            text="TRANSCRIPTOR BRAILLE",
            fill="#FFFFFF", 
            font=("Segoe UI", 82, "bold"),
            anchor="center" 
        )

        # Botonsito de "Comenzar"
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
        """Redimensiona la imagen de fondo cuando se redimensiona la ventana.
        """
        
        if self.original_image:

            new_width = event.width
            new_height = event.height

            resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_image)

            # Si la imagen ya existe en el canvas, actualizarla
            if hasattr(self, '_bg_image_id'):
                self.canvas.itemconfig(self._bg_image_id, image=self.bg_photo)
            else:
                self._bg_image_id = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
                self.canvas.lower(self._bg_image_id) 

            # Reajustar el texto y el botonsito de "Comenzar"
            self.canvas.coords(self.title_id, new_width / 2, new_height * 0.2)
            self.canvas.coords(self.button_id, new_width / 2, new_height * 0.8)


# Pantalla 2, menú de opciones
class MenuScreen(ctk.CTkFrame):
    """Pantalla de menú principal que permite elegir entre:
    - Texto → Braille
    - Braille → Texto
    - Regresar a la pantalla inicial
    """
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#304171")
        self.controller = controller

        # Titulito
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
            fg_color="#6F83E5",
            hover_color="#505DA1",
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
    Pantalla para convertir texto a Braille.
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

        # Entrada de texto
        ctk.CTkLabel(self, text="Texto de entrada:", font=("Segoe UI", 14), text_color="#cccccc").pack()
        
        self.input_text = ctk.CTkTextbox(
            self, width=600, height=100, corner_radius=10, 
            fg_color="#2d2d2d", text_color="white", font=("Segoe UI", 14)
        )
        self.input_text.pack(pady=10)

        # Botón convertir
        ctk.CTkButton(
            self,
            text="Convertir",
            font=("Segoe UI", 20, "bold"),
            fg_color="#3d79e1",
            hover_color="#2e61bb",
            corner_radius=30,
            width=250,
            height=50,
            command=self.convert
        ).pack(pady=20)

        # Resultado
        ctk.CTkLabel(self, text="Resultado:", font=("Segoe UI", 14), text_color="#cccccc").pack()

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
        """Convierte el texto de entrada a Braille y muestra el resultado.
        """
        raw_text = self.input_text.get("0.0", "end").strip()
        text = clean_input(raw_text)

        if not text:
             return

        if not is_valid_text(text):
            messagebox.showerror("Error", "Texto inválido.")
            return

        result = self.translator.text_to_braille(text)

        self.output_text.delete("0.0", "end")
        self.output_text.insert("0.0", result)


# Pantalla 4, aquí se convierte de puntitos a texto
class BrailleToTextScreen(ctk.CTkFrame):
    """
    Pantalla para convertir Braille a texto.
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

        # Entrada de Braille
        ctk.CTkLabel(self, text="Texto Braille:", font=("Segoe UI", 14), text_color="#cccccc").pack()

        self.input_text = ctk.CTkTextbox(
            self, width=600, height=100, corner_radius=10,
            fg_color="#2d2d2d", text_color="white", font=("Segoe UI", 14)
        )
        self.input_text.pack(pady=10)

        # Botón convertir
        ctk.CTkButton(
            self,
            text="Convertir",
            font=("Segoe UI", 20, "bold"),
            fg_color="#6F83E5",
            hover_color="#505DA1",
            corner_radius=30,
            width=250,
            height=50,
            command=self.convert
        ).pack(pady=20)

        ctk.CTkLabel(self, text="Resultado:", font=("Segoe UI", 14), text_color="#cccccc").pack()

        # Resultado
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
        """Convierte el texto Braille de entrada a texto normal y muestra el resultado.
        """
        raw_text = self.input_text.get("0.0", "end").strip()
        text = clean_input(raw_text)

        if not text:
            return

        if not is_braille(text):
            messagebox.showerror("Error", "Braille inválido.")
            return

        result = self.translator.braille_to_text(text)

        self.output_text.delete("0.0", "end")
        self.output_text.insert("0.0", result)