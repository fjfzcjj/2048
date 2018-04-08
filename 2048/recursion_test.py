from random import sample



exp_list = [[[sample(range(0,100),3) for x in range(4)] for y in range(4)] for j in range(4)]
print(len(exp_list))
print(exp_list)

def findAva( leveled_list, list_depth = 0):
	# Using recursion to find the level of depth of a list.

	selection = leveled_list[0]
	if isinstance(selection, list) == True:
		list_depth += 1
		return findAva(selection, list_depth)
	else:
		print('Depth of list is: ', list_depth)

findAva(exp_list)

