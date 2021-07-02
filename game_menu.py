import tkinter as tk
import tkinter.messagebox as mb
import numpy as np
import game_logic as gl
import game_data as gd
import time #ntavares edit 4/7/2019
import random


# NOTE:
#
# The following methods are from an outside implementation of 2048, https://github.com/KuoAiTe/python-tkinter-2048 from user: KuoAiTe on github
#   buildMenu()
#   evNew() evSave() evExit() evHelp() evAbout() evRestore()
#   builgBoard()
#   gametocells()
#   cellstogame()
#   keypress()
#   downkey() upkey() leftkey() rightkey()
#
#
# The following methods are from our team (group 10)
#   nextBestMoveMergeHeuristic()
#   nextBestMoveMergeHeuristicHypothetical()
#   nextBestMoveMergeCorner()
#   nextBestMoveCornerHeuristic()
#   several lines in main() to run our heuristics





#ntavares edit 4/21/2019
#variables for changing Delays across all references
initialDelay = 1000
loopDelay = 100

#creates the menu at the top of the window
def buildMenu(parent):
    #parent is a top level menu bar object
    menus = (
        ("File",(("New",evNew), ("Restore",evRestore), ("Save",evSave), ("Quit",evExit))),
        ("Help",(("Help",evHelp), ("About",evAbout))) #ntavares edit 4/21/2019
    )
    menubar = tk.Menu(parent)
    
    for menu in menus:
        m = tk.Menu(parent)
        for item in menu[1]:
            m.add_command(label=item[0],command=item[1])
        menubar.add_cascade(label=menu[0],menu=m)
    return menubar

def evNew():
    if status ['text'] == "Playing game":
        save = mb.askyesnocancel("Start New Game", "Do you want to save this game before starting a new game?")
        if save:
            evSave()
        elif save == None:
            pass
        else:
            status['text'] = "Playing game"
            gametocells(gl.newGame())
    else:
        status['text'] = "Playing game"
        gametocells(gl.newGame())
def evSave():
    game = cellstogame()
    gd.saveGame(game)
def evExit():
    if status['text'] == "Playing game":
        save = mb.askyesnocancel("Quitting","Do you want to save the game before quitting?")
        if save:
            evSave()
        elif save == None:
            pass
        else:
            top.quit()
            top.destroy()
    else:
        top.quit()
        top.destroy()
def evHelp():
    mb.showinfo("Help","Press the arrow keys to start playing")
def evAbout():
    mb.showinfo("About","2048game GUI made by Lingyi")
def evRestore():
    status['text'] = "Playing game"
    game = gd.restoreGame()
    gametocells(game)

    #ntavares edit 4/7/2019
    #a function that makes a random choice of moving up/down/left/right
    #doesn't check for validity or anything. Loops every 1 second until user exits game
    #for testing interaction with board.
def randomChoice(top, loop):
    if (gl.gameOver(cellstogame()) == False):
        loop = loop + 1
        print("loop iteration: " + str(loop))
        my_move = random.randrange(1, 5, 1) #random int from 1 to 4
        key = "up" #default 
        if (my_move == 1):
            key = "left" #go left
        if (my_move == 2):
            key = "right" #go right
        if (my_move == 3):
            key = "up" #go up
        if (my_move == 4):
            key = "down" #go down
        keypress(key)
        top.after(loopDelay, randomChoice, top, loop)
    else:
        print("Game Ended")




    #ntavares edit 4/11/2019
    #this function will take: tkinter object, loop counter[debug], and the current board
    #it will find the child boards of the given board
    #then using a given heuristic it will rank each possible child board
    #then we will make the best move
    #then it will call this function again, with the currentBoard = the best possible child board and move direction
    #this will loop until the game board is full and can no longer go 
def nextBestMoveMergeHeuristic(top, loop, currentBoard):
    
    if (gl.gameOver(cellstogame()) == False): #has the game ended?

        #DEBUG:
        loop = loop + 1
        print("loop iteration: " + str(loop))

        #get child boards and moves:
        #children = gl.generateChildren(currentBoard)
        #boards = children[0]
        #moves = children[1]
        
        moves = ["up", "down", "left", "right"]

        #this block is just to make sure that if no moves make a merge it picks one that slides something
        best_move = [moves[random.randint(0,3)],0]
        while (gl.userMove(currentBoard, best_move[0]) == currentBoard).all():
            best_move = [moves[random.randint(0, 3)], 0]

        #this just goes through all the moves and picks whichever has the best score
        for move in moves:
            score = gl.getMergeScore(currentBoard, move)
            if score > best_move[1]:
                best_move = [move, score]
            
            
        
        #i changed this a little bit just to fit my for loop implementation
        #best_move = "up"  <---- replace "up"       CALL HEURISTIC HERE ON CHILDREN BOARDS AND RETURNS THE BEST MOVE ("up", "down", "left", "right")
        currentBoard = keypress(best_move[0])
        
        #keep looping until we can't anymore
        top.after(loopDelay, nextBestMoveMergeHeuristic, top, loop, currentBoard) #recalls the loop every 1000ms or 1sec
    else:
        print("Game Ended")

    #this is just merge heuristic, but it considers two moves ahead instead of one.
def nextBestMoveMergeHeuristicHypothetical(top, loop, currentBoard):
    
    if (gl.gameOver(cellstogame()) == False): #has the game ended?

        #DEBUG:
        loop = loop + 1
        print("loop iteration: " + str(loop))
        #get child boards and moves:
        #children = gl.generateChildren(currentBoard)
        #boards = children[0]
        #moves = children[1]
        
        moves = ["up", "down", "left", "right"]

        #this block is just to make sure that if no moves make a merge it picks one that slides something
        best_move = [moves[random.randint(0,3)],0]
        while (gl.userMove(currentBoard.copy(), best_move[0]) == currentBoard).all():
            best_move = [moves[random.randint(0, 3)], 0]

        #this just goes through all the moves and picks whichever has the best score
        for move in moves:
            tempScore = gl.getMergeScore(currentBoard.copy(), move)
            if(gl.userMove(currentBoard.copy(), move) == currentBoard.copy()).all():
                continue
            for move2 in moves:
                score = gl.getMergeScoreHypothetical(gl.userMove(currentBoard.copy(), move), move2) + (tempScore - 1)
                if score > best_move[1]:
                    best_move = [move, score]
            
        #i changed this a little bit just to fit my for loop implementation
        #best_move = "up"  <---- replace "up"       CALL HEURISTIC HERE ON CHILDREN BOARDS AND RETURNS THE BEST MOVE ("up", "down", "left", "right")
        currentBoard = keypress(best_move[0])
        
        #keep looping until we can't anymore
        top.after(loopDelay, nextBestMoveMergeHeuristicHypothetical, top, loop, currentBoard) #recalls the loop every 1000ms or 1sec
    else:
        print("Game Ended")

#this is the function that combines merge hypothetical with the corner heuristic.
def nextBestMoveMergeCorner(top, loop, currentBoard):
    
    if (gl.gameOver(cellstogame()) == False): #has the game ended?

        #DEBUG:
        loop = loop + 1
        print("loop iteration: " + str(loop))
        #get child boards and moves:
        #children = gl.generateChildren(currentBoard)
        #boards = children[0]
        #moves = children[1]
        
        moves = ["up", "down", "left", "right"]

        #this block is just to make sure that if no moves make a merge it picks one that slides something
        best_move = [moves[random.randint(0,3)],0]
        while (gl.userMove(currentBoard.copy(), best_move[0]) == currentBoard).all():
            best_move = [moves[random.randint(0, 3)], 0]

        #this just goes through all the moves and picks whichever has the best score
        for move in moves:
            tempScore = gl.getMergeScore(currentBoard.copy(), move)
            if(gl.userMove(currentBoard.copy(), move) == currentBoard.copy()).all():
                continue
            for move2 in moves:
                #sorry I know this line is kinda unwieldy. Basically it considers merges but it mostly prioritizes that
                # the very next move has a good corner.
                score = gl.getMergeScoreHypothetical(gl.userMove(currentBoard.copy(), move), move2) + (gl.highCorner3(gl.userMoveHypothetical(currentBoard.copy(), move))) + (gl.highCorner3(gl.userMove(currentBoard.copy(), move))) + tempScore
                if score > best_move[1]:
                    best_move = [move, score]
            
            
        #i changed this a little bit just to fit my for loop implementation
        #best_move = "up"  <---- replace "up"       CALL HEURISTIC HERE ON CHILDREN BOARDS AND RETURNS THE BEST MOVE ("up", "down", "left", "right")
        currentBoard = keypress(best_move[0])
        
        #keep looping until we can't anymore
        top.after(loopDelay, nextBestMoveMergeCorner, top, loop, currentBoard) #recalls the loop every 1000ms or 1sec
    else:
        print("Game Ended")


    # a heuristic thats favors the corner and the board with the best possible next move. They are scored separetly and then combined.
def nextBestMoveCornerHeuristic(top, loop, currentBoard):
    
    if (gl.gameOver(cellstogame()) == False): #has the game ended?

        oldgame = currentBoard.copy()


        #DEBUG:
        loop = loop + 1
        print("loop iteration: " + str(loop))
        
        children = gl.generateChildren(currentBoard) #[children, moves]
        moves = children[1]

        print("# children, len(moves): " + str(len(moves)))

        best_move = ["left", 0]

        #this is for testing the highCorner and openSpace heuristic by looping through
        #alll of the child boards and finding the best move with corresponding score - Jake
        high = 0
        for i in range(0, len(children)):
            score = gl.highCorner(children[0][i]) #this is for tesing the highCorne heuristic - Jake
            if score > high:
                high = score
                best_move = [children[1][i], score]
            
            
        currentBoard = oldgame
        #i changed this a little bit just to fit my for loop implementation
        #best_move = "up"  <---- replace "up"       CALL HEURISTIC HERE ON CHILDREN BOARDS AND RETURNS THE BEST MOVE ("up", "down", "left", "right")
        print("move: " + str(best_move[0]))
        print("Current Board: \n")
        print(currentBoard)

        currentBoard = keypress(best_move[0])
        print("New Board: \n")
        print(currentBoard)

        
        #keep looping until we can't anymore
        top.after(loopDelay, nextBestMoveCornerHeuristic, top, loop, currentBoard) #recalls the loop every 1000ms or 1sec

    else:
        print("Game Ended")


buttons=[]
def buildBoard(parent,size=4):
    outer = tk.Frame(parent,border=2,relief="sunken")
    inner = tk.Frame(outer)
    inner.pack()
    global buttons
    buttons = []
    for row in range(size):
        temp = []
        for col in range(size):
            cell = tk.Button(inner,text=" ",width="10",height="4")
            temp.append(cell)
            cell.grid(row=row,column=col)
        buttons.append(temp)
    return outer

def gametocells(game):
    size = len(game[0])
    table = board.pack_slaves()[0]
    copy = game
    for row in range(size):
        for col in range(size):
            num = copy[row][col]
            if num == 0:
                num = " "
            #writes the numbers on the buttons, if number is 0, it writes nothing
            table.grid_slaves(row=row,column=col)[0]['text']=str(num)
            #setting different colours for different numbers
            if num == " ":
                colour = "silver"
            elif num == 2:
                colour = "white"
            elif num == 4:
                colour = "grey"
            elif num == 8:
                colour = "sandybrown"
            elif num == 16:
                colour = "coral"
            elif num == 32:
                colour = "orangered"
            elif num == 64:
                colour = "red"
            elif num == 128:
                colour = "yellow"
            elif num == 256:
                colour = "gold"
            elif num == 512:
                colour = "green"
            elif num == 1024:
                colour = "teal"
            elif num == 2048:
                colour = "blue"
            else:
                colour = "purple"
            
            buttons[row][col].configure(bg=colour)

def cellstogame():
    table = board.pack_slaves()[0] #table is a frame object
    values = []
    size = 4
    for row in range(size):
        r = []
        for col in range(size):
            value = table.grid_slaves(row=row,column=col)[0]['text']
            try:
                value = int(value)
            except ValueError:
                #if value is empty, then it is considered 0
                value = 0
            r.append(value)
        values.append(r)
    return np.array(values)

def keypress(key):
    game = cellstogame()
    oldgame = game.copy()
    game = gl.userMove(game,key)
    if (oldgame == game).all():
        #check if it's a valid move, a valid move makes changes to the board
        #if not valid move, then it doesn't fill a cell with a new number
        pass
    else:
        #if valid move, fill a random cell with 2 or 4
        game = gl.fillCell(game)
        gametocells(game)
    if gl.gameOver(game):
        #no more valid moves left
        mb.showinfo("Game Over","Oh no, you lost!")
        new = mb.askyesno("","Do you want to start a new game?")
        if new:
            status['text'] = "Playing game"
            gametocells(gl.newGame()) #clears board and starts a new game
        else:
            status['text'] = "Game Over"

    #ntavares edit 4/11/2019:
    #need to return the new game board for feeding into our nextBestMove function
    #only returns if game isn't over
    return game

def downkey(event):
    key = "down"
    keypress(key)
def upkey(event):
    key = "up"
    keypress(key)
def leftkey(event):
    key = "left"
    keypress(key)
def rightkey(event):
    key = "right"
    keypress(key)


if __name__ == "__main__":
    top = tk.Tk()
    mbar = buildMenu(top)
    top["menu"] = mbar
    board = buildBoard(top)
    board.pack()
    status = tk.Label(top,text="2048",border=3,background = "lightgrey",foreground="red")
    status.pack(anchor="s",expand=True)
    
    w = 340
    h = 320

    sw = top.winfo_screenwidth()
    sh = top.winfo_screenheight()
        
    x = (sw - w)/2
    y = (sh - h)/2
    top.geometry('%dx%d+%d+%d' % (w, h, x, y))
    top.title("2048")
    
    top.bind("<Down>",downkey)

    top.bind("<Up>",upkey)
    top.bind("<Left>",leftkey)
    top.bind("<Right>",rightkey)
    status['text'] = "Playing game"
    gametocells(gl.newGame())
    top.lift()

    



    #here is where you can change the heuristic.

    #ntavares edit 4/11/2019:

    #uncomment to test random Heurstic
    #top.after(initialDelay, randomChoice, top, 0)

    #uncomment to test Merge Heurstic
    #top.after(initialDelay, nextBestMoveMergeHeuristic, top, 0, gl.newGame())

    #uncomment to test Corner Heuristic
    #top.after(initialDelay, nextBestMoveCornerHeuristic, top, 0, gl.newGame())

    #uncomment to test the Merge Heuristic that looks forward a move
    #top.after(initialDelay, nextBestMoveMergeHeuristicHypothetical, top, 0, gl.newGame())

    #uncomment to test the Merge Heuristic/Corner Heuristic that looks forward a move
    top.after(initialDelay, nextBestMoveMergeCorner, top, 0, gl.newGame())

    




    tk.mainloop()