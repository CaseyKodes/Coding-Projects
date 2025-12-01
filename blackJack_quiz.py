# situational blackjack tester

# what this file will be doing when it is run
''' 
show the player their 2 cards and the dealers 1 card 
ask the player what they should do give them options 
    1 stand
    2 hit
    3 double
    4 split, only if they have a pair
take their option and tell them if it was correct or not, if not show the correct option 
'''

# how the file will be implimented
'''
What classes / functions / data is needed?

data - 
    need ways to store what the correct answer would be 
        this can be in 3 dictoanries of dictonaites 
            1 hard totals
            2 soft totals 
            3 pairs  
        the first layer to actual get into 1 of the 3 dictonaties will be the above values 
        the second layer will be the players card total unless they have a pair then it will be half card total
        and the final layer will be dealer cards

functions - 
    get_correct_play(playersHand, dealersCard)
        function will evaluate the player hand to determine what diconatry to look in
        then return the correct move the player should take
    
classes - 
    shoe class
        can be similar from the other black jack code 
        but there is no need for the show to ever be bigger than 1 deck
        
    do we need a hand or card class?
        keeping them since a lot of things are already implimented 
'''

import random as r

# data
pairDict = {2: {2:'Split', 3:'Split', 4:'Split', 5:'Split', 6:'Split', 7:'Split', 8:'No Split', 9:'No Split', 10:'No Split', 11:'No Split',},
            3: {2:'Split', 3:'Split', 4:'Split', 5:'Split', 6:'Split', 7:'Split', 8:'No Split', 9:'No Split', 10:'No Split', 11:'No Split',},
            4: {2:'No Split', 3:'No Split', 4:'No Split', 5:'Split', 6:'Split', 7:'No Split', 8:'No Split', 9:'No Split', 10:'No Split', 11:'No Split',},
            5: {2:'No Split', 3:'No Split', 4:'No Split', 5:'No Split', 6:'No Split', 7:'No Split', 8:'No Split', 9:'No Split', 10:'No Split', 11:'No Split',},
            6: {2:'Split', 3:'Split', 4:'Split', 5:'Split', 6:'Split', 7:'No Split', 8:'No Split', 9:'No Split', 10:'No Split', 11:'No Split',},
            7: {2:'Split', 3:'Split', 4:'Split', 5:'Split', 6:'Split', 7:'Split', 8:'No Split', 9:'No Split', 10:'No Split', 11:'No Split',},
            8: {2:'Split', 3:'Split', 4:'Split', 5:'Split', 6:'Split', 7:'Split', 8:'Split', 9:'Split', 10:'Split', 11:'Split',},
            9: {2:'Split', 3:'Split', 4:'Split', 5:'Split', 6:'Split', 7:'No Split', 8:'Split', 9:'Split', 10:'No Split', 11:'No Split',},
            10:{2:'No Split', 3:'No Split', 4:'No Split', 5:'No Split', 6:'No Split', 7:'No Split', 8:'No Split', 9:'No Split', 10:'No Split', 11:'No Split',},
            11:{2:'Split', 3:'Split', 4:'Split', 5:'Split', 6:'Split', 7:'Split', 8:'Split', 9:'Split', 10:'Split', 11:'Split',},
            }
softDict = {2: {2:'Hit', 3:'Hit', 4:'Hit', 5:'Double', 6:'Double', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
            3: {2:'Hit', 3:'Hit', 4:'Hit', 5:'Double', 6:'Double', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
            4: {2:'Hit', 3:'Hit', 4:'Double', 5:'Double', 6:'Double', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
            5: {2:'Hit', 3:'Hit', 4:'Double', 5:'Double', 6:'Double', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
            6: {2:'Hit', 3:'Hit', 4:'Double', 5:'Double', 6:'Double', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
            7: {2:'Double', 3:'Double', 4:'Double', 5:'Double', 6:'Double', 7:'Stand', 8:'Stand', 9:'Hit', 10:'Hit', 11:'Hit',},
            8: {2:'Stand', 3:'Stand', 4:'Stand', 5:'Stand', 6:'Double', 7:'Stand', 8:'Stand', 9:'Stand', 10:'Stand', 11:'Stand',},
            9: {2:'Stand', 3:'Stand', 4:'Stand', 5:'Stand', 6:'Stand', 7:'Stand', 8:'Stand', 9:'Stand', 10:'Stand', 11:'Stand',},
            }
hardDict = { 4: {2:'Hit', 3:'Hit', 4:'Hit', 5:'Hit', 6:'Hit', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
             5: {2:'Hit', 3:'Hit', 4:'Hit', 5:'Hit', 6:'Hit', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
             6: {2:'Hit', 3:'Hit', 4:'Hit', 5:'Hit', 6:'Hit', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
             7: {2:'Hit', 3:'Hit', 4:'Hit', 5:'Hit', 6:'Hit', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
             8: {2:'Hit', 3:'Hit', 4:'Hit', 5:'Hit', 6:'Hit', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
             9: {2:'Hit', 3:'Double', 4:'Double', 5:'Double', 6:'Double', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
            10: {2:'Double', 3:'Double', 4:'Double', 5:'Double', 6:'Double', 7:'Double', 8:'Double', 9:'Double', 10:'Hit', 11:'Hit',},
            11: {2:'Double', 3:'Double', 4:'Double', 5:'Double', 6:'Double', 7:'Double', 8:'Double', 9:'Double', 10:'Double', 11:'Double',},
            12: {2:'Hit', 3:'Hit', 4:'Stand', 5:'Stand', 6:'Stand', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
            13: {2:'Stand', 3:'Stand', 4:'Stand', 5:'Stand', 6:'Stand', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
            14: {2:'Stand', 3:'Stand', 4:'Stand', 5:'Stand', 6:'Stand', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
            15: {2:'Stand', 3:'Stand', 4:'Stand', 5:'Stand', 6:'Stand', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
            16: {2:'Stand', 3:'Stand', 4:'Stand', 5:'Stand', 6:'Stand', 7:'Hit', 8:'Hit', 9:'Hit', 10:'Hit', 11:'Hit',},
            17: {2:'Stand', 3:'Stand', 4:'Stand', 5:'Stand', 6:'Stand', 7:'Stand', 8:'Stand', 9:'Stand', 10:'Stand', 11:'Stand',},
            18: {2:'Stand', 3:'Stand', 4:'Stand', 5:'Stand', 6:'Stand', 7:'Stand', 8:'Stand', 9:'Stand', 10:'Stand', 11:'Stand',},
            19: {2:'Stand', 3:'Stand', 4:'Stand', 5:'Stand', 6:'Stand', 7:'Stand', 8:'Stand', 9:'Stand', 10:'Stand', 11:'Stand',},
            20: {2:'Stand', 3:'Stand', 4:'Stand', 5:'Stand', 6:'Stand', 7:'Stand', 8:'Stand', 9:'Stand', 10:'Stand', 11:'Stand',},
            }

class Card():
    # card objects have a value 
    # they also contain a string which is just how a card would be said or writen down
    def __init__(self, val, suit):
        self.Suit = suit
        self.Val = val
        self.string = f'{self.Val} {self.Suit} '
    def getVal(self):
        return self.Val
    def getValnum(self):
        if self.Val == 'Ace' :
            return 11
        if self.Val == 'King' :
            return 10
        if self.Val == 'Queen' :
            return 10
        if self.Val == 'Jack':
            return 10
        return self.Val
    def getStr(self):
        return self.string
    def __str__(self):
        return self.getStr()     

class Hand():
    # hand objects contain a list of card objects
    # we can add and remove cards from a hand, clear a hand
    def __init__(self, cards):
        self.cards = list()
        for card in cards:
            self.cards.append(card)

    def getCards(self):
        return self.cards
    def addCard(self, card):
        self.cards.append(card)
    def removeCard(self, index):
        try:
            self.cards.pop(index)
        except:
            print('There is no card at that index.')
    
    def clearHand(self):
        self.cards.clear()
    
    def getValue(self): 
        value = 0
        aces = 0
        for card in self.cards:
            if card.getVal() != 'Ace':
                value += card.getValnum()
            if card.getVal() == 'Ace':
                aces += 1

        if aces>0:
            if (value+11+aces-1) > value+aces and (value+11+aces-1)<=21:
                return (value+11+aces-1)
            else:
                return value+aces
        return value

    def __str__(self):
        toreturn = ('Player has: ')
        for card in self.cards:
            toreturn += card.getStr()
            if card!=self.cards[-1]: toreturn+='& '
        return toreturn

class shoe():
    def __init__(self):
        self.deck = list()
        self.dealer = Hand([])
        self.players = list()

        suits = ['s', 'h', 'c', 'd']
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
        for suit in suits:
            for value in values:
                self.deck.append(Card(value, suit))

    def shuffle(self):  
        shuffled = []
        while len(self.deck)>0:
            spot = r.randint(0, len(self.deck)-1)
            shuffled.append(self.deck.pop(spot))
        self.deck = shuffled

    def deal(self):
        for player in self.players:
            player.clearHand()
        self.dealer.clearHand()
        for card in range(2):
            if 0 < len(self.players):
                self.players[0].addCard(self.deck.pop(0))
            else:
                self.players.append(Hand([self.deck.pop(0)]))
            self.dealer.addCard(self.deck.pop(0))

    def showHands(self):
        i = 1
        for hand in self.players:
            print(f'{hand}- Value: {hand.getValue()}')
            i+=1
        print(f'Dealers top card is: {self.dealer.getCards()[0]}')

def get_correct_play(playersHand : Hand, dealersTopCard : Card, cat):
    if cat == 'Hard':
        return hardDict[playersHand.getValue()][dealersTopCard.getValnum()]

    if cat == 'Soft':
        return softDict[playersHand.getValue()-11][dealersTopCard.getValnum()]
    
    if cat == 'Pair':
        splitAction = pairDict[playersHand.getValue()/2][dealersTopCard.getValnum()]
        if splitAction == 'Split':
            return splitAction
        else:
            return hardDict[playersHand.getValue()][dealersTopCard.getValnum()]

def game(numQ, mode):
    numberCorrect = 0

    for i in range(numQ):

        while True:
            s = shoe() # make a shoe
            s.shuffle() # shuffle it
            s.deal() # deal it

            # if player has blkacjack skip iteration since there is nothing for them to do
            if (s.players[0].getValue() == 21):
                continue
            break

        if mode in [2, 3, 4]:
            s.players[0].clearHand()

            suits = ['s', 'h', 'c', 'd']
            values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
            tens = [10, 'Jack', 'Queen', 'King',]

            match mode:
                # case 1 is dealt with by skipping this section of code

                case 2: # hard totals only
                    # we need to make sure there is no ace in the hand and it is not paired
                    v1 = values[r.randint(0, len(values)-2)]
                    if v1 in tens:
                        for v in tens:
                            values.remove(v)
                    else:
                        values.remove(v1)
                    v2 = values[r.randint(0, len(values)-2)]
                    s1 = suits[r.randint(0,len(suits)-1)]
                    s2 = suits[r.randint(0,len(suits)-1)]
                    s.players[0].addCard(Card(v1, s1))
                    s.players[0].addCard(Card(v2, s2))
                                         
                case 3: # soft totals only
                    # need to make sure there is an ace in the hand but only 1
                    values.remove(10)
                    values.remove('Jack')
                    values.remove('Queen')
                    values.remove('King')

                    v1 = values[r.randint(0, len(values)-2)]
                    s1 = suits[r.randint(0,len(suits)-1)]
                    sAce = suits[r.randint(0,len(suits)-1)]
                    s.players[0].addCard(Card(v1, s1))
                    s.players[0].addCard(Card('Ace', sAce))
                    
                case 4: # pair totals only
                    # need to make sure the both cards have equal values
                    v1 = values[r.randint(0, len(values)-1)]
                    if v1 in tens:
                        v2 = tens[r.randint(0,len(tens)-1)]
                    else: v2 = v1
                    s1 = suits[r.randint(0,len(suits)-1)]
                    s2 = suits[r.randint(0,len(suits)-1)]
                    s.players[0].addCard(Card(v1, s1))
                    s.players[0].addCard(Card(v2, s2))

        s.showHands() # show the player

        # catorgarize the hand
        catagory = ''
        playersCards = s.players[0].getCards()
        if (playersCards[0].getValnum() == playersCards[1].getValnum()):
            # hand is a pair offer the split option
            catagory = 'Pair'
        elif (playersCards[0].getVal() == 'Ace' or playersCards[1].getVal() == 'Ace'):
            # hand is a soft total
            catagory = 'Soft'
        else:
            # hand is a hard total
            catagory = 'Hard'

        # get the right play
        correctPlay = get_correct_play(s.players[0], s.dealer.getCards()[0], catagory)

        # TODO
        # this is where we actuall get user input
        # if we want to make this into somewhat of an actauyl UI it would start here

        # get their reaction 
        choice = ''
        if catagory == 'Pair':
            toShow = f'Does player want to hit, stand, split or double down? '
        else:
            toShow = f'Does player want to hit, stand, or double down? '
            
        while True:
            try:
                choice = input(toShow)
                choice = choice.lower()

                if catagory == 'Pair':
                    options = choice[0:2]!='hi' and choice[0:2]!='st' and choice[0:2]!='sp' and choice[0:2]!='do'
                    errorM = "Choice must be 'Hit', 'Stand', 'Split', or 'Double'."
                else:
                    options = choice[0:2]!='hi' and choice[0:2]!='st' and choice[0:2]!='do'
                    errorM = "Choice must be 'Hit', 'Stand', or 'Double'."

                if options:
                    raise KeyError
            except:
                print(errorM)
                continue
            break

        # tell them if it is right or wrong
        if correctPlay[0:2].lower() == choice[0:2]:
            numberCorrect+=1
            print("Correct!")
        else:
            print(f'Incorrect, the correct choice was to {correctPlay}.')
        print()

    return numberCorrect


if __name__ == '__main__':
    keepPlaying = True
    while keepPlaying:
        while True:
            try:
                print('Pick a specific type of hand you would like to practice.')
                mode = int(input('1 - All, 2 - Hard only, 3 - Soft only, 4 - Pair only\n' ))
                if mode not in [1,2,3,4]:
                    raise Exception('Not a valid hand type.')
            except Exception as e:
                print(f'An error occured try again, {e}.')
                continue
            break
        while True:
            try:
                numQ = int(input("Enter number of practice Situations to complete. "))
            except Exception as e:
                print(f'An error occured try again, {e}.')
                continue
            break

        percent = game(numQ, mode)
        print(f'{percent} / {numQ} Correct Answers, {(percent*100)/numQ:.2f}%')
    
        toExit = input('Do you want to keep playing? ("y" or "n") ')
        if len(toExit) > 0 and toExit[0].lower() == 'n':
            keepPlaying = False