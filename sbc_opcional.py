from modelo import *

#=============================================================================
# Hipotesis a considerar

H1  = Fact(
    "animal es perro",
    0.0)

H2  = Fact(
    "animal es cheetah",
    0.0)

H3  = Fact(
    "animal es tigre",
    0.0)

H4  = Fact(
    "animal es elefante",
    0.0)

H5  = Fact(
    "animal es jirafa",
    0.0)

H6  = Fact(
    "animal es cebra",
    0.0)

H7  = Fact(
    "animal es murciélago",
    0.0)

H8  = Fact(
    "animal es tortuga",
    0.0)

H9  = Fact(
    "animal es avestruz",
    0.0)

H10 = Fact(
    "animal es gaviota",
    0.0)

H11 = Fact(
    "animal es loro",
    0.0)

#=============================================================================
# Reglas a considerar

R1  = Rule(
    ["animal da leche"],
    ["animal es mamífero", "animal es ave", "animal es reptil"],
    [1.0, -1.0, -1.0])

R2  = Rule(
    ["animal tiene pelo"],
    ["animal es mamífero", "animal es ave", "animal es reptil"],
    [0.8, -1.0, -1.0])

R3  = Rule(
    ["animal pone huevos", "animal tiene piel dura"],
    ["animal es mamífero", "animal es ave", "animal es reptil"],
    [-1.0, -1.0, 1.0])

R4  = Rule(
    ["animal pone huevos", "animal puede volar"],
    ["animal es ave", "animal es reptil"],
    [1.0, -1.0])

R5  = Rule(
    ["animal tiene plumas"],
    ["animal es mamífero", "animal es ave", "animal es reptil"],
    [-1.0, 1.0, -1.0])

R6  = Rule(
    ["animal tiene garras"],
    ["animal es carnívoro"],
    [0.8])

R7  = Rule(
    ["animal come carne"],
    ["animal es carnívoro"],
    [1.0])

R8  = Rule(
    ["animal es mamífero", "animal es rumiante"],
    ["animal es ungulado"],
    [0.75])

R9  = Rule(
    ["animal es mamífero", "animal tiene pezuñas"],
    ["animal es ungulado"],
    [1.0])

R10 = Rule(
    ["animal vive con personas"],
    ["animal es doméstico"],
    [0.9])

R11 = Rule(
    ["animal vive en zoológico"],
    ["animal es doméstico"],
    [-0.8])

R12 = Rule(
    ["animal es mamífero", "animal es carnívoro", "animal tiene manchas oscuras"],
    ["animal es cheetah"],
    [0.9])

R13 = Rule(
    ["animal es mamífero", "animal es carnívoro", "animal tiene rayas negras"],
    ["animal es tigre"],
    [0.85])

R14 = Rule(
    ["animal es mamífero", "animal es carnívoro", "animal es doméstico"],
    ["animal es perro"],
    [0.9])

R15 = Rule(
    ["animal es reptil", "animal es doméstico"],
    ["animal es tortuga"],
    [0.7])

R16 = Rule(
    ["animal es mamífero", "animal es ungulado", "animal tiene cuello largo"],
    ["animal es jirafa"],
    [1.0])

R17 = Rule(
    ["animal es mamífero", "animal es ungulado", "animal tiene rayas negras"],
    ["animal es cebra"],
    [0.95])

R18 = Rule(
    ["animal es mamífero", "animal puede volar", "animal es feo"],
    ["animal es murciélago"],
    [0.9])

R19 = Rule(
    ["animal es ave", "animal vuela bien"],
    ["animal es gaviota"],
    [0.9])

R20 = Rule(
    ["animal es ave", "animal corre rápido"],
    ["animal es avestruz"],
    [1.0])

R21 = Rule(
    ["animal es ave", "animal es parlanchín"],
    ["animal es loro"],
    [0.95])

R22 = Rule(
    ["animal es mamífero", "animal es grande", "animal es ungulado", "animal tiene trompa"],
    ["animal es elefante"],
    [0.9])

#=============================================================================
# Creacion de conjuntos

# Base de hechos
FB = FactBase()

# Base de Reglas
RB = RuleBase([R1,R2,R3,R4,R5,R6,R7,R8,R9,R10,R11,R12,R13,R14,R15,R16,R17,R18,R19,R20,R21,R22])

# Conjunto de Hipotesis
HS = HypothesisSet([H1,H2,H3,H4,H5,H6,H7,H8,H9,H10,H11])

#=============================================================================
# Ejecucion del programa
HS.aei(FB, RB)