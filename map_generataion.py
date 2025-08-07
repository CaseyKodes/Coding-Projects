# map generataion

import random as r
import turtle as t

size = r.randint(15,25)

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
                grid[i][j] = r.randint(0,9)

    # they are now to random
    # want to make each point the average of the points around it
    
    for i in range(size-1):
        for j in range(size-1):
            sum = grid[i][j]+grid[i+1][j]+grid[i-1][j]+grid[i][j+1]+grid[i][j-1]+\
                grid[i+1][j+1]+grid[i-1][j-1]+grid[i-1][j+1]+grid[i+1][j-1]
            average = int(sum/9)
            averagedGrid[i+1][j+1] = average
            
    #print(grid)
    #print()
    #print(averagedGrid)
    return grid, averagedGrid

def colorGrid(generated, calculated):
    colors = ["#0A0068", "#0F4788", "#198CB9",
              "#08A765", "#2CDA43", "#BBC529", 
              "#CF8E15", "#DA570C", "#DA0C0C", 
              "#FFFFFF"]
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
    hold = [calculated]

    for grid in hold:
        t.setx(start)
        t.sety(start)

        for row in range(len(grid)):
            for column in range(len(grid)):
                t.color(colors[grid[row][column]])
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