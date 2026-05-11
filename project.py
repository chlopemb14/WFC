import random
import colorama
from colorama import Fore, Style

colorama.init()

#Similar will remove tiles that are duplicates: not used in program normally
def similar(tiles):
    new_tiles = []
    for i in tiles:
        if i not in new_tiles:
            new_tiles.append(i)
    return new_tiles
   
#testing function unused normally
def printRow(final_board):
    #Prints out the row of a list passed in
    BLOCK = "\u2588\u2588"

    row = final_board

    for tile in row:
        if tile == ["X","X","X","X"]:
            print("    ", end="")
        else:
            print(colors[tile[0]] + BLOCK + colors[tile[1]] + BLOCK, end="")
    print(Style.RESET_ALL)

    for tile in row:
        if tile == ["X","X","X","X"]:
            print("    ", end="")
        else:
            print(colors[tile[2]] + BLOCK + colors[tile[3]] + BLOCK, end="")
    print(Style.RESET_ALL)
       
    return 0
  
#Checks every tile against its neighbors to ensure color borders match perfectly  
def isValidBoard(board, image_Size):
    
    for index, tile in enumerate(board):

        if tile == ["X","X","X","X"]:
            continue

        row = index // image_Size
        col = index % image_Size

        # RIGHT
        if col < image_Size - 1:

            right = board[index + 1]

            if right != ["X","X","X","X"]:

                if [tile[1], tile[3]] != [right[0], right[2]]:
                    return False

        # DOWN
        if row < image_Size - 1:

            down = board[index + image_Size]

            if down != ["X","X","X","X"]:

                if [tile[2], tile[3]] != [down[0], down[1]]:
                    return False

    return True
   
#getValidChoices will return a list containing all tiles that are avalible for a given index
def getValidChoices(board, tiles, index, image_Size):
    valid = tiles.copy()

    row = index // image_Size
    col = index % image_Size

    # TOP MATCH 
    if row > 0:
        nearby = board[index - image_Size]
        if nearby != ["X","X","X","X"]:
            valid = [t for t in valid if t[0] == nearby[2] and t[1] == nearby[3]]

    # BOTTOM MATCH 
    if row < image_Size - 1:
        nearby = board[index + image_Size]
        if nearby != ["X","X","X","X"]:
            valid = [t for t in valid if t[2] == nearby[0] and t[3] == nearby[1]]

    # LEFT MATCH 
    if col > 0:
        nearby = board[index - 1]
        if nearby != ["X","X","X","X"]:
            valid = [t for t in valid if t[0] == nearby[1] and t[2] == nearby[3]]

    # RIGHT MATCH 
    if col < image_Size - 1:
        nearby = board[index + 1]
        if nearby != ["X","X","X","X"]:
            valid = [t for t in valid if t[1] == nearby[0] and t[3] == nearby[2]]

    return valid
   
#getRandomTile will call the getValidChoices function and return a random tile if there are no options it
#returns a ["X","X","X","X"] tile


#findNumTiles will return the number of tiles availible for a given index
def findNumTiles(board, tiles, index, image_Size):
    return len(getValidChoices(board, tiles, index, image_Size))

#Unnecessary function that starts the program by randomly selecting a tile to place in the middle of the board
#it is here just to organize things
def firstIterate(tiles):
    return weighted_choice(tiles)
    
 #Adjusts probability of tiles so the world looks more natural (e.g., more land, less sand)
def weighted_choice(valid):
    
    weights = []
    for tile in valid:
        water_count = tile.count('b') 
        green_count = tile.count('g') 
        yellow_count = tile.count('y') 

      
        if water_count >= 3:
            weights.append(8)  
        elif green_count >= 3:
            weights.append(10) 
        elif yellow_count >= 3:
            weights.append(4)  
        else:
            # Transitional tiles
            weights.append(15) 

    return random.choices(valid, weights=weights)[0]

   
def getRandomTile(board, tiles, index, image_Size):
    valid = getValidChoices(board, tiles, index, image_Size)
    if len(valid) == 0:
        return ["X","X","X","X"]
    return weighted_choice(valid)

#Iterate function is the main function call, it created a list that will store all tiles that have the least number of possible
#options to choose from (that isnt zero). If there are multiple tiles with the lowest number of possible options the function
#will randomly select one. If the smallestTiles list has no tiles in it the function returns true which will stop program if the
#backtracking program does not find any ["X","X","X","X"] tiles
# This will check—find spaces with the fewest legal moves to solve first
def iterate(collapsed, tiles, image_Size, board):
    numberOftiles = 0
    smallestTiles = []
    minn = float('inf')
    
    for i in range(len(collapsed)):
        if not collapsed[i]:
            numberOftiles = (findNumTiles(board, tiles, i, image_Size))
            if numberOftiles < minn:
                minn = numberOftiles
                smallestTiles = [i]
            elif numberOftiles == minn:
                smallestTiles.append(i)
    if not smallestTiles:
        return True
    ran = random.choice(smallestTiles)
    board[ran] = getRandomTile(board,tiles,ran,image_Size)
    collapsed[ran] = True
    return False

#Chunk function all contain the main loop with different functionallities, regular chunk() will print out a board of any size
#bigger than 10, if greater than 30 takes an insane amount of time
#Main loop:
    #   board, collapsed, and backing are all cleared and reinitialized in loop, board is assigned with all values starting as
    #   ["X","X","X","X"] board_center finds center index and uses firsIterate function to get the first tile. Afterwords
    #   collapsed is changed to True for the position of that tile.(This tells the iterate function to ignore that position now that
    #   it already had a tile in it). The while loop runs until the iterate function returns true which is only after it fills all
    #   tiles. Inside the while loop there is a for loop with list backing. If the iterate function produces a ["X","X","X","X"]
    #   tile it will remove the imediate surrounding tiles and increasing that tiles backing count, if that count gets to 20 for any
    #   singular tile the program will stop and restart from the beggining. Finnally after filling all tiles the loop will end
    #   and will print out the board list.
def chunk(current_board, collapsed, backing, image_Size):
    restart = True
    trials = 1
    while restart:
        restart = False
        current_board.clear()
        collapsed.clear()
        backing.clear()
        for i in range(image_Size**2):
            current_board.append(["X","X","X","X"])
            collapsed.append(False)
            backing.append(0)

        board_center = image_Size**2//2

        current_board[board_center] = firstIterate(tiles)
        collapsed[board_center] = True

        is_done = False
        while not is_done:
            is_done = iterate(collapsed, tiles, image_Size, current_board)
            for idx, tile in enumerate(current_board):
                if  tile == ["X","X","X","X"] and collapsed[idx]:
                    if backing[idx] <= 20:
                        #If a contradiction occurs, "un-collapse" neighbors to try a different path
                        for nearby in [idx,idx-1,idx+1,idx-image_Size,idx+image_Size, idx-image_Size-1, idx-image_Size+1,idx+image_Size-1, idx+image_Size+1, idx+2*image_Size, idx-2*image_Size, idx-2, idx+2]:
                            if 0 <= nearby <len(current_board):
                                current_board[nearby] = ["X","X","X","X"]
                                collapsed[nearby] = False
                        backing[idx] +=1
        if (
            ["X","X","X","X"] in current_board
            or not isValidBoard(current_board, image_Size)
        ):
            restart = True
            trials += 1
    return current_board

#get corner tile will take in 2 boards and will find a tile that meets both conditions of the boards to place in the corner
#the corner its refering to is if the boards were placed diagonally it would be the inner corner space
def getCornerTile(topboard, leftboard, tiles):
    
    valid = tiles.copy()
    
    if topboard:
        # The neighbor is the tile at the bottom-left of the chunk above
        neighbor_above = topboard[len(topboard) - CHUNK] 
        valid = [t for t in valid if t[0] == neighbor_above[2] and t[1] == neighbor_above[3]]
        
    if leftboard:
        # The neighbor is the tile at the top-right of the chunk to the left
        neighbor_left = leftboard[CHUNK - 1]
        valid = [t for t in valid if t[0] == neighbor_left[1] and t[2] == neighbor_left[3]]

    return random.choice(valid) if valid else random.choice(tiles)
   
#chunk normalCorner will take in two lists as constraints to use as the left and top starter pieces then will print out next chunk
#the function treats it as a 11x11 size board in order to use those lists, but at the end we have a function to remove the
#top and left row/column to make it the desired 10x10
def chunkNormalCorner(current_board, collapsed, backing, image_Size, above_List, left_List, topboard, leftboard, tiles):
    restart = True
    trials = 1
    current_image_size = image_Size + 1
    while restart:
        restart = False
        current_board.clear()
        collapsed.clear()
        backing.clear()
        
        # Pre-fill the 11x11 board with constraints
        for i in range(current_image_size):
            for z in range(current_image_size):
                if i == 0 and z == 0:
                    # Corner piece
                    current_board.append(getCornerTile(topboard, leftboard, tiles))
                    collapsed.append(True)
                elif i == 0:
                    # Top Row Constraint
                    current_board.append(above_List[z-1]) # Use z-1 because above_List is size 10
                    collapsed.append(True)
                elif z == 0:
                    # Left Column Constraint
                    current_board.append(left_List[i-1]) # Use i-1 because left_List is size 10
                    collapsed.append(True)
                else:
                    # Empty space to fill
                    current_board.append(["X","X","X","X"])
                    collapsed.append(False)
                backing.append(0)

        is_done = False
        while not is_done:
            is_done = iterate(collapsed, tiles, current_image_size, current_board)
          
            for idx, tile in enumerate(current_board):
                if tile == ["X","X","X","X"] and collapsed[idx]:
                    if backing[idx] <= 20:
                        for nearby in [idx,idx-1,idx+1,idx-current_image_size,idx+current_image_size]:
                            if 0 <= nearby < len(current_board):
                                
                                if nearby // current_image_size != 0 and nearby % current_image_size != 0:
                                    current_board[nearby] = ["X","X","X","X"]
                                    collapsed[nearby] = False
                        backing[idx] += 1
        
        if ["X","X","X","X"] in current_board:
            restart = True
            trials += 1
        if trials > 15: return []
            
    return removeRowCollumn(current_board)

#chunkNormalAbove takes in two lists but will assign the left starter column with empty tiles to be filled as placeholders
#otherwise same function as chunk normal corner
def chunkNormalAbove(current_board, collapsed, backing, image_Size, above_List, left_List, topboard, leftboard, tiles):
    restart = True
    trials = 1
    current_image_size = image_Size + 1
    while restart:
        restart = False
        current_board.clear()
        collapsed.clear()
        backing.clear()
        for i in range(current_image_size):
            for z in range(current_image_size):
                if i == 0 and z > 0:
                    current_board.append(above_List[z-1])
                    collapsed.append(True)
                else:
                    current_board.append(["X","X","X","X"])
                    collapsed.append(False)
                backing.append(0)

        is_done = False
        while not is_done:
            is_done = iterate(collapsed, tiles, current_image_size, current_board)
            # CRITICAL: Backtracking logic added below
            for idx, tile in enumerate(current_board):
                if tile == ["X","X","X","X"] and collapsed[idx]:
                    if backing[idx] <= 20:
                        # Reset 2 tiles away to give the algorithm room to breathe
                        for nearby in [idx, idx-1, idx+1, idx-current_image_size, idx+current_image_size]:
                            if 0 <= nearby < len(current_board):
                                # Do NOT reset the fixed top border (row 0)
                                if nearby // current_image_size != 0:
                                    current_board[nearby] = ["X","X","X","X"]
                                    collapsed[nearby] = False
                        backing[idx] += 1

        if ["X","X","X","X"] in current_board:
            restart = True
            trials += 1
        if trials > 15: return [] # Safety break

    return removeRowCollumn(current_board)
    
#chunkNormalLeft takes in two lists but will assign the above starter row with empty tiles to be filled as placeholders
#otherwise same function as chunk normal corner
def chunkNormalLeft(current_board, collapsed, backing, image_Size, above_List, left_List, topboard, leftboard, tiles):
    restart = True
    trials = 1
    current_image_size = image_Size + 1
    while restart:
        restart = False
        current_board.clear()
        collapsed.clear()
        backing.clear()
        
        # Initialization logic...
        for i in range(current_image_size):
            for z in range(current_image_size):
                if z == 0 and i > 0:
                    current_board.append(left_List[i-1])
                    collapsed.append(True)
                else:
                    current_board.append(["X","X","X","X"])
                    collapsed.append(False)
                backing.append(0)

        is_done = False
        while not is_done:
            is_done = iterate(collapsed, tiles, current_image_size, current_board)
            for idx, tile in enumerate(current_board):
                if tile == ["X","X","X","X"] and collapsed[idx]:
                    # INCREASED BACKING LIMIT TO 50
                    if backing[idx] <= 50:
                        # Reset a wider area (3x3) to solve complex constraints
                        for nearby in [idx, idx-1, idx+1, idx-current_image_size, idx+current_image_size]:
                            if 0 <= nearby < len(current_board):
                                if nearby % current_image_size != 0:
                                    current_board[nearby] = ["X","X","X","X"]
                                    collapsed[nearby] = False
                        backing[idx] += 1
        
        if ["X","X","X","X"] in current_board:
            restart = True
            trials += 1
        # INCREASED TRIAL LIMIT TO 50
        if trials > 50: 
            print("Critical Failure: Could not resolve constraints.")
            return [["bl","bl","bl","bl"]] * (image_Size**2) # Return black tiles instead of empty
            
    return removeRowCollumn(current_board)


 
#getAboveRow takes in the board we want a row of and returns the bottom row (only works for a 10x10 board)
# Returns exactly the bottom 'size' tiles
def getAboveRow(board, size):
    return board[-size:]

 # Returns exactly the tiles on the right edge
def getRightColumn(board, size):
   
    return [board[i] for i in range(size-1, len(board), size)]


#Removes the top row and left column from a 11X11 board
#After using the 11x11 grid for border matching, we crop it back to 10x10
def removeRowCollumn(theBoard):
    
    lister = []
    for i in range(len(theBoard)):
        row = i // 11
        col = i % 11
       
        if row != 0 and col != 0:
            lister.append(theBoard[i])
    return lister
   
#Prints out the board with colors!!!
def printer(final_board, image_Size):
    colors = {
    'g': Fore.GREEN,
    'y': Fore.YELLOW,
    'b': Fore.BLUE,
    'c': Fore.CYAN,
    'm': Fore.MAGENTA,
    'r': Fore.RED,
    'w': Fore.WHITE,
    'bl': Fore.BLACK
}

    BLOCK = "\u2588\u2588"

    for i in range(image_Size):
        row = final_board[i*image_Size : (i+1)*image_Size]

        for tile in row:
            if tile == ["X","X","X","X"]:
                print("    ", end="")
            else:
                print(colors[tile[0]] + BLOCK + colors[tile[1]] + BLOCK, end="")
        print(Style.RESET_ALL)

        for tile in row:
            if tile == ["X","X","X","X"]:
                print("    ", end="")
            else:
                print(colors[tile[2]] + BLOCK + colors[tile[3]] + BLOCK, end="")
        print(Style.RESET_ALL)
       
    return 0

#dissolver function takes in the final_board with all smaller boards and will rip it apart and stitch it back together in a single list/board
# Merges separate 10x10 lists into one large continuous coordinate list for printing
def dissolver(final_board, image_Size, width_chunks, height_chunks):
    return_board = []
    for grid_row in range(height_chunks):
        row_boards = final_board[
            grid_row * width_chunks :
            (grid_row + 1) * width_chunks
        ]
        
        for i in range(image_Size):
            combined_row = []
            for board in row_boards:
                start = i * image_Size
                end = start + image_Size
                combined_row.extend(board[start:end])
            return_board.extend(combined_row)
    return return_board

#The most painfull function of my life: it took me 3 hours to find out that the chunk() function, which is suppose to be simplest, was wrong
#After finding that out it took me all of 5 seconds to fix the error
#spent another 2 hours after to realize the reason my boards were printing out wrong was because i needed to make copies before appending: do not
#ever want to make this function again
#Now after complaining the function will take the image size you want as long as it is a multiple of 10 and break it down into smaller chunks
#each chunk is 10x10 and are appended to final_board where the dissolver function breaks them apart and puts it back together to be passed
#to the printer function try catch is there if one of the boards goes over 10 trials(unlikely) and will restart program
def chunks(board, collapsed, backing, image_Size, tiles):
    if image_Size <= 20:
        res = chunk(board, collapsed, backing, image_Size)
        printer(res, image_Size)
        return

    final_board = []
    chunk_count = image_Size // 10

    for row in range(chunk_count):
        for col in range(chunk_count):
            
            if row == 0 and col == 0:
                new_chunk = chunk([], [], [], 10)
 
            elif row == 0:
                left_chunk = final_board[-1]
                constraints = getRightColumn(left_chunk, 10)
                new_chunk = chunkNormalLeft([], [], [], 10, ["none"], constraints, [], left_chunk, tiles)
            

            elif col == 0:
                above_chunk = final_board[(row - 1) * chunk_count]
                constraints = getAboveRow(above_chunk, 10)
                new_chunk = chunkNormalAbove([], [], [], 10, constraints, ["none"], above_chunk, [], tiles)
            

            else:
                above_chunk = final_board[(row - 1) * chunk_count + col]
                left_chunk = final_board[-1]
                new_chunk = chunkNormalCorner(
                    [], [], [], 10, 
                    getAboveRow(above_chunk, 10), 
                    getRightColumn(left_chunk, 10), 
                    above_chunk, 
                    left_chunk, 
                    tiles
                )
            
            # Safety check: if a chunk failed, append a blank one to prevent crashing
            if not new_chunk:
                new_chunk = [tiles[0]] * 100
                
            final_board.append(new_chunk.copy())

    # Stitch them all together and print
    # Note: dissolver needs the grid dimensions to work!
    stitched_map = dissolver(final_board, 10, chunk_count, chunk_count)
    printer(stitched_map, image_Size)
   
#--------------------------------------------------------------------------------------------------------------------------------------
#User Input/Main Interface


size = 4
grid = []

#User inputed values
#for i in range(size):
 #   grid.append([])
 #   for z in range(size):
 #       grid[i].append(str(input()))
 #   print()

grid = [
["g","g","g","g"],
["g","g","y","y"],
["y","y","b","b"],
["b","b","b","b"],
]

#List declarations
breakdown = []
tiles = []
collapsed = []
board = []
backing = []

#Breaks down the given image from user input into 4x4 squares and assigns them to breakdown
for i in range(0, size-1):
    for z in range(0, size-1):
        breakdown.append([grid[i][z], grid[i][z+1], grid[i+1][z], grid[i+1][z+1]])
        

#Rotates all tiles into every position and assigns all results to tiles list
length = len(breakdown)

for i in range(length):
    a, b, c, d = breakdown[i]
    # 0°
    tiles.append([a, b, c, d])
    # 90°
    tiles.append([c, a, d, b])
    # 180°
    tiles.append([d, c, b, a])
    # 270°
    tiles.append([b, d, a, c])

#Removes duplicates when uncommented
#tiles = similar(tiles)

#User enters how big they want the given image to be
import os

CHUNK = 10

world = {}
world[(0,0)] = chunk(board, collapsed, backing, CHUNK).copy()

min_x = 0
max_x = 0
min_y = 0
max_y = 0


#Creates the list of chunks based on current exploration (S/D moves)
def build_full_map():
    boards = []

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            boards.append(world[(x,y)])

    width_chunks = max_x - min_x + 1
    height_chunks = max_y - min_y + 1

    return dissolver(
        boards,
        CHUNK,
        width_chunks,
        height_chunks
    )


def add_right():
    global max_x
    new_x = max_x + 1

    for y in range(min_y, max_y + 1):
        left_chunk = world[(new_x - 1, y)]
        left_constraints = getRightColumn(left_chunk, CHUNK)

        if y > min_y:
            above_chunk = world[(new_x, y - 1)]
            above_constraints = getAboveRow(above_chunk, CHUNK)
            
            res = chunkNormalCorner(
                [], [], [],
                CHUNK,
                above_constraints,
                left_constraints,
                above_chunk,
                left_chunk,
                tiles
            )
            # Safety: If generation fails, fill with a basic tile instead of crashing
            world[(new_x, y)] = res.copy() if res else [tiles[0]] * (CHUNK**2)
        else:
            res = chunkNormalLeft(
                [], [], [],
                CHUNK,
                ["none"],
                left_constraints,
                [],
                left_chunk,
                tiles
            )
            world[(new_x, y)] = res.copy() if res else [tiles[0]] * (CHUNK**2)

    max_x += 1

def add_down():
    global max_y
    new_y = max_y + 1

    for x in range(min_x, max_x + 1):
        above_chunk = world[(x, new_y - 1)]
        above_constraints = getAboveRow(above_chunk, CHUNK)

        if x > min_x:
            # CORNER CASE: Needs both top and left
            left_chunk = world[(x - 1, new_y)]
            left_constraints = getRightColumn(left_chunk, CHUNK)

            world[(x, new_y)] = chunkNormalCorner(
                [], [], [],
                CHUNK,
                above_constraints,
                left_constraints,
                above_chunk,
                left_chunk,
                tiles
            ).copy()
        else:
            # Just top constraint
            world[(x, new_y)] = chunkNormalAbove(
                [], [], [],
                CHUNK,
                above_constraints,
                ["none"],
                above_chunk,
                [],
                tiles
            ).copy()

    max_y += 1


while True:
    os.system("cls")

    final_map = build_full_map()

    width = (max_x - min_x + 1) * CHUNK

    printer(final_map, width)
    print("S = Add Bottom Row")
    print("D = Add Right Column")
    print("Q = Quit")

    move = input("Choice: ").lower()

    if move == "q":
        break

    elif move == "d":
        add_right()

    elif move == "s":
        add_down()