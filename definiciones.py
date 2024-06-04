from modelo import *

#=============================================================================
# Hipotesis a considerar

H1  = Hecho(
    ["animal es perro"],
    0.0)

H2  = Hecho(
    ["animal es cheetah"],
    0.0)

H3  = Hecho(
    ["animal es tigre"],
    0.0)

H4  = Hecho(
    ["animal es elefante"],
    0.0)

H5  = Hecho(
    ["animal es jirafa"],
    0.0)

H6  = Hecho(
    ["animal es cebra"],
    0.0)

H7  = Hecho(
    ["animal es murciélago"],
    0.0)

H8  = Hecho(
    ["animal es tortuga"],
    0.0)

H9  = Hecho(
    ["animal es avestruz"],
    0.0)

H10 = Hecho(
    ["animal es gaviota"],
    0.0)

H11 = Hecho(
    ["animal es loro"],
    0.0)

#=============================================================================
# Reglas a considerar

R1  = Regla(
    ["animal da leche"],
    ["animal es mamífero", "animal es ave", "animal es reptil"],
    [1.0, -1.0, -1.0])

R2  = Regla(
    ["animal tiene pelo"],
    ["animal es mamífero", "animal es ave", "animal es reptil"],
    [0.8, -1.0, -1.0])

R3  = Regla(
    ["animal pone huevos", "animal tiene piel dura"],
    ["animal es mamífero", "animal es ave", "animal es reptil"],
    [-1.0, -1.0, 1.0])

R4  = Regla(
    ["animal pone huevos", "animal puede volar"],
    ["animal es ave", "animal es reptil"],
    [1.0, -1.0])

R5  = Regla(
    ["animal tiene plumas"],
    ["animal es mamífero", "animal es ave", "animal es reptil"],
    [-1.0, 1.0, -1.0])

R6  = Regla(
    ["animal tiene garras"],
    ["animal es carnívoro"],
    [0.8])

R7  = Regla(
    ["animal come carne"],
    ["animal es carnívoro"],
    [1.0])

R8  = Regla(
    ["animal es mamífero", "animal es rumiante"],
    ["animal es ungulado"],
    [0.75])

R9  = Regla(
    ["animal es mamífero", "animal tiene pezuñas"],
    ["animal es ungulado"],
    [1.0])

R10 = Regla(
    ["animal vive con personas"],
    ["animal es doméstico"],
    [0.9])

R11 = Regla(
    ["animal vive en zoológico"],
    ["animal es doméstico"],
    [-0.8])

R12 = Regla(
    ["animal es mamífero", "animal es carnívoro", "animal tiene manchas oscuras"],
    ["animal es cheetah"],
    [0.9])

R13 = Regla(
    ["animal es mamífero", "animal es carnívoro", "animal tiene rayas negras"],
    ["animal es tigre"],
    [0.85])

R14 = Regla(
    ["animal es mamífero", "animal es carnívoro", "animal es doméstico"],
    ["animal es perro"],
    [0.9])

R15 = Regla(
    ["animal es reptil", "animal es doméstico"],
    ["animal es tortuga"],
    [0.7])

R16 = Regla(
    ["animal es mamífero", "animal es ungulado", "animal tiene cuello largo"],
    ["animal es jirafa"],
    [1.0])

R17 = Regla(
    ["animal es mamífero", "animal es ungulado", "animal tiene rayas negras"],
    ["animal es cebra"],
    [0.95])

R18 = Regla(
    ["animal es mamífero", "animal puede volar", "animal es feo"],
    ["animal es murciélago"],
    [0.9])

R19 = Regla(
    ["animal es ave", "animal vuela bien"],
    ["animal es gaviota"],
    [0.9])

R20 = Regla(
    ["animal es ave", "animal corre rápido"],
    ["animal es avestruz"],
    [1.0])

R21 = Regla(
    ["animal es ave", "animal es parlanchín"],
    ["animal es loro"],
    [0.95])

R22 = Regla(
    ["animal es mamífero", "animal es grande", "animal es ungulado", "animal tiene trompa"],
    ["animal es elefante"],
    [0.9])

#=============================================================================
# Creacion de conjuntos

# Base de reglas
BDR = BaseDeReglas([R1,R2,R3,R4,R5,R6,R7,R8,R9,R10,R11,R12,R13,R14,R15,R16,R17,R18,R19,R20,R21,R22])