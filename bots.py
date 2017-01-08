#!/usr/bin/python
# -*- coding: iso8859-1 -*-
# Autor: Víctor Ruiz Gómez
# Descripción: Este script define distintos bots que son jugadores del
# juego Othello.

from game2 import Player
from random import choice


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
