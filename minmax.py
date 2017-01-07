#!/usr/bin/python
# -*- coding: iso8859-1 -*-
# Autor: Víctor Ruiz Gómez
# Descripción: Este script define el algoritmo min-max y el algoritmo min-max
# con poda alpha-beta (orientado a juegos de 2 jugadores), además de todas la estructuras de datos necesarias para estos.

from utils import Inf
from graph import MinMaxTree


# Esta clase define el estado de una partida de dos jugadores. Por ejemplo, en el juego
# tres en raya, el estado indicará que fichas hay en el tablero y en que posiciones se 
# encuentran, y que jugador tiene el turno actual de la partida.
class State:
	def __init__(self,curr_player):
		self.curr_player = curr_player
	
	# Debe devolver un valor booleano si el estado es terminal (fin de la partida)
	def is_leaf(self):
		pass
	
	# Debe devolver todos los posibles movimientos que puede realizar un jugador dada esta
	# configuración de la partida
	def next_moves(self):
		pass
	
	# Debe devolver otro estado que sea el resultado de aplicar el movimiento indicado
	# como parámetro dado el estado actual de la partida.
	def transform(self,move):
		pass

	# Devuelve el jugador que tiene el turno actual de la partida.
	# Devuelve el valor True si el jugador MAX tiene el turno actual o False si MIN tiene el turno.
	def get_curr_player(self):
		return self.curr_player

# Esta clase define un posible movimiento que permite cambiar de un estado a otro.
class Move:
	pass



# Esta clase representa la evaluación estatica de un estado: Como de bueno es el estado (la configuración de 
# la partida), para el jugador MAX
class StaticEval:
	def __call__(self, *args):
		return self.eval(*args)
	
	def __str__(self):
		return str(self.__class__.__name__)
		
	def __repr__(self):
		return repr(self.__class__.__name__)
		
		
	# Este método debe devolver un entero indicando como de bueno es el estado para MAX 
	# (mayor cuanto más favorable sera)
	def eval(self,state):
		pass 


# Este método define el algoritmo Min-Max sin poda alpha-beta, indicando una función de evaluación
# estática, la profundidad máxima de expansión del árbol y el estado inicial (nodo raíz del árbol)
# La función estática debe coincidir con la función de utilidad en los nodos hoja del árbol.
# Se presupone que el turno inicial lo posee el jugador MAX.
# Devuelve el siguiente movimiento que debe realizar el jugador MAX para maximizar su ventaja con respecto
# a MIN
def minmax(inicio, static_eval, max_deep = Inf):
	if max_deep <= 0:
		raise Exception('El nivel de profundidad debe ser mayor que 0!');
		
	moves = inicio.next_moves();
	if len(moves) == 0:
		raise Exception('No es posible realizar ningún movimiento dado el estado inicial de la partida!');
	
	# Obtenemos el siguiente movimiento que más máximice la ventaja de MAX con respecto a MIN
	ventaja, mejor_movimiento = _minmax(inicio, static_eval, max_deep, True);
	#debug_graph = MinMaxTree(repr(inicio))
	#venta, mejor_movimiento = _minmax(inicio, static_eval, max_deep, True, debug_graph=debug_graph)
	#debug_graph.show()
	return mejor_movimiento;
	
# Este método auxiliar devuelve como de mejor es una configuración del juego dada para MAX con respecto a MIN y 
# el siguiente movimiento que debería tomar el jugador MAX/MIN para que MAX alcanze esa ventaja con MIN.
def _minmax(nodo, static_eval, max_deep, is_max, **kargs):
	#debug_graph = kargs['debug_graph']
	
	# Si es un nodo terminal o se alcanza la profundidad máxima, no expandir más el árbol.
	# Devolver su evaluación estática (si es terminal, coincide con su función de utilidad)
	if nodo.is_leaf() or max_deep == 0:
		#debug_graph.set_curr_node_value(str(static_eval(nodo)))
		#debug_graph.backtrace()
		return static_eval(nodo), None;
	
	# Expandir el nodo.
	mejor_ventaja = -Inf if is_max else Inf;
	mejor_movimiento = None;
	
	# Encontramos el movimiento que maximiza la ventaja de MAX con respecto a MIN..
	for move in nodo.next_moves():
		#debug_graph.add_node(repr(nodo.transform(move)), repr(move), not is_max)
		# Minimizamos si es un nodo MIN y máximizamos si es un nodo MÁX
		ventaja, movimiento = _minmax(nodo.transform(move), static_eval, max_deep-1, not is_max, **kargs);
		if (is_max and (ventaja > mejor_ventaja)) or (not is_max and (ventaja < mejor_ventaja)):
			mejor_ventaja = ventaja;
			mejor_movimiento = move;
			
	#debug_graph.set_curr_node_value(mejor_ventaja)
	#debug_graph.backtrace()
	
	return (mejor_ventaja, mejor_movimiento);
	
	
# Este método es igual que el anterior, solo que se poda el árbol (poda alpha-beta)
def minmax_alphabeta(inicio, static_eval, max_deep = Inf): 
	if max_deep <= 0:
		raise Exception('El nivel de profundidad debe ser mayor que 0!');
		
	moves = inicio.next_moves();
	if len(moves) == 0:
		raise Exception('No es posible realizar ningún movimiento dado el estado inicial de la partida!');
	
	# Obtenemos el siguiente movimiento que más máximice la ventaja de MAX con respecto a MIN
	ventaja, mejor_movimiento = _minmax_alphabeta(inicio, static_eval, max_deep, -Inf, Inf, True);
	#debug_graph = MinMaxTree(repr(inicio))
	#ventaja, mejor_movimiento = _minmax_alphabeta(inicio, static_eval, max_deep, -Inf, Inf, True, debug_graph=debug_graph);
	#debug_graph.show()
	return mejor_movimiento;
	
	
def _minmax_alphabeta(nodo, static_eval, max_deep, alpha, beta, is_max, **kargs):
	#debug_graph = kargs['debug_graph']
	if nodo.is_leaf() or max_deep == 0:
		#debug_graph.set_curr_node_value(str(static_eval(nodo)))
		#debug_graph.backtrace()
		return static_eval(nodo), None;
	
	mejor_movimiento = None;
	
	if is_max:
		# El nodo actual es MAX. 
		for move in nodo.next_moves():
			#debug_graph.add_node(repr(nodo.transform(move)), repr(move), not is_max)
			ventaja, movimiento = _minmax_alphabeta(nodo.transform(move), static_eval, max_deep-1, alpha, beta, False, **kargs);
			# Si el valor del nodo hijo (beta) es mayor que el valor alpha del nodo actual, asignar el 
			# primero a este último.
			if ventaja > alpha:
				alpha = ventaja;
				mejor_movimiento = move;
			# Hay poda alpha?
			if beta <= alpha:
				# No procesar el resto de ramas.
				break;
		#debug_graph.set_curr_node_value('(a=' + str(alpha) + ',b=' + str(beta) + ')')
		#debug_graph.backtrace()
		return alpha, mejor_movimiento;
	else:
		for move in nodo.next_moves():
			#debug_graph.add_node(repr(nodo.transform(move)), repr(move), not is_max)
			ventaja, movimiento = _minmax_alphabeta(nodo.transform(move), static_eval, max_deep-1, alpha, beta, True, **kargs);
			if ventaja < beta:
				beta = ventaja;
				mejor_movimiento = move;
			# Hay poda beta?
			if beta <= alpha:
				# No procesar el resto de ramas
				break;
		#debug_graph.set_curr_node_value('(a=' + str(alpha) + ',b=' + str(beta) + ')')
		#debug_graph.backtrace()
		return beta, mejor_movimiento
