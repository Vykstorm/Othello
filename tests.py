#!/usr/bin/python
# -*- coding: iso8859-1 -*-

# Script para testear las distintas mÃ¡quinas implementadas.

from othello import OthelloGame
from game2 import play
from bots import *
from othello_gui import GUIPlayer

# Cada una de estas instancias es una partida entre dos jugadores Othello.
class Match:
	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.game = OthelloGame()
	
	def play(self, verbose = True):
		return play(self.game, self.player1, self.player2, verbose)
		
		
	def __repr__(self):
		return 'Enfrentamiento entre ' + repr(self.player1) + ' y ' + repr(self.player2)


if __name__ == '__main__':
	# Este parámetro establece la profundidad máxima del árbol al usar algoritmos min-max
	profundidad = 2
	
	# Imprime más información de la partida
	verbose = True
	
	# Primer escenario. Jugador min-max vs Jugador que selecciona jugada que más piezas come.
	#player1 = BotPlayerMinMax(profundidad)
	#player2 = BotPlayerMaxFeed()
	
	# Segundo escenario. Jugador min-max con poda alpha-beta vs jugador que selecciona movimiento que más piezas
	# come.
	#player1 = BotPlayerMinMaxAlphaBeta(profundidad)
	#player2 = BotPlayerMaxFeed()
	
	# Tercer escenario. Jugador min-max con poda alpha beta con función de evaluación estática distinta vs
	# jugador min-max con poda alphabeta normal.
	#player1 = BotPlayerComplex(profundidad)
	#player2 = BotPlayerMinMaxAlphaBeta(profundidad)
	
	# Un escenario de prueba. Usuario vs min-max con poda alpha beta y función de evaluación distinta
	player1 = GUIPlayer()
	player2 = BotPlayerComplex(profundidad)
	
	partida = Match(player1, player2)
	
	print partida
	
	results = partida.play(verbose)
	print 'puntuacion de ' + repr(player1) + ' = ' + repr(results['score'])
	print 'puntuacion de ' + repr(player2) + ' = ' + repr(-results['score'])
	print 'secs/movimiento de ' + repr(player1) + ' = ' + repr(results['time_per_play'][0])
	print 'secs/movimiento de ' + repr(player2) + ' = ' + repr(results['time_per_play'][1])
	if results['score'] != 0:
		print 'gana el jugador ' + repr(player1 if results['score'] > 0  else player2)
	else:
		print 'Empate!'
	
	print player1.get_static_eval().call_count()
