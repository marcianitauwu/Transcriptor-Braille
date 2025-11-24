import tkinter as tk
import ctypes
import sys
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk 

from translator import BrailleTranslator
from utils import clean_input, is_valid_text, is_braille

class BrailleApp(ctk.CTk):
    """Aplicación principal para la traducción de texto a Braille y viceversa.
    
    Esta clase crea la ventana principal de la aplicación y maneja la navegación
    entre las diferentes pantallas (inicio, menú, conversiones).
    """
    
    def __init__(self):
        """Inicializa la aplicación Braille.
        
        Configura la ventana principal, establece el ícono, crea el traductor
        y prepara todas las pantallas de la aplicación.
        """
        super().__init__()
        
        self.geometry("850x600")
        
        # Para ponerle inoconito jeje
        if sys.platform == "win32":
            app_id = "samira.braille.transcriptor.1.0"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        try:
            self.iconbitmap("src/img/icono2.ico")
        except:
            pass

        self.title("Transcriptor Braille")

        self.translator = BrailleTranslator()

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (StartScreen, MenuScreen, TextToBrailleScreen, BrailleToTextScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(StartScreen)

    def show_frame(self, screen):
        """Muestra la pantalla especificada.
        
        Args:
            screen (class): Clase de la pantalla a mostrar.
        """
        frame = self.frames[screen]
        frame.tkraise()

# Pantallita de inicio
class StartScreen(ctk.CTkFrame):
    """Pantalla de inicio de la aplicación.
    
    Muestra el título de la aplicación con una imagen de fondo
    y un botón para comenzar.
    """

    def __init__(self, parent, controller):
        """Inicializa la pantalla de inicio.
        
        Args:
            parent: Widget padre que contendrá esta pantalla.
            controller (BrailleApp): Instancia principal de la aplicación.
        """
        super().__init__(parent, fg_color="#1e1e1e")
        self.controller = controller

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
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

        # Botón de "Comenzar"
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
        """Redimensiona la imagen de fondo cuando cambia el tamaño de la ventana.
        
        Args:
            event: Evento de configuración de tkinter con las nuevas dimensiones.
        """
        if self.original_image:

            new_width = event.width
            new_height = event.height

            resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_image)

            if hasattr(self, '_bg_image_id'):
                self.canvas.itemconfig(self._bg_image_id, image=self.bg_photo)
            else:
                self._bg_image_id = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
                self.canvas.lower(self._bg_image_id) 

            # Reajustar el texto y el botonsito de "Comenzar"
            self.canvas.coords(self.title_id, new_width / 2, new_height * 0.2)
            self.canvas.coords(self.button_id, new_width / 2, new_height * 0.8)


# Pantalla 2, escoger opción
class MenuScreen(ctk.CTkFrame):
    """Pantalla de menú principal.
    
    Permite al usuario seleccionar entre convertir texto a Braille
    o Braille a texto, o regresar a la pantalla de inicio.
    """
    
    def __init__(self, parent, controller):
        """Inicializa la pantalla de menú.
        
        Args:
            parent: Widget padre que contendrá esta pantalla.
            controller (BrailleApp): Instancia principal de la aplicación.
        """
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
    """Pantalla de conversión de texto a Braille.
    
    Permite al usuario ingresar texto normal y obtener su
    representación en Braille.
    """
    
    def __init__(self, parent, controller):
        """Inicializa la pantalla de conversión texto a Braille.
        
        Args:
            parent: Widget padre que contendrá esta pantalla.
            controller (BrailleApp): Instancia principal de la aplicación.
        """
        super().__init__(parent, fg_color="#39426E")
        self.controller = controller
        self.translator = controller.translator

        ctk.CTkLabel(
            self,
            text="Texto ➜ Braille",
            text_color="white",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(30, 20))

        ctk.CTkLabel(self, text="Texto de entrada:", font=("Segoe UI", 14), text_color="#cccccc").pack()
        
        self.input_text = ctk.CTkTextbox(
            self, width=600, height=100, corner_radius=10, 
            fg_color="#2d2d2d", text_color="white", font=("Segoe UI", 14)
        )
        self.input_text.pack(pady=10)

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

        ctk.CTkLabel(self, text="Resultado:", font=("Segoe UI", 14), text_color="#cccccc").pack()

        self.output_text = ctk.CTkTextbox(
            self, width=600, height=100, corner_radius=10, 
            fg_color="#2d2d2d", text_color="white", font=("Segoe UI", 14)
        )
        self.output_text.pack(pady=10)

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
        """Convierte el texto ingresado a Braille.
        
        Obtiene el texto del campo de entrada, lo valida y muestra
        el resultado de la conversión. Muestra un mensaje de error
        si el texto es inválido.
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
    """Pantalla de conversión de Braille a texto.
    
    Permite al usuario ingresar caracteres Braille y obtener
    su representación en texto normal.
    """
    
    def __init__(self, parent, controller):
        """Inicializa la pantalla de conversión Braille a texto.
        
        Args:
            parent: Widget padre que contendrá esta pantalla.
            controller (BrailleApp): Instancia principal de la aplicación.
        """
        super().__init__(parent, fg_color="#354A6D")
        self.controller = controller
        self.translator = controller.translator

        ctk.CTkLabel(
            self,
            text="Braille ➜ Texto",
            text_color="white",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(30, 20))

        ctk.CTkLabel(self, text="Texto Braille:", font=("Segoe UI", 14), text_color="#cccccc").pack()

        self.input_text = ctk.CTkTextbox(
            self, width=600, height=100, corner_radius=10,
            fg_color="#2d2d2d", text_color="white", font=("Segoe UI", 14)
        )
        self.input_text.pack(pady=10)

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

        self.output_text = ctk.CTkTextbox(
            self, width=600, height=100, corner_radius=10,
            fg_color="#2d2d2d", text_color="white", font=("Segoe UI", 14)
        )
        self.output_text.pack(pady=10)

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
        """Convierte el Braille ingresado a texto.
        
        Obtiene el Braille del campo de entrada, lo valida y muestra
        el resultado de la conversión. Muestra un mensaje de error
        si el Braille es inválido.
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