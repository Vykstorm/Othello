#!/usr/bin/python
# -*- coding: iso8859-1 -*-
# Descripción: Este script define el juego Othello: La configuración de una
# partida en cierto instante de tiempo (estado). Y que movimientos puede
# realizar el jugador con el turno actual dada cierta configuración de la partida.


from minmax import State, Move, StaticEval



# each side of the game board
size = 8
# pre-computed values
range_size = range(size)
size_m = size - 1

# direction vectors (delta_row, delta_colum)
directions = [(-1,-1), (-1,0), (-1,1),
              (0,-1),          (0,1),
              (1,-1),  (1,0),  (1,1)]

tuple_in_dir = lambda tuple,dir: (tuple[0]+dir[0], tuple[1]+dir[1])
tuple_valid = lambda tuple: (tuple[0]>=0 and tuple[0]<size
                             and tuple[1]>=0 and tuple[1]<size)



# Esta clase representa la configuración de una partida del juego Othello en cierto instante de 
# tiempo (estado)
class OthelloState(State):
	
	# Este método inicializa la información sobre el estado de la partida.
	# Esta instancia representará la configuración inicial de una partida Othello si no
	# se indica ningún parámetro.
	# Puede especificarse la información sobre las casillas del tablero y que jugador tiene
	# el turno (MAX/MIN) por defecto MAX tiene el turno.
	# Las fichas blancas son del jugador MAX mientras que las fichas negras son las del
	# jugador MIN.
	def __init__(self, curr_player = True, board = None):	
		State.__init__(self, curr_player)
		if board is None:
			# initially an 8 by 8 square
			self.board = [[0 for j in range_size] for i in range_size]
			# with the middle four squares filled in
			# -1 is black +1 is white, 0 => empty
			self.board[3][3] = 1
			self.board[4][4] = 1
			self.board[3][4] = -1
			self.board[4][3] = -1
		else:
			# copy all the pieces from the old game
			self.board = [[board[i][j] for j in range_size]
						  for i in range_size]

	def get_color(self, tuple):
		return self.board[tuple[0]][tuple[1]]

	def set_color(self, tuple, playernum):
		self.board[tuple[0]][tuple[1]] = playernum


	# Devuelve la puntuación total del jugador que juega con las fichas blancas.
	# Si este valor es negativo significa que la puntuación del jugador con las fichas
	# negras es superior. Si es 0, hay un empate
	def score(game):
		# first compute the score with +ve for white and -ve for blacks
		score = 0
		for i in range_size:
			for j in range_size:
				score += game.board[i][j]

		return score
		
	# Comprueba si el juego ha finalizado
	def terminal_test(self):
		player = 1 if self.get_curr_player() else -1
		
		# first find an empty square
		for i in range_size:
			for j in range_size:
				if self.board[i][j] != 0:
					continue
				# now we'll test if either player can put a piece in this square
				for player in [-1, 1]:
					opp = -1 * player # compute this player's opponent
					# look in every direction
					for dir in directions:
						t = tuple_in_dir((i,j), dir)
						# till you find an opponent piece
						if (not tuple_valid(t)) or (self.get_color(t) != opp):
							continue
						# now, skip all the opponent pieces
						while self.get_color(t) == opp:
							t = tuple_in_dir(t, dir)
							if not tuple_valid(t):
								break
						else:
							# finally, if we get one of player's piece then
							# we can make the move
							if self.get_color(t) == player:
								return False
		return True
		
	def generate_moves(self):		
		player = 1 if self.get_curr_player() else -1
		opp = -1 * player # opponent player num
		
		# A legal move is an empty square, s.t.
		# there is a contiguous straight line from this square consisting of
		# opponent squares followed by player's square.
		moves = []
		for i in range_size:
			for j in range_size:
				# find an empty square
				if self.board[i][j] != 0:
					continue
				# look in every direction
				for dir in directions:
					t = tuple_in_dir((i,j), dir)
					# till you find an opponent piece
					if (not tuple_valid(t)) or (self.board[t[0]][t[1]] != opp):
						continue
					# now, skip all the opponent pieces
					while self.board[t[0]][t[1]] == opp:
						t = tuple_in_dir(t, dir)
						if not tuple_valid(t):
							break
					else:
						# finally if we get one of our own pieces then
						# make the move
						if self.get_color(t) == player:
							moves.append((i,j))
							# no point looking in any other direction
							break

		# if we don't have a move and the game is not over then
		# return the None move or "no move."
		if not moves and not self.terminal_test():
			moves = [None]
			
		return moves
		
	def play_move(self, move):
		new = OthelloState(not self.get_curr_player(), self.board)
				
		player = 1 if self.get_curr_player() else -1
		opp = -1 * player # opponent player
		
		new.set_color(move, player)

		# look in all directions
		for dir in directions:
			t = tuple_in_dir(move, dir)
			# if we don't find an opponent piece then there is nothing to flip
			if (not tuple_valid(t)) or (new.get_color(t) != opp):
				continue
			# now keep skip over all the opponent pieces
			while new.get_color(t) == opp:
				t = tuple_in_dir(t, dir)
				# there is nothing to flip we have reached the end of the board
				# without seeing our own color piece
				if not tuple_valid(t):
					break
			else:
				# now if we find our own piece then flip all these pieces
				if new.get_color(t) == player:
					t = tuple_in_dir(move, dir)
					while new.get_color(t) == opp:
						new.set_color(t, player)
						t = tuple_in_dir(t, dir)
		return new

	def __str__(self):
		ret = ''
		for i in range_size:
			for j in range_size:
				if self.board[i][j] == 0:
					ret += '. '
				elif self.board[i][j] == 1:
					ret += 'W '
				elif self.board[i][j] == -1:
					ret += 'B '
				else:
					return None
			ret += "\n"
		
		return ret


	## Métodos sobrecargados para poder usar el algoritmo Min-Max en Othello:

	# Debe devolver un valor booleano si el estado es terminal (fin de la partida)
	def is_leaf(self):
		return self.terminal_test()
	
	# Debe devolver todos los posibles movimientos que puede realizar un jugador dada esta
	# configuración de la partida
	def next_moves(self):
		return [OthelloMove(casilla) for casilla in self.generate_moves()];

	# Debe devolver otro estado que sea el resultado de aplicar el movimiento indicado
	# como parámetro dado el estado actual de la partida.
	def transform(self, move):
		return self.play_move(move.get_casilla())

	def __repr__(self):
		return repr(self.score())

# Las instancias de esta clase representan configuraciones del juego Othello en su estado
# inicial.
class OthelloGame(OthelloState):
	# Debe indicarse quién mueve primero MAX/MIN, por defecto, si no se indica, MAX tiene
	# el primer turno.
	def __init__(self, curr_player = True):
		OthelloState.__init__(self, curr_player)


# Esta clase representará un movimiento de un jugador en la partida Othello.
class OthelloMove:
	# Un movimiento en Othello es colocar una ficha sobre el tablero.
	# Debe indicarse en que posición se añade la ficha.
	# Si la casilla es None, representará que el jugador en cuestión ha dejado
	# pasar el turno y no ha movido la casilla.
	def __init__(self, casilla):
		self.casilla = casilla
		
	def get_casilla(self):
		return self.casilla
	
	def __repr__(self):
		return repr(self.casilla)
	
	def __str__(self):
		return str(self.casilla)



# Esta clase permite evaluar para cierta configuración de una partida del juego Othello,
# como de buena es la situación para MAX con respecto de MIN.
class OthelloEval(StaticEval):
	# Este método debe devolver un entero indicando como de bueno es el estado para MAX 
	# (mayor cuanto más favorable sera)
	def eval(self,state):
		pass
	
# Esta clase representa una función de evaluación estática para cierta configuración de una partida del juego
# Othello: El jugador que va en cabeza es aquel que tiene más fichas colocadas en el tablero.
class OthelloEvalSuma(OthelloEval):
	def eval(self,state):
		return state.score()



