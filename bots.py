#!/usr/bin/python
# -*- coding: iso8859-1 -*-
# Autor: Víctor Ruiz Gómez
# Descripción: Este script define distintos bots que son jugadores del
# juego Othello.

from game2 import Player
from random import choice
from minmax import MinMax, MinMaxAlphaBeta
from othello import OthelloEval, OthelloEvalDiffPiezas, OthelloEvalComplex

# El siguiente bot selecciona un movimiento al azar entre el conjunto de
# movimientos posibles que puede realizar

class BotPlayerRandom(Player):
	
	def play(self, game, opp_move):
		# Obtenemos el conjunto de movimientos posibles.
		moves = game.next_moves()
		if len(moves) == 0:
			return None
		
		# Seleccionamos uno aleatoriamente.
		return choice(moves)

# El siguiente bot selecciona el movimiento que más piezas come.
class BotPlayerMaxFeed(Player):
	def play(self, game, opp_move):
		moves = game.next_moves()
		if len(moves) == 0:
			return None
		
		best_move = moves[0]
		max_pieces_eat = abs(game.transform(best_move).score() - game.score())
		for i in range(1,len(moves)):
			move = moves[i]
			pieces_eat = abs(game.transform(move).score() - game.score())
			if pieces_eat > max_pieces_eat:
				max_pieces_eat = pieces_eat
				best_move = move
		return best_move

# El siguiente bot usa el algorito MinMax para seleccionar el siguiente movimiento,
# usando la diferencia de piezas entre MIN y MAX como función de evaluación estática.
class BotPlayerMinMax(Player):
	# Inicializa la instancia. Se puede indicar como parámetro el nivel de profundidad
	# máxima para el algoritmo MinMax.
	def __init__(self, max_deep):
		self.max_deep = max_deep
	
	def play(self, game, opp_move):
		if len(game.next_moves()) == 0:
			return None
		minmax = MinMax(game, OthelloEvalDiffPiezas(), self.max_deep)
		best_move = minmax()
		return best_move


# Es igual que el anterior solo que el algoritmo Min-Max con poda alpha-beta
class BotPlayerMinMaxAlphaBeta(BotPlayerMinMax):
	def __init__(self, max_deep):
		BotPlayerMinMax.__init__(self, max_deep)

	def play(self, game, opp_move):
		if len(game.next_moves()) == 0:
			return None
		minmax = MinMaxAlphaBeta(game, OthelloEvalDiffPiezas(), self.max_deep)
		best_move = minmax()
		return best_move
		
		
# Este último robot usa el algoritmo MinMax con poda alpha beta, usando
# una función de evaluación estática que tiene en cuenta posiciones estableces 
# del tablero (bordes y esquinas)
class BotPlayerComplex(BotPlayerMinMax):
	def __init__(self, max_deep):
		BotPlayerMinMax.__init__(self, max_deep)
	
	def play(self, game, opp_move):
		if len(game.next_moves()) == 0:
			return None
		minmax = MinMaxAlphaBeta(game, OthelloEvalComplex(), self.max_deep)
		best_move = minmax()
		return best_move
