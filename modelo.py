#=============================================================================
# Parametros de control

alpha   = 0.7   # Para detener el AEI cuando se demuestre una hipotesis
beta    = 0.2   # Para determinar si un hecho tiene un grado de certidumbre suficiente
gamma   = 0.85  # Para determinar si se debe seguir buscando un mejor grado de certidumbre para un hecho
epsilon = 0.5   # Para determinar cuando una regla tiene un grado de certidumbre suficiente para inferir una hipotesis
delta   = 0.2   # Para determinar si el grado de certidumbre es suficiente para gatillar una regla (es variable)

#=============================================================================
# Estructuras basicas

class Hecho:
    def __init__(self, prem, vc):
        self.prem   = prem
        self.vc     = vc

class Regla:
    def __init__(self, prem, con, vc):
        self.prem   = prem
        self.con    = con
        self.vc     = vc
    
    def es_evaluable(self, bdh):
        """
        Metodo para saber si la regla es evaluable en la base de hechos
        """
        # Tripletas de la base de hechos
        bdh_lista_trip = bdh.lista_trip
        # Retorno booleano si la regla se puede evaluar
        return set(self.prem).issubset(bdh_lista_trip)

#=============================================================================
# Conjuntos a utilizar

class BaseDeHechos:
    def __init__(self):
        self.lista_trip  = []
        self.lista_vc    = []
    
    def agregar_hecho(self, hecho):
        """
        Metodo para agregar hechos
        """
        # Premisa y valor del hecho
        prem = hecho.prem
        vc = hecho.vc
        # Guardar valores
        self.lista_trip.append(prem[0])
        self.lista_vc.append(vc)

class BaseDeReglas:
    def __init__(self, reglas):
        self.reglas = reglas

    def trip_en_con(self, trip):
        """
        Metodo para encontrar las reglas utiles que tienen como conclusion una determinada tripleta
        """
        # Lista de reglas que cumplen requisito
        lista_reglas = []

        # Se revisan todas las reglas presentes
        for regla in self.reglas:
            # Conclusiones de la regla
            regla_con = regla.con
            # Si la tripleta esta en las conclusiones se procede
            if trip in regla_con:
                # Grados de implicacion de conclusiones de la regla
                regla_vc = regla.vc
                # Posicion de la tripleta en conclusiones
                indice_trip = regla_con.index(trip)
                # Grado de implicacion de la tripleta
                vc_trip =  regla_vc[indice_trip]
                # Si su grado de implicacion supera el umbral, la regla se considera util y se guarda
                if abs(vc_trip) >= epsilon: 
                    lista_reglas.append(regla)
        
        # Retorno lista de reglas 
        return lista_reglas