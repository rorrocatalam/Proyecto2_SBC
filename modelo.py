#=============================================================================
# Parametros de control

alpha   = 0.7   # Para detener el AEI cuando se demuestre una hipotesis
beta    = 0.2   # Para determinar si un hecho tiene un grado de certidumbre suficiente
gamma   = 0.85  # Para determinar si se debe seguir buscando un mejor grado de certidumbre para un hecho
epsilon = 0.5   # Para determinar cuando una regla tiene un grado de certidumbre suficiente para inferir una hipotesis
delta   = 0.2   # Para determinar si el grado de certidumbre es suficiente para gatillar una regla (es variable)

#=============================================================================
# Estructuras basicas

class Fact:
    def __init__(self, prem, vc):
        self.prem   = prem
        self.vc     = vc

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