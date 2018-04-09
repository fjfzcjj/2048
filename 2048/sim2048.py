import turtle
from game2048 import play2048
import sys
import gc

# MODE
mode = "sim" # set to user, viewSim, or sim

# screen parameters
wX = 700	# size of the screen in the x-direction (pixels)
wY = 700	# size of the screen in the y-direction (pixels)
oX = 0		# top left corner of screen x value (pixels)
oY = 0		# top left corner of screen y value (pixels)
timeDelay = 0  # delay in ms

# world coordinates
lX = 0					# value of bottom left corner X (in WCS)
lY = 0					# value of bottom left corner Y (in WCS)
uX = 10					# value of upper right corner X (in WCS)
uY = 10					# value of upper right corner Y (in WCS)

# game board
shapesize = 6.5			# how much to stretch a single 2048 tile by 
startX = 2				# the starting x-value of the game board (in WCS)
startY = 1 				# the starting y-value of the game board (in WCS)
delta = 2				# the spacing between tiles on the game board
offsetY = 0.4			# a number for positioning the text on tiles

# position of score box and score text (measured in WCS)
scoreBoxX = 1		# the bottom left corner x-value of the scoreboard
scoreBoxY = 8.5     # the bottom left corner y-value of the scoreboard
scoreSizeX = 3		# the x-width of the scoreboard
scoreSizeY = 1		# the y-width of the scoreboard
scoreTextX = 1.1	# the x-position of the word 'score'
scoreTextY = 8.8	# the y-position of the word 'score'
scoreX = 4			# the x-position of where the score value is printed
scoreY = scoreTextY	# the y-position of where the score value is printed
scoreTextSize = 25  # the fontsize of the score

# initial tiles found on the board
#tiles = [[0,2,4,8],[16,32,64,128],[256,512,1024,2048],[4096,8192,16384,32768]] 
tiles = [[0,0,0,0],[4,0,0,0],[0,0,2,0],[0,0,0,0]]

# package constants into lists
screenSetup = [wX,wY,oX,oY,timeDelay]
wCor = [lX,lY,uX,uY]
scoreSetup = [scoreSizeX,scoreSizeY,scoreBoxX,scoreBoxY]
scoreText = [scoreTextX,scoreTextY,scoreX,scoreY,scoreTextSize]
shapeInfo = [shapesize,delta,startX,startY,offsetY]

# colors of tiles (in RGB values)
colors = dict()
colors[0] = (1,1,1)
colors[2] = (1,0,0)
colors[4] = (1,0.4,0)
colors[8] = (1,0.8,0)
colors[16] = (0.8,1,0)
colors[32] = (0.4,1,1)
colors[64] = (0,1,0)
colors[128] = (0,1,0.4)
colors[256] = (0,1,0.8)
colors[512] = (0,0.8,1)
colors[1024] = (0,0.4,1)
colors[2048] = (0,0,1)
colors[4096] = (0.4,0,1)
colors[8192] = (0.8,0,1)
colors[16384] = (1,0,0.8)
colors[32768] = (1,0,0.4)

# objects
if mode!="sim":
	screen = turtle.Screen()	# the screen
	pen = turtle.Turtle()		# the object that draws everything except for the score
	scoreObj = turtle.Turtle()	# the object that draws the score
	sys.setrecursionlimit(2000)
else:
	screen = "BOOP"
	pen = "BAP"
	scoreObj = "BLIP"

# start game
if mode=="sim":
	scores = list()
	avScor = 0
	N = 1000
	for n in range(N):
		game = play2048(screenSetup,scoreSetup,scoreText,wCor,shapeInfo,colors,screen,pen,scoreObj,tiles,mode) # create the game object
		game.setupGame()	# setup the game
		game.loop()			# start the game
		scores.append(game.currentScore)
		del game
		avScor += scores[n]/N
		print("Done {} of {}, score = {}".format(n+1,N,scores[n]))
	print("Average Score: {:0.2f}".format(avScor))
else:
	game = play2048(screenSetup,scoreSetup,scoreText,wCor,shapeInfo,colors,screen,pen,scoreObj,tiles,mode)
	game.setupGame()
	game.loop()
# exit condition
# game = play2048(screenSetup,scoreSetup,scoreText,wCor,shapeInfo,colors,screen,pen,scoreObj,tiles,mode) # create the game object
# game.setupGame()	# setup the game
# game.loop()			# start the game
if mode != "sim":
	turtle.mainloop()		
