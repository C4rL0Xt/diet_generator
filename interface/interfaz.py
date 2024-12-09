import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Modern styling
from threading import Thread
from time import sleep
from core.models import DietaGenerator
from core.utils import calcular_imc

class DietaApp:
    def __init__(self, root):
        # Configuración de la ventana
        self.root = root
        self.root.title("✨ Generador de Dietas Saludables ✨")
        self.center_window(900, 700)
        self.root.config(bg="#f8f5f2")  # Fondo aesthetic

        # Fondo personalizado
        self.background_image = ImageTk.PhotoImage(Image.open("background.jpg").resize((900, 700)))
        bg_label = tk.Label(self.root, image=self.background_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Encabezado
        title = tk.Label(
            self.root,
            text="✨ Generador de Dietas ✨",
            font=("Lobster", 36, "bold"),
            fg="#6c5ce7",
            bg="#f8f5f2",
        )
        title.pack(pady=20)

        # Marco principal
        main_frame = tk.Frame(self.root, bg="#ffffff", bd=10, relief="groove")
        main_frame.pack(pady=20, padx=20)

        # Entrada de peso
        self.create_input(main_frame, "Peso (kg):", "peso_entry")

        # Entrada de altura
        self.create_input(main_frame, "Altura (m):", "altura_entry")

        # Selección de sexo
        self.create_combobox(main_frame, "Sexo:", ["Masculino", "Femenino"], "sexo_combobox")

        # Selección de preferencias
        self.create_combobox(main_frame, "Tipo de alimentación:", ["Normal", "Vegetariana", "Vegana"], "pref_combobox")

        # Botón con animación
        self.generar_button = tk.Button(
            main_frame,
            text="✨ Generar Dieta ✨",
            font=("Montserrat", 16),
            bg="#81ecec",
            fg="#2d3436",
            activebackground="#74b9ff",
            activeforeground="#ffffff",
            cursor="hand2",
            command=self.on_generate_click,
        )
        self.generar_button.pack(pady=20, ipadx=10)

        # Área de resultados
        self.dieta_frame = tk.Frame(main_frame, bg="#f7f1e3", bd=5, relief="ridge")
        self.dieta_frame.pack(pady=10)
        self.dieta_text = tk.Text(
            self.dieta_frame,
            wrap=tk.WORD,
            height=15,
            width=60,
            bg="#f7f1e3",
            fg="#2d3436",
            font=("Montserrat", 12),
            relief="flat",
        )
        self.dieta_text.pack(pady=10)

        # Indicador de carga
        self.loading_label = tk.Label(
            self.root,
            text="Cargando...",
            font=("Montserrat", 14),
            fg="#d63031",
            bg="#f8f5f2",
        )
        self.loading_label.place_forget()

        # Objeto generador de dieta
        self.dieta_generator = DietaGenerator()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_input(self, parent, label_text, entry_var_name):
        """Crea un campo de entrada aesthetic."""
        frame = tk.Frame(parent, bg="#ffffff")
        frame.pack(fill=tk.X, pady=5)
        label = tk.Label(frame, text=label_text, font=("Montserrat", 14), bg="#ffffff", fg="#2d3436")
        label.pack(side=tk.LEFT, padx=10)
        entry = ttk.Entry(frame, font=("Montserrat", 12))
        entry.pack(side=tk.RIGHT, padx=10, pady=5, ipadx=10)
        setattr(self, entry_var_name, entry)

    def create_combobox(self, parent, label_text, values, combobox_var_name):
        """Crea un combobox aesthetic."""
        frame = tk.Frame(parent, bg="#ffffff")
        frame.pack(fill=tk.X, pady=5)
        label = tk.Label(frame, text=label_text, font=("Montserrat", 14), bg="#ffffff", fg="#2d3436")
        label.pack(side=tk.LEFT, padx=10)
        combobox = ttk.Combobox(frame, values=values, state="readonly", font=("Montserrat", 12))
        combobox.pack(side=tk.RIGHT, padx=10, pady=5)
        setattr(self, combobox_var_name, combobox)

    def on_generate_click(self):
        """Muestra el indicador de carga y genera la dieta en segundo plano."""
        self.generar_button.config(state="disabled")
        self.loading_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

        def background_task():
            self.generar_dieta()
            self.generar_button.config(state="normal")
            self.loading_label.place_forget()

        Thread(target=background_task).start()

    def generar_dieta(self):
        """Genera una dieta aesthetic."""
        try:
            peso = float(self.peso_entry.get())
            altura = float(self.altura_entry.get())
            sexo = self.sexo_combobox.get()
            preferencias = self.pref_combobox.get()

            if not sexo or not preferencias:
                raise ValueError("Debe seleccionar el sexo y el tipo de alimentación.")

            sleep(2)  # Simula un retraso en el cálculo
            imc = calcular_imc(peso, altura)
            dieta = self.dieta_generator.generar_dieta(imc, sexo, preferencias)

            self.dieta_text.delete(1.0, tk.END)
            self.dieta_text.insert(tk.END, dieta)
        except ValueError as e:
            messagebox.showerror("Error", f"Error: {str(e)}")