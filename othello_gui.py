#!/usr/bin/python
# -*- coding: iso8859-1 -*-

#    othello_gui: a GUI based interface to get the user's move
#    Copyright (C) 2006  Nimar S. Arora
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#    nimar.arora@gmail.com
    
import Tkinter
import time
import othello
from othello import OthelloMove
from game2 import Player


BOXWIDTH=80
BOXHEIGHT=80

class GUIPlayer(Player):
    """Make a user player to play the game via a GUI."""

    def __init__(self):
        # create the GUI state variables
        self.alive = True
        self.move = None
        self.move_played = False
        # create the GUI windows and handlers
        self.root = Tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        # create a button to get the No move command from the user
        Tkinter.Button(self.root, text="No Move", command = self.nomove).pack()
        # create a label for displaying the next player's name
        self.movemesg = Tkinter.StringVar()
        Tkinter.Label(self.root, textvariable=self.movemesg).pack()
        self.canvas = Tkinter.Canvas(self.root, bg="lightblue",
                                    height = BOXHEIGHT*othello.size,
                                    width = BOXWIDTH*othello.size)
        self.canvas.bind("<Button-1>", self.click)
        # create a box for highlighting the last move
        self.lastbox = self.canvas.create_rectangle(0, 0, BOXWIDTH*othello.size,
                                                    BOXHEIGHT*othello.size,
                                                    outline="yellow")
        
        # draw the game canvas
        for i in xrange(1,othello.size):
            # horizontal lines
            self.canvas.create_line(0, i*BOXHEIGHT,
                                   BOXWIDTH*othello.size, i*BOXHEIGHT)                                   
            # vertical lines
            self.canvas.create_line(i*BOXWIDTH, 0,
                                   i*BOXWIDTH, BOXHEIGHT*othello.size)                                
        # the board will store the widgets to be displayed in each square
        self.board = [[None for y in range(othello.size)]
                      for x in range(othello.size)]
        # display the window
        self.canvas.pack()
        self.canvas.focus_set()
        self.root.update()

    def draw_board(self, game, last_move):
        """Draw an othello game on the board."""

        if not game.get_curr_player():
            self.movemesg.set("Black to play")
        else:
            self.movemesg.set("White to play")

        for i in range(othello.size):
            for j in range(othello.size):
                color = game.get_color((i,j))
                if color == -1:
                    board_color = "black"
                elif color == 1:
                    board_color = "white"
                else:
                    if self.board[i][j] is not None:
                        self.canvas.delete(self.board[i][j])
                        self.board[i][j] = None
                    continue

                if self.board[i][j] is None:
                    self.board[i][j] = self.canvas.create_oval(
                        j*BOXWIDTH+2, i*BOXHEIGHT+2, (j+1)*BOXWIDTH-2,
                        (i+1)*BOXHEIGHT-2, fill = board_color)
                else:
                    self.canvas.itemconfig(self.board[i][j], fill=board_color)
                                                            
        # highlight the last move
        if last_move is None:
            self.canvas.coords(self.lastbox,
                               1, 1, BOXWIDTH*othello.size-1,BOXHEIGHT*othello.size-1)
        else:
            self.canvas.coords(
                self.lastbox, last_move[1]*BOXWIDTH+1, last_move[0]*BOXHEIGHT+1,
                (last_move[1]+1)*BOXWIDTH-1, (last_move[0]+1)*BOXHEIGHT-1)
                                

    def nomove(self):
        self.move = None
        self.move_played = True
        
    def click(self, event):
        self.move = (event.y/BOXHEIGHT, event.x/BOXWIDTH)
        self.move_played = True
        
    def quit(self):
        self.alive = False
        self.root.destroy()
        
    def play(self, game, last_move):

        # keep looping for a user move unless the user quits        
        while self.alive:
            # wait for a user move
            self.move_played = False
            # grab the focus to ask the user for a move
            self.draw_board(game, last_move)
            self.canvas.focus_force()
            self.root.configure(cursor="target")
            while (not self.move_played) and self.alive:
                self.root.update()
                time.sleep(0.1)

            if not self.move_played:
                continue

            # check the move
            if self.move not in game.generate_moves():
                self.root.bell()
                continue

            # display the new move
            game.play_move(self.move)
            self.draw_board(game, self.move)
            self.root.configure(cursor="watch")
            self.root.update()
            # give a pause so I can see my move
            time.sleep(.1)
            return OthelloMove(self.move)
            
        # if the user has quit the GUI then the game has to terminate,
        # we force a termination by returning an illegal value
        else:
            return None

    def gameover(self, game, last_move):

        score = game.score() * (1 if game.get_curr_player() else -1)
        if score > 0:
            win_text = "White Won"
        elif score < 0:
            win_text = "Black Won"
        else:
            win_text = "Draw"

        self.draw_board(game, last_move)        
        self.root.configure(cursor="X_cursor")
        self.movemesg.set("Game Over "+win_text)

        # wait for the user to quit the game        
        while self.alive:
            self.root.update()
            time.sleep(.1)
