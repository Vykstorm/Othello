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
	# el turno (jugador1=True, jugador2=False) por defecto jugador1 tiene el turno.
	# Las fichas blancas son del jugador 1 mientras que las fichas negras son las del
	# jugador 2
	def __init__(self, curr_player = True, board = None):	
		State.__init__(self,curr_player)
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
	# negras es superior. Si es 0, hay un empate.
	# Puede indicarse de forma opcional, dos parámetros. El primero indica el valor que tendrán
	# las fichas que estén en los bordes del tablero (En vez de tener valor 1). 
	# El otro, indicará el valor de las fichas que se encuentren en las esquinas.
	# Por defecto, estos parámetros son 1.
	def score(game, valor_borde = 1, valor_esquina = 1):
		# first compute the score with +ve for white and -ve for blacks
		score = 0
		for i in range_size:
			for j in range_size:
				if (i == 0) or (j == 0) or (i == size_m) or (j == size_m):
					# Estamos en un borde o en una esquina
					if abs(i-j) in [0, size_m]:
						# Estamos en una esquina.
						score += game.board[i][j] * valor_esquina
					else:
						# Estamos en un borde.
						score += game.board[i][j] * valor_borde
				else:
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
		if not moves and not self.terminal_test():
			moves = [None]
		
		return moves
		
	def play_move(self, move):
		new = OthelloState(not self.get_curr_player(), self.board)
				
		player = 1 if self.get_curr_player() else -1
		opp = -1 * player # opponent player
		
		if not move is None:
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
		return [OthelloMove(casilla) if not casilla is None else None for casilla in self.generate_moves()];

	# Debe devolver otro estado que sea el resultado de aplicar el movimiento indicado
	# como parámetro dado el estado actual de la partida.
	def transform(self, move):
		return self.play_move(move.get_casilla()) if not move is None else self.play_move(None)

	def __repr__(self):
		return repr(self.score())



	# M�todos adicionales.
	# Devuelve una lista de listas. La lista en la posici�n i-�sima representa la fila i-�sima del tablero.
	def get_rows(self):
		return self.board
		
	# Devuelve una lista de listas. La lista en la posici�n i-�sima representa la columna i-�sima del tablero.
	def get_cols(self):
		return [map(lambda R:R[j], self.board) for j in range(0,size)]
		
	# Devuelve una lista de listas. La lista en la posici�n i-�sima representa la diagonal i-�sima de 45�
	def get_diags45(self):
		diags = [[self.board[i][j] for i,j in zip(range(k,-1,-1),range(0,k+1))] for k in range(0,size)]
		diags = diags + [[self.board[i][j] for i,j in zip(range(k,size),range(size_m,k-1,-1))] for k in range(1,size)]
		return diags
		
	# Devuelve una lista de listas. La lista en la posici�n i-�sima representa la diagonal i-�sima de 135�
	def get_diags135(self):
		diags = [[self.board[i][j] for i,j in zip(range(0,k+1),range(size_m-k,size))] for k in range(0,size)]
		diags = diags + [[self.board[i][j] for i,j in zip(range(k,size),range(0,size_m-k+1))] for k in range(1,size)]
		return diags

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
	
	def __eq__(self, otro):
		return isinstance(otro,OthelloMove) and (self.get_casilla() == otro.get_casilla())
		
	def get_casilla(self):
		return self.casilla
	
	def __repr__(self):
		return repr(self.casilla)
	
	def __str__(self):
		return str(self.casilla)

	def __getitem__(self, index):
		if (type(index) != int) or not (index in [0, 1]):
			raise IndexError()
		return self.casilla[index]


# Esta clase permite evaluar para cierta configuración de una partida del juego Othello,
# como de buena es la situación para MAX con respecto de MIN.
class OthelloEval(StaticEval):
	# Este método debe devolver un entero indicando como de bueno es el estado para MAX 
	# (mayor cuanto más favorable sera)
	def eval(self,state,jugador_max):
		pass
		
# Esta clase representa una función de evaluación estática en base a la diferencia de piezas entre el jugador
# MAX y el jugador MIN
class OthelloEvalDiffPiezas(OthelloEval):
	def eval(self,state,jugador_max):
		return state.score() if jugador_max else -state.score()
			

# Esta clase representa una función de evaluación estática que tiene en cuenta posiciones estables del tablero
# (bordes y esquinas)
class OthelloEvalComplex(OthelloEval):
	def eval(self,state,jugador_max):
		# Penalizamos cuando hay fichas del contrincante en zonas estables y premiamos
		# cuando el jugador tiene fichas en esas zonas
		valor_borde = 2
		valor_esquina = 4
		score = state.score(valor_borde, valor_esquina) if jugador_max else -state.score(valor_borde, valor_esquina)
		
		# Adem�s, penalizamos situaciones en las cuales:
		# EL jugador tiene varias fichas colocadas consecutivamente en una direcci�n
		# ya sea fila, columna o diagonal y estas est�n encerradas por un lado por una casilla
		# vac�a y por una ficha del contrincante por el otro lado. Si la casilla vac�a es adem�s
		# una posici�n estable, se incrementa la penalizaci�n.
		# Esto tambi�n se aplica cuando al rev�s, para premiar al jugador cuando la situaci�n es la
		# contraria.
		
		board = state.board
		penalti = 0
		for V in state.get_rows() + state.get_cols() + state.get_diags45() + state.get_diags135():
			k = 0
			while k+1 < len(V):
				while ((V[k] == (1 if jugador_max else -1)) or (V[k+1] != (1 if jugador_max else -1))) and (k < (len(V)-2)):
					k = k + 1
				
				if (V[k] != (1 if jugador_max else -1)) and (V[k+1] == (1 if jugador_max else -1)):
					j = k + 1
					if j == len(V)-1:
						break
					while (j < (len(V)-1)) and (V[j] == (1 if jugador_max else -1)):
						j = j + 1
					
					if V[j] != (1 if jugador_max else -1):
						if V[k] != V[j]:
							# Num fichas entre la ficha contrincante y la casilla vac�a.
							n = j - k - 1 
							# Penalizar...
							if n >= 3:
								if ((V[k] == 0) and ((k == 0) or (k == len(V)-1))) or ((V[j] == 0) and ((j == 0) or (j == len(V)-1))):
									penalti = penalti + 2 * n
								else:
									penalti = penalti + n
					k = j
				else:
					k = k + 1

		score = score - penalti 
		return score

o = OthelloGame()
o.set_color((4,2), -1)
o.set_color((4,1), -1)
print OthelloEvalComplex().eval(o,1)
