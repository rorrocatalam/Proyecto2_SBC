import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Directorio con imagenes de animales
animals_path = "C:/Users/rodri/Desktop/Proyecto2_SBCEI/Opcionales/Animales/"

class Interface:
    def __init__(self, root):
        # Ventana principal
        self.root = root
        self.root.title("Interfaz")

        # Dimensiones
        self.width, self.height = 1920, 1080
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)

        # Tamano de la fuente
        fontsize = 24
        # Configuracion de estilo
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", fontsize))
        style.configure("TButton", font=("Helvetica", fontsize))
        style.configure("TScale", font=("Helvetica", fontsize))
        
        # Frame izquierdo para preguntas
        self.left_frame = ttk.Frame(self.root, width=self.width//2, height=self.height, relief='solid', borderwidth=1)
        self.left_frame.place(x=0, y=0, width=self.width//2, height=self.height)
        # Sub-frame para centrar las preguntas
        self.center_left_frame = ttk.Frame(self.left_frame)
        self.center_left_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Frame superior derecho para el grafico con resultados
        self.top_right_frame = ttk.Frame(self.root, width=self.width//2, height=self.height//2, relief='solid', borderwidth=1)
        self.top_right_frame.place(x=self.width//2, y=0, width=self.width//2, height=self.height//2)
        
        # Frame inferior derecho para imagen del animal
        self.bottom_right_frame = ttk.Frame(self.root, width=self.width//2, height=self.height//2, relief='solid', borderwidth=1)
        self.bottom_right_frame.place(x=self.width//2, y=self.height//2, width=self.width//2, height=self.height//2)
        
        # Slider entre -1 y 1 para ingresar respuestas
        self.slider_label = ttk.Label(self.center_left_frame, text="Pregunta:")
        self.slider_label.pack(pady=(0, 60))
        self.slider = ttk.Scale(self.center_left_frame, from_=-1, to=1, orient=tk.HORIZONTAL, length=350)
        self.slider.pack(pady=10)
        
        # Etiquetas del slider y posicionamiento
        self.slider_label1 = ttk.Label(self.center_left_frame, text="No", font=("Helvetica", 18))
        self.slider_label1.place(relx=0.05, rely=0.6, anchor=tk.CENTER)
        self.slider_label2 = ttk.Label(self.center_left_frame, text="No sé", font=("Helvetica", 18))
        self.slider_label2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.slider_label3 = ttk.Label(self.center_left_frame, text="Sí", font=("Helvetica", 18))
        self.slider_label3.place(relx=0.95, rely=0.6, anchor=tk.CENTER)

        # Boton para continuar
        self.save_button = ttk.Button(self.center_left_frame, text="Continuar", command=self.save_ans)
        self.save_button.pack(pady=(120, 10))  # Más abajo

        # Variable para almacenar la respuesta y control del flujo
        self.ans = tk.DoubleVar()
        self.cont = tk.BooleanVar()

    def show_plot(self, fig):
        """
        Metodo para mostrar grafico con resultados en el frame superior derecho
        """
        # Limpiar el frame antes de mostrar el grafico
        for widget in self.top_right_frame.winfo_children():
            widget.destroy()
        
        # Canvas para el gráfico y agregarlo al frame
        canvas = FigureCanvasTkAgg(fig, master=self.top_right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

    def show_img(self, animal, vc):
        # Limpiar el frame antes de mostrar la nueva imagen
        for widget in self.bottom_right_frame.winfo_children():
            widget.destroy()
        
        # Mensaje a mostrar
        msg = f"Su animal es {animal} con certeza {vc}"
        msg_label = ttk.Label(self.bottom_right_frame, text=msg, font=("Helvetica", 24))
        msg_label.pack(pady=(10, 20))

        # Mostrar la imagen en el frame
        imagen = Image.open(f"{animals_path}{animal}.jpg")
        # Redimensionamiento la imagen
        frame_width = self.width // 2
        frame_height = self.height // 2
        max_width = int(frame_width * 0.9)
        max_height = int(frame_height * 0.9)
        imagen.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        imagen = ImageTk.PhotoImage(imagen)
        label = tk.Label(self.bottom_right_frame, image=imagen)
        label.image = imagen
        label.pack()

    def save_ans(self):
        self.ans.set(self.slider.get())
        self.cont.set(True)
        print("Respuesta guardada:", self.ans.get())

    def ask_user(self, prem):
        """
        Metodo para preguntar al usuario y obtener su respuesta por medio del slider
        """
        self.slider_label.config(text=prem)
        self.cont.set(False)
        self.root.wait_variable(self.cont)  # Esperar hasta que el botón de continuar sea presionado
        return self.ans.get()

if __name__ == "__main__":
    # Ventana principal
    root = tk.Tk()
    app = Interface(root)
    
    # Inicializacion vacia del frame con grafico
    fig = plt.figure()
    app.show_plot(fig)

    respuesta1 = app.ask_user("¿Qué opinas del clima?")
    print("Respuesta 1:", respuesta1)

    app.show_img("murciélago",1)
    # Ejemplo de uso
    fig, ax = plt.subplots(figsize=(5, 2.5))
    ax.plot([0, 1, 2, 3], [10, 20, 25, 30])
    ax.set_title("Gráfico de Línea")
    app.show_plot(fig)

    respuesta2 = app.ask_user("¿Cómo te sientes hoy?")
    print("Respuesta 2:", respuesta2)
    
    fig2, ax2 = plt.subplots(figsize=(5, 2.5))
    ax2.bar([0, 1, 2, 3], [10, 20, 25, 30])
    ax2.set_title("Gráfico de Barras")
    app.show_plot(fig2)

    app.show_img("perro",1)
    
    root.mainloop()