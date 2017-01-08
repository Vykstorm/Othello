#!/usr/bin/python
# -*- coding: iso8859-1 -*-
# Autor: Víctor Ruiz Gómez
# Descripción: Este script define el algoritmo min-max y el algoritmo min-max
# con poda alpha-beta (orientado a juegos de 2 jugadores), además de todas la estructuras de datos necesarias para estos.

from utils import Inf

# Esta clase define el estado de una partida de dos jugadores. Por ejemplo, en el juego
# tres en raya, el estado indicará que fichas hay en el tablero y en que posiciones se 
# encuentran, y que jugador tiene el turno actual de la partida.
class State:
	# Inicializa la instancia.
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
	# Se indica además como parámetro quién es el jugador MAX: jugador 1 (True) o jugador 2
	# (False)
	def eval(self,state,jugador_max):
		pass 


# Las instancias de esta clase permiten resolver problemas de juegos con el algoritmo MinMax
class MinMax:
	# Inicializa la instancia, debe indicarse el estado inicial, la función de evaluación
	# estática y el nivel de profundidad máximo del árbol Min-Max (infinito en caso de que no se
	# especifique ningún valor)
	def __init__(self, inicio, static_eval, max_deep = Inf, *args, **kargs):
		if max_deep <= 0:
			raise Exception('El nivel de profundidad debe ser mayor que 0!');
			
		self.inicio = inicio
		self.static_eval = static_eval
		self.max_deep = max_deep
		self.args = args
		self.kargs = kargs
		
	# Es un alias de self.next_move(...)
	def __call__(self):
		return self.next_move()
		
		
	# Devuelve una instancia de esta misma clase (que resuelve el mismo problema), pero que a la hora
	# de resolverlo, muestra información de depuración de la traza del algoritmo MinMax
	def debug(self):
		return MinMaxDebug(self.inicio, self.static_eval, self.max_deep, *self.args, **self.kargs)
	
	# Este método resuelve el problema Min-Max: Devuelve el siguiente movimiento que maximize la ventaja
	# de MAX con respecto de MIN. Se invoca pasandole los parámetros que se indicaron en el constructor.
	def next_move(self):
		if len(self.inicio.next_moves()) == 0:
			raise Exception('No es posible realizar ningún movimiento dado el estado inicial de la partida!');	
	
		# Primera llamada al algoritmo.
		ventaja_max, best_move = self._next_move(self.inicio, self.max_deep, True, *self.args, **self.kargs)
		return best_move
		
	def _next_move(self, nodo, max_deep, is_max, *args, **kargs):		
		# Si es un nodo terminal o se alcanza la profundidad máxima, no expandir más el árbol.
		# Devolver su evaluación estática (si es terminal, coincide con su función de utilidad)
		if nodo.is_leaf() or max_deep == 0:
			return self.static_eval(nodo, self.inicio.get_curr_player()), None;
		
		# Expandir el nodo.
		mejor_ventaja = -Inf if is_max else Inf;
		best_move = None;
		
		# Encontramos el movimiento que maximiza la ventaja de MAX con respecto a MIN..
		for move in nodo.next_moves():
			# Minimizamos si es un nodo MIN y máximizamos si es un nodo MÁX
			ventaja, movimiento = self._next_move(nodo.transform(move), max_deep-1, not is_max);
			if (is_max and (ventaja > mejor_ventaja)) or (not is_max and (ventaja < mejor_ventaja)):
				mejor_ventaja = ventaja;
				best_move = move;
		return mejor_ventaja, best_move

# Las instancias de esta clase permiten resolver problemas de juegos con el algoritmo MinMax usando poda
# alpha-beta
class MinMaxAlphaBeta(MinMax):
	# Inicializa la instancia..
	def __init__(self, inicio, static_eval, max_deep = Inf):
		 MinMax.__init__(self, inicio, static_eval, max_deep, -Inf, Inf)
		 
	def debug(self):
		return MinMaxAlphaBetaDebug(self.inicio, self.static_eval, self.max_deep, *self.args, **self.kargs)

	def _next_move(self, nodo, max_deep, is_max, alpha, beta, *args, **kargs):
		if nodo.is_leaf() or max_deep == 0:
			return self.static_eval(nodo, self.inicio.get_curr_player()), None;
		
		mejor_movimiento = None;
		if is_max:
			# El nodo actual es MAX. 
			for move in nodo.next_moves():
				ventaja, movimiento = self._next_move(nodo.transform(move), max_deep-1, False, alpha, beta);
				# Si el valor del nodo hijo (beta) es mayor que el valor alpha del nodo actual, asignar el 
				# primero a este último.
				if ventaja > alpha:
					alpha = ventaja;
					mejor_movimiento = move;
				# Hay poda alpha?
				if beta <= alpha:
					# No procesar el resto de ramas.
					break;
			return alpha, mejor_movimiento;
		else:
			# El nodo actual es MIN.
			for move in nodo.next_moves():
				ventaja, movimiento = self._next_move(nodo.transform(move), max_deep-1, True, alpha, beta);
				if ventaja < beta:
					beta = ventaja;
					mejor_movimiento = move;
				# Hay poda beta?
				if beta <= alpha:
					# No procesar el resto de ramas
					break;
			return beta, mejor_movimiento





# Las instancias de esta clase son como las de la clase MinMax (resuelven problemas usando el algoritmo MinMax),
# solo que muestran información de depuración de la traza del algoritmo.
class MinMaxDebug(MinMax):
	def __init__(self, inicio, *args, **kargs):
		from graph import MinMaxTree
		
		MinMax.__init__(self, inicio, *args, **kargs)
		# Vamos a visualizar la traza del algoritmo, representada visualmente en forma
		# de árbol.
		self.graph = MinMaxTree(repr(inicio))
		
	def next_move(self):
		# Obtenemos el siguiente movimiento
		best_move = MinMax.next_move(self)
		
		# Mostramos la traza MinMax
		self.graph.show()
		
		return best_move

	def _next_move(self, nodo, max_deep, is_max, *args, **kargs):
		if nodo.is_leaf() or max_deep == 0:
			self.graph.set_curr_node_value(repr(self.static_eval(nodo)))
			self.graph.backtrace()
			return self.static_eval(nodo,self.get_curr_player()), None;
		
		mejor_ventaja = -Inf if is_max else Inf;
		best_move = None;
		
		for move in nodo.next_moves():
			self.graph.add_node(repr(nodo.transform(move)), repr(move), not is_max)
			ventaja, movimiento = self._next_move(nodo.transform(move), max_deep-1, not is_max);
			if (is_max and (ventaja > mejor_ventaja)) or (not is_max and (ventaja < mejor_ventaja)):
				mejor_ventaja = ventaja;
				best_move = move;
				
		self.graph.set_curr_node_value(repr(mejor_ventaja))
		self.graph.backtrace()
		return mejor_ventaja, best_move


# Es igual que el anterior, solo que usando el algoritmo MinMax con poda alpha-beta
class MinMaxAlphaBetaDebug(MinMaxDebug):
	def __init__(self, *args, **kargs):
		MinMaxDebug.__init__(self, *args, **kargs)
	
	def _next_move(self, nodo, max_deep, is_max, alpha, beta, *args, **kargs):
		if nodo.is_leaf() or max_deep == 0:
			self.graph.set_curr_node_value(repr(self.static_eval(nodo)))
			self.graph.backtrace()
			return self.static_eval(nodo,self.inicio.get_curr_player()), None;
		
		mejor_movimiento = None;
		if is_max:
			# El nodo actual es MAX. 
			for move in nodo.next_moves():
				self.graph.add_node(repr(nodo.transform(move)), repr(move), False)
				ventaja, movimiento = self._next_move(nodo.transform(move), max_deep-1, False, alpha, beta);
				if ventaja > alpha:
					alpha = ventaja;
					mejor_movimiento = move;
				if beta <= alpha:
					break;
			self.graph.set_curr_node_value('a=' + repr(alpha) + ',b=' + repr(beta))
			self.graph.backtrace()
			return alpha, mejor_movimiento;
		else:
			# El nodo actual es MIN.
			for move in nodo.next_moves():
				self.graph.add_node(repr(nodo.transform(move)), repr(move), True)
				ventaja, movimiento = self._next_move(nodo.transform(move), max_deep-1, True, alpha, beta);
				if ventaja < beta:
					beta = ventaja;
					mejor_movimiento = move;
				if beta <= alpha:
					break;
			self.graph.set_curr_node_value('a=' + repr(alpha) + ',b=' + repr(beta))
			self.graph.backtrace()
			return beta, mejor_movimiento
	
