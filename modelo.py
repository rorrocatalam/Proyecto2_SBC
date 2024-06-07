#=============================================================================
# Parametros de control

alpha   = 0.7   # Para detener el AEI cuando se demuestre una hipotesis
beta    = 0.2   # Para determinar si un hecho tiene un grado de certidumbre suficiente
gamma   = 0.85  # Para determinar si se debe seguir buscando un mejor grado de certidumbre para un hecho
epsilon = 0.5   # Para determinar cuando una regla tiene un grado de certidumbre suficiente para inferir una hipotesis
delta   = 0.2   # Para determinar si el grado de certidumbre es suficiente para gatillar una regla (es variable)

#=============================================================================
# Operadores para propagar valores de certidumbre

def max_mod(list):
    """
    Funcion que retorna el numero cuyo valor absoluto es el maximo
    """
    if not list:
        return None
    return max(list, key=abs)

def min_mod(list):
    """
    Funcion que retorna el numero cuyo valor absoluto es el minimo
    """
    if not list:
        return None
    return min(list, key=abs)

#=============================================================================
# Estructuras basicas

class Fact:
    def __init__(self, prem, vc):
        self.prem   = prem
        self.vc     = vc
    
    def hypothesis(self, fb, rb):
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
        rule_list = rb.prem_in_con(self.prem)
        # Caso Base (lista vacía -> no hay reglas que tienen como conclusion la premisa)
        if not rule_list:
            # Se pregunta al usuario
            vc = fb.ask_user(self.prem)
            return vc 
        
        # Se revisan reglas que podrian probar la hipotesis
        else:
            ##### SIGUIENTE PASO: EVALUAR REGLAS HASTA SUPERAR UMBRAL O HASTA QUE SE ACABEN LAS REGLAS #####
            #####                 SI LAS REGLAS NO FUNCIONARON, PREGUNTAR AL USUARIO                   #####
            return rule_list
    
class Rule:
    def __init__(self, prem, con, vc):
        self.prem   = prem
        self.con    = con
        self.vc     = vc
    
    def is_evaluable(self, fb):
        """
        Metodo para saber si la regla es evaluable en la base de hechos
        """
        # Premisas de la base de hechos
        fb_list_prem = fb.list_prem
        # Retorno booleano si la regla se puede evaluar
        return set(self.prem).issubset(fb_list_prem)
    
    def evaluate(self, fb, rb, prem_obj):
        """
        Método para evaluar una regla concentrandose en la informacion que se quiere obtener
        """
        # Parametros de la regla
        prem = self.prem 
        con = self.con
        vc = self.vc

        # vc de la conclusion que se quiere obtener
        index_r = con.index(prem_obj)
        vc_r = vc[index_r]
        # Umbral para seguir y gatillar regla
        delta_r = delta/vc_r

        # vc acumulado de la regla
        vc_acc = -10.0 # valor fuera de rango entre [-1,1]

        # Se ve cada premisa de la regla
        for prem_i in prem:
            # Se ve como hipotesis para obtener su valor
            h_i = Fact(prem_i, 0)
            # Se obtiene su valor de forma recursiva
            vc_i = h_i.hypothesis(fb, rb)
            # Actualizacion del vc acumulado
            vc_acc = min_mod([vc_acc,vc_i])
            # Si no se supera el umbral, no vale la pena seguir con las demas premisas
            if abs(vc_acc) < delta_r:
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
            
#=============================================================================
# Conjuntos a utilizar

class FactBase:
    def __init__(self):
        self.list_prem  = []
        self.list_vc    = []

    def print_info(self):
        """
        Metodo para mostrar la informacion contenida en la base de hechos
        """
        i = 0
        # Se revisan las premisas
        for prem in self.list_prem:
            # Se muestra su información
            print(f"{prem}: {self.list_vc[i]}")
            i += 1
            
    def is_in(self, prem):
        """
        Metodo para saber si el hecho esta en la base de hechos, dada su premisa
        """
        # Retorno booleano si la regla se puede evaluar
        if prem in self.list_prem:
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
            index_f = self.list_prem.index(prem)
            # vc del hecho
            vc_f = self.list_vc[index_f]
            # Se actualiza si hay mayor certeza
            if max_mod([vc, vc_f]) == vc_f:
                self.list_vc[index_f] = vc_f

        # Si no existe se añade
        else:
            # Guardar valores
            self.list_prem.append(prem)
            self.list_vc.append(vc)

    def get_vc(self, prem):
        """"
        Metodo para obtener el vc de una premisa presente en la base de hechos
        """
        # Posicion del hecho en la base de hechos
        index_f = self.list_prem.index(prem)
        # Se retorna el vc del hecho
        return self.list_vc[index_f]

    def ask_user(self, prem):
        """
        Metodo para agregar un hecho dada la entrada del usuario
        """
        vc = -10.0 # valor fuera de rango entre [-1,1]
        while vc < -1.0 or vc > 1.0:
            usr_in = input("\n¿Su " + prem + "?\n")
            try:
                vc = float(usr_in)
                if vc < -1.0 or vc > 1.0:
                    print("Favor ingresar un número entero entre -1 y 1.")
                else:
                    # Se crea el hecho
                    fact = Fact(prem, vc)
                    # Se guarda en la base de hechos
                    self.add_mod_fact(fact)
                    # Se retorna el valor indicado
                    return vc
            except ValueError:
                print("Favor ingresar un número entero entre -1 y 1.")

class RuleBase:
    def __init__(self, rules):
        self.rules = rules

    def prem_in_con(self, prem):
        """
        Metodo para encontrar las reglas utiles que tienen como conclusion una determinada premleta
        """
        # Lista de reglas que cumplen requisito
        rule_list = []

        # Se revisan todas las reglas presentes
        for rule in self.rules:
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
                    rule_list.append(rule)
        
        # Retorno lista de reglas 
        return rule_list