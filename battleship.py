# making a two player battle ship game

'''
classes 
    players - 
        used to hold player data, where tehy puth their ships, where they have attacked
        has funcitons to know if a player has any ships left, to attack another player, and to print out the grids of a player

    difficulty -
        used to make global variables that determine how big a board is and how many ships go on a board
    
    ship -
        holds a list of tuples (x,y), its length and how many times it has been hit
        if how many times it has been hit is equal to its length we say a ship was sank
    
Multi or Single player
    a bot is able if users choose to run code as a single player
    ask what level of the AI they want currently only AI level that works is 1 which is random guess

'''

import os
import random as r

class difficulty():
    def __init__(self, dif):
        global shipLens
        global validcords
        global validcordsString 
        validcordsString = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        match dif:
            case 1:
                validcords = [0, 1, 2, 3]
                shipLens = [3, 2, 2, 1]
                pass
            case 2:
                validcords = [0, 1, 2, 3, 4, 5]
                shipLens = [5, 4, 3, 2, 1]
                pass
            case 3:
                validcords = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                shipLens = [5, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1]
                pass

class ship():
    def __init__(self, length):
        self.cords = []
        self.length = length
        self.hits = 0
        self.sunk = False
    def setCord(self, x, y):
        self.cords.append((x,y))
    def getCords(self):
        return self.cords
    def isSank(self):
        if self.hits == self.length:
            print(f'Ship of length {self.length} has been sunk!')
            self.sunk = True
            return True
        return False
    def isHit(self):
        self.hits+=1

class player():
    def __init__(self, isAI = False, level = 0):
        # init should not take params 
        # in the function is where we decide where the boats are
        self.AI = isAI
        self.AIlevel = level
        self.lastHit = [0,0]
        self.AImoveResult = [False, False] # [if hit, hit sunk]
        self.attacks = [['-' for i in range(len(validcords))] for j in range(len(validcords))] # text here bc this is what we will show a user
        self.shipVals = [['-' for i in range(len(validcords))] for j in range(len(validcords))] # we can show a player what the other players has hit and missed
        self.ships = [[0 for i in range(len(validcords))] for j in range(len(validcords))] # numbers here bc this is what we will use for logic 
        self.turn = True
        self.shipLoactions = [[]]*len(shipLens)
        self.army = []
        if not self.AI:
            print(f'Grid size is {len(validcords)}x{len(validcords)}.')
        for num in shipLens:
            if not self.AI: 
                print('Updated grid')
                self.printMap(self.shipVals)
                print(f'Current ship length {num}.')
            while True:
                try:
                    if self.AI:
                        startX = r.randint(0, validcords[-1])
                        startY = r.randint(0, validcords[-1])
                    else:
                        startX = int(input('X start coord of the current ship. '))
                        startY = int(input('Y start coord of the current ship. '))
                    direction=1
                    if num!=1:
                        if self.AI:
                            direction = r.randint(1, 4)
                        else:
                            direction = int(input('What direction from the start should the ship go?\n1 - Up, 2 - Down, 3 - Right, 4 - Left. '))
                    if startX not in validcords: 
                        raise Exception('This is not a valid starting location.')
                    if startY not in validcords: 
                        raise Exception('This is not a valid starting location.')
                    if direction not in [1, 2, 3, 4]:
                        raise Exception('This is not a valid direction.')
                    match direction: # in each case we need to see if all the indexes in direction are unoccupided and are inbetween 1-10
                        case 1:
                            if (startY - num +1) not in validcords:
                                raise Exception('Boat would go off screen.')
                            for i in range(num):
                                #need to check if each point the boat will be on is valid 
                                #if it is valid we should store the coords if not we throw an error
                                if(self.ships[startY - i][startX]):
                                    raise Exception('Boat would go onto another boat.')
                            # if we get out here we know that all pints the boat will be on are vlaid so now we should place the baot on those points 
                            self.army.append(ship(num))
                            for i in range(num):
                                self.army[-1].setCord(startX, startY-i)
                                self.ships[startY-i][startX] = 1
                                self.shipVals[startY-i][startX] = 'S' 
                            pass
                        case 2:
                            if (startY + num -1) not in validcords:
                                raise Exception('Boat would go off screen try again.')
                            for i in range(num):
                                if(self.ships[startY + i][startX]):
                                    raise Exception('Boat would go onto another boat.')
                            self.army.append(ship(num))
                            for i in range(num):
                                self.army[-1].setCord(startX, startY+i)
                                self.ships[startY+i][startX] = 1
                                self.shipVals[startY+i][startX] = 'S' 
                            pass
                        case 3:
                            if (startX + num -1) not in validcords:
                                raise Exception('Boat would go off screen try again.')
                            for i in range(num):
                                if(self.ships[startY][startX+i]):
                                    raise Exception('Boat would go onto another boat.')
                            self.army.append(ship(num))
                            for i in range(num):
                                self.army[-1].setCord(startX+i, startY)
                                self.ships[startY][startX+i] = 1
                                self.shipVals[startY][startX+i] = 'S' 
                            pass
                        case 4:
                            if (startX - num +1) not in validcords:
                                raise Exception('Boat would go off screen try again.')
                            for i in range(num):
                                if(self.ships[startY][startX-i]):
                                    raise Exception('Boat would go onto another boat.')
                            self.army.append(ship(num))
                            for i in range(num):
                                self.army[-1].setCord(startX-i, startY)
                                self.ships[startY][startX-i] = 1
                                self.shipVals[startY][startX-i] = 'S' 
                            pass
                except Exception as e:
                    if not self.AI:
                        print(f'An error occured try again, {e}')
                    continue
                break

    def tryAttack(self, other, x, y):
        if self.attacks[y][x] == '-':
            print(f'Attacking {x}, {y}.')
            if other.ships[y][x]:
                print('Target is a hit!')
                self.attacks[y][x] = 'H'
                other.shipVals[y][x] = 'H'
                self.AImoveResult[0] = True
                for ship in other.army:
                    for location in ship.getCords():
                        if location[0] == x and location[1] == y:
                            ship.isHit() # tells the ship is was hit
                            if (ship.isSank()): # checks if the ship was sank
                                self.AImoveResult[1] = True
                other.ships[y][x] = 0
                return True
            else:
                print('Target is a miss.')
                self.attacks[y][x] = 'm'
                other.shipVals[y][x] = 'm'
                self.AImoveResult[0] = False
                return False
        else:
            if not self.AI:
                print('Target has already been attacked, pick a different location.')
            return True
    
    def AImove(self):
        # depending on the level of AI
        match self.AIlevel:
            case 1: # dumb AI random guess
                attaX = r.randint(0, validcords[-1])
                attaY = r.randint(0, validcords[-1])
                return [attaX, attaY]
            case 2:
                print('\n\nNOT YET IMLPIMENTED\n\n')
                # smarter AI, depends on if we hit to see where to go
                # if we sunk the ship it should go back to random guessing
                # if we did not sink the ship is should try the four cardinal directions from the spot it hit, 
                # when it finds that another one of those is a hit it keeps going in that direction, 
                # if that direction ends up being a miss but the ship is not sank we need to try the exact opposite direction 
                # we need a field to know if the last move was a hit
                # and a field to know if the last hit sunk a ship
                if self.AImoveResult[0] and not self.AImoveResult[1]: # second term becuase if we sunk the ship now we should not use logic to make next guess
                    # now we need to know the coords of the last hit
                    if self.direct not in [1,2,3,4]:
                        # this is when we already have a direction that we know we should go
                        self.direct = r.randint(1,4)
                    match self.direct:
                        case 1:
                            return [self.lastHit[1]-1, self.lastHit[0]]
                        case 2:
                            return [self.lastHit[1]+1, self.lastHit[0]]
                        case 3:
                            return [self.lastHit[1], self.lastHit[0]-1]
                        case 4:
                            return [self.lastHit[1], self.lastHit[0]+1]
                else:
                    attaX = r.randint(0, validcords[-1])
                    attaY = r.randint(0, validcords[-1])
                    return [attaX, attaY]    

    def stillAlive(self):
        toreturn = False
        for row in self.ships:
            for x in row:
                if x:
                    toreturn = True
                    break
            if toreturn:
                break
        return toreturn
    
    def printMap(self, map):
        cords = validcordsString[:len(validcords)]
        print(f'Y/X {cords}')
        for row in range(len(map)):
            print(f'{row} - {map[row]}')

def game():
    while True:
        try:
            dif = int(input('Choose you game length: \n1 - short, 2 - medium, 3 - long. '))
            if dif not in [1, 2, 3]:
                raise Exception('Not a valid option')
            break
        except Exception as e:
            print(f'Something went wrong try again, {e}')
            continue

    length = difficulty(dif)

    playerCount = 0
    while True:
        try:
            playerCount = int(input('1 or 2 players? '))
            if playerCount not in [1, 2]:
                raise Exception('Not a valid option')
            break
        except Exception as e:
            print(f'Something went wrong try again, {e}')
            continue
    
    if playerCount==1:
        while True:
            try:
                level = int(input('What is the computers level? '))
                # for now only 1 bot level
                if level not in [1]:#,2]:
                    raise Exception("Level should be either '1'")# or '2'.")
                break
            except Exception as e:
                print(f'An error occured try again, {e}')
            
    
    # getting player ship locations
    GOON = input('Player 1\'s turn to enter boats')
    p1 = player()

    os.system('cls') 
    
    if playerCount==2:
        os.system('cls')
        GOON = input('Player 2\'s turn to enter boats')
        p2 = player()
        os.system('cls')
    else:
        # function for computer to place its ships
        # probably same as normal player just have random generated numbers 
        p2 = player(True, level)
        print('Computer has finished placing its ships.')

    playerArry = [p1, p2]
    p = 0
    notp = 1

    # plays while both players have ships left
    while(p1.stillAlive() and p2.stillAlive()):
        playerArry[p].turn = True
        if playerArry[p].AI:
            print('Computers Turn')
            ready = input('Ready? ')
            while playerArry[p].turn:
                spots = playerArry[p].AImove()
                playerArry[p].turn = playerArry[p].tryAttack(playerArry[notp], spots[0], spots[1])
                if not playerArry[notp].stillAlive(): break
        else:
            print(f'Player {p+1}\'s turn.')
            print('Your boats (Includes other players attackes)')
            playerArry[p].printMap(playerArry[p].shipVals)
            while playerArry[p].turn:
                print('Your attacks.')
                toprint = 'Ships lengths left to sink are: '
                for ship in playerArry[notp].army:
                    if ship.sunk: continue
                    else: toprint += f'{ship.length}, '
                print(toprint)
                playerArry[p].printMap(playerArry[p].attacks)
                try:
                    attaX = int(input('X coord to attack. '))
                    attaY = int(input('Y coord to attack. '))
                    invalid = 'This is not a valid target location.'
                    if attaX not in validcords: 
                        raise Exception(invalid)
                    if attaY not in validcords: 
                        raise Exception(invalid)
                except Exception as e:
                    print(f'An error occured try again, {e}')
                    continue
                playerArry[p].turn = playerArry[p].tryAttack(playerArry[notp], attaX, attaY)
                if not playerArry[notp].stillAlive(): break
        
        if playerArry[p].turn: # we know we had a hit since it is still the same players turn
            if playerArry[notp].stillAlive(): continue
            else:
                print('\n\nWinning attacks.')
                playerArry[p].printMap(playerArry[p].attacks)
                break
        else: # if we get here we know we missed so we need to change what player is acting
            hold = p
            p = notp
            notp = hold
            if not playerArry[notp].AI:
                os.system('cls')
            print('Last attack was a miss next player\'s turn.')
            ready = input('Next player ready? ')
            os.system('cls')

    toprint = f'Game over: '
    if playerArry[p].AI:
        toprint += 'Computer won.'
    else:
        toprint += f'Player {p+1} won.'

    print(toprint)

game()