# game2: play a 2 person game

from time import time
from othello import OthelloMove

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
    while not game.terminal_test():
        # compute the next move for the player
        t1 = time()
        if next == 1:
            (value, move) = player1.play(game, last_move)
        else:
            (value, move) = player2.play(game, last_move)
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
            print ("player %d plays %s (in %.1f s) evaluation value %d"
                   % (next, str(move), t2-t1, value))
        #check that the move is valid before applying it
        if move not in game.generate_moves():
            raise IllegalMove
        game = game.transform(OthelloMove(move))
        if verbose:
            print game
            print "(player", next, "score", -1*game.score(), ")"
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

    temp = game.copy()
    player1.gameover(temp, last_move)
    player2.gameover(temp, last_move)

    if player1_ply and player2_ply:
        print "%d ply: Player 1 %.1f s per ply. Player2 %.1f s per ply" % (
            player1_ply+player2_ply, player1_think/player1_ply,
            player2_think/player2_ply)

class player:
    def __init__(self, play_fn):
        self.play_fn = play_fn

    def play(self, game, opp_move):
        return self.play_fn(game)

    def gameover(self, game, last_move):
        pass

