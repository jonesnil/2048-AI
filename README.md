This is a heuristic based AI for 2048 I made in college with some other programmers, Jake and Nathanael. 
Our goal was for it to make a 2048 tile at least once, and we ended up reaching that. It makes 2048 20% 
of the time with our best performing heuristic, and when it doesn't it usually gets at least 1024.

The 2048 python implementation wasn't made by us, but we programmed all the AI stuff on top of it.

# b351-final-project
# repository created 3/31/2019

# Instructions To Run 2048 AI (Updated: 5/1/2019)
Imports used/needed: tkinter, numpy, time, random
In order to launch the application. Navigate in a command prompt or terminal to the folder that contains the game_menu.py script.
Launch the game_menu.py script in a command prompt by typing "game_menu.py" and the game will automatically play with the configured heuristic.
In order to change the heuristic, you can open the game_menu.py script, scroll to the main method in the bottom and comment/uncomment what heursitic you'd like to run. The comments in the code will provide more information.
You can change the speed that the AI program runs by editing the global variables at the top of the game_menu.py file. The variable you want to change is, "loopDelay". Default = 100ms or 1/10 of a second per loop. Another example you can use is: loopDelay = 1000 (1000ms or 1 second per loop)
