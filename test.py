from modelo import *
from definiciones import *

# Base de hechos de prueba (Contiene informacion necesaria para regla 12)
FB = FactBase()
FB.add_fact(Fact(["animal es mamífero"], 0.95))
FB.add_fact(Fact(["animal es carnívoro"], 0.95))
FB.add_fact(Fact(["animal tiene manchas oscuras"], 0.95))

print(FB.list_trip)
print(FB.list_vc)

print(R1.is_evaluable(FB))
print(R12.is_evaluable(FB))

FB.ask_user("animal da leche")