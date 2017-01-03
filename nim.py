#!/usr/bin/python
# -*- coding: iso8859-1 -*-
# Autor: Víctor Ruiz Gómez
# Descripción: Este script sirve para testear los algoritmo Min-Max con y sin poda
# alpha-beta (se trata de un juego más sencillo que Othello -> Nim)


from minmax import minmax, minmax_alphabeta;
from minmax import State, Move, StaticEval;

# Definición de estado en el juego Nim: numero de fichas en la mesa
class NimState(State):
	def __init__(self,fichas):
		self.fichas = fichas;
		
	# Cuando un estado es terminal?
	def is_leaf(self):
		return self.fichas == 0;
		
	# Posibles siguientes movimientos que pueden realizarse dada esta
	# configuración?
	def next_moves(self, is_max):
		return [NimMove(x+1) for x in range(0,self.fichas)];

	# Como pasar de un estado a otro dado que uno de los jugadores ha realizado
	# un movimiento...
	def transform(self, move):
		return NimState(self.fichas - move.fichas_tomadas);
	
	
	def __repr__(self):
		return repr(self.fichas);
		
	def __str__(self):
		return str(self.fichas);
	
# Definición de un movimiento del juego: Número de fichas tomadas
class NimMove(Move):
	def __init__(self, fichas_tomadas):
		self.fichas_tomadas = fichas_tomadas;
		
	def __repr__(self):
		return repr(self.fichas_tomadas);
	
	def __str__(self):
		return str(self.fichas_tomadas);


# Definición de la función de evaluación estática.
class NimStaticEval(StaticEval):
	# Como evaluamos como de bueno es un nodo para MAX?
	def eval(self, state):
		return 1 if state.fichas > 0 else -1;




if __name__ == '__main__':
	num_fichas = 5;
	print 'Numero de fichas inicial: ' + str(num_fichas);
	
	# Ejecuta min-max sin poda alpha beta.
	move = minmax(NimState(num_fichas), NimStaticEval());
	print 'Siguiente movimiento, tomar ' + str(move) + ' fichas';

	
