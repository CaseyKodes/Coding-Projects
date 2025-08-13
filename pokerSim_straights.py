# similar to poker sim but just for chirs's "Straights" game


"""

QUESTIONS THAT NEED TO BE ANSWERED
    - does having 2 starights, 5 and 3 or 4 and 4 or 3 and 4, mean you have a better hand that just 1 straight?
        ANSWER - yes players hand should be worht more if they have 2 straights how much more not sure

"""

import random as r
import sys
import time

class Rankings(): 
    # all lone straights are one hand type, 
    # multie straihgts are another hand type
    
    # to keep as reference 
    AllHandsReference = [
        'High Card', 
        'S 3', 'SF 3', 'Multi S3+S3', 'Multi SF3+S3', 'Multi SF3+SF3',
        'S 4', 'SF 4', 'Multi S4+S3', 'Multi S4+S4', 'Multi S4+SF3', 'Multi SF4+S3', 'Multi SF4+S4', 'Multi SF4+SF3', 'Multi SF4+SF4',
        'S 5', 'SF 5', 'Multi S5+S3', 'Multi S5+SF3', 'Multi SF5+S3', 'Multi SF5+SF3',
        'S 6', 'SF 6',
        'S 7', 'SF 7',
        'S 8', 'SF 8',
        ]

    chatsRanking = [
        'High Card',
        'S 3','S 4','S 5','Multi S3+S3','SF 3','S 6','Multi S4+S3',
        'S 7','SF 4','Multi S4+S4','Multi S5+S3','Multi SF3+S3',
        'Multi S4+SF3','Multi SF4+S3','S 8','SF 5','Multi SF3+SF3',
        'Multi S5+SF3','SF 6','Multi SF4+S4','Multi SF4+SF3',
        'Multi SF5+S3','Multi SF4+SF4','Multi SF5+SF3','SF 7','SF 8',
    ]

    # number of ways to make the normal straight flushes of varying lengths
    # XF where X <=8 28+4*(8-X) number of ways in a standard deck there are to make a straight flush of X length

    CardValueOrder = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def getCrank(): return Rankings.CardValueOrder
    def getHrank(): return Rankings.chatsRanking

class Card():
    # card objects have a value and suit which are the defining attributes 
    # they also contain a string which is just how a card would be said or writen down
    # can directly compare cards to see which one is a higher value
    def __init__(self, val, suit, sp):
        self.Suit = suit
        self.Val = val
        self.shortPrint = sp
        self.cr = Rankings.getCrank()
    def getVal(self):
        return self.Val
    def getSuit(self):
        return self.Suit
    def getStr(self):
        if self.shortPrint:
            if self.getVal() == '10':
                return f'{self.getVal()[:2]}{self.getSuit()[0]} '
            else:
                return f'{self.getVal()[0]}{self.getSuit()[0]} '
        else:
            return f'{self.Val} of {self.Suit} '
    def __str__(self):
        return self.getStr()
    def __eq__(self, other):
        return self.getVal() == other.getVal() and self.getSuit() == other.getSuit()
    def __ne__(self, other):
        return not ((self.getVal() == other.getVal()) and (self.getSuit() == other.getSuit()))
    def __lt__(self, other):
        return self.cr.index(self.getVal()) < self.cr.index(other.getVal())
    def __gt__(self, other):
        return self.cr.index(self.getVal()) > self.cr.index(other.getVal())
    def __le__(self, other):
        return (self<other or self==other)
    def __ge__(self, other):
        return (self>other or self==other)       

class Hand():
    # hand objects contain a list of card objects
    # they also have a rank that depends on the cards in a players hand and the cards on the board 
    # rank is a list to accomodate having multiple baords 
    # we can add and remove cards from a hand, clear a hand, get and set the rank of a hand
    def __init__(self, cards, numboards, sp):
        self.cards = list()
        self.shortPrint = sp
        self.rank = 'High Card' # default lowest value of a hand
        for card in cards:
            self.cards.append(card)
        self.cards.sort()
    def getCards(self):
        return self.cards
    def addCard(self, card):
        self.cards.append(card)
        self.cards.sort()
    def removeCard(self, index):
        try:
            self.cards.pop(index)
        except:
            print('There is no card at that index.')
    def clearHand(self):
        self.cards.clear()

    def setRank(self, rank):
        self.rank = rank
    def getRank(self):
        return self.rank
    def getRanks(self):
        return self.rank
      
    def __str__(self):
        toreturn = ('Hand is: ')
        for card in self.cards:
            toreturn += card.getStr()
            if card!=self.cards[-1]: toreturn+='& '
        return toreturn
    
class Deck():
    # deck objects contain 52 cards, 4 suits, and 13 values
    # it contains lists of hands that players have
    # it keeps track of the current deck after being dealt and we can save what 
    # cards are burnt (good to have if we need to test something)
    # we have funcitons to deal hands to players, deal a board of shared cards, 
    # shuffle the deck ( in two different ways ), and calculate the rank of each hand

    def __init__(self, wild=[], dead=[], numdecks=1, short=False, shortp=False): # creates a deck of 52 cards, 13 ranks and 4 suits
        self.deck = list()
        self.playerHands = list()
        self.boardList = []
        self.burnt = list()
        self.winnerstr = str()
        self.winningLevel = list()
        self.hr = Rankings.getHrank()
        self.cr = Rankings.getCrank()
        self.numBorads = int()
        self.dead = dead
        self.wild = wild
        self.shortPrint = shortp
        self.short = short
        self.seed = int()

        suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        if short: values = ['6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        else: values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for deck in range(numdecks):
            for suit in suits:
                for value in values:
                    self.deck.append(Card(value, suit, self.shortPrint))

    def __str__(self):
        toprint = ''
        for card in self.deck:
            toprint += card.getStr()
        return(toprint)

    def shuffle(self): # shuffles a deck 
        seed = r.randint(-sys.maxsize-1, sys.maxsize) # seeding the random and printing the seed so if there is weird behavior we can rerun the same seed
        seed = seed # if we ever want to change the value easily
        r.seed(seed)
        self.seed = seed

        shuffled = []
        while len(self.deck)>0:
            spot = r.randint(0, len(self.deck)-1)
            shuffled.append(self.deck.pop(spot))
        self.deck = shuffled
    
    def perfectShuffle(self, numtimes): 
        # shuffeles a deck as if someone spit it perfectly in have and alternated exactly between each half
        # probably just for fun 
        # split deck in half 
        # now we need to take one card from each half and add it back to the new shuffeled deck
        for time in range(numtimes):
            newdeck = []
            halflen = int(len(self.deck)/2)
            for card in range(halflen):
                halfway = self.deck.pop(int(len(self.deck)/2))
                first = self.deck.pop(0)
                newdeck.append(first)
                newdeck.append(halfway)
            self.deck = newdeck

    def deal(self, numPlayers, handsize, numboards): # deals to a numPlayers number of players a handsize sized hand from the top of the deck 
        for card in range(handsize):
            for player in range(numPlayers):
                if player < len(self.playerHands):
                    self.playerHands[player].addCard(self.deck.pop(0))
                else:
                    self.playerHands.append(Hand([self.deck.pop(0)], numboards, self.shortPrint))
                 
    def calcHandRanks(self): # figure out which hand has the best hand 
        # need to look at each hand in player hands and every card on the board
        # card then we will update their hand type if they make a better hand
        # since it is possible we did multiple baords we add a rank for each board to each hand
        for hand in self.playerHands:
            # filtering hands into suit ditionary
            numwilds = 0
            suitcount = {'Spades':[], 'Hearts':[], 'Clubs':[], 'Diamonds':[]}
            for card in hand.getCards():
                if card.getVal() in self.dead:
                    continue
                if card.getVal() in self.wild:
                    numwilds+=1
                    continue
                suitcount[card.getSuit()].append(card)
            

            straights = ['S 3','S 4', 'S 5', 'S 6', 'S 7', 'S 8', ]
            straightFlushes = ['SF 3','SF 4','SF 5','SF 6','SF 7','SF 8',]

            for TruestraightLength in range(3,9):# need to chnge this to go through the range [3,8] both inclusive
                if any(len(x) > 4-numwilds for x in suitcount.values()):
                    # if we are here we know we have a flush now we want to check if those cards are in order 
                    # looking for straight flush
                    for key, value in suitcount.items():
                        if self.short: rankcount = {'6':0, '7':0, '8':0, '9':0, '10':0, 'Jack':0, 'Queen':0, 'King':0, 'Ace':0}
                        else: rankcount = {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'Jack':0, 'Queen':0, 'King':0, 'Ace':0}
                        for card in value:
                            if card.getVal() in self.dead or card.getVal() in self.wild:
                                continue
                            rankcount[card.getVal()]+=1
                        straightlist = []
                        for i in range(2): # do this so we can have wrap around straights
                            for value in rankcount.values():
                                straightlist.append(value)
                        for beg in range(len(straightlist)-TruestraightLength+1):
                            gaps = 0
                            for i in range(TruestraightLength):
                                if not straightlist[beg+i]: gaps+=1
                            if gaps<=numwilds:
                                if self.hr.index(hand.getRank()) < self.hr.index(straightFlushes[TruestraightLength-3]):
                                    hand.setRank(straightFlushes[TruestraightLength-3])
                # filling how many instances of a card value there are 
                # if the value is not wild or dead
                if self.short: rankcount = {'6':0, '7':0, '8':0, '9':0, '10':0, 'Jack':0, 'Queen':0, 'King':0, 'Ace':0}
                else: rankcount = {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'Jack':0, 'Queen':0, 'King':0, 'Ace':0}
                for card in hand.getCards():
                    if card.getVal() in self.dead or card.getVal() in self.wild:
                        continue
                    rankcount[card.getVal()]+=1
                # find straights
                straightlist = []
                for i in range(2): # do this so we can have wrap around straights
                    for value in rankcount.values():
                        straightlist.append(value)
                # this works by taking sections of 5 out of the array of numbers
                # if there are 0s in that gaps in increased 
                # we then check to see if the number of gaps is less than or equal to the number of wilds
                # if it is we know we can fill all the gaps with wilds so we have a straight
                for beg in range(len(straightlist)-TruestraightLength+1):
                    gaps = 0
                    for i in range(TruestraightLength):
                        if not straightlist[beg+i]: gaps+=1
                    if gaps<=numwilds:
                        hand.setRank(straights[TruestraightLength-3])
            
    def calcWinner(self): # from the player hand ranks find which is the best
        toreturn = f'Dead cards were {self.dead} \nWild cards were {self.wild}\n'
        winnershand = []
        winnerslevel = ''
        for playersHand in self.playerHands:
            if len(winnerslevel)==0:
                winnerslevel=(playersHand.getRank())
                winnershand.append(playersHand)
            else:
                if (self.hr.index(playersHand.getRank()) 
                    > self.hr.index(winnerslevel)):
                    # we have a worse hand then the new one
                    winnerslevel = playersHand.getRank()
                    winnershand.clear()
                    winnershand.append(playersHand)
                elif (self.hr.index(playersHand.getRank()) 
                    < self.hr.index(winnerslevel)):
                    # we have the better hand do nothing 
                    continue
                elif (self.hr.index(playersHand.getRank()) 
                    == self.hr.index(winnerslevel)):
                    # we have equal rank hands
                    # we  then need to call the tiebreak function 
                    winnershand.append(playersHand)
                    
                    # do not do this yet since we do  not have the tiebreak function implimented for this game
                    #winnershand = self.tiebreak(winnershand, winnerslevel, boardIndex)

            toreturn += f'Winning hand had rank of {winnerslevel} '
            toreturn += '\nWith a hand of: \n'
            for hand in winnershand:
                for card in hand.getCards():
                    toreturn += card.getStr()
                    if card != hand.getCards()[-1]:
                        toreturn += '& '
                if len(winnershand) > 1 and not hand == winnershand[-1]:
                    toreturn += '\nand '
            toreturn += '\n'
            self.winningLevel.append(winnerslevel)
        self.winnerstr=toreturn

    # if i just want to see how often each type of hand happens we do not need to run this  
    def tiebreak(self, hands, level, boardIndex):
        # make a list that has all hands with all cards in a hand including board and hole cards
        fullHand = [[]]*len(hands)
        wilds = [[]]*len(hands)
        for hand in range(len(hands)):
            new = []
            wild = 0
            if len(self.boardList)>0:
                for b in self.boardList[boardIndex]:
                    for card in b:
                        if card.getVal() in self.dead:
                            continue
                        if card.getVal() in self.wild:
                            wild+=1
                            continue
                        new.append(card)
            for card in hands[hand].getCards():
                if card.getVal() in self.dead:
                    continue
                if card.getVal() in self.wild:
                    wild+=1
                    continue
                new.append(card)
            fullHand[hand] = new
            wilds[hand] = wild

        #getting the exact number of each rank card in the first and last hand
        if self.short: # if we have a short deck dont use 2-5
            ranknums = [{'6':0, '7':0, '8':0, '9':0, '10':0, 'Jack':0, 'Queen':0, 'King':0, 'Ace':0},
                    {'6':0, '7':0, '8':0, '9':0, '10':0, 'Jack':0, 'Queen':0, 'King':0, 'Ace':0}]
        else:
            ranknums = [{'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'Jack':0, 'Queen':0, 'King':0, 'Ace':0},
                    {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'Jack':0, 'Queen':0, 'King':0, 'Ace':0}]
        for card in fullHand[0]:
            ranknums[0][card.getVal()]+=1
        for card in fullHand[-1]:
            ranknums[-1][card.getVal()]+=1 
        counts1 = [value for value in ranknums[0].values()]
        counts2 = [value for value in ranknums[-1].values()] 
        # we reverse the count so we now that the order of the cards goes from highest ranked card to lowest ranked card
        counts1.reverse()
        counts2.reverse()

        # sort that each list of cards in each hand so we can compare the lists easily
        for hand in fullHand:
            hand.sort(reverse=True)
        
        # seting how many cards make up a full hand if we have over 5+ cards we only 
        # look at 5 but if we have less than 5 we look at all of them
        if len(fullHand[0])>4 and len(fullHand[-1])>4:
            top = 5
        else:
            top = min(len(fullHand[0]), len(fullHand[-1])) 
            # we set the top to the minimum amount of cards
            # then we know that if we check the min amount of cards in both 
            # we can say the one that has more cards wins
        
        # one case for each hand type
        match level:
            case 'Straight': 
                # section off into groups of 5 
                # if in the 5 there are 0s (gaps) less in number than the wild number we know we found the straight
                topnums = [-1,-1] # start at -1 so if we need to test it will be easier to see when it is not overridden  
                uses = [counts1, counts2]
                wuse = [0,-1]

                # updated logic now works to break ties 
                # straights can use wilds in the middle or on the outsides or not at all and it still works 
                for hand in range(2):
                    straightlist = [num for num in uses[hand]]
                    straightlist.append(straightlist[0])
                    for cardSpot in range(len(straightlist)-4):
                        gaps = 0
                        for i in range(5):
                            if straightlist[cardSpot+i]==0:gaps+=1
                        if gaps<=wilds[wuse[hand]]: 
                            topnums[hand] = cardSpot
                            break
                if topnums[0] == topnums[-1]:
                    return hands
                if topnums[0] < topnums[-1]:
                    hands.pop(-1)
                    return hands
                if topnums[0] > topnums[-1]:
                    while len(hands) > 1:
                        hands.pop(0)
                    return hands

                pass
            case 'Straight Flush':
                # similar to straigth and flush but we need to do both 
                # first we should seperate the cards in each hand by suit
                # then for each suit check if it has more than 5 minus number of wilds cards
                # if it does check for a straight same way as in straight case
                #print('case Straight Flush solved')
                tocompare = [0 for _ in range(len(fullHand))] # the list that will hold the highest flush for all hands 
                for hand in range(len(fullHand)): # this loop is finding what cards in a hand are actually the ones that make the flush
                    suitcount = {'Spades':[], 'Hearts':[], 'Clubs':[], 'Diamonds':[]}
                    for card in fullHand[hand]:
                        suitcount[card.getSuit()].append(card)
                    maybeadd = []
                    for numSuited in suitcount.values():
                        if len(numSuited)>4-wilds[hand]:
                            maybeadd.append(numSuited)
                    # now for every list of cards that makes a flush we need to see if there is a stright in them
                    topcard = []
                    for flush in maybeadd:
                        if self.short:
                            rankcount = {'6':0, '7':0, '8':0, '9':0, '10':0, 'Jack':0, 'Queen':0, 'King':0, 'Ace':0}
                        else:
                            rankcount = {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, 
                                        '8':0, '9':0, '10':0, 'Jack':0, 'Queen':0, 'King':0, 'Ace':0}
                        for card in flush:
                            rankcount[card.getVal()]+=1
                        straightlist = []
                        straightlist.append(rankcount['Ace'])
                        for value in rankcount.values():
                            straightlist.append(value)
                        straightlist.reverse()
                        for cardSpot in range(len(straightlist)-4):
                            gaps = 0
                            for i in range(5):
                                if straightlist[cardSpot+i]==0:gaps+=1
                            if gaps<=wilds[hand]: 
                                topcard.append(cardSpot)
                    tocompare[hand] = min(topcard)
                if tocompare[0] == tocompare[-1]:
                    return hands
                elif tocompare[0] < tocompare[-1]:
                    hands.pop(-1)
                    return hands
                elif tocompare[0] > tocompare[-1]:
                    while len(hands)>1:
                        hands.pop(0)
                    return hands
                
                pass
        return hands

def handelInput(L:list): # just makes sure all the values in the list are actual card values
    changed = []
    for value in L:
        match value:
            case 'two': changed.append('2'); pass
            case 'three':changed.append('3'); pass
            case 'four':changed.append('4'); pass
            case 'five':changed.append('5'); pass
            case 'six':changed.append('6'); pass
            case 'seven':changed.append('7'); pass
            case 'eight':changed.append('8'); pass
            case 'nine':changed.append('9'); pass
            case 'ten':changed.append('10'); pass
            case 'jack' | 'j':changed.append('Jack'); pass
            case 'queen' | 'q':changed.append('Queen'); pass
            case 'king' | 'k':changed.append('King'); pass
            case 'ace' | 'a':changed.append('Ace'); pass
            case _: changed.append(value); pass # default case 
    return changed 

def simPrint(deck:Deck): # printing the results as if we are just simulating the hand
    for hand in deck.playerHands:
        print(f'{hand}- Ranks are {hand.getRanks()}')
    print(deck.winnerstr) # not complete since we are only basing off of hand rank and not doing tie breakers

def printStats(tot:dict, win:dict):
    ranks = Rankings.getHrank()
    percentdict = {rank:0 for rank in ranks}

    print('\nStats of all hands played.')
    for key in percentdict.keys():
        try:
            percentdict[key] = (win[key]/tot[key])*100
        except ZeroDivisionError:
            print(f"Hand type -{key}- did not occur.")

    print(f'# times a hand won / # times it was dealt = Winning percent.')        
    for key in percentdict.keys():
        print(f'Hand type {key} percent of times it won {percentdict[key]}.')

def seedfind():
    # this will be where we ask the user if they want to find a seed for a certain type of hand
    while True:
        try: 
            seedfinder = input('Are you trying to search for a seed? ')
            if seedfinder[0] != 'y' and seedfinder[0] != 'n': raise KeyError
            elif seedfinder[0] == 'y': return True, sys.maxsize, True
            elif seedfinder[0] == 'n': return False, 1, False
        except KeyError:
            print("Must 'y' or 'n''.")
            continue
        break

def specialcards(): # getting what types of cards are dead or wild
    while True:
        try:
            dead = input('Are there any dead cards? Seperate the values with spaces. ')
            if len(dead)>0:
                dead = dead.split(' ')
                dead = [item.lower() for item in dead]
                dead = handelInput(dead)
                for i in range(len(dead)):
                    if (dead[i] not in Rankings.getCrank()):
                        raise KeyError
        except KeyError or IndexError:
            print("Inproper input for dead cards.")
            continue
        try:
            wild = input('Are there any wild cards? Seperate the values with spaces. ')
            if len(wild):
                wild = wild.split(' ')
                wild = [item.lower() for item in wild]
                wild = handelInput(wild)
                for i in range(len(wild)):
                    if (wild[i] not in Rankings.getCrank()):
                        raise KeyError
        except KeyError or IndexError:
            print("Inproper input for wild cards.")
            continue
        set1 = set(dead)
        set2 = set(wild)
        intersec = set1.intersection(set2)
        if intersec:
            print('There is at least 1 value in both dead and wild. \nPlease re-enter.')
            continue
        return dead, wild

def printdata(find): # getting the type of print the sim should do 
    sp = False
    printStyle = ''
    while True:
        if find: return sys.maxsize, printStyle, True # if we are looking for a seed we should go through as many hands as needed to find the seed
        try:
            handsAtaTime = int(input('How many hands should be dealt at a time? '))
        except:
            print("Must input a number.")
            continue
        break
    return handsAtaTime, 's', True

def game():
    # default values
    numhands = 0
    numrounds = 0
    numdecks = 1
    numboards = 1
    numplayers = 6
    numcards = 2
    handsAtaTime = 1
    printStyle = 's'
    con = 'yes'
    round = 0
    changeDets = 'y'
    handsplayed = 0

    ranks = Rankings.getHrank()
    tothanddict = {rank:0 for rank in ranks}
    winninghanddict = {rank:0 for rank in ranks}

    while con != 'n':
        if changeDets == 'y':

            find, handsAtaTime, sp, = seedfind()
            sd, numboards, numplayers, numcards, numdecks = False, 0, 6, 8, 1
            dead, wild = specialcards()

            while True:
                if find:
                    try: # asking user what hand they want to find with thier seed searching
                        print('What winning rank are you trying to find?')
                        length = len(Rankings.getHrank())
                        if len(wild)==0: length-=1
                        for rank in range(length):
                            print(f'{rank+1} -> {Rankings.getHrank()[rank]}')
                        toFind = int(input())
                        if toFind not in range(1,length+1):
                            print(f'Must be within 1-{length}.')
                            raise KeyError
                    except KeyError or IndexError:
                        continue
                break

            handsAtaTime, printStyle, sp = printdata(find)
        
        # simulating a round of poker
        part=1
        start = time.time()
        cur = start
        interval = 10
        for handnum in range(handsAtaTime):
            round+=1
            org = Deck(wild, dead, numdecks, short=sd, shortp=sp)
            org.shuffle()
            org.deal(numplayers,numcards,numboards)
            org.calcHandRanks()
            org.calcWinner()

            # keep track of all the hands that were dealt
            for hand in org.playerHands:
                tothanddict[hand.getRank()]+=1
            numrounds += 1
            numhands += len(org.playerHands)

            for level in org.winningLevel:
                winninghanddict[level]+=1

            if find:
                if time.time()>cur+interval: # shows the user the prgram is running even if it is taking a long time
                    print(f'{(time.time()-start):.4} seconds elapsed')
                    cur+=interval
                if Rankings.getHrank()[toFind-1] in org.winningLevel: # prints the hand with the winning rank of what the user wanted 
                    print(f'\nIt took {handnum+1} hands to find the valid seed of {org.seed}')
                    simPrint(org)
                    break
            else:
                if printStyle[0] == 's':
                    print()
                    print(f'Round {round}')
                    simPrint(org)
                elif printStyle[0] == 'n' and handsAtaTime>1000:
                    oneto100 = [i for i in range(1,101)]
                    if any(round-handsplayed == x*handsAtaTime/100 for x in oneto100):
                        print(f'{part}% of hands dealt')
                        part+=1

        handsplayed+=handsAtaTime

        changeDets = input('Do you want to change the format of the hands? Y/N ')
        changeDets = changeDets.lower()
        con = input('Do you want to continue? Y/N ')
        con = con.lower()

    if not find:
        printStats(tothanddict, winninghanddict) 


game()