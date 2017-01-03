#!/usr/bin/python
# -*- coding: iso8859-1 -*-
# Autor: V�ctor Ruiz G�mez
# Descripci�n: Este script define el algoritmo min-max y el algoritmo min-max
# con poda alpha-beta (orientado a juegos de 2 jugadores), adem�s de todas la estructuras de datos necesarias para estos.

from utils import Inf


# Esta clase define el estado de una partida de dos jugadores. Por ejemplo, en el juego
# tres en raya, el estado indicar� que fichas hay en el tablero y en que posiciones se 
# encuentran.
class State:
	# Debe devolver un valor booleano si el estado es terminal (fin de la partida)
	def is_leaf(self):
		pass
	
	# Debe devolver todos los posibles movimientos que puede realizar un jugador dada esta
	# configuraci�n de la partida
	# @param is_max Es un valor booleano indicando si el jugador que realiza dichos movimientos
	# es el jugador MAX o si por el contrario es el jugador MIN.
	def next_moves(self,is_max):
		pass
	
	# Debe devolver otro estado que sea el resultado de aplicar el movimiento indicado
	# como par�metro dado el estado actual de la partida.
	def transform(self,move):
		pass


# Esta clase define un posible movimiento que permite cambiar de un estado a otro.
class Move:
	pass



# Esta clase representa la evaluaci�n estatica de un estado: Como de bueno es el estado (la configuraci�n de 
# la partida), para el jugador MAX
class StaticEval:
	def __call__(self, *args):
		return self.eval(*args)
	
	def __str__(self):
		return str(self.__class__.__name__)
		
	def __repr__(self):
		return repr(self.__class__.__name__)
		
		
	# Este m�todo debe devolver un entero indicando como de bueno es el estado para MAX 
	# (mayor cuanto m�s favorable sera)
	def eval(self,state):
		pass 


# Este m�todo define el algoritmo Min-Max sin poda alpha-beta, indicando una funci�n de evaluaci�n
# est�tica, la profundidad m�xima de expansi�n del �rbol y el estado inicial (nodo ra�z del �rbol)
# La funci�n est�tica debe coincidir con la funci�n de utilidad en los nodos hoja del �rbol.
# Se presupone que el turno inicial lo posee el jugador MAX.
# Devuelve el siguiente movimiento que debe realizar el jugador MAX para maximizar su ventaja con respecto
# a MIN
def minmax(inicio, static_eval, max_deep = Inf):
	if max_deep <= 0:
		raise Exception('El nivel de profundidad debe ser mayor que 0!');
		
	moves = inicio.next_moves(True);
	if len(moves) == 0:
		raise Exception('No es posible realizar ning�n movimiento dado el estado inicial de la partida!');
	
	# Obtenemos el siguiente movimiento que m�s m�ximice la ventaja de MAX con respecto a MIN
	ventaja, mejor_movimiento = _minmax(inicio, static_eval, max_deep, True);
	return mejor_movimiento;
	
# Este m�todo auxiliar devuelve como de mejor es una configuraci�n del juego dada para MAX con respecto a MIN y 
# el siguiente movimiento que deber�a tomar el jugador MAX/MIN para que MAX alcanze esa ventaja con MIN.
def _minmax(nodo, static_eval, max_deep, is_max):
	# Si es un nodo terminal o se alcanza la profundidad m�xima, no expandir m�s el �rbol.
	# Devolver su evaluaci�n est�tica (si es terminal, coincide con su funci�n de utilidad)
	if nodo.is_leaf() or max_deep == 0:
		return static_eval(nodo), None;
	
	# Expandir el nodo.
	mejor_ventaja = -Inf if is_max else Inf;
	mejor_movimiento = None;
	
	# Encontramos el movimiento que maximiza la ventaja de MAX con respecto a MIN..
	for move in nodo.next_moves(is_max):
		# Minimizamos si es un nodo MIN y m�ximizamos si es un nodo M�X
		ventaja, movimiento = _minmax(nodo.transform(move), static_eval, max_deep-1, not is_max);
		if (is_max and (ventaja > mejor_ventaja)) or (not is_max and (ventaja < mejor_ventaja)):
			mejor_ventaja = ventaja;
			mejor_movimiento = move;
	return (mejor_ventaja, mejor_movimiento);
	
# Este m�todo es igual que el anterior, solo que se poda el �rbol (poda alpha-beta)
def minmax_alphabeta(inicio, static_eval, max_deep): 
	pass

