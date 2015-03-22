import sys
import random
import signal
import pdb

#list of xnums and onums
list_xnums = set()
list_onums = set()


#Timer handler, helper function
class TimedOutExc(Exception):
        pass

def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    raise TimedOutExc()


class board:
	winning_dic = {
		0  : (set([(0,0), (0,1), (0,2)]), set([(1,0), (1,1), (1,2)]), set([(2,0), (2,1), (2,2)]), set([(0,0),(1,0),(2,0)]), set([(0,1),(1,1),(2,1)]), set([(0,2),(1,2),(2,2)]), set([(0,0),(1,1),(2,2)]), set([(2,0),(1,1),(0,2)])),
		1  : (set([(0,3), (0,4), (0,5)]), set([(1,3), (1,4), (1,5)]), set([(2,3), (2,4), (2,5)]), set([(0,3),(1,3),(2,3)]), set([(0,4),(1,4),(2,4)]), set([(0,5),(1,5),(2,5)]), set([(0,3),(1,4),(2,5)]), set([(2,3),(1,4),(0,5)])),
		2  : (set([(0,6), (0,7), (0,8)]), set([(1,6), (1,7), (1,8)]), set([(2,6), (2,7), (2,8)]), set([(0,6),(1,6),(2,6)]), set([(0,7),(1,7),(2,7)]), set([(0,8),(1,8),(2,8)]), set([(0,6),(1,7),(2,8)]), set([(2,6),(1,7),(0,8)])),
		3  : (set([(3,0), (3,1),(3,2)]), set([(4,0), (4,1), (4,2)]), set([(5,0), (5,1), (5,2)]), set([(3,0),(4,0),(5,0)]), set([(3,1),(4,1),(5,1)]), set([(3,2),(4,2),(5,2)]), set([(3,0),(4,1),(5,2)]), set([(5,0),(4,1),(3,2)])),
		4  : (set([(3,3), (3,4), (3,5)]), set([(4,3), (4,4), (4,5)]), set([(5,3), (5,4), (5,5)]), set([(3,3),(4,3),(5,3)]), set([(3,4),(4,4),(5,4)]), set([(3,5),(4,5),(5,5)]), set([(3,3),(4,4),(5,5)]), set([(5,3),(4,4),(3,5)])),
		5  : (set([(3,6), (3,7), (3,8)]), set([(4,6), (4,7), (4,8)]), set([(5,6), (5,7), (5,8)]), set([(3,6),(4,6),(5,6)]), set([(3,7),(4,7),(5,7)]), set([(3,8),(4,8),(5,8)]), set([(3,6),(4,7),(5,8)]), set([(5,6),(4,7),(3,8)])),
		6  : (set([(6,0), (6,1), (6,2)]), set([(7,0), (7,1), (7,2)]), set([(8,0), (8,1), (8,2)]), set([(6,0),(7,0),(8,0)]), set([(6,1),(7,1),(8,1)]), set([(6,2),(7,2),(8,2)]), set([(6,0),(7,1),(8,2)]), set([(8,0),(7,1),(6,2)])),
		7  : (set([(6,3), (6,4), (6,5)]), set([(7,3), (7,4), (7,5)]), set([(8,3), (8,4), (8,5)]), set([(6,3),(7,3),(8,3)]), set([(6,4),(7,4),(8,4)]), set([(6,5),(7,5),(8,5)]), set([(6,3),(7,4),(8,5)]), set([(8,3),(7,4),(6,5)])),
		8  : (set([(6,6), (6,7), (6,8)]), set([(7,6), (7,7), (7,8)]), set([(8,6), (8,7), (8,8)]), set([(6,6),(7,6),(8,6)]), set([(6,7),(7,7),(8,7)]), set([(6,8),(7,8),(8,8)]), set([(6,6),(7,7),(8,8)]), set([(8,6),(7,7),(6,8)]))
	}		
	def __init__(self, blocks_allowed):
		self.board, temp = get_init_board_and_blockstatus()
		pointslist = corners_noncorners(blocks_allowed, False)
		if (len(pointslist) >= 1):
			self.avail = pointslist[0][0] + pointslist[0][1]
		self.xnums = set()
		self.onums = set()

	def winner(self, block):
		temp = board([])
		for way in temp.winning_dic[block]:
            		if way.issubset(self.xnums):
	            		return 'x'
			if way.issubset(self.onums):
				return 'o'
			if len(self.xnums) + len(self.onums) == 9:
				return 't'
		return False

	def play(self, n, piece=None):
		global list_xnums, list_onums
		x = n[0]
		y = n[1]
		if piece:
			self.board[y][x] = piece
			(self.xnums if piece == 'x' else self.onums).add(n)
			self.avail.remove(n)
		else:
			self.board[y][x] = "_"
			self.avail.append(n)
			(self.xnums if n in self.xnums else self.onums).remove(n)

	def evaluate(self, piece, block):
		state = self.winner(block)
		if state:
			return (1 if state == piece else 0 if state == 't' else -1)
		scores = []
		opponent = "xo".replace(piece, "")
		for n in self.avail:
			self.play(n, opponent)
			scores.append(0 - self.evaluate(opponent, block))
			self.play(n)
		safest = min(scores)
		return safest


class Manual_player:
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
		global list_xnums, list_onums
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		(list_xnums if flag == 'x' else list_onums).add((int(mvp[0]), int(mvp[1])))
		return (int(mvp[0]), int(mvp[1]))
		

class Player8:	
	def __init__(self):
		pass

	def move(self,temp_board,temp_block,old_move,flag):
		for i in xrange(len(temp_block)):
			if temp_block[i] != '-':
	     			pointslist = corners_noncorners([i], False)
	     			for j in pointslist[0][0] + pointslist[0][1]:
					 (list_xnums if temp_block[i] == 'x' else list_onums).add(j)
		global list_xnums, list_onums
		(list_onums if flag == 'x' else list_xnums).add(old_move)
#		while(1):
#			pass
		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:
			## we will have 3 representative blocks, to choose from

			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left 3 blocks are allowed
				blocks_allowed = [0, 1, 3]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right 3 blocks are allowed
				blocks_allowed = [1,2,5]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left 3 blocks are allowed
				blocks_allowed  = [3,6,7]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right 3 blocks are allowed
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				## upper-center block
				blocks_allowed = [1]
	
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				## middle-left block
				blocks_allowed = [3]
		
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				## lower-center block
				blocks_allowed = [7]

			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				## middle-right block
				blocks_allowed = [5]
			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]

                for i in reversed(blocks_allowed):
                    if temp_block[i] != '-':
                        blocks_allowed.remove(i)
		return_value = move_allowed_blocks(temp_board, blocks_allowed, flag, temp_block)
		(list_onums if flag == 'o' else list_xnums).add(return_value)
		return return_value
		#We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		#cells = get_empty_out_of(temp_board, blocks_allowed,temp_block)
class Player2:
	def __init__(self):
		pass
	def move(self,temp_board,temp_block,old_move,flag):
		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:
			## we will have 3 representative blocks, to choose from

			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left 3 blocks are allowed
				blocks_allowed = [0, 1, 3]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right 3 blocks are allowed
				blocks_allowed = [1,2,5]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left 3 blocks are allowed
				blocks_allowed  = [3,6,7]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right 3 blocks are allowed
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				## upper-center block
				blocks_allowed = [1]
	
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				## middle-left block
				blocks_allowed = [3]
		
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				## lower-center block
				blocks_allowed = [7]

			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				## middle-right block
				blocks_allowed = [5]
			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]
                
                for i in reversed(blocks_allowed):
                    if temp_block[i] != '-':
                        blocks_allowed.remove(i)

	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cells = get_empty_out_of(temp_board,blocks_allowed,temp_block)
		return cells[random.randrange(len(cells))]

#function for one step winning
def one_step_winning(temp_board, blocks_allowed, flag):
	for i in xrange(len(blocks_allowed)):
		Board = board([])
		winning_dic = Board.winning_dic
		global list_xnums, list_onums
		for way in winning_dic[blocks_allowed[i]]:
			mov1 = list(way - set(list_xnums if flag == 'o' else list_onums))
			mov = list(way - set(list_xnums if flag == 'x' else list_onums))
			#print way,
			#print mov,
			#print list(way - set(list_xnums if flag == 'o' else list_onums))
			if len(mov1) is 1 and mov1[0] not in list(list_xnums) + list(list_onums):
				#print mov1[0],
				#print ">>>>",
				#print list(list_xnums) + list(list_onums) 
				#print "Against Section"	
				#(list_xnums if flag == 'x' else list_onums).add(mov1[0])
				return mov1[0]
			elif len(mov) is 1 and mov[0] not in list(list_xnums) + list(list_onums): 
				#print mov[0],
				#print ">>>>",
				#print list(list_xnums) + list(list_onums) 
				#print "Favour Section"
				#(list_xnums if flag == 'x' else list_onums).add(mov[0])
				return mov[0]
	return None

#function for returning corners
def block_corners(blocks_allowed, pointslist, flag):
	for i in xrange(len(blocks_allowed)):	
		if len(pointslist[i][0]) is 4:
			choice = random.choice(pointslist[i][0])
			#(list_xnums if flag == 'x' else list_onums).add(choice)
			#print "Corners Section"
			return choice
	return None
	
#returns the list of corner and non cromer points
def corners_noncorners(blocks_allowed, check):
	return_list = []
	for block in blocks_allowed:
		corners = []
		noncorners = []
		if block is 0:
			corners = [(0,0), (0,2), (2,0), (2,2)]
			noncorners = [(0,1), (1,0), (1,1), (1,2), (2,1)]
		elif block is 1:
			corners = [(0,3), (0,5), (2,3), (2,5)]
			noncorners = [(0,4), (1,3), (1,4), (1,5), (2,4)]
		elif block is 2:
			corners = [(0,6), (0,8), (2,6), (2,8)]
			noncorners = [(0,7), (1,6), (1,7), (1,8), (2,7)]
		elif block is 3:
			corners = [(3,0), (3,2), (5,0), (5,2)]
			noncorners = [(3,1), (4,0), (4,1), (4,2), (5,1)]
		elif block is 4:
			corners = [(3,3), (3,5), (5,3), (5,5)]
			noncorners = [(3,4), (4,3), (4,4), (4,5), (5,4)]
		elif block is 5:
			corners = [(3,6), (3,8), (5,6), (5,8)]
			noncorners = [(3,7), (4,6), (4,7), (4,8), (5,7)]
		elif block is 6:
			corners = [(6,0), (6,2), (8,0), (8,2)]
			noncorners = [(6,1), (7,0), (7,1), (7,2), (8,1)]
		elif block is 7:
			corners = [(6,3), (6,5), (8,3), (8,5)]
			noncorners = [(6,4), (7,3), (7,4), (7,5), (8,4)]
		elif block is 8:
			corners = [(6,6), (6,8), (8,6), (8,8)]
			noncorners = [(6,7), (7,6), (7,7), (7,8), (8,7)]
		else:
			print "SOMETHING REALLY WEIRD HAPPENED"
			sys.exit(1)
		if check:
			corners = filter(lambda x: x not in list(list_xnums) + list(list_onums), corners)
			noncorners = filter(lambda x: x not in list(list_xnums) + list(list_onums), noncorners)
		pointslist = []
		pointslist.append(corners)
		pointslist.append(noncorners)
		return_list.append(pointslist)
		#print ">>>>",
		#print pointslist
	return return_list


def move_not_in_allowed_blocks(temp_board, block_stat, flag):
	allowed_blocks = []
	for i in xrange(len(block_stat)):
		if block_stat[i] == '-':
			allowed_blocks.append(i)
	#print "Allowed Blocks:",
	#print allowed_blocks
	if len(allowed_blocks) >= 1:
		return_value = move_allowed_blocks(temp_board, allowed_blocks, flag, block_stat)
		return return_value
	return None
	

def move_allowed_blocks(temp_board, blocks_allowed, flag, block_stat):	
	global list_xnums, list_onums
	pointslist = corners_noncorners(blocks_allowed, True)
	vertex = one_step_winning(temp_board, blocks_allowed, flag)
	#print "^^^^",
	#print vertex
	if vertex:
		return vertex
	#print "*****",
	#print vertex
	vertex = block_corners(blocks_allowed, pointslist, flag)
	if vertex:
		return vertex
	for i in xrange(len(blocks_allowed)):
		scores = []
		avail = pointslist[i][0] + pointslist[i][1]
		for n in avail:
			node = board([blocks_allowed[i]])
			node.play(n, flag) #piece is x or o
			scores.append(node.evaluate(flag, blocks_allowed[i])) #piece is x or o
		best = max(enumerate(scores), key = lambda x:x[1])
		#print "best",
		#print best
		for k in xrange(len(best)):
			j = avail[best[k]]
			#print "Veretex",
			#print j
			if temp_board[j[0]][j[1]] == '-':
				#(list_xnums if flag == 'x' else list_onums).add(j)
				#print "Min_Max Section"
				return j
	return_value = move_not_in_allowed_blocks(temp_board, block_stat, flag)
	return return_value


#Initializes the game
def get_init_board_and_blockstatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)
	
	block_stat = ['-']*9
	return board, block_stat

# Checks if player has messed with the board. Don't mess with the board that is passed to your move function. 
def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	

# Checks if player has messed with the block. Don't mess with the block array that is passed to your move function. 
def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat	

#Gets empty cells from the list of possible blocks. Hence gets valid moves. 
def get_empty_out_of(gameb, blal,block_stat):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		for i in range(9):
			for j in range(9):
                                no = (i/3)*3
                                no += (j/3)
				if gameb[i][j] == '-' and block_stat[no] == '-':
					cells.append((i,j))	
	return cells
		
# Note that even if someone has won a block, it is not abandoned. But then, there's no point winning it again!
# Returns True if move is valid
def check_valid_move(game_board,block_stat, current_move, old_move):

	# first we need to check whether current_move is tuple of not
	# old_move is guaranteed to be correct
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	#Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True


	for_corner = [0,2,3,5,6,8]

	#List of permitted blocks, based on old move.
	blocks_allowed  = []

	if old_move[0] in for_corner and old_move[1] in for_corner:
		## we will have 3 representative blocks, to choose from

		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			## top left 3 blocks are allowed
			blocks_allowed = [0,1,3]
		elif old_move[0] % 3 == 0 and old_move[1] in [2,5,8]:
			## top right 3 blocks are allowed
			blocks_allowed = [1,2,5]
		elif old_move[0] in [2,5,8] and old_move[1] % 3 == 0:
			## bottom left 3 blocks are allowed
			blocks_allowed  = [3,6,7]
		elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
			### bottom right 3 blocks are allowed
			blocks_allowed = [5,7,8]

		else:
			print "SOMETHING REALLY WEIRD HAPPENED!"
			sys.exit(1)

	else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
		if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
			## upper-center block
			blocks_allowed = [1]
	
		elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
			## middle-left block
			blocks_allowed = [3]
		
		elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
			## lower-center block
			blocks_allowed = [7]

		elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
			## middle-right block
			blocks_allowed = [5]

		elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
			blocks_allowed = [4]

        #Check if the block is won, or completed. If so you cannot move there. 

        for i in reversed(blocks_allowed):
            	if block_stat[i] != '-':
                	blocks_allowed.remove(i)
        # We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
	#print "Blocks Allowed",
	#print blocks_allowed
        cells = get_empty_out_of(game_board, blocks_allowed,block_stat)
	#print cells,
	#print current_move
	#Checks if you made a valid move. 
        if current_move in cells:
     	    return True
        else:
    	    return False

def update_lists(game_board, block_stat, move_ret, fl):
	#move_ret has the move to be made, so we modify the game_board, and then check if we need to modify block_stat
	game_board[move_ret[0]][move_ret[1]] = fl

	block_no = (move_ret[0]/3)*3 + move_ret[1]/3
	id1 = block_no/3
	id2 = block_no%3
	mg = 0
	mflg = 0
	if block_stat[block_no] == '-':
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		
                if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                                mflg = 1
                                break

                ### row-wise
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                                mflg = 1
                                break
	else:
	     	pointslist = corners_noncorners([block_no], False)
	     	for i in pointslist[0][0] + pointslist[0][1]:
				 (list_xnums if block_stat[block_no] == 'x' else list_onums).add(i)

	

	
	if mflg == 1:
		block_stat[block_no] = fl
	
        #check for draw on the block.

        id1 = block_no/3
	id2 = block_no%3
        cells = []
	for i in range(id1*3,id1*3+3):
	    for j in range(id2*3,id2*3+3):
		if game_board[i][j] == '-':
		    cells.append((i,j))

        if cells == [] and mflg!=1:
            block_stat[block_no] = 'd' #Draw
        
        return

def terminal_state_reached(game_board, block_stat):
	
        #Check if game is won!
        bs = block_stat
	## Row win
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		print block_stat
		return True, 'W'
	## Col win
	elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
		print block_stat
		return True, 'W'
	## Diag win
	elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
		print block_stat
		return True, 'W'
	else:
		smfl = 0
		for i in range(9):
			for j in range(9):
				if game_board[i][j] == '-' and block_stat[(i/3)*3+(j/3)] == '-':
					smfl = 1
					break
		if smfl == 1:
                        #Game is still on!
			return False, 'Continue'
		
		else:
                        #Changed scoring mechanism
                        # 1. If there is a tie, player with more boxes won, wins.
                        # 2. If no of boxes won is the same, player with more corner move, wins. 
                        point1 = 0
                        point2 = 0
                        for i in block_stat:
                            if i == 'x':
                                point1+=1
                            elif i=='o':
                                point2+=1
			if point1>point2:
				return True, 'P1'
			elif point2>point1:
				return True, 'P2'
			else:
                                point1 = 0
                                point2 = 0
                                for i in range(len(game_board)):
                                    for j in range(len(game_board[i])):
                                        if i%3!=1 and j%3!=1:
                                            if game_board[i][j] == 'x':
                                                point1+=1
                                            elif game_board[i][j]=='o':
                                                point2+=1
			        if point1>point2:
				    return True, 'P1'
			        elif point2>point1:
				    return True, 'P2'
                                else:
				    return True, 'D'	


def decide_winner_and_get_message(player,status, message):
	if player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NO ONE','DRAW')
	return


def print_lists(gb, bs):
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="

	print "=========== Block Status ========="
	for i in range(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2] 
	print "=================================="
	print
	

def simulate(obj1,obj2):
	
	# Game board is a 9x9 list, block_stat is a 1D list of 9 elements
	game_board, block_stat = get_init_board_and_blockstatus()
	
	pl1 = obj1 
	pl2 = obj2

	### basically, player with flag 'x' will start the game
	pl1_fl = 'x'
	pl2_fl = 'o'

	old_move = (-1, -1) # For the first move

	WINNER = ''
	MESSAGE = ''

        #Make your move in 6 seconds!
	TIMEALLOWED = 60
	print_lists(game_board, block_stat)
	global list_xnums, list_onums
	while(1):

		# Player1 will move
		
		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]
	
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		flag_set1 = 0
		# Player1 to complete in TIMEALLOWED secs. 
		try:
			#print "Printing Bock_stat",
			#print temp_block_stat
                        ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)
			#(list_xnums if pl1_fl == 'x' else list_onums).add(ret_move_pl1)
			#print "list_xnums",
			#print list_xnums
			#print "list_onums",
			#print list_onums
			#print "----->",
			#print ret_move_pl1
	
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'TIMED OUT')
			break
		signal.alarm(0)
	
                #Checking if list hasn't been modified! Note: Do not make changes in the lists passed in move function!
		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			#Player1 loses - he modified something
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
		
		# Check if the move made is valid
		if not check_valid_move(game_board, block_stat,ret_move_pl1, old_move) and flag_set1 is 0:
			## player1 loses - he made the wrong move.
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 1 made the move:", ret_move_pl1, 'with', pl1_fl

                #So if the move is valid, we update the 'game_board' and 'block_stat' lists with move of pl1
		update_lists(game_board, block_stat, ret_move_pl1, pl1_fl)	

		# Checking if the last move resulted in a terminal state
		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
		if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P1', mesg,  'COMPLETE')	
			break

		
		old_move = ret_move_pl1
		print_lists(game_board, block_stat)

                # Now player2 plays

                temp_board_state = game_board[:]
                temp_block_stat = block_stat[:]
		flag_set2 = 0

		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		try:
                	ret_move_pl2 = pl2.move(temp_board_state, temp_block_stat, old_move, pl2_fl)
			#(list_xnums if pl2_fl == 'x' else list_onums).add(ret_move_pl2)
			#print "list_xnums",
			#print list_xnums
			#print "list_onums",
			#print list_onums
			#print "----->",
			#print ret_move_pl2
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'TIMED OUT')
			break
		signal.alarm(0)

                if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
			
                if not check_valid_move(game_board, block_stat,ret_move_pl2, old_move) and flag_set2 is 0:
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 2 made the move:", ret_move_pl2, 'with', pl2_fl
                update_lists(game_board, block_stat, ret_move_pl2, pl2_fl)


		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
                if gamestatus == True:
			print_lists(game_board, block_stat)
                        WINNER, MESSAGE = decide_winner_and_get_message('P2', mesg,  'COMPLETE' )
                        break
		old_move = ret_move_pl2
		print_lists(game_board, block_stat)
	
	print WINNER + " won!"
	print MESSAGE

if __name__ == '__main__':
	## get game playing objects

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	if option == '1':
		obj1 = Player8()
		obj2 = Player2()

	elif option == '2':
		obj1 = Player8()
		obj2 = Manual_player()
	elif option == '3':
		obj1 = Manual_player()
		obj2 = Manual_player()
        
        # Deciding player1 / player2 after a coin toss
        # However, in the tournament, each player will get a chance to go 1st. 
        num = random.uniform(0,1)
        if num > 0.5:
		simulate(obj2, obj1)
	else:
		simulate(obj1, obj2)
