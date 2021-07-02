'''
saves and restores data for a 2048 game
'''

import os.path
import numpy as np
game_file = ".2048game.dat"

def _getPath():
    # returns a valid path to save the data file
    return os.getcwd()

def restoreGame():
    #returns previously saved game as a 4 by 4 array
    path = os.path.join(_getPath(),game_file)
    with open(path,'r') as gf:
        oldgame = np.loadtxt(path)
    return oldgame.astype(int)

def saveGame(game):
    #saves a game object in the data file in the current folder
    #input is an array
    path = os.path.join(_getPath(),game_file)
    np.savetxt(path,game)
    with open(path,'w') as gf:
        np.savetxt(path,game)