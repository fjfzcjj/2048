def strategy(self):
	moves = ['up', 'down', 'left', 'right']  # The sequence here matters. [0, 1, 2, 3]
	self.list_depth = 0  # Initialize the search for current empty tiles.
	self.steps = 2  # We are looking at how many steps ahead.
	for a in range(4):
		for b in range(4):
			if self.numListOld[a][b] = 0:
				self.empty.append((a, b))
	# Creating a record for current empty tiles.
	self.ava = len(self.empty)
	print('current empty tiles: ', self.ava, end='')
	self.result = 0
	# The idea here is to iterate different moves, through 'up', 'down', 'left', 'right' in sequence, to create
	# a list that is 'n' in depth, depending on how many steps we want to look ahead. The values of elements in the
	# list will be the number of empty tiles after moves.
	# eg. result[1][2][3] = 5 means that after moving 'down', 'left', 'right' consequently, there will be 5 empty
	# tiles.
	# THE MORE EMPTY TILES, THE BETTER. BECAUSE WE ARE LOOKING FOR LONGEVITY HERE IN THE GAME.
	# The time complexity will be f(x^n) depending on 'n'-th steps ahead we are looking for.
	# After each independent search, the program only takes one step afterwards, and then repeat the process again.

	self.step_iteration(self.steps)

	return move
