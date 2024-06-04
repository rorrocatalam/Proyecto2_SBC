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
        Metodo para encontrar reglas que tienen como conclusion una determinada tripleta
        """
        # Lista de reglas que cumplen requisito
        lista_reglas = []

        # Se revisan todas las reglas presentes
        for regla in self.reglas:
            # Conclusiones de la regla
            regla_con = regla.con
            # Se guarda la regla si cumple requisito
            if trip in regla_con:
                lista_reglas.append(regla)
        
        # Retorno lista de reglas 
        return lista_reglas
