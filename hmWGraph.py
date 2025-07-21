# hang man with graphics
import turtle
import random
import tkinter as tk

def drawings():
    level = pickdif()
    #draw the hanging part
    screen = turtle.Screen()
    w = h = 500
    screen.setup(width = w, height=h)
    turtle.color('black')
    turtle.penup()
    turtle.setpos(0,0-h/3)
    turtle.pendown()
    turtle.fd(.2*w)
    turtle.back(.1*w)
    turtle.lt(90)
    turtle.fd(.6*h)
    turtle.lt(90)
    turtle.fd(.2*w)
    turtle.lt(90)
    turtle.fd(.15*w)
    vec = turtle.pos()
    turtle.hideturtle()
    canvas = screen.getcanvas()

    wordguessed = False
    chosenword = ''

    pickline = random.randint(0,level)
    
    # user needs to put the right path to the file here

    with open (fr"\\words{level}.txt", 'r') as file:
        contents = file.readlines()
        chosenword = contents[pickline].split('\n')[0]
    found = '-'*len(chosenword)
    letters=[]
    changed = False
    mistakeleft = 6
    num = 0
    toadd = tk.StringVar()
    word = tk.StringVar()
    checkChanged = tk.BooleanVar()
    while not wordguessed:
        # want to move away from prints and just have it all on a window 
        # make the things to put in the window 
        label = tk.Label(master=canvas, text=f'{found} \n {letters}', font=('Comic Sans', 13))
        guessbox = tk.Text(master=canvas, height=1, width=15)
        guessbutt = tk.Button(master=canvas, text='Make a guess', font=('Comic Sans', 13), 
                                command=lambda: (toadd.set(guessbox.get('1.0', 'end-1c')), checkChanged.set(not checkChanged)))
        # put them on the window
        label.grid(row=2, column=1)
        guessbox.grid(row=3, column=1)
        guessbutt.grid(row=4, column=1)

        guessbutt.wait_variable(checkChanged)
        check = toadd.get()
        # validation checking
        if check in letters or not check.isalpha():
            error = tk.Toplevel()
            error.geometry('300x120')
            label = tk.Label(master=error, text="Guesses need to be new and letters only", font=('Comic Sans', 13))
            label.pack()
            moveon = tk.BooleanVar()
            exit = tk.Button(master=error, text='Next', command=lambda: moveon.set(True), font=('Comic Sans', 13))
            exit.pack()
            label.wait_variable(moveon)
            error.destroy()
            continue
        if len(check)>1:
            if check==chosenword:
                drawcase(99, w, h, vec)
                label = tk.Label(master = canvas, text = "You WON YIPPIE YIPPIE YIPPIE!!!", font=('Comic Sans', 13))
                label.grid(row=1, column=2)
                break
            else:
                mistakeleft-=1
                num+=1
                drawcase(num, w, h, vec)
                continue
            
        # these can stay they work with the additional funcitons
        letters.append(check)
        found = ''
        if letters[-1] not in chosenword:
            mistakeleft-=1
            num+=1
            drawcase(num, w, h, vec)
            # if they mess up we also want to draw the person 
        letters.sort()
        for ch in chosenword:
            for letter in letters:
                if letter==ch:
                    found+=letter
                    changed = True
            if not changed:
                found +='-'
            changed = False

        if found == chosenword:
            # window for winning 
            drawcase(99, w, h, vec)
            label = tk.Label(master = canvas, text = "You WON YIPPIE YIPPIE YIPPIE!!!", font=('Comic Sans', 13))
            label.grid(row=1, column=2)
            break
            
        if mistakeleft==0 and '-' in found:
            # window for loosing
            drawcase(98, w, h, vec)
            label = tk.Label(master = canvas, text = f'Word was: {chosenword} \nYou lost you loser!', font=('Comic Sans', 13))
            label.grid(row=1, column=2)
            break

    turtle.Screen().exitonclick()

def pickdif():
    choice = tk.Tk()
    choice.geometry('200x100')
    choice.title('Choose Difficulty')
    label = tk.Label(master=choice, text='Pick a difficulty')
    label.pack()
    level = tk.IntVar()
    Easy = tk.Button(master=choice, text='Easy', command=lambda:level.set(1000))
    Hard = tk.Button(master=choice, text='Hard', command=lambda:level.set(10000))
    Easy.pack()
    Hard.pack()
    label.wait_variable(level)
    choice.destroy()
    
    return level.get()

def drawcase(num, w, h, vec):
    turtle.color('red')
    match num:
        case 1:
            # draw head 
            turtle.shape('circle')
            turtle.stamp()
            pass
        case 2:
            # draw body
            turtle.shape('classic')
            turtle.fd(.169*h)
            turtle.bk(.1*h)
            pass
        case 3:
            # draw right arm
            turtle.rt(30)
            turtle.fd(.075*h)
            turtle.bk(.075*h)
            turtle.lt(30)
            pass
        case 4:
            # draw left arm
            turtle.lt(30)
            turtle.fd(.075*h)
            turtle.bk(.075*h)
            turtle.rt(30)
            turtle.fd(.1*h)
            pass
        case 5:
            # draw right leg
            turtle.rt(30)
            turtle.fd(.075*h)
            turtle.bk(.075*h)
            turtle.lt(30)
            pass
        case 6:
            # draw left leg
            turtle.lt(30)
            turtle.fd(.075*h)
            turtle.bk(.075*h)
            turtle.rt(30)
            pass
        case 98:
            turtle.color('black')
            turtle.penup()
            turtle.setpos(vec[0]-7, vec[1]+7)
            turtle.pendown()
            turtle.lt(45)
            turtle.fd(10)
            turtle.bk(5)
            turtle.lt(90)
            turtle.fd(5)
            turtle.bk(10)
            turtle.penup()

            turtle.setpos(vec[0]+2, vec[1])
            turtle.pendown()
            turtle.fd(10)
            turtle.bk(5)
            turtle.lt(90)
            turtle.fd(5)
            turtle.bk(10)

            pass
        case 99:
            # they won we should do something funny 
            turtle.Screen().clear()
            turtle.color('brown')
            turtle.rt(90)
            # draw happy guy 
            turtle.shape('circle')
            turtle.stamp()
            # draw head 
            # draw body
            turtle.shape('classic')
            turtle.fd(.169*h)
            turtle.bk(.1*h)
            # draw right arm
            turtle.rt(120)
            turtle.fd(.075*h)
            turtle.bk(.075*h)
            turtle.lt(120)
            # draw left arm
            turtle.lt(120)
            turtle.fd(.075*h)
            turtle.bk(.075*h)
            turtle.rt(120)
            turtle.fd(.1*h)
            # draw right leg
            turtle.rt(30)
            turtle.fd(.1*h)
            turtle.bk(.1*h)
            turtle.lt(30)
            # draw left leg
            turtle.lt(30)
            turtle.fd(.1*h)
            turtle.bk(.1*h)
            turtle.rt(30)
            turtle.hideturtle()
            
drawings()