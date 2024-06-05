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
    
    def evaluate(self, fb, rb):
        """
        aaa
        """
        # Si el hecho esta en la base de hechos
        if fb.is_in(self.prem[0]):
            vc = fb.get_vc(self.prem[0])
            # El hecho sera relevante solo si existe suficiente certeza
            if abs(vc) >= beta:
                return vc
        
        # El hecho no esta en la base de hechos o no hay conocimiento suficiente (no supera el umbral beta)
        rule_list = rb.trip_in_con(self.prem[0])
        if not rule_list: # si esta vacia
            vc = fb.ask_user(self.prem[0])
            return vc 
        else:
            ##### SIGUIENTE PASO: HACER FUNCION PARA EVALUAR REGLAS
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
        # Tripletas de la base de hechos
        fb_list_trip = fb.list_trip
        # Retorno booleano si la regla se puede evaluar
        return set(self.prem).issubset(fb_list_trip)

#=============================================================================
# Conjuntos a utilizar

class FactBase:
    def __init__(self):
        self.list_trip  = []
        self.list_vc    = []

    def is_in(self, prem):
        """
        Metodo para saber si el hecho esta en la base de hechos, dada su premisa
        """
        # Retorno booleano si la regla se puede evaluar
        if prem in self.list_trip:
            return True
        else:
            return False
    
    def get_vc(self, prem):
        """"
        Metodo para obtener el vc de una premisa presente en la base de hechos
        """
        # Posicion del hecho en la base de hechos
        index_f = self.list_trip.index(prem)
        # Se retorna el vc del hecho
        return self.list_vc[index_f]

    ###### MODIFICAR ESTA FUNCION PARA QUE TAMBIEN SE MODIFIQUE VC EN CASO DE QUE SE MEJORE CONOCIMIENTO ######
    def add_fact(self, hecho):
        """
        Metodo para agregar hechos
        """
        # Premisa y valor del hecho
        prem = hecho.prem
        vc = hecho.vc
        # Guardar valores
        self.list_trip.append(prem[0])
        self.list_vc.append(vc)

    def ask_user(self, prem):
        """
        Metodo para agregar un hecho dada la entrada del usuario
        """
        vc = -10.0
        while vc < -1.0 or vc > 1.0:
            usr_in = input("\n¿Su " + prem + "?\n")
            try:
                vc = float(usr_in)
                if vc < -1.0 or vc > 1.0:
                    print("Favor ingresar un número entero entre -1 y 1.")
                else:
                    # Se crea el hecho
                    fact = Fact([prem], vc)
                    # Se guarda en la base de hechos
                    self.add_fact(fact)
                    # Se retorna el valor indicado
                    return vc
            except ValueError:
                print("Favor ingresar un número entero entre -1 y 1.")


    


class RuleBase:
    def __init__(self, rules):
        self.rules = rules

    def trip_in_con(self, trip):
        """
        Metodo para encontrar las reglas utiles que tienen como conclusion una determinada tripleta
        """
        # Lista de reglas que cumplen requisito
        rule_list = []

        # Se revisan todas las reglas presentes
        for rule in self.rules:
            # Conclusiones de la regla
            rule_con = rule.con
            # Si la tripleta esta en las conclusiones se procede
            if trip in rule_con:
                # Grados de implicacion de conclusiones de la regla
                regla_vc = rule.vc
                # Posicion de la tripleta en conclusiones
                indice_trip = rule_con.index(trip)
                # Grado de implicacion de la tripleta
                vc_trip =  regla_vc[indice_trip]
                # Si su grado de implicacion supera el umbral, la regla se considera util y se guarda
                if abs(vc_trip) >= epsilon: 
                    rule_list.append(rule)
        
        # Retorno lista de reglas 
        return rule_list