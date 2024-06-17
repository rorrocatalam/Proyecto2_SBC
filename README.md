# PROYECTO 2: SISTEMA BASADO EN CONOCIMIENTO CON ENCADENAMIENTO INVERSO

El siguiente repositorio contiene los códigos de un sistema basado en conocimiento con encadenamiento inverso hecho con Python para el curso EL7038-1 Introducción a la Teoría de Conjuntos Difusos y Sistemas Inteligentes.
Las clases utilizadas se encuentran en modelo.py, mientras que la utilización de estas de forma particular para el proyecto y su ejecución se encuentran en sbc.py.

En la carpeta "Opcionales" se encuentran los códigos implementados (que siguen la misma estructura mencionada anteriormente) con los siguientes opcionales:

* Interfaz gráfica (Se necesitan las librerías tkinter, Pillow (PIL) y matplotlib). Para su instalación, se puede realizar mediante consola con $pip$ $install$ (librería).

* Precalificador de reglas.

* Marcador de conclusiones.

* Representación gráfica (Diagrama.png).


## CONSIDERACIONES PARA EJECUTAR OPCIONALES

Antes de ejecutar la interfaz gráfica con sbc.py de la carpeta Opcionales, se debe considerar lo siguiente:

* En la línea 9 de model.py se encuentra la dirección en que estarán las imágenes de los animales. Esta debe ser actualizada por cada usuario para no generar fallos en la interfaz al momento de llegar a conclusiones exitosas.

* Para desactivar el precalificador de reglas, en la línea 140 de model.py, se debe modificar el retorno de True a False (así siempre se dirá que es factible evaluar una regla).

* Para desactivar el marcador de conclusiones, en la línea 149 de model.py, se debe cambiar self.i por False (así no se dirá que la regla ya se ejecutó anteriormente).