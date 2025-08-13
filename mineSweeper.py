# mine sweeper

# going to use a default of 16% of the board is bombs
# players can choose any board size
# where the bombs are are randomly generated
# board prints as a table 

import random as r
import os
import sys

global PERCENT
PERCENT = .13 # the percent of the board we want to be bombs at the least

def createBoard(size:int):
    # first create a 2D grid of sizeXsize
    grid = []
    for row in range(size):
        grid.append([0]*(size))

    numberOfBombs = int(PERCENT * (size*size))
    bomb = 'B'
    actualBombs = 0

    # going through the grid until we have at least PERCENT% bombs
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
    return grid, actualBombs

def show0s(board:list, shown:list, y:int, x:int):
    # if the user selects a 0 we should automatically claer all the spcaes around it to save the suer time
    # this also clears squars around neighboring zeros 

    # list of a 3x3 box around the space we pick
    attemptedspots = [[0,1],[0,-1],[0,0],
                      [1,0],[1,1],[1,-1],
                      [-1,0],[-1,1],[-1,-1]]
    # making sure we do not try to access arryas that are negative or outside of the list
    ranges = [x for x in range(len(board))]

    # array of zeros we found, starts as just one but it can grow
    zeros = [[x,y]]
    for zero in zeros: # loop through all the zeros we know of
        for spot in attemptedspots: # for each spot around it
            # if the spot is actually on the grid, and has not been cleared yet clear it
            if (zero[0]+spot[0] in ranges and zero[1]+spot[1] in ranges 
                and shown[zero[1]+spot[1]][zero[0]+spot[0]] == '#'):
                # if the spot is a 0 add it to the zero array so we do this same loop on the new spot
                if not board[zero[1]+spot[1]][zero[0]+spot[0]]: 
                    zeros.append([zero[0]+spot[0],zero[1]+spot[1]])
                # show the value on the grid the user sees 
                shown[zero[1]+spot[1]][zero[0]+spot[0]] = str(board[zero[1]+spot[1]][zero[0]+spot[0]])
    return shown

def play(grid:list, bombs:int):
    
    # we should keep playing until there are either
        # 1 no more non-bomb squares to uncover - Win
        # 2 the player hit a bomb square - Lose

    toshow = []
    for row in range(len(grid)):
        toshow.append(["#"]*(len(grid)))

    while True:
        # if the number of # on the board = number of bombs the player is done
        hashes = 0
        for row in toshow:
            for char in row:
                if char == "#":
                    hashes+=1 

        # print how many bombs are on the board and what the user has found so far
        print(f'There are {bombs} bombs.')
        axis = [str(i) for i in range(1,len(grid)+1)]
        yrow = 0
        for row in toshow:
            print(f'{axis[len(grid)-yrow-1]}\t{row}')
            yrow += 1
        print(f'Y\n    X -\t{axis}')

        # check to see if we have revealed all the squares if so they win 
        if hashes == bombs:
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
        # since the indexes that show up on the users end are technically not what the actual indexes are
        checkX -= 1
        checkY = len(grid) - checkY

        # if the square the user picked is a bomb the game is over adn we can reveal the whole board
        if grid[checkY][checkX] == 'B':
            print('Location was a bomb game over.')
            print('Full board was:')
            yrow = 0
            for row in grid: # printing what the board looked like 
                for val in range(len(row)):
                    row[val] = str(row[val])
                print(f'{axis[len(grid)-yrow-1]}\t{row}')
                yrow += 1
            print(f'Y\n    X -\t{axis}')
            break
        elif toshow[checkY][checkX] == '#': 
            # if the spot is not a bomb and the player has not checked it yet reveal the square 
            if not grid[checkY][checkX]: 
                # if teh square is a 0 run the clear 0s function
                toshow = show0s(grid, toshow, checkY, checkX)
            else:
                toshow[checkY][checkX] = str(grid[checkY][checkX]) 
            #os.system('cls') # do we want to clear the screen? it is kinda cool without clearing it
        else:
            # if the player has looked at this spot before tell them
            print('Location has already been cleared.')

def main():
    # get user input for the size of the baord
    while True:
        try:
            size = int(input('What is the size of the minesweeper board? '))
        except Exception as e:
            print(f'An error occured {e}, try again.')
            continue
        break
    
    # seed the map so we can test it again if something funny happens
    seed = r.randint(-sys.maxsize-1, sys.maxsize)
    seed = seed
    r.seed(seed)
    print(f'Seed was: {seed}.')

    # create the board and play the game
    board, bombNum = createBoard(size)
    play(board, bombNum)

main()