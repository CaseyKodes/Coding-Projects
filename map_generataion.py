# map generataion

import random as r
import turtle as t
import sys

seed = r.randint(-sys.maxsize-1, sys.maxsize)
seed = seed
print(f'Seed was {seed}.')
r.seed(seed)
size = r.randint(15,25)
scale = r.randint(0,1)
#size = 15

def createGrid(): # ceates a gird of a size in 15-25 and populates it with random numbers 0-9
    grid = []
    averagedGrid = []
    for row in range(size+1):
        grid.append([0]*(size+1))
        averagedGrid.append([0]*(size+1))
    for i in range(size+1):
        for j in range(size+1):
            if i==0 or j==0 or i==size or j==size:
                grid[i][j] = 0
            else:
                picked = [r.randint(0,9), r.randint(1,22)]
                grid[i][j] = picked[scale]

    # they are now to random
    # want to make each point the average of the points around it
    
    for i in range(1,size):
        for j in range(1,size):
            sum = grid[i][j]+grid[i+1][j]+grid[i-1][j]+grid[i][j+1]+grid[i][j-1]+\
                grid[i+1][j+1]+grid[i-1][j-1]+grid[i-1][j+1]+grid[i+1][j-1]
            average = int(sum/9)
            averagedGrid[i][j] = average
            
    print(grid)
    print()
    print(averagedGrid)
    return grid, averagedGrid

def colorGrid(generated, calculated): # prints the grid in a turtle window according to the color list
    # red   = "#ff0000"
    # green = "#00ff00"
    # blue  = "#0000ff"
    # red plus green = yellow
    # red plus blue = pruple
    # green plus blue = light blue

    morecolors = ['#000080', '#0000d5', '#0050ff', '#0088ff', '#00baff', 
                  '#00ffff', '#00ffc0', '#00ff80', '#00ff30', '#00ff00', 
                  '#b8ff00', '#f0f000', '#ffd000', '#ffbf00', '#ffa000',
                  '#ff8000', '#ff5000', '#ff0000', '#ff0050', '#ff0080', 
                  '#ff00a0', '#ff00d5', '#ff00ff']

    colors = ["#0A0068", "#0F4788", "#198CB9",
              "#08A765", "#2CDA43", "#BBC529", 
              "#CF8E15", "#DA570C", "#DA0C0C", 
              "#FFFFFF"]
    
    colorChoice = [colors, morecolors]

    # for every color possible we will stamp in a turtle window the coorosponding color
    # i want to see at least a little gradient
    t.shape('square')
    t.hideturtle()
    t.speed(9001)
    screen = t.Screen()
    screenSize = (25*size)
    screen.setup(width=screenSize, height=screenSize)
    screen.bgcolor('black')

    stampSize = 20
    start = y = -(screenSize/2)+20

    hold = [generated, calculated]
    #hold = [calculated]

    for grid in hold:
        t.setx(start)
        t.sety(start)

        for row in range(len(grid)-1,-1,-1):
            for column in range(len(grid)):
                t.color(colorChoice[scale][grid[row][column]])
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
    random, averaged = createGrid()
    colorGrid(random, averaged)

show()