#!/usr/bin/python3 

from game import Game 
from players import BMPlayer, BMSmithyPlayer
def main(): 
    game = Game([BMPlayer(), BMSmithyPlayer()]) 
    game.play() 
    print(game) 
    return game 

main()    