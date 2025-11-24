import tkinter as tk
from tkinter import messagebox

from translator import BrailleTranslator
from util import clean_input, is_valid_text, is_braille

class BrailleApp(tk.Tk):
    """Aplicación principal para la traducción de texto a Braille y viceversa.
    
    Esta clase crea la ventana principal de la aplicación y maneja la navegación
    entre las diferentes pantallas (inicio, menú, conversiones).
    """
    
    def __init__(self):
        """Inicializa la aplicación Braille.
        
        Configura la ventana principal, crea el traductor y prepara todas 
        las pantallas de la aplicación.
        """
        super().__init__()
        
        self.title("Transcriptor Braille - Multipantalla")
        self.geometry("800x600")

        # Instancia única del traductor compartida por todas las pantallas
        self.translator = BrailleTranslator()

        # Contenedor principal donde se apilan las "hojas" (frames)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Inicializamos todas las pantallas y las guardamos en memoria
        for F in (StartPage, MenuPage, TextToBraillePage, BrailleToTextPage):
            frame = F(container, self)
            self.frames[F] = frame
            # Poner todas las pantallas en la misma celda, una encima de otra
            frame.grid(row=0, column=0, sticky="nsew")

        # Mostrar la primera pantalla
        self.show_frame(StartPage)

    def show_frame(self, cont):
        """Muestra la pantalla especificada.
        
        Args:
            cont (class): Clase de la pantalla a mostrar.
        """
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    """Pantalla de inicio de la aplicación.
    
    Muestra el título de la aplicación y un botón para comenzar.
    """
    
    def __init__(self, parent, controller):
        """Inicializa la pantalla de inicio.
        
        Args:
            parent: Widget padre que contendrá esta pantalla.
            controller (BrailleApp): Instancia principal de la aplicación.
        """
        super().__init__(parent)
        
        label = tk.Label(self, text="TRANSCRIPTOR BRAILLE", font=("Arial", 30, "bold"))
        label.pack(pady=80)

        # Botón simple para ir al menú
        btn = tk.Button(self, text="Comenzar", font=("Arial", 14),
                        command=lambda: controller.show_frame(MenuPage),
                        width=20, height=2, bg="#cccccc")
        btn.pack()


class MenuPage(tk.Frame):
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
        super().__init__(parent)
        
        label = tk.Label(self, text="Seleccione una opción", font=("Arial", 20))
        label.pack(pady=40)

        # Opción 1
        btn1 = tk.Button(self, text="Texto → Braille", font=("Arial", 14),
                         command=lambda: controller.show_frame(TextToBraillePage),
                         width=25, height=2)
        btn1.pack(pady=10)

        # Opción 2
        btn2 = tk.Button(self, text="Braille → Texto", font=("Arial", 14),
                         command=lambda: controller.show_frame(BrailleToTextPage),
                         width=25, height=2)
        btn2.pack(pady=10)

        # Regresar
        btn_back = tk.Button(self, text="Volver al Inicio", font=("Arial", 10),
                             command=lambda: controller.show_frame(StartPage))
        btn_back.pack(pady=40)


class TextToBraillePage(tk.Frame):
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
        super().__init__(parent)
        self.controller = controller  # Para acceder al traductor

        tk.Label(self, text="Texto ➜ Braille", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(self, text="Texto de entrada:").pack()
        self.input_text = tk.Text(self, width=60, height=5, font=("Arial", 12))
        self.input_text.pack(pady=5)

        btn_convert = tk.Button(self, text="Convertir", command=self.convert, bg="#2196F3", fg="white")
        btn_convert.pack(pady=10)

        tk.Label(self, text="Resultado:").pack()
        self.output_text = tk.Text(self, width=60, height=5, font=("Arial", 12))
        self.output_text.pack(pady=5)

        tk.Button(self, text="Regresar al Menú", command=lambda: controller.show_frame(MenuPage)).pack(pady=20)

    def convert(self):
        """Convierte el texto ingresado a Braille.
        
        Obtiene el texto del campo de entrada, lo valida y muestra
        el resultado de la conversión. Muestra un mensaje de error
        si el texto es inválido.
        """
        raw = self.input_text.get("1.0", "end-1c")
        text = clean_input(raw)
        
        if not text:
            return

        if not is_valid_text(text):
            messagebox.showerror("Error", "Texto inválido.")
            return

        # Usamos el traductor que vive en el controlador principal
        res = self.controller.translator.text_to_braille(text)
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", res)


class BrailleToTextPage(tk.Frame):
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
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Braille ➜ Texto", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(self, text="Texto de entrada:").pack()
        self.input_text = tk.Text(self, width=60, height=5, font=("Arial", 12))
        self.input_text.pack(pady=5)

        btn_convert = tk.Button(self, text="Convertir", command=self.convert, bg="#2196F3", fg="white")
        btn_convert.pack(pady=10)

        tk.Label(self, text="Resultado:").pack()
        self.output_text = tk.Text(self, width=60, height=5, font=("Arial", 12))
        self.output_text.pack(pady=5)

        tk.Button(self, text="Regresar al Menú", command=lambda: controller.show_frame(MenuPage)).pack(pady=20)

    def convert(self):
        """Convierte el Braille ingresado a texto.
        
        Obtiene el Braille del campo de entrada, lo valida y muestra
        el resultado de la conversión. Muestra un mensaje de error
        si el Braille es inválido.
        """
        raw = self.input_text.get("1.0", "end-1c")
        text = clean_input(raw)
        
        if not text:
            return

        if not is_braille(text):
            messagebox.showerror("Error", "Caracteres Braille inválidos.")
            return

        res = self.controller.translator.braille_to_text(text)
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", res)
