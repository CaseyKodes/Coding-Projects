# map generataion

import random as r
import turtle as t
import time
import sys

def createGrid(colorNum): 
    # creates a grid of numbers random from 0-number the user picks
    # using those random numbers it averages them out to get a more smoot gradient

    numcolors = [7,42] # number of colors in the few, many colors array respectivly 

    grid = []
    averagedGrid = []
    for row in range(size):
        grid.append([0]*(size))
        averagedGrid.append([0]*(size))
    for i in range(size):
        for j in range(size):
            if i==0 or j==0 or i==size-1 or j==size-1:
                grid[i][j] = 0
            else:
                grid[i][j] = r.randint(0,numcolors[colorNum])

    # they are now to random
    # want to make each point the average of the points around it
    attemptedspots = [[0,0],[0,1],[0,-1],
                      [1,0],[1,1],[1,-1],
                      [-1,0],[-1,1],[-1,-1]]
    ranges = [x for x in range(len(grid))]
    for i in range(size):
        for j in range(size):
            sum = 0
            todivide = 9
            for spot in attemptedspots:
                # only average points that exist 
                # points with index <0 or >len(grid) 
                # should not be considered in averaging
                if i+spot[0] in ranges and j+spot[1] in ranges:
                    sum+=grid[i+spot[0]][j+spot[1]]
                else:
                    todivide -= 1
            average = int(sum/todivide)
            averagedGrid[i][j] = average
    
    #print(grid)
    #print()
    #print(averagedGrid)
    return grid, averagedGrid

def colorGrid(colorNum, generated, calculated): # prints the grid in a turtle window according to the color list

    # keep white at the end of both arrays as a place holder since technically the indexed only go to number of colors-1

    # 42 colors total 
    morecolors = ['#000070', '#0000af', '#0000d5', '#0020ff', '#0050ff', '#0075ff',
                  '#0088ff', '#0098ff', '#00baff', '#00d5ff', '#00ffff', '#00ffd5', 
                  '#00ffb0', '#00ff80', '#00ff40', '#00ff18', '#00ff00', '#a0ff00',
                  '#bfff00', '#dfff00', '#fff000', '#ffe300', '#ffd000', '#ffc700',
                  '#ffbf00', '#ffb000', '#ffa000', '#ff8000', '#ff7000', '#ff6500',
                  '#ff5000', '#ff2800', '#ff0000', '#ff0010', '#ff0030', '#ff0050', 
                  '#ff0067', '#ff0080', '#ff00b0', "#ff00c0", '#ff00d0', '#ff00f0',
                  '#ffffff']
    
    # 7 colors total 
    fewcolors = ['#000070','#0088ff','#00ffb0','#bfff00','#ffbf00','#ff3300','#ff00c8',
                 '#ffffff']

    colorchoice = [fewcolors, morecolors]
    
    # for every color possible we will stamp in a turtle window the coorosponding color
    # i want to see at least a little gradient
    t.shape('square')
    t.hideturtle()
    t.speed(9001)
    screen = t.Screen()
    screenSize = (25*20)
    screen.setup(width=screenSize, height=screenSize)
    screen.bgcolor('black')
    
    t.shapesize(ratio,ratio,1)
    stampSize = 20*ratio
    start = y = -(screenSize/2)+stampSize

    hold = [generated, calculated]
    hold = [calculated]

    for grid in hold:
        t.setx(start)
        t.sety(start)

        for row in range(len(grid)-1,-1,-1):
            for column in range(len(grid)):
                t.color(colorchoice[colorNum][grid[row][column]])
                t.pendown()
                t.stamp()
                t.penup()
                t.fd(stampSize)
            t.setx(start)
            y = y+stampSize
            t.sety(y)
        y = start
    
    screen.exitonclick()

def show():
    while True:
        try:
            seedfind = (input('Do you want to find a seed? (Y or N) '))
            if seedfind[0].lower() == 'y':
                seedfind = 1
            elif seedfind[0].lower() == 'n':
                seedfind = 0
            else:
                raise KeyError('Must be Y or N')
        except Exception as e:
            print(f'An error occured {e}, try again. ')
            continue
        break
    global size, ratio
    while True:
        try:
            colorNum = int(input('Do you want to use a few colors (0 -> 7 total), \nor a lot of colors (# > 0 -> 42 total)? '))
            size = int(input('What should the length of your square map be? '))
        except Exception as e:
            print(f'An error occured {e}, try again. ')
            continue
        if colorNum>1: colorNum = 1
        if seedfind:
            ranges = [7,42]
            while True:
                searchfor = int(input(f'Enter a number to find between 0 and {ranges[colorNum]}. '))
                if searchfor>ranges[colorNum]:
                    print('Number is not in the range that will appear try again.')
                    continue
                break
        break
    ratio = 20/size
    
    if seedfind:
        counter = 0
        start = time.time()
        elapsed = 10
        while True:
            seed = r.randint(-sys.maxsize-1, sys.maxsize)
            counter += 1
            seed = seed
            r.seed(seed)
            random, averaged = createGrid(colorNum)
            for row in averaged:
                for num in row:
                    if num == searchfor:
                        print(f'Seed was {seed}. {counter} number of seeds checked.')
                        colorGrid(colorNum, random, averaged)
                        quit()
            end = time.time()
            if end-start > elapsed:
                print(f'{elapsed} seconds passed, and {counter} seeds checked.')
                elapsed += 10
                
    else:
        seed = r.randint(-sys.maxsize-1, sys.maxsize)
        seed = seed
        print(f'Seed was {seed}.')
        r.seed(seed)
        random, averaged = createGrid(colorNum)
        colorGrid(colorNum, random, averaged)

show()