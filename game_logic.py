'''
main logic for a 2048 game
functions are:
'''
import numpy as np
# import 2048data
from random import randint
import game_menu as gm


# NOTE:
#
# The following methods are from an outside implementation of 2048, https://github.com/KuoAiTe/python-tkinter-2048 from user: KuoAiTe on github
#   newGame()   
#   fillCell()
#   gameOver()
#   mergeCells()
#   userMove()
#   
#
# The following methods are from our team (group 10)
#   getScore()
#   getSum()
#   highCorner()
#   highCorner3()
#   highLines()
#   openSpaces()
#   getMergeScore()
#   mergeCellsHypothetical()
#   userMoveHypothetical()
#   mergeScoreHelperHypothetical
#   getMergeScoreHypothetical()
#   generateChildren()




def newGame(size=4):
    empty = np.zeros((size,size), dtype=np.int)
    return fillCell(empty)

def fillCell(game):
    # fills a random empty cell with 2
    # takes an array, returns an array with a random empty cell filled
    size = len(game)
    emptycells = []
    # the loop gets a list of empty cells
    for row in range(size):
        for col in range(size):
            if game[row][col] == 0:
                emptycells.append([row, col])
    # check if there are empty cells
    if emptycells:
        # uses randint to get a random index from the list of empty cells
        celltofill = emptycells[randint(0, len(emptycells)-1)]
        r, c = celltofill
        # gets a distribution with 10% chance of 4
        distribution = [2 for i in range(9)]
        distribution.append(4)
        num = np.random.choice(np.array(distribution))
        # fills the cell with 2 or 4
        game[r][c] = num
        return game
    else:
        # case when no empty cells
        return


def getScore(game):
    #every board should have at least a 2
    max = 2
    for row in game:
        for column in row:
            if column > max:
                max = column
    return max


#This is the heuristic that scores based on the sum of the tiles added together - Jake

def getSum(game):
    total = 0
    size = len(game)
    for r in range(size):
        for c in range(size):
            total += game[r][c]
    return total

#This is a heuristic that scores based on the highest scored tiles in one of the corners - Jake
#not sure if this is the best or correct way to do this one

def highCorner(child):
    top_left = child[0][0]
    top_right = child[0][3]
    bot_left = child[3][0]
    bot_right = child[3][3]

    highest = max([top_left, top_right, bot_left, bot_right])
    return highest

#this is a slightly changed high corner which considers the spots right next to a corner.
def highCorner3(child):
    top_left = child[0][0]*2 + child[0][1] + child[1][0] 
    top_right = child[0][3]*2 + child[0][2] + child[1][3] 
    bot_left = child[3][0]*2 + child[3][1] + child[2][0] 
    bot_right = child[3][3]*2 + child[3][2] + child[2][3] 

    highest = max([top_left, top_right, bot_left, bot_right])
    return highest

def highLines(child):
    top_left = child[0][0]*4 + child[0][1]*2 + child[0][2] + child[0][3]/2
    top_right = child[0][0]*4 + child[1][0]*2 + child[2][0] + child[3][0]/2
    bot_left = child[3][3]*4 + child[3][2]*2 + child[3][1] + child[3][0]/2
    bot_right = child[3][3]*4 + child[2][3]*2 + child[1][3] + child[0][3]/2

    highest = max([top_left, top_right, bot_left, bot_right])
    return highest


            

#This is a heuristic that scores based on how many open spaces there are - Jake

def openSpaces(child):
    opens = 0
    size = len(child)
    for r in range(size):
        for c in range(size):
            if child[r][c] == 0:
                opens +=1
    return opens



# This is the heuristic that scores based on new merging. It's mostly a rework of the userMove
# and mergeCells function, because it's really just simulating a user move but just keeping track of 
# the merges themselves.

def getMergeScore(game, key):
    score = 0
    size = len(game)
    if key == "up" or key == "down":
        for col in range(size):
            a = game[:, col] 
            score += mergeScoreHelper(a, key)
        return score
    elif key == "left" or key == "right":
        for row in range(size):
            a = game[row]
            score += mergeScoreHelper(a, key)
        return score
    

#While getMergeScore is a rework of userMove, this one below is a rework of mergeCells.
#it does the same thing except it doesn't bother making a new board and it tallys its merges.

def mergeScoreHelper(rc, direction):
    score = 0
    # first argument is a row/col as a 1d array,
    # second argument can be "left","right","up" or "down"
    # effect of "left" and "up" is the same, "right" and "down" also
    # finds cells to merge and returns the row/col as an array
    if direction == "right" or direction == "down":
        rc = rc[::-1]
    
    if not np.all(rc):
        # if there are zeros, shifts all the zeros to the right
        nonzero_elements = []
        for i in range(len(rc)):
            if rc[i] != 0:
                nonzero_elements.append(rc[i])
        zeros = len(rc)-len(nonzero_elements)
        for extra in range(zeros):
            nonzero_elements.append(0)
        rc = np.array(nonzero_elements)
    
    # find adjacent cells that are the same and merge. 

    #this last system is just to make sure 3 in a row isnt treated as two pairs but four
    # is still two pairs -Nick
    justMergedThis = 0
    for i in range(1, len(rc)):
        if rc[i] == rc[i-1] and rc[i] != 0:
            if not(rc[i] == justMergedThis):
                score += rc[i-1]*2
                justMergedThis = rc[i]
            else:
                justMergedThis = 0
        else:
            justMergedThis = 0
            
 
    return score

def gameOver(game):
    # checks if there are any possible moves left
    if np.all(game):
        # check that there are no empty cells
        can_merge = False
        size = len(game)
        # check if can merge with cell on the right
        for r in range(size):
            for c in range(size-1):
                if game[r][c] == game[r][c+1]:
                    can_merge = True
        #check if can merge with cell below
        for r in range(size-1):
            for c in range(size):
                if game[r][c] == game[r+1][c]:
                    can_merge = True
    # if there are empty cells, return gameover = False
    else:
        return False
    
    if can_merge == True:
        return False
    else:
        return True

def mergeCells(rc,direction):
    # first argument is a row/col as a 1d array,
    # second argument can be "left","right","up" or "down"
    # effect of "left" and "up" is the same, "right" and "down" also
    # finds cells to merge and returns the row/col as an array
    if direction == "right" or direction == "down":
        rc = rc[::-1]
    
    if not np.all(rc):
        # if there are zeros, shifts all the zeros to the right
        nonzero_elements = []
        for i in range(len(rc)):
            if rc[i] != 0:
                nonzero_elements.append(rc[i])
        zeros = len(rc)-len(nonzero_elements)
        for extra in range(zeros):
            nonzero_elements.append(0)
        rc = np.array(nonzero_elements)
    
    # find adjacent cells that are the same and merge
    for i in range(1, len(rc)):
        if rc[i] == rc[i-1] and rc[i] != 0:
            rc[i-1] *= 2
            rc[i] = 0
    # shift all the zeros to the right again
    if not np.all(rc):
        nonzero_elements = []
        for i in range(len(rc)):
            if rc[i] != 0:
                nonzero_elements.append(rc[i])
        zeros = len(rc)-len(nonzero_elements)
        for extra in range(zeros):
            nonzero_elements.append(0)
        rc = np.array(nonzero_elements)
    if direction == "right" or direction == "down":
        return rc[::-1]
    else:
        return rc


def userMove(game, key):
    # moves the numbers according to the keys pressed
    # returns the new game array
    oldgame = game
    size = len(game)
    if key == "up" or key == "down":
        newgame = []
        for col in range(size):
            # uses slicing to get each column
            a = game[:, col]  # a is a column
            newcol = mergeCells(a, key)
            newgame.append(newcol)
        return np.array(newgame).T
    elif key == "left" or key == "right":
        newgame = []
        for row in range(size):
            a = game[row]
            newrow = mergeCells(a,key)
            newgame.append(newrow)
        return np.array(newgame)

# merge cells hypothetical and usermove hypothetical together make a board like usermove, except it doesn't
# merge any block with a 0 between it and what it would merge with. This is because those 0's could potentially
# be 2's or 4's when the board places one. -Nick

def mergeCellsHypothetical(rc,direction):
    # first argument is a row/col as a 1d array,
    # second argument can be "left","right","up" or "down"
    # effect of "left" and "up" is the same, "right" and "down" also
    # finds cells to merge and returns the row/col as an array
    if direction == "right" or direction == "down":
        rc = rc[::-1]
    
    # find adjacent cells that are the same and merge
    for i in range(1, len(rc)):
        if rc[i] == rc[i-1] and rc[i] != 0:
            rc[i-1] *= 2
            rc[i] = 0

    # shift all the zeros to the right again
    if not np.all(rc):
        nonzero_elements = []
        for i in range(len(rc)):
            if rc[i] != 0:
                nonzero_elements.append(rc[i])
        zeros = len(rc)-len(nonzero_elements)
        for extra in range(zeros):
            nonzero_elements.append(0)
        rc = np.array(nonzero_elements)

    if direction == "right" or direction == "down":
        return rc[::-1]
    else:
        return rc

def userMoveHypothetical(game, key):
    # moves the numbers according to the keys pressed
    # returns the new game array
    oldgame = game
    size = len(game)
    if key == "up" or key == "down":
        newgame = []
        for col in range(size):
            # uses slicing to get each column
            a = game[:, col]  # a is a column
            newcol = mergeCellsHypothetical(a, key)
            newgame.append(newcol)
        return np.array(newgame).T
    elif key == "left" or key == "right":
        newgame = []
        for row in range(size):
            a = game[row]
            newrow = mergeCellsHypothetical(a,key)
            newgame.append(newrow)
        return np.array(newgame)

# The mergeScore Hypothetical functions down here are just mergeScores version
# of usermove hypothetical and mergecells hypothetical. They let mergeScore look two 
# moves ahead.  -Nick
def mergeScoreHelperHypothetical(rc,direction):
    # first argument is a row/col as a 1d array,
    # second argument can be "left","right","up" or "down"
    # effect of "left" and "up" is the same, "right" and "down" also
    # finds cells to merge and returns the row/col as an array
    if direction == "right" or direction == "down":
        rc = rc[::-1]
    
    # find adjacent cells that are the same and merge
    score = 0
    justMergedThis = 0
    for i in range(1, len(rc)):
        if rc[i] == rc[i-1] and rc[i] != 0:
            if not(rc[i] == justMergedThis):
                score += rc[i-1]*2
                justMergedThis = rc[i]
            else:
                justMergedThis = 0
        else:
            justMergedThis = 0
    return score

def getMergeScoreHypothetical(game, key):
    # moves the numbers according to the keys pressed
    # returns the new game array
    oldgame = game
    size = len(game)
    score = 0
    if key == "up" or key == "down":
        newgame = []
        for col in range(size):
            # uses slicing to get each column
            a = game[:, col]  # a is a column
            score += mergeScoreHelperHypothetical(a, key)
        return score
    elif key == "left" or key == "right":
        for row in range(size):
            a = game[row]
            score += mergeScoreHelperHypothetical(a,key)
        return score

    


    #ntavares edit 4/11/2019
    #this function will take a game (in array form) and return a tuple of child boards and child moves
    # EX:
    #   myChildBoards[2] = myChildMoves[2] so we know what move is binded to what board
    #   View the main function to see how this is used better

def generateChildren(game):
    #This function will create the possible child boards from a given gameboard
    #it does not include the 2 or 4 being randomly generated

    oldgame = game.copy()

    game = oldgame.copy()
    board1 = userMove(game, "up")
    game = oldgame.copy()
    board2 = userMove(game, "down")
    game = oldgame.copy()
    board3 = userMove(game, "left")
    game = oldgame.copy()
    board4 = userMove(game, "right")
    game = oldgame.copy()

    myBoards = [board1, board2, board3, board4] #create our list of child boards to return
    myMoves = ["up", "down", "left", "right"] #binds each move to its board ^ (needed later)

    #if the child board is the same as the parent board don't add it to the list because this move isn't a valid move
    #This is because with this given implementation of 2048 when you slide in one direction multiple times it doens't check to
    #see if it's "valid" per say. It will not shift the contents of the array, thus you know it was a useless slide.
    #like this line of code implemented below in main:

    #  if not (a == b).all():
    #          a = b
    #          fillCell(a)

    #we only fill the cell if it was a "valid" move

    myChildBoards = []
    myChildMoves = []

    #so let's check our boards and then add the possible children ones:
    for i in range(0, 4):
        if (myBoards[i] == oldgame).all():
            print("found matching board from child")
        if not ((myBoards[i] == game).all()):
            #keeps track of possible boards and their move values. 
            #the move values will be needed in the heursitic function so we know what MOVE (not board) to return
            myChildBoards.append(myBoards[i])
            myChildMoves.append(myMoves[i])


    #return our child boards for the heurstics to then iterate through and rank each one
    #note that child boards do not include the random 2 or 4 since this is random

    print("DEBUG: possible child boards: ")

    print("GAME: \n")
    print(game)
    
    for i in range(0, len(myChildBoards)):
        print(myChildBoards[i])
        print("\n")

    return myChildBoards, myChildMoves



if __name__ == "__main__":
    a = newGame()

    while not gameOver(a):
        print(a)

        # uncomment below to test getScore - Nick
        #print("Score =", getScore(a))

        char = input("Please press a key")
        if char == "w":
            key = "up"
        elif char == "s":
            key = "down"
        elif char == "a":
            key = "left"
        elif char == "d":
            key = "right"
        
        # uncomment below to test getMergeScore. Also, if the first key you type is not 
        # WASD it will error. (because key wont be instantiated) - Nick
        # print("Merge Score =", getMergeScore(a, key))
        
        # Below is what I added to make the game not slide or add a tile if no change would come of a move. -Nick

        newBoard = userMove(a, key)
        if not (a == newBoard).all():
            hypotheticalBoard = userMoveHypothetical(a, key)
            print(hypotheticalBoard)
            a = newBoard
            fillCell(a)
            

        #ntavares edit 4/11/2019
        #un-comment this and run game_logic.py to see that this function returns the possible child boards correclty

        """
        print("\n")
        print("Our Child Boards Test: \n")
        print("child boards created... ")
        print("PARENT BOARD: ")
        print(a)
        print("\n")
        children = generateChildren(a)
        
        #get our moves and children
       
        boards = children[0]
        moves = children[1]

        board_string = 1
        for i in range (0, len(boards)):
            print("CHILD BOARD " + str(board_string) + " MOVE DIRECTION: " + moves[i])
            print(boards[i])
            board_string += 1
        print("end debug for child boards. \n")
        """


        
        
    else:
        print("gameover!")
