

Autor: Víctor Ruiz Gómez


- El script minmax.py implementa el algoritmo Min-Max y el algoritmo 
Min-Max con poda alpha-beta

- othello.py crea código para poder usar el algoritmo Min-Max en el juego Othello.

- utils.py define funciones y variables auxiliares necesarias en otros scripts

- graph.py es un script que permite visualizar la traza del algoritmo Min-Max en forma de árbol,
usando la librería ete3

- game2.py crea una función con la que se puede enfrentar a dos jugadores en el 
juego othello

- bots.py y othello_gui.py definen jugadores del juego Othello. El primero define máquinas que 
juegan a Othello (Usando el algoritmo Min-Max, Min-Max con poda, ...)
El segundo crea una interfaz de usuario mediante la cual el usuario puede enfrentarse a una de las
máquinas.

- Las funciones de evaluación estáticas para el juego Othello están definidas en el script othello.py al
final

- Para hacer pruebas y ejecutar distintos escenarios (enfrentar a dos máquinas o al usuario frente
a la máquina), configurar y ejecutar el script tests.py (leer código al final del script)

python tests.py 
