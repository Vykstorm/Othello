#!/usr/bin/python
# -*- coding: iso8859-1 -*-

# Script para testear las distintas máquinas implementadas.

from othello import OthelloGame
from game2 import play
from bots import *

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
	player1 = BotPlayerComplex(2);
	player2 = BotPlayerMinMaxAlphaBeta(2);
	verbose = True
	
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
