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
            # Se pregunta al usuario
            vc = fb.ask_user(self.prem)
            return vc 
        
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
                    # Se dice que no se puede demostrar
                    print(f"No se puede demostrar si su {self.prem}.")
                    # Se retorna None
                    return None

                # Se pregunta al usuario
                else:
                    vc = fb.ask_user(self.prem)
                    return vc
    
class Rule:
    def __init__(self, prem, con, vc):
        self.prem   = prem
        self.con    = con
        self.vc     = vc
    
    def evaluate(self, fb, rb, prem_obj, hs):
        """
        Metodo para evaluar una regla concentrandose en la informacion que se quiere obtener
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
            
#=============================================================================
# Conjuntos a utilizar

class FactBase:
    def __init__(self):
        self.lst_prem  = []
        self.lst_vc    = []

    def print_info(self):
        """
        Metodo para mostrar la informacion contenida en la base de hechos
        """
        i = 0
        # Se revisan las premisas
        for prem in self.lst_prem:
            # Se muestra su información
            print(f"{prem}: {round(self.lst_vc[i],2)}")
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
        # lsta de reglas que cumplen requisito
        rule_lst = []

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
                    rule_lst.append(rule)
        
        # Retorno lsta de reglas 
        return rule_lst
    
class HypothesisSet:
    def __init__(self, lst_hyp):
        self.lst_hyp = lst_hyp
        self.lst_prem = [fact.prem for fact in lst_hyp]
        self.lst_vc = [fact.vc for fact in lst_hyp]
    
    def print_info(self):
        """
        Metodo para mostrar la informacion contenida en la base de hipotesis
        """
        i = 0
        # Se revisan las premisas
        for prem in self.lst_prem:
            # Se muestra su información
            print(f"{prem}: {round(self.lst_vc[i],2)}")
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
                    # Se dice que animal es y la certeza
                    print(f"Su {hyp.prem} con certeza {round(vc_hyp, 2)}.")
                    # Se termina el proceso
                    return
        
            # Siguiente hipotesis    
            idx_hyp += 1

        # Ninguna hipotesis supero el umbral
        print("Ninguna hipótesis se cumplió con suficiente certeza. Los resultados se muestran a continuación:")
        self.print_info()
        return