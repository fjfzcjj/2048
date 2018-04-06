import turtle
import random
import drawHelp
import time
import copy

class play2048():

	def __init__(self,screenSetup,scoreSetup,scoreText,wCor,shapeInfo,colors,screen,pen,scoreObj,tiles,mode):
		self.wX = screenSetup[0]
		self.wY = screenSetup[1]
		self.oX = screenSetup[2]
		self.oY = screenSetup[3]
		self.wait = screenSetup[4]
		self.scoreSizeX = scoreSetup[0]
		self.scoreSizeY = scoreSetup[1]
		self.scoreBoxX = scoreSetup[2]
		self.scoreBoxY = scoreSetup[3]
		self.scoreTextX = scoreText[0]
		self.scoreTextY = scoreText[1]
		self.scoreX = scoreText[2]
		self.scoreY = scoreText[3]
		self.scoreTextSize = scoreText[4]
		self.lX = wCor[0]
		self.lY = wCor[1]
		self.uX = wCor[2]
		self.uY = wCor[3]
		self.shapesize = shapeInfo[0]
		self.delta = shapeInfo[1]
		self.startX = shapeInfo[2]
		self.startY = shapeInfo[3]
		self.offsetY = shapeInfo[4]
		self.screen = screen
		self.pen = pen
		self.scoreObj = scoreObj
		self.colors = colors
		self.currentScore = 0
		self.numList = copy.deepcopy(tiles)
		self.numListOld = [[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
		self.stampID = [[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
		self.testList = [[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
		self.moveQueue = list()
		self.numMoves = 0
		self.simMove = 0
		self.mode = mode
		if mode=="sim":
			self.startSim()
		return

	def __str__(self):
		list1 = self.numList
		list2 = self.numListOld
		list3 = self.stampID
		output1 = "NUMLIST:\n{:5d} {:5d} {:5d} {:5d}\n{:5d} {:5d} {:5d} {:5d}\n{:5d} {:5d} {:5d} {:5d}\n{:5d} {:5d} {:5d} {:5d}\n".format(list1[0][3], \
			list1[1][3],list1[2][3],list1[3][3],list1[0][2],list1[1][2],list1[2][2],list1[3][2],list1[0][1],list1[1][1],list1[2][1],list1[3][1],list1[0][0],\
			list1[1][0],list1[2][0],list1[3][0])

		output2 = "NUMLIST OLD:\n{:5d} {:5d} {:5d} {:5d}\n{:5d} {:5d} {:5d} {:5d}\n{:5d} {:5d} {:5d} {:5d}\n{:5d} {:5d} {:5d} {:5d}\n".format(list2[0][3], \
			list2[1][3],list2[2][3],list2[3][3],list2[0][2],list2[1][2],list2[2][2],list2[3][2],list2[0][1],list2[1][1],list2[2][1],list2[3][1],list2[0][0],\
			list2[1][0],list2[2][0],list2[3][0])

		if self.mode=="user" or self.mode=="viewSim":
			output3 = "STAMPID:\n{:5d} {:5d} {:5d} {:5d}\n{:5d} {:5d} {:5d} {:5d}\n{:5d} {:5d} {:5d} {:5d}\n{:5d} {:5d} {:5d} {:5d}\n".format(list3[0][3], \
				list3[1][3],list3[2][3],list3[3][3],list3[0][2],list3[1][2],list3[2][2],list3[3][2],list3[0][1],list3[1][1],list3[2][1],list3[3][1],list3[0][0],\
				list3[1][0],list3[2][0],list3[3][0])
		else:
			output3 = "SCORE:\n{:5d}\n".format(self.currentScore)


		output4 = "MOVE QUEUE:\n"
		for i in range(len(self.moveQueue)):
			output4 = output4+self.moveQueue[i]+","
		output4 = output4 + "\n"
		output5 = "NUMBER OF USER MOVES:\n{:5d}\n".format(self.numMoves)
		output6 = "____________________________\n"

		return output6+output1+output2+output3+output4+output5+output6

	def setupGame(self):
		# setup screen
		screen = self.screen 
		pen = self.pen
		scoreObj = self.scoreObj
		#setup screen
		if self.mode=="user" or self.mode=="viewSim":
			screen.setup(self.wX,self.wY,self.oX,self.oY) 
			screen.setworldcoordinates(self.lX,self.lY,self.uX,self.uY) 
			screen.bgcolor("black")
			screen.tracer(0,0)
			# setup pen and score obj
			pen.speed(0)
			pen.shape("square")
			pen.shapesize(self.shapesize)
			pen.penup()
			pen.hideturtle()
			scoreObj.speed(0)
			scoreObj.hideturtle()
			scoreObj.penup()
			scoreObj.color("black")
			# draw score board
			drawHelp.drawRectFill(self.scoreBoxX,self.scoreBoxY,self.scoreSizeX,self.scoreSizeY,pen,"white")
			pen.goto(self.scoreTextX,self.scoreTextY)
			pen.color("black")
			pen.write("SCORE:",font=("Times",self.scoreTextSize,"bold"))
			self.updateScore()
			self.drawBoard()
			self.screen.update()
			for i in range(0,4):
				for j in range(0,4):
					self.numListOld[i][j] = self.numList[i][j]
		# bind event functions
			screen.onkeypress(self.up,"Up")
			screen.onkeypress(self.down,"Down")
			screen.onkeypress(self.right,"Right")
			screen.onkeypress(self.left,"Left")
			screen.listen()
			print(self)


	def updateScore(self):
		turt = self.scoreObj
		turt.clear()
		turt.goto(self.scoreX,self.scoreY)
		turt.write(self.currentScore,align="right",font=("Times",self.scoreTextSize,"bold"))

	def drawBoard(self):
		pen = self.pen
		for j in range(0,4):
			for i in range(0,4):
				pen.goto(self.startX+i*self.delta,self.startY+j*self.delta)
				pen.color(self.colors[self.numList[i][j]])
				if self.numList[i][j]!=self.numListOld[i][j]:
					pen.clearstamp(self.stampID[i][j])
					self.stampID[i][j] = pen.stamp()
					pen.goto(self.startX+i*self.delta,self.startY+j*self.delta-self.offsetY)
					string = str(self.numList[i][j])
					if self.numList[i][j]<1000:
						pen.color("black")
						fontsize = 45
					elif self.numList[i][j]<16000:
						pen.color("white")
						fontsize = 40
					else:
						pen.color("white")
						fontsize = 35
					if self.numList[i][j]:
						pen.write(string,align="center",font=("Times",fontsize,"bold"))

	def up(self):
		self.moveQueue.append("up")


	def down(self):
		self.moveQueue.append("down")


	def right(self):
		self.moveQueue.append("right")


	def left(self):
		self.moveQueue.append("left")


	def startSim(self):
		move = self.strategy()
		self.moveQueue.append(move)

	def upRule(self,actualList,doScore):
		numList = copy.deepcopy(actualList)
		for i in range(0,4):
			sumNum = numList[i][0]+numList[i][1]+numList[i][2]+numList[i][3]
			while numList[i][3]==0 and sumNum!=0:
				numList[i][3] = numList[i][2]
				numList[i][2] = numList[i][1]
				numList[i][1] = numList[i][0]
				numList[i][0] = 0

			sumNum = numList[i][0]+numList[i][1]+numList[i][2]
			while numList[i][2]==0 and sumNum!=0:
				numList[i][2] = numList[i][1]
				numList[i][1] = numList[i][0]
				numList[i][0] = 0

			sumNum = numList[i][0]+numList[i][1]
			while numList[i][1]==0 and sumNum!=0:
				numList[i][1] = numList[i][0]
				numList[i][0] = 0

			if numList[i][3]==numList[i][2] and numList[i][3]!=0:
				numList[i][3] = numList[i][3]+numList[i][2]
				numList[i][2] = numList[i][1]
				numList[i][1] = numList[i][0]
				numList[i][0] = 0
				if doScore:
					self.currentScore += numList[i][3]

			if numList[i][2]==numList[i][1] and numList[i][2]!=0:
				numList[i][2] = numList[i][2]+numList[i][1]
				numList[i][1] = numList[i][0]
				numList[i][0] = 0
				if doScore:
					self.currentScore += numList[i][2]

			if numList[i][1]==numList[i][0] and numList[i][1]!=0:
				numList[i][1] = numList[i][1]+numList[i][0]
				numList[i][0] = 0
				if doScore:
					self.currentScore += numList[i][1]
		return numList

	def downRule(self,actualList,doScore):
		numList = copy.deepcopy(actualList)
		for i in range(0,4):
			sumNum = numList[i][0]+numList[i][1]+numList[i][2]+numList[i][3]
			while numList[i][0]==0 and sumNum!=0:
				numList[i][0] = numList[i][1]
				numList[i][1] = numList[i][2]
				numList[i][2] = numList[i][3]
				numList[i][3] = 0
			sumNum = numList[i][1]+numList[i][2]+numList[i][3]
			while numList[i][1]==0 and sumNum!=0:
				numList[i][1] = numList[i][2]
				numList[i][2] = numList[i][3]
				numList[i][3] = 0
			sumNum = numList[i][2]+numList[i][3]
			while numList[i][2]==0 and sumNum!=0:
				numList[i][2] = numList[i][3]
				numList[i][3] = 0

			if numList[i][0]==numList[i][1] and numList[i][0]!=0:
				numList[i][0] = numList[i][0]+numList[i][1]
				numList[i][1] = numList[i][2]
				numList[i][2] = numList[i][3]
				numList[i][3] = 0
				if doScore:
					self.currentScore += numList[i][0]

			if numList[i][1]==numList[i][2] and numList[i][1]!=0:
				numList[i][1] = numList[i][2]+numList[i][1]
				numList[i][2] = numList[i][3]
				numList[i][3] = 0
				if doScore:
					self.currentScore += numList[i][1]

			if numList[i][2]==numList[i][3] and numList[i][2]!=0:
				numList[i][2] = numList[i][2]+numList[i][3]
				numList[i][3] = 0
				if doScore:
					self.currentScore += numList[i][2]

		return numList


	def leftRule(self,actualList,doScore):
		numList = copy.deepcopy(actualList)
		for i in range(0,4):
			sumNum = numList[0][i]+numList[1][i]+numList[2][i]+numList[3][i]
			while numList[0][i]==0 and sumNum!=0:
				numList[0][i] = numList[1][i]
				numList[1][i] = numList[2][i]
				numList[2][i] = numList[3][i]
				numList[3][i] = 0
			sumNum = numList[1][i]+numList[2][i]+numList[3][i]
			while numList[1][i]==0 and sumNum!=0:
				numList[1][i] = numList[2][i]
				numList[2][i] = numList[3][i]
				numList[3][i] = 0
			sumNum = numList[2][i]+numList[3][i]
			while numList[2][i]==0 and sumNum!=0:
				numList[2][i] = numList[3][i]
				numList[3][i] = 0

			if numList[0][i]==numList[1][i] and numList[0][i]!=0:
				numList[0][i] = numList[0][i]+numList[1][i]
				numList[1][i] = numList[2][i]
				numList[2][i] = numList[3][i]
				numList[3][i] = 0
				if doScore:
					self.currentScore += numList[0][i]

			if numList[1][i]==numList[2][i] and numList[1][i]!=0:
				numList[1][i] = numList[2][i]+numList[1][i]
				numList[2][i] = numList[3][i]
				numList[3][i] = 0
				if doScore:
					self.currentScore += numList[1][i]

			if numList[2][i]==numList[3][i] and numList[2][i]!=0:
				numList[2][i] = numList[2][i]+numList[3][i]
				numList[3][i] = 0
				if doScore:
					self.currentScore += numList[2][i]
		return numList

	def rightRule(self,actualList,doScore):
		numList = copy.deepcopy(actualList)
		for i in range(0,4):
			sumNum = numList[0][i]+numList[1][i]+numList[2][i]+numList[3][i]
			while numList[3][i]==0 and sumNum!=0:
				numList[3][i] = numList[2][i]
				numList[2][i] = numList[1][i]
				numList[1][i] = numList[0][i]
				numList[0][i] = 0
			sumNum = numList[0][i]+numList[1][i]+numList[2][i]
			while numList[2][i]==0 and sumNum!=0:
				numList[2][i] = numList[1][i]
				numList[1][i] = numList[0][i]
				numList[0][i] = 0
			sumNum = numList[0][i]+numList[1][i]
			while numList[1][i]==0 and sumNum!=0:
				numList[1][i] = numList[0][i]
				numList[0][i] = 0

			if numList[3][i]==numList[2][i] and numList[3][i]!=0:
				numList[3][i] = numList[3][i]+numList[2][i]
				numList[2][i] = numList[1][i]
				numList[1][i] = numList[0][i]
				numList[0][i] = 0
				if doScore:
					self.currentScore += numList[3][i]

			if numList[2][i]==numList[1][i] and numList[2][i]!=0:
				numList[2][i] = numList[1][i]+numList[2][i]
				numList[1][i] = numList[0][i]
				numList[0][i] = 0
				if doScore:
					self.currentScore += numList[2][i]

			if numList[1][i]==numList[0][i] and numList[1][i]!=0:
				numList[1][i] = numList[0][i]+numList[1][i]
				numList[0][i] = 0
				if doScore:
					self.currentScore += numList[1][i]
		return numList

	def move_up(self):
		tempList = self.upRule(self.numList,True)
		self.numList = copy.deepcopy(tempList)
		self.placeRandom()
		if self.mode=="user" or self.mode=="viewSim":
			self.drawBoard()
			self.updateScore()
			self.screen.update()
			print(self)
		self.numListOld = copy.deepcopy(self.numList)
		return

	def move_down(self):
		tempList = self.downRule(self.numList,True)
		self.numList = copy.deepcopy(tempList)
		self.placeRandom()
		if self.mode=="user" or self.mode=="viewSim":
			self.drawBoard()
			self.updateScore()
			self.screen.update()
			print(self)
		self.numListOld = copy.deepcopy(self.numList)
		return	

	def move_left(self):
		tempList = self.leftRule(self.numList,True)
		self.numList = copy.deepcopy(tempList)		
		self.placeRandom()
		if self.mode=="user" or self.mode=="viewSim":
			self.drawBoard()
			self.updateScore()
			self.screen.update()
			print(self)
		self.numListOld = copy.deepcopy(self.numList)
		return


	def move_right(self):
		tempList = self.rightRule(self.numList,True)
		self.numList = copy.deepcopy(tempList)
		self.placeRandom()
		if self.mode=="user" or self.mode=="viewSim":
			self.drawBoard()
			self.updateScore()
			self.screen.update()
			print(self)
		self.numListOld = copy.deepcopy(self.numList)
		return


	def placeRandom(self):
		numList = self.numList
		numListOld = self.numListOld
		if numList!=numListOld:
			allowed = list()
			for i in range(0,4):
				for j in range(0,4):
					if numList[i][j]==0:
						allowed.append([i,j])
			sliceVal = random.randint(0,len(allowed)-1)
			gridLoc = allowed[sliceVal]
			testNum = random.uniform(0,1)
			if testNum<0.99:
				numList[gridLoc[0]][gridLoc[1]] = 2
			else:
				numList[gridLoc[0]][gridLoc[1]] = 4


	def loop(self):
		if len(self.moveQueue)>0:
			move = self.moveQueue.pop(0)
			self.numMoves = self.numMoves+1
			if move == "left":
				self.move_left()
			elif move == "right":
				self.move_right()
			elif move == "up":
				self.move_up()
			else:
				self.move_down()

		if not(self.gameOver()):
			if self.mode!="user":
				move = self.strategy()
				self.moveQueue.append(move)
			if self.mode=="sim":
				time.sleep(self.wait/1000)
				self.loop()
			else:
				self.screen.ontimer(self.loop , self.wait)
		else:
			if self.mode!="sim":
				self.scoreObj.showturtle()
				self.scoreObj.goto(self.scoreX+10,self.scoreY)
				self.scoreObj.color("pink")
				self.scoreObj.write("Game Over",align="right",font=("Times",self.scoreTextSize,"bold"))
				self.screen.update()
				print("Game Over!")


	# def findAva(self, original,leveled_list, list_depth = 0):
	# 	# Using recursion to find the level of depth of a list.
	# 	# And once it finds the level, it will try to figure out
	# 	selection = leveled_list[0]
	# 	if isinstance(selection, list) == True:
	# 		list_depth += 1
	# 		return self.findAva(original,selection, list_depth)
	# 	else:
	# 		print('Depth of list is: ', self.list_depth)

	# def step_iteration(self, final_step, current_step = 0):
	# 	pass
	# 	depth = final_step


	def strategy(self, games_per_move = 100):
		"""
		Monte Carlo algorithm is used here.
		Starting at any move, clone a second game board, simulate it till its end.
		Repeat this loop for pre-defined games-per-move amount of times, with the initial move recorded.
		(Drop 2,4 as well).
		Record the end score for each game, and the initial move with the highest average will be used as second move.
		O(f(100n))

		:param:
		games_per_move: How many games to simulate for each move.

		:return:
		move: Decided upon tested games.
		"""

		current_board = self.numList
		sim_board = current_board
		moves = ['up', 'down', 'left', 'right']
		methods = {'up': self.upRule, 'down': self.downRule, 'left': self.leftRule,'right': self.rightRule}
		average = {'up': 0, 'down': 0, 'left': 0, 'right': 0}

		def end(board = sim_board):
			for i in range(4):
				for j in range(4):
					if board[i][j] == 0:
						return False
			else:
				return True

		def drop(board):
			allowed = []
			for i in range(0, 4):
				for j in range(0, 4):
					if board[i][j] == 0:
						allowed.append([i, j])
			choice = random.choice(allowed)
			time.sleep(1/4)
			testNum = random.uniform(0, 1)
			if testNum < 0.99:
				board[choice[0]][choice[1]] = 2
				return choice
			else:
				board[choice[0]][choice[1]] = 4
				return choice

		def random_move(board):
			"""Checks end first, and then drop, and then generate one move and return next regression."""
			if not end(board):
				dir = random.choice(moves)
				result_board = methods[dir](board, doScore = True)
				print('After a move in', dir, 'direction, resultant board is', result_board)
				drop_pos = drop(result_board)
				print('After dropping at', drop_pos, 'direction, resultant board is', result_board)
				return random_move(result_board)

		def weird_recursion_looper(default_score):
			for games in range(games_per_move):
				first_move = random.choice(moves)
				result = methods[first_move](actualList = sim_board, doScore = True)
				drop(result)
				print(result)
				time.sleep(2)
				random_move(result)
				getattr(self,)
				print(games, 'th games out of ', games_per_move,'with a score of', )
				print('First move was', dir)
				average[first_move] += score/games_per_move
				score = default_score


			pairs = None
			for key in iter(average.keys()):
				duo = (key, average[key])
				pairs.append(duo)

			result = sorted(pairs, key = lambda x: x[2], reverse= True)

			return  result[0][0]

		weird_recursion_looper(self.currentScore)





	def gameOver(self):
		notFull = False
		for i in range(0,4):
			for j in range(0,4):
				if self.numList[i][j]==0:
					notFull = True
					break
		if notFull:
			return False
		else:
			testList = self.upRule(self.numList,False)
			if testList!=self.numList:
				return False
			
			testList = self.downRule(self.numList,False)
			if testList!=self.numList:
				return False

			testList = self.rightRule(self.numList,False)
			if testList!=self.numList:
				return False

			testList = self.leftRule(self.numList,False)
			if testList!=self.numList:
				return False


			return True










