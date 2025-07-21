# roulette
# going to be pretty easy 

''' 
user can place 1 bet at a time and can see if they win 
'''

import random as r
import csv
import os



numbers = ['00', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 
        '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
        '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35' '36']
        
def play():
    while True:
        try: 
            startingB = float(input("How much does the player start with? "))
        except:
            print("Must input a number.")
            continue
        break
    fullHistory = False
    while True:
        try:
            history = input("Do you want to see the full history of spins played? ('Y' or 'N')" )
            history = history.lower()
            if history[0] != 'y' and history[0] != 'n':
                print('Must enter "Y" or "N"')
                raise KeyError
            elif history[0] == 'y': 
                fullHistory = True
                break
            elif history[0] == 'n': 
                fullHistory = False
                break
        except Exception as e:
            print(e)
            continue 

    while True:
        RB = False
        EO = False
        HALVES = False
        THIRDS = False
        ROWS = False
        SOLO = False
        try: 
            bet = float(input(f"What is the bet size must be less than {startingB}? "))
            if bet>startingB: raise Exception
        except:
            print(f"Must input a number less than {startingB}.")
            continue
        placedBet = ''
        betType = int(input(f'Choose the type of bet you want to make. Balance is currently {startingB}\
                            \noptions are \
                            \n\t 1 - black or red pay 1:1\
                            \n\t 2 - even or odd pay 1:1\
                            \n\t 3 - 1-18 19-36 pay 1:1\
                            \n\t 4 - first 12 second 12 third 12 pay 2:1\
                            \n\t 5 - any of the rows pays 2:1 \
                            \n\t\t   row 1 = 1,4,5,10,13,16,19,22,25,28,31,34\
                            \n\t\t   row 2 = 2,5,8,11,14,17,20,23,26,29,32,35\
                            \n\t\t   row 3 = 3,6,9,12,15,18,21,24,27,30,33,36\
                            \n\t 6 - any individual number pays 36:1\n'))
        choices = [1,2,3,4,5,6]
        if betType not in choices:
            print('Not a valid selection.')
            continue
        while True:
            match betType:
                case 1:
                    RB = True
                    placedBet = input('1 for Red or 2 for black?\n')
                    placedBet.lower()
                    if placedBet!='1' and placedBet!='2':
                        print('Not a valid selection.')
                        continue
                    if placedBet == '1': placedBet = 'red'
                    elif placedBet == '2': placedBet = 'black'
                    break
                case 2:
                    EO = True
                    placedBet = input('1 for Even or 2 for Odd?\n')
                    placedBet.lower()
                    if placedBet!='1' and placedBet!='2':
                        print('Not a valid selection.')
                        continue
                    if placedBet == '1': placedBet = 'even'
                    elif placedBet == '2': placedBet = 'odd'
                    break
                case 3:
                    HALVES = True
                    placedBet = (input('1 for 1-18 or 2 for 19-36?\n'))
                    if placedBet!='1' and placedBet!='2':
                        print('Not a valid selection.')
                        continue
                    if placedBet == '1': placedBet = '1st half'
                    elif placedBet == '2': placedBet = '2nd half'
                    break
                case 4:
                    THIRDS = True
                    placedBet = (input('1 for 1-12 or 2 for 13-24 or 3 for 25-36?\n'))
                    if placedBet!='1' and placedBet!='2' and placedBet!='3':
                        print('Not a valid selection.')
                        continue
                    if placedBet == '1': placedBet = '1st third'
                    elif placedBet == '2': placedBet = '2nd third'
                    elif placedBet == '3': placedBet='3rd third'
                    break
                case 5:
                    ROWS = True
                    placedBet = (input('1 for row 1 or 2 for row 2 or 3 for row 3?\n\
                                    row 1 = 1,4,5,10,13,16,19,22,25,28,31,34\n\
                                    row 2 = 2,5,8,11,14,17,20,23,26,29,32,35\n\
                                    row 3 = 3,6,9,12,15,18,21,24,27,30,33,36\n'))
                    if placedBet!='1' and placedBet!='2' and placedBet!='3':
                        print('Not a valid selection.')
                        continue
                    if placedBet == '1': placedBet = 'bottom'
                    elif placedBet == '2': placedBet = 'middle'
                    elif placedBet == '3': placedBet='top'
                    break
                case 6:
                    SOLO = True
                    placedBet = input('Enter the specific number you want to pick.\n')
                    if placedBet not in numbers:
                        print('Not a valid selection.')
                        continue
                    break
        #placedBet
        result = r.randint(1,39)
        data = []
        if startingB==69 and SOLO:
            result = 2 # double 0

        # user needs to input path to file here 
        with open(r"\\midfile01\Departments\Metrology MFG\Casey Provitera\funzies\\roulette_dictionary.csv", 'r') as file:

            reader = csv.reader(file)
            i = 1
            for row in reader:
                if i == result:
                    print(f'Row {i}, {row}')
                    data = row
                i+=1
        
        if RB: # check color
            if placedBet == str(data[1]):
                print('Bet won')
                startingB+=bet
            else: 
                print('Bet lost')
                startingB-=bet
        elif EO: #check parity
            if placedBet == str(data[2]):
                print('Bet won')
                startingB+=bet
            else: 
                print('Bet lost')
                startingB-=bet
        elif HALVES: # check for number in specified half
            if placedBet == str(data[3]):
                print('Bet won')
                startingB+=bet
            else: 
                print('Bet lost')
                startingB-=bet
        elif THIRDS: # check for number in specified third
            if placedBet == str(data[4]):
                print('Bet won')
                startingB+=(bet*2)
            else: 
                print('Bet lost')
                startingB-=bet
        elif ROWS: # check for number in specified row
            if placedBet == str(data[5]):
                print('Bet won')
                startingB+=(bet*2)
            else: 
                print('Bet lost')
                startingB-=bet
        elif SOLO: # check number is exactly what is landed on 
            if placedBet == str(data[0]):
                print('Bet won')
                startingB+=(bet*32)
            else: 
                print('Bet lost')
                startingB-=bet
        
        print(f'Current balance {startingB}')

        if startingB<=0:
            print('Out of money leave the table.')
            quit()

        exit = input('Enter any character to play the next hand. \nEnter 0 to exit. ')
        if exit != '0': 
            if not fullHistory:
                os.system('cls')
            continue
        else: print('Thanks for playing.'); quit()

play()