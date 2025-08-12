# mine sweeper

# going to use a default of 16% of the board is bombs
# players can choose any board size
# where the bombs are are randomly generated
# board prints as a table 

import random as r
import os

global PERCENT
PERCENT = .16 # the percent of the board we want to be bombs

def createBoard(size:int):
    # first create a 2D grid of sizeXsize
    grid = []
    for row in range(size):
        grid.append([0]*(size))

    numberOfBombs = int(PERCENT * (size*size))
    bomb = 'B'
    actualBombs = 0

    # going through the grid until we have at least 16% bombs
    while actualBombs < numberOfBombs:
        for i in range(len(grid)):
            for j in range(len(grid)):
                chance = r.randint(1,100)
                if chance <= PERCENT*100:
                    grid[i][j] = bomb # using negative one to indicate that the space is a bomb
                    actualBombs += 1
    
    # now we need to go through the grid and replace the non-bombs with the number of bombs that are around that spot

    attemptedspots = [[0,1],[0,-1],
                      [1,0],[1,1],[1,-1],
                      [-1,0],[-1,1],[-1,-1]]
    ranges = [x for x in range(len(grid))]

    for i in range(len(grid)):
        for j in range(len(grid)):
            bombCount = 0
            if grid[i][j] == 0: # if the spot is not a bomb we should look at all the spots around it and see how many bombs are around it 
                for spot in attemptedspots:
                    if i+spot[0] in ranges and j+spot[1] in ranges:
                        if grid[i+spot[0]][j+spot[1]] == bomb:
                            bombCount += 1
                grid[i][j] = bombCount
    
    # return the grid we made
    return grid

def show0s(board:list, y:int, x:int):
    return 1, [[x,y]] # temporary
    # this function needs to return how many spots we are able to revealed
    # based on the fact the user just selecte a spot with 0 bombs around it 

    # this should be a recursive function 
    # we check every square around the initial one in each of the 4 cardinal directions 
        # this could then lead to infinite recursion if we have a 2x2 grid of zeros 
    # if any of those are '0's we run this function on that spot also 
    # base case is when none of the spots around a 0 are 0
        # could get complicated since if we have two zeros next to each other it would just go back and forth forever 

    pass

def play(grid:list):
    # we should keep playing until there are either
        # 1 no more non-bomb squares to uncover
        # 2 the player hit a bomb square 

    nonbombs = len(grid)*len(grid) - int(PERCENT * (len(grid)*len(grid)))
    revealed = 0
    toshow = []
    for row in range(len(grid)):
        toshow.append(["#"]*(len(grid)))

    while True:
        # print what the user has found
        axis = [str(i) for i in range(1,len(grid)+1)]
        yrow = 0
        for row in toshow:
            print(f'{axis[len(grid)-yrow-1]}\t{row}')
            yrow += 1
        print(f'Y/X\t{axis}')

        # check to see if we have revealed all the squares
        if revealed == nonbombs:
            print('You revealed all non-bombs you win.')
            break

        # get what square the player wants to guess
        try:
            checkX = int(input('What is the X coord of the location you would like to guess? '))
            checkY = int(input('What is the Y coord of the location you would like to guess? '))
            if checkX > len(grid) or checkY > len(grid) or checkX < 1 or checkY < 1:
                raise KeyError(f'Coords must be between 1 and {len(grid)}.') 
        except Exception as e:
            print(f'An error occured {e}, try again.')
            continue

        # adjusting the spots we check to actully be the values we want to look at 
        checkX -= 1
        checkY = len(grid) - checkY

        # check if that square is a bomb
            # if it is a bomb ende game player lost
        if grid[checkY][checkX] == 'B':
            print('Location was a bomb game over.')
            print('Full board was:')
            yrow = 0
            for row in grid: # printing what the board looked like 
                for val in range(len(row)):
                    row[val] = str(row[val])
                print(f'{axis[len(grid)-yrow-1]}\t{row}')
                yrow += 1
            print(f'Y/X\t{axis}')
            break
        else: # it not reveal the square
            # if the spot we hit is a '0' we wna to clear all the '0's around it 
            # make a new funciton for that
            if not grid[checkY][checkX]: 
                found, spotsToReveal = show0s(grid, checkY, checkX)
                revealed += found
                for spot in spotsToReveal:
                    toshow[spot[1]][spot[0]] = str(grid[spot[1]][spot[0]])
            else:
                revealed += 1
                toshow[checkY][checkX] = str(grid[checkY][checkX]) 
            os.system('cls')

def main():
    while True:
        try:
            size = int(input('What is the size of the minesweeper board? '))
        except Exception as e:
            print(f'An error occured {e}, try again.')
            continue
        break
    board = createBoard(size)
    play(board)

main()