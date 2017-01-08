#!/usr/bin/python
# -*- coding: iso8859-1 -*-

# game2: play a 2 person game

from time import time
from othello import OthelloMove

# Esta clase representa un jugador. 
class Player:
    def __init__(self):
		pass
		
	# Este método debe devolver el siguiente movimiento del jugador.
	# Toma como parámetro la configuración actual del juego que está jugando
	# el jugador, y el movimiento anterior de su contrincante, o el valor None,
	# si el jugador es el primero en mover.
	# Debe devolver el movimiento a realizar o none si no hay ning�n posible movimiento
	# o el jugador pasa el turno. 
    def play(self, game, opp_move):
        pass
	
	# Esta rutina es invocada cuando la partida finaliza.
    def gameover(self, game, last_move):
        pass

class IllegalMove(Exception):
    pass


def play(game, player1, player2, verbose = True):
	"""Play a game between two players. Can raise IllegalMove"""

	next = 1 # player 1 has to move first
	player1_think = 0.0 # total think time
	player1_ply = 0
	player2_think = 0.0
	player2_ply = 0

	if verbose:
		print game
		
	last_move = None
	while not game.is_leaf():
		# compute the next move for the player
		t1 = time()
		if next == 1:
			move = player1.play(game, last_move)
		else:
			move = player2.play(game, last_move)
		if move is None:
			if verbose:
				print ('player ' + str(next) + ' skips his turn')
			game = game.transform(None)
			next = 3 - next 
			continue
			
		t2 = time()
		last_move = move
		# update player think time statistics
		if next == 1:
			player1_ply += 1
			player1_think += t2-t1
		else:
			player2_ply += 1
			player2_think += t2-t1

		if verbose:            
			print("player %d plays %s (in %.1f s)"
				 % (next, str(move), t2-t1))
		#check that the move is valid before applying it
		if move not in game.next_moves():
			raise IllegalMove
		game = game.transform(move)
		if verbose:
			print game
			print "player: ", next, "score: ", -1*game.score(), ")"
		# switch the next player and continue the game play loop
		next = 3 - next


	score = game.score()
	if score > 0:
		print "player "+str(next)+" won with score", score
	elif score < 0:
		print "player "+str(3-next)+" won with score", -1*score
	else:
		winner = 0
		print "DRAW!!"
		
	player1.gameover(game, last_move)
	player2.gameover(game, last_move)

	if player1_ply and player2_ply:
		print "%d ply: Player 1 %.1f s per ply. Player2 %.1f s per ply" % (
			player1_ply+player2_ply, player1_think/player1_ply,
			player2_think/player2_ply)


