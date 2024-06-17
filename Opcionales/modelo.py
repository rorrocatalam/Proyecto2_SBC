#=============================================================================
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Directorio con imagenes de animales
animals_path = "C:/.../Proyecto2_SBCEI/Opcionales/Animales/"

#=============================================================================
# Parametros de control

alpha   = 0.7   # Para detener el AEI cuando se demuestre una hipotesis
beta    = 0.2   # Para determinar si un hecho tiene un grado de certidumbre suficiente
gamma   = 0.85  # Para determinar si se debe seguir buscando un mejor grado de certidumbre para un hecho
epsilon = 0.5   # Para determinar cuando una regla tiene un grado de certidumbre suficiente para inferir una hipotesis
delta   = 0.2   # Para determinar si el grado de certidumbre es suficiente para gatillar una regla (es variable)

#=============================================================================
# Operadores para propagar valores de certidumbre

def max_mod(lst):
    """
    Funcion que retorna el numero cuyo valor absoluto es el maximo,
    prefiriendo valores negativos en caso de empate.
    """
    if not lst:
        return None
    return max(lst, key=lambda x: (abs(x), x if x < 0 else -float('inf')))

def min_mod(lst):
    """
    Funcion que retorna el número cuyo valor absoluto es el minimo,
    prefiriendo valores negativos en caso de empate.
    """
    if not lst:
        return None
    return min(lst, key=lambda x: (abs(x), x if x < 0 else float('inf')))

#=============================================================================
# Estructuras basicas

class Fact:
    def __init__(self, prem, vc):
        self.prem   = prem
        self.vc     = vc
    
    def hypothesis(self, fb, rb, hs):
        """
        Metodo que obtiene el vc de una hipotesis
        """
        # Si el hecho esta en la base de hechos
        if fb.is_in(self.prem):
            vc = fb.get_vc(self.prem)
            # El hecho sera relevante solo si existe suficiente certeza
            if abs(vc) >= beta:
                return vc
        
        # El hecho no esta en la base de hechos o no hay conocimiento suficiente (no supera el umbral beta)
        rule_lst = rb.prem_in_con(self.prem)
        # Caso Base (lsta vacía -> no hay reglas que tienen como conclusion la premisa)
        if not rule_lst:
            # Se pregunta al usuario en caso de no haber preguntado antes
            if not self.prem in fb.lst_ques:
                vc = fb.ask_user(self.prem)
                return vc
            else:
                return 0
        # Se revisan reglas que podrian probar la hipotesis
        else: 
            # Inicializacion de conocimiento acumulado
            vc_acc = 0.0
            # Indicador de exito de reglas
            i = False

            # Se recorren las reglas hasta superar el umbral o no queden reglas
            for rule in rule_lst:
                
                # Salida de la regla
                res = rule.evaluate(fb,rb,self.prem, hs)
                if res != None:
                    # Se indica que al menos una regla se gatillo
                    i = True
                    # Se actualiza el vc acumulado
                    vc_acc =  max_mod([vc_acc, res])
                    # Se ve si se supero el umbral gamma
                    if abs(vc_acc) >= gamma:
                        # Se crea el hecho
                        fact = Fact(self.prem, vc_acc)
                        # Se agrega el hecho a la base de hechos
                        fb.add_mod_fact(fact)
                        # Se retorna al vc acumulado
                        return vc_acc
            
            # No se supera el umbral con las reglas
            if i: 
                # Se crea el hecho
                fact = Fact(self.prem, vc_acc)
                # Se agrega el hecho a la base de hechos
                fb.add_mod_fact(fact)
                # Se retorna al vc acumulado
                return vc_acc
            
            # Ninguna regla se pudo gatillar y por ende se pregunta el usuario
            else:
                # Si se encuentra en la base de hipotesis de alto nivel
                if hs.is_in(self.prem):
                    # Se retorna None
                    return None

                # Se pregunta al usuario en caso de no haber preguntado antes
                elif not self.prem in fb.lst_ques:
                    vc = fb.ask_user(self.prem)
                    return vc
                
                else:
                    return 0
    
class Rule:
    def __init__(self, prem, con, vc):
        self.prem   = prem
        self.con    = con
        self.vc     = vc
        self.i      = False     # Indicador si la regla se ha evaluado
    
    def rule_preq(self, fb, delta_r):
        """
        Precalificador de reglas. Retorna True si sus premisas son desconocidas o superan el umbral
        """
        # Premisas de la base de hechos
        fb_lst_prem = fb.lst_prem
        # Se revisan las premisas
        for prem in fb_lst_prem:
            # Si la premisa esta, se revisa su vc
            if fb.is_in(prem):
                vc_r = fb.get_vc(prem)
                # La premisa es falsa si no supera el umbral
                if abs(vc_r) < abs(delta_r):
                    return False
        # Es factible evaluar la regla
        return True
    
    def evaluate(self, fb, rb, prem_obj, hs):
        """
        Metodo para evaluar una regla concentrandose en la informacion que se quiere obtener
        """
        # Como se intentara evaluar la regla, se cambia su indicador
        self.i = True

        # Parametros de la regla
        prem = self.prem 
        con = self.con
        vc = self.vc

        # vc de la conclusion que se quiere obtener
        index_r = con.index(prem_obj)
        vc_r = vc[index_r]
        # Umbral para seguir y gatillar regla
        delta_r = delta/vc_r

        # Se procede solo en caso de que sea factible evaluar la regla
        if self.rule_preq(fb, delta_r):
            # vc acumulado de la regla
            vc_acc = -10.0 # valor fuera de rango entre [-1,1]

            # Se ve cada premisa de la regla
            for prem_i in prem:
                # Se ve como hipotesis para obtener su valor
                h_i = Fact(prem_i, 0)
                # Se obtiene su valor de forma recursiva
                vc_i = h_i.hypothesis(fb, rb, hs)
                # Actualizacion del vc acumulado
                vc_acc = min_mod([vc_acc,vc_i])
                # Si no se supera el umbral, no vale la pena seguir con las demas premisas
                if abs(vc_acc) < abs(delta_r):
                    return None
            
            # Se gatilla la regla y se guardan resultados en la base de hechos
            i = 0
            while i < len(con):
                # Resultado conclusion
                res = vc_acc * vc[i]
                # Se crea el hecho
                fact_i = Fact(con[i], res)
                # Se guarda
                fb.add_mod_fact(fact_i)
                # Proxima conclusion
                i+=1
            
            # Se retorna la informacion que se estaba buscando, que ya esta presente en la base de hechos
            return fb.get_vc(prem_obj)
        # Ni siquiera fue factible evaluar la regla
        else:
            return None
            
#=============================================================================
# Conjuntos

class FactBase:
    def __init__(self, hs, app):
        self.lst_prem  = []
        self.lst_vc    = []
        self.hs         = hs
        self.app        = app
        self.lst_ques  = []

    def print_info(self):
        """
        Metodo para mostrar la informacion contenida en la base de hechos
        """
        i = 0
        # Se revisan las premisas
        for prem in self.lst_prem:
            # Se muestra su información
            print(f"{prem}: {self.lst_vc[i]}")
            i += 1
            
    def is_in(self, prem):
        """
        Metodo para saber si el hecho esta en la base de hechos, dada su premisa
        """
        # Retorno booleano si la regla se puede evaluar
        if prem in self.lst_prem:
            return True
        else:
            return False
    
    def add_mod_fact(self, fact):
        """
        Metodo para agregar o modificar hechos presentes en la base
        """
        # Premisa y valor del hecho
        prem = fact.prem
        vc = fact.vc
        
        # Se ya existe el hecho
        if self.is_in(prem):
            # Se busca su posicion
            index_f = self.lst_prem.index(prem)
            # vc del hecho
            vc_f = self.lst_vc[index_f]
            # Se actualiza si hay mayor certeza
            if max_mod([vc, vc_f]) == vc:
                self.lst_vc[index_f] = vc

        # Si no existe se annade
        else:
            # Guardar valores
            self.lst_prem.append(prem)
            self.lst_vc.append(vc)

    def get_vc(self, prem):
        """"
        Metodo para obtener el vc de una premisa presente en la base de hechos
        """
        # Posicion del hecho en la base de hechos
        index_f = self.lst_prem.index(prem)
        # Se retorna el vc del hecho
        return self.lst_vc[index_f]

    def ask_user(self, prem):
        """
        Metodo para agregar un hecho dada la entrada del usuario
        """
        # Se annade a la lsta de premisas preguntadas
        self.lst_ques.append(prem)

        # Se obtiene la respuesta del usuario
        q = f"¿Su {prem}?"
        n = round(self.app.ask_user(q),4)

        # Se actualiza el grafico
        self.app.show_plot(self.hs.plot_hyp())
        return n

class RuleBase:
    def __init__(self, rules):
        self.rules = rules

    def prem_in_con(self, prem):
        """
        Metodo para encontrar las reglas utiles que tienen como conclusion una determinada premisa
        """
        # lsta de reglas que cumplen requisito
        rule_lst = []

        # Se revisan todas las reglas presentes
        for rule in self.rules:
            #Si no se ha intentado evaluar la regla
            if not rule.i:
                # Conclusiones de la regla
                rule_con = rule.con
                # Si la premisa esta en las conclusiones se procede
                if prem in rule_con:
                    # Grados de implicacion de conclusiones de la regla
                    regla_vc = rule.vc
                    # Posicion de la premleta en conclusiones
                    index_prem = rule_con.index(prem)
                    # Grado de implicacion de la premisa
                    vc_prem =  regla_vc[index_prem]
                    # Si su grado de implicacion supera el umbral, la regla se considera util y se guarda
                    if abs(vc_prem) >= epsilon: 
                        rule_lst.append(rule)
        
        # Retorno lsta de reglas 
        return rule_lst
    
class HypothesisSet:
    def __init__(self, lst_hyp, app):
        self.lst_hyp = lst_hyp
        self.lst_prem = [fact.prem for fact in lst_hyp]
        self.lst_vc = [fact.vc for fact in lst_hyp]
        self.app = app

    def print_info(self):
        """
        Metodo para mostrar la informacion contenida en la base de hipotesis
        """
        i = 0
        # Se revisan las premisas
        for prem in self.lst_prem:
            # Se muestra su información
            print(f"{prem}: {self.lst_vc[i]}")
            i += 1

    def is_in(self, prem):
        """
        Metodo para saber si la hipotesis se encuentra en la base de hipotesis
        """
        # Retorno booleano si la hipotesis esta en la base de hipotesis
        if prem in self.lst_prem:
            return True
        else:
            return False
        
    def aei(self, fb, rb):
        """
        Metodo que ejecuta el AEI para todas las hipotesis de alto nivel
        """
        # Indice de la hipotesis
        idx_hyp = 0

        # Se recorren todas las hipotesis
        for hyp in self.lst_hyp:
            # Se obtiene su vc
            vc_hyp = hyp.hypothesis(fb, rb, self)
            if vc_hyp != None:
                # Se actualiza el vc de la lsta
                self.lst_vc[idx_hyp] = vc_hyp
                # Se actualiza el vc de la hipotesis
                hyp.vc = vc_hyp

                # Se ve si supera el umbral alpha
                if vc_hyp >= alpha:
                    # Animal en cuestion
                    animal = hyp.prem.split()[-1]
                    # Se muestra el animal 
                    self.app.show_img(animal, round(vc_hyp,2))
                    # Se actualiza el grafico
                    self.app.show_plot(self.plot_hyp())
                    # Cambio de texto para el boton
                    self.app.save_button.config(text="Finalizar")
                    # Muestro fin del programa en la seccion de preguntas
                    self.app.ask_user("Hipótesis demostrada con suficiente certeza")
                    # Se termina el proceso
                    return
            # Se actualiza el grafico
            self.app.show_plot(self.plot_hyp())
            # Siguiente hipotesis    
            idx_hyp += 1

        # Cambio de texto para el boton
        self.app.save_button.config(text="Finalizar")
        # Muestro fin del programa en la seccion de preguntas
        self.app.ask_user("Ninguna hipótesis se cumplió con suficiente certeza")
        return
    
    def plot_hyp(self):
        """
        Metodo que crea un grafico que muestra los vc de las hipotesis de alto nivel
        """
        # Nombre de los animales
        names = [hyp.split()[-1] for hyp in self.lst_prem]
        # Creacion de la figura
        fig, ax = plt.subplots(figsize=(10, 5))
        # Grafico de barras con cada vc
        ax.bar(names, self.lst_vc, color='orange', width=0.4)
        # Linea en y =0
        ax.axhline(0, color='black', linestyle='--')
        # Limites en y
        ax.set_ylim(-1, 1)
        # Rotacion de etiquetas
        plt.xticks(rotation=45, ha='right')
        # Títulos y etiquetas
        ax.set_xlabel('Animales')
        ax.set_ylabel('Valor de certeza')
        ax.set_title('Valor de certeza de cada animal')
        # Ajuste para evitar solapamientos
        plt.tight_layout()
        # Se retorna la figura
        return fig

class Interface:
    def __init__(self, root):
        # Ventana principal
        self.root = root
        self.root.title("Sistema basado en conocimiento con Encadenamiento Inverso")

        # Dimensiones
        self.width, self.height = 1080, 720
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)

        # Tamano de la fuente
        fontsize1 = int(self.width/80)
        fontsize2 = int(0.75*fontsize1)

        # Configuracion de estilo
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", fontsize1))
        style.configure("TButton", font=("Helvetica", fontsize1))
        style.configure("TScale", font=("Helvetica", fontsize1))
        
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
        self.slider_label1 = ttk.Label(self.center_left_frame, text="No", font=("Helvetica", fontsize2))
        self.slider_label1.place(relx=0.05, rely=0.6, anchor=tk.CENTER)
        self.slider_label2 = ttk.Label(self.center_left_frame, text="No sé", font=("Helvetica", fontsize2))
        self.slider_label2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.slider_label3 = ttk.Label(self.center_left_frame, text="Sí", font=("Helvetica", fontsize2))
        self.slider_label3.place(relx=0.95, rely=0.6, anchor=tk.CENTER)

        # Boton para continuar
        self.save_button = ttk.Button(self.center_left_frame, text="Continuar", command=self.save_ans)
        self.save_button.pack(pady=(120, 10))

        # Variable para almacenar la respuesta y control del flujo
        self.ans = tk.DoubleVar()
        self.cont = tk.BooleanVar()

        self.current_fig = None

    def show_plot(self, fig):
        """
        Metodo para mostrar grafico con resultados en el frame superior derecho
        """
        # Limpiar el frame antes de mostrar el grafico
        for widget in self.top_right_frame.winfo_children():
            widget.destroy()

        # Cerrar la figura actual si existe
        if self.current_fig is not None:
            plt.close(self.current_fig)
        
        # Canvas para el grafico y se agrega al frame
        canvas = FigureCanvasTkAgg(fig, master=self.top_right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

        # Almacenar la referencia a la figura actual
        self.current_fig = fig

    def show_img(self, animal, vc):
        """
        Metodo para mostrar imagen con animal en frame inferior derecho
        """
        # Limpiar el frame antes de mostrar la imagen
        for widget in self.bottom_right_frame.winfo_children():
            widget.destroy()
        
        # Cerrar la figura actual si existe
        if self.current_fig is not None:
            plt.close(self.current_fig)
            self.current_fig = None
        
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
        """
        Metodo para obtener el valor apuntado en el slider
        """
        self.ans.set(self.slider.get())
        self.cont.set(True)

    def ask_user(self, prem):
        """
        Metodo para mostrar la pregunta sobre la que se quiera obtener la informacion
        """
        self.slider_label.config(text=prem)
        self.cont.set(False)
        self.root.wait_variable(self.cont)
        return self.ans.get()