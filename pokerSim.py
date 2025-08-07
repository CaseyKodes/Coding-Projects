# Poker simulator
 
# things that are possible
    # can play short deck with adjusted hand ranking
    # as long as there are enough cards in the deck
        # deal hands to any number of players 
        # the hands can be any size 
        # we can deal any number of boards of 5 cards (3 flop, 1 turn, 1 river) and 3 burn cards
    # we can calculate the rank of each players hand on each board
    # break ties between players if they have the same hand rank
    # have dead and or wild cards
    # can find seeds with specific winning hands

import random as r
import sys
import time

class Rankings(): # basically just a place to hold these arrays which tell us the ordering of hands 
    HandValueOrder = ['High Card', 'Pair', 'Two Pair', 'Three of a kind', 'Straight', 'Flush', 'Full House', 'Four of a kind', 'Straight Flush', 'Five of a kind']
    HandValueOrderShort = ['High Card', 'Pair', 'Two Pair', 'Three of a kind', 'Straight', 'Full House', 'Flush', 'Four of a kind', 'Straight Flush', 'Five of a kind']
    CardValueOrder = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    def getCrank(): return Rankings.CardValueOrder
    def getHrank(short): 
        if short:
            return Rankings.HandValueOrderShort
        else:
            return Rankings.HandValueOrder

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
        self.rank = ['High Card']*max(numboards, 1) # default lowest value of a hand
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

    def setRank(self, rank, index):
        self.rank[index] = rank
    def getRank(self, index):
        return self.rank[index]
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
        self.hr = Rankings.getHrank(short)
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
        self.dealboards(numboards)
                
    def dealboards(self, numB):
        flops = []
        turns = []
        rivers = []
        for i in range(numB):
            toaddF = []
            self.burnt.append(self.deck.pop(0))
            for card in range(3):
                toaddF.append(self.deck.pop(0))
            flops.append(toaddF)
        for i in range(numB):
            self.burnt.append(self.deck.pop(0))
            toaddT = []
            toaddT.append(self.deck.pop(0))
            turns.append(toaddT)
        for i in range(numB):
            self.burnt.append(self.deck.pop(0))
            toaddR = []
            toaddR.append(self.deck.pop(0))
            rivers.append(toaddR)
        for board in range(numB):
            b = [flops[board]+turns[board]+rivers[board]]
            self.boardList.append(b)    
        
    def calcHandRanks(self): # figure out which hand has the best hand 
        # need to look at each hand in player hands and every card on the board
        # card then we will update their hand type if they make a better hand
        # since it is possible we did multiple baords we add a rank for each board to each hand
        for hand in self.playerHands:
            board=-1
            for rank in hand.getRanks():
                board+=1 
                # finding flushes 
                numwilds = 0
                suitcount = {'Spades':[], 'Hearts':[], 'Clubs':[], 'Diamonds':[]}
                for card in hand.getCards():
                    if card.getVal() in self.dead:
                        continue
                    if card.getVal() in self.wild:
                        numwilds+=1
                        continue
                    suitcount[card.getSuit()].append(card)
                if len(self.boardList) > 0:
                    for b in self.boardList[board]:
                        for card in b:
                            if card.getVal() in self.dead:
                                continue
                            if card.getVal() in self.wild:
                                numwilds+=1
                                continue
                            suitcount[card.getSuit()].append(card)
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
                        straightlist.append(rankcount['Ace'])
                        for value in rankcount.values():
                            straightlist.append(value)
                        TruestraightLength = 5 
                        for beg in range(len(straightlist)-TruestraightLength+1):
                            gaps = 0
                            for i in range(TruestraightLength):
                                if not straightlist[beg+i]: gaps+=1
                            if gaps<=numwilds:
                                if self.hr.index(hand.getRank(board)) < self.hr.index('Straight Flush'):
                                    hand.setRank('Straight Flush', board)
                    if self.hr.index(hand.getRank(board)) < self.hr.index('Flush'):
                        hand.setRank('Flush', board)

                # filling how many instances of a card value there are 
                # if the value is not wild or dead
                if self.short: rankcount = {'6':0, '7':0, '8':0, '9':0, '10':0, 'Jack':0, 'Queen':0, 'King':0, 'Ace':0}
                else: rankcount = {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'Jack':0, 'Queen':0, 'King':0, 'Ace':0}
                if len(self.boardList) > 0:
                    for b in self.boardList[board]:
                        for card in b:
                            if card.getVal() in self.dead or card.getVal() in self.wild:
                                continue
                            rankcount[card.getVal()] += 1
                for card in hand.getCards():
                    if card.getVal() in self.dead or card.getVal() in self.wild:
                        continue
                    rankcount[card.getVal()]+=1
                # find straights
                straightlist = []
                straightlist.append(rankcount['Ace'])
                for value in rankcount.values():
                    straightlist.append(value)

                # this works by taking sections of 5 out of the array of numbers
                # if there are 0s in that gaps in increased 
                # we then check to see if the number of gaps is less than or equal to the number of wilds
                # if it is we know we can fill all the gaps with wilds so we have a straight
                TruestraightLength = 5 
                for beg in range(len(straightlist)-TruestraightLength+1):
                    if self.hr.index(hand.getRank(board))>self.hr.index('Straight'): break
                    gaps = 0
                    for i in range(TruestraightLength):
                        if not straightlist[beg+i]: gaps+=1
                    if gaps<=numwilds:
                        hand.setRank('Straight', board)

                # determining based off the number of instances of that card value what type of hand a player has
                # this is for pairs two pairs three of a kind full house and four of a kind
                if any(x>=5-numwilds for x in rankcount.values()):
                    # this is the 5 of a kind case 
                    if self.hr.index(hand.getRank(board)) < self.hr.index('Five of a kind'):
                        hand.setRank('Five of a kind', board)
                        continue
                elif any(x==4-numwilds for x in rankcount.values()):
                    if self.hr.index(hand.getRank(board)) < self.hr.index('Four of a kind'):
                        hand.setRank('Four of a kind', board)
                        continue
                elif any(x==3-numwilds for x in rankcount.values()):
                    for key in rankcount.keys():
                        if rankcount[key] == 3-numwilds:
                            smaller = {key: value for key, value in rankcount.items()}
                            smaller.pop(key)
                            if any(y==2 for y in smaller.values()):
                                if self.hr.index(hand.getRank(board)) < self.hr.index('Full House'):
                                    hand.setRank('Full House', board)
                                    continue
                            if self.hr.index(hand.getRank(board)) < self.hr.index('Three of a kind'):
                                hand.setRank('Three of a kind', board)
                                continue
                elif any(x==2-numwilds for x in rankcount.values()):
                    for key in rankcount.keys():
                        if rankcount[key] == 2:
                            smaller = {key: value for key, value in rankcount.items()}
                            smaller.pop(key)
                            if any(y==2 for y in smaller.values()):
                                if self.hr.index(hand.getRank(board)) < self.hr.index('Two Pair'):
                                    hand.setRank('Two Pair', board)
                                    continue
                                break 
                    if self.hr.index(hand.getRank(board)) < self.hr.index('Pair'):
                        hand.setRank('Pair', board) 
            
    def calcWinner(self): # from the player hand ranks find which is the best
        toreturn = f'Dead cards were {self.dead} \nWild cards were {self.wild}\n'
        loopover = max(1, len(self.boardList))
        for boardIndex in range(loopover):
            winnershand = []
            winnerslevel = ''
            for playersHand in self.playerHands:
                if len(winnerslevel)==0:
                    winnerslevel=(playersHand.getRank(boardIndex))
                    winnershand.append(playersHand)
                else:
                    if (self.hr.index(playersHand.getRank(boardIndex)) 
                        > self.hr.index(winnerslevel)):
                        # we have a worse hand then the new one
                        winnerslevel = playersHand.getRank(boardIndex)
                        winnershand.clear()
                        winnershand.append(playersHand)
                    elif (self.hr.index(playersHand.getRank(boardIndex)) 
                        < self.hr.index(winnerslevel)):
                        # we have the better hand do nothing 
                        continue
                    elif (self.hr.index(playersHand.getRank(boardIndex)) 
                        == self.hr.index(winnerslevel)):
                        # we have equal rank hands
                        # we  then need to call the tiebreak function 
                        winnershand.append(playersHand)
                        winnershand = self.tiebreak(winnershand, winnerslevel, boardIndex)
            toreturn += f'Winning hand had rank of {winnerslevel} '
            if len(self.boardList)>0:
                toreturn += f'on Board number {boardIndex+1}, with board of: \n'
                if len(self.boardList)>0:
                    for b in self.boardList[boardIndex]:
                        for card in b:
                            toreturn += card.getStr()
                            if card != b[-1]: toreturn +='& '
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

        # this uses the wilds in a hand to make that hand better for pairs
        # only doing for pair type hands since for the ther types we only need 1 of a card value
        if level != 'Straight' and level != 'Flush' and level != 'Straight Flush': 
            maximum = 0
            maxIndex = 0
            for index in range(len(counts1)):
                if counts1[index]+wilds[0] > maximum:
                    maximum = counts1[index]+wilds[0]
                    maxIndex = index
            counts1[maxIndex] = maximum
            maximum = 0
            maxIndex = 0
            for index in range(len(counts2)):
                if counts2[index]+wilds[-1] > maximum:
                    maximum = counts2[index]+wilds[-1]
                    maxIndex = index
            counts2[maxIndex] = maximum

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
        ties = 0
        match level:
            case 'High Card':
                #print('case High Card solved') 
                for chance in range(5):
                    try:
                        spot1 = counts1.index(1)
                        spot2 = counts2.index(1)
                    except ValueError as e:
                        # one of the hands does not have 5 active cards
                        if len(fullHand[0])>len(fullHand[-1]):
                            hands.pop(-1)
                            return hands
                        elif len(fullHand[0])<len(fullHand[-1]):
                            while len(hands)>1:
                                hands.pop(0)
                            return hands
                        else:
                            return hands
                    if spot1==spot2:
                        counts1.pop(spot1)
                        counts2.pop(spot2)
                        continue
                    elif spot1<spot2:
                        hands.pop(-1)
                        return hands
                    elif spot1>spot2:
                        while len(hands)>1:
                            hands.pop(0)
                        return hands
                pass
            case 'Pair' | 'Three of a kind' | 'Four of a kind':
                # we do this since they all use the exact same logic 
                # only difference is what number we look for in the list
                # and how many times we check high card to complete the hand

                #print('case Two/Three/Four of a kind solved')
                if level == 'Pair': maxties = 3
                elif level == 'Three of a kind': maxties = 2
                elif level == 'Four of a kind' : maxties = 1

                spot1 = counts1.index(5-maxties)
                spot2 = counts2.index(5-maxties)
                if spot1==spot2:
                    counts1.pop(spot1)
                    counts2.pop(spot2)
                    for highspot1 in range(len(counts1)):
                        if counts1[highspot1]!=0:
                            for highspot2 in range(len(counts2)):
                                if counts2[highspot2]!=0:
                                    if highspot1==highspot2:
                                        ties+=1
                                        if ties==maxties:
                                            return hands
                                        continue
                                    elif highspot1>highspot2:
                                        while len(hands)>1:
                                            hands.pop(0)
                                        return hands
                                    elif highspot1<highspot2:
                                        hands.pop(-1)
                                        return hands
                    # if we got here we know the hands are  <=4 cards long 
                    # so we need to check the lengths of the hands now
                    if len(fullHand[0])>len(fullHand[-1]):
                        hands.pop(-1)
                        return hands
                    elif len(fullHand[0])<len(fullHand[-1]):
                        while len(hands)>1:
                            hands.pop(0)
                        return hands
                    else:
                        return hands
                elif spot1>spot2:
                    while len(hands)>1:
                        hands.pop(0)
                    return hands
                elif spot1<spot2:
                    hands.pop(-1)
                    return hands
                pass
            case 'Two Pair':
                #print('case Two Pair solved')
                spot1 = counts1.index(2)
                spot2 = counts2.index(2)
                if spot1==spot2:
                    counts1.pop(spot1)
                    counts2.pop(spot2)
                    pairspot1 = counts1.index(2)
                    pairspot2 = counts2.index(2)
                    if pairspot1 == pairspot2:
                        counts1.pop(pairspot1)
                        counts2.pop(pairspot2)
                        #if they have equal pairs for both we should check if one has a longer length than the other right away
                        if len(fullHand[0]) < 5 or len(fullHand[-1]) < 5:
                            if len(fullHand[0])>len(fullHand[-1]):
                                hands.pop(-1)
                                return hands
                            elif len(fullHand[0])<len(fullHand[-1]):
                                while len(hands)>1:
                                    hands.pop(0)
                                return hands
                            else: return hands
                        for high1 in range(len(counts1)):
                            if counts1[high1]!=0:
                                for high2 in range(len(counts2)):
                                    if counts2[high2]!=0:
                                        if high1==high2:
                                            return hands
                                        elif high1>high2:
                                            while len(hands)>1:
                                                hands.pop(0)
                                            return hands
                                        elif high1<high2:
                                            hands.pop(-1)
                                            return hands
                    elif pairspot1>pairspot2:
                        while len(hands)>1:
                            hands.pop(0)
                        return hands
                    elif pairspot1<pairspot2:
                        hands.pop(-1)
                        return hands
                elif spot1>spot2:
                    while len(hands)>1:
                        hands.pop(0)
                    return hands
                elif spot1<spot2:
                    hands.pop(-1)
                    return hands
                pass
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
            case 'Flush':
                #print('case Flush solved')
                tocompare = [[]]*len(fullHand) # the list that will hold the highest flush for all hands 
                for hand in range(len(fullHand)): # this loop is finding what cards in a hand are actually the ones that make the flush
                    suitcount = {'Spades':[], 'Hearts':[], 'Clubs':[], 'Diamonds':[]}
                    for card in fullHand[hand]:
                        suitcount[card.getSuit()].append(card)
                    for number in range(wilds[hand]):
                        for key in suitcount.keys():
                            suitcount[key].append(Card('Ace', key, self.shortPrint))
                            suitcount[key].sort(reverse=True)
                    maybeadd = []
                    for numSuited in suitcount.values():
                        if len(numSuited)>4:
                            maybeadd.append(numSuited[0:top])
                    while len(maybeadd)>1:
                        # need to compare the flushes in a single hand 
                        for card in range(len(maybeadd[0])):
                            if maybeadd[0][card] > maybeadd[-1][card]:
                                maybeadd.pop(-1)
                            elif maybeadd[0][card] < maybeadd[-1][card]:
                                maybeadd.pop(0)
                            elif maybeadd[0][card] == maybeadd[-1][card]:
                                continue
                    tocompare[hand] = maybeadd

                # now we have tocompare filled with the flushes from each hand so we need to compare them
                for card in range(len(tocompare[0])):
                    if tocompare[0][card] == tocompare[-1][card]:
                        continue
                    elif tocompare[0][card] > tocompare[-1][card]:
                        hands.pop(-1)
                        return hands
                    elif tocompare[0][card] < tocompare[-1][card]:
                        while len(hands) > 1:
                            hands.pop(0)
                        return hands
                pass
            case 'Full House': 
                #print('case Full House solved')
                # find the highest 3 of a kind for each hand and compare them 
                # if equal value compare highest paired card 
                spot1 = counts1.index(3)
                spot2 = counts2.index(3)
                if spot1==spot2:
                    counts1.pop(spot1)
                    counts2.pop(spot2)
                    pairspot1 = counts1.index(2)
                    pairspot2 = counts2.index(2)
                    if pairspot1 == pairspot2:
                        return hands
                    elif pairspot1>pairspot2:
                        while len(hands)>1:
                            hands.pop(0)
                        return hands
                    elif pairspot1<pairspot2:
                        hands.pop(-1)
                        return hands
                elif spot1>spot2:
                    while len(hands)>1:
                        hands.pop(0)
                    return hands
                elif spot1<spot2:
                    hands.pop(-1)
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
            case 'Five of a kind':
                #print('case Five of a kind') 
                for spot1 in range(len(counts1)):
                    if counts1[spot1] >= 5:
                        for spot2 in range(len(counts2)):
                            if counts2[spot2] >= 5:
                                if spot1==spot2:
                                    return hands
                                elif spot1>spot2:
                                    while len(hands)>1:
                                        hands.pop(0)
                                    return hands
                                elif spot1<spot2:
                                    hands.pop(-1)
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
    print(deck.winnerstr)

def printStats(tot:dict, win:dict):
    percentdict = {'High Card':0, 'Pair':0, 'Two Pair':0, 'Three of a kind':0, 'Straight':0
                    , 'Flush':0, 'Full House':0, 'Four of a kind':0, 'Straight Flush':0, 'Five of a kind':0}
    print('\nStats of all hands played.')
    for key in percentdict.keys():
        try:
            percentdict[key] = (win[key]/tot[key])*100
        except ZeroDivisionError:
            print(f"Hand type -{key}- did not occur.")

    print(f'# times a hand won / # times it was dealt = Winning percent.')        
    for key in percentdict.keys():
        if key in ['High Card', 'Two Pair', 'Straight', 'Flush', 'Full House']:
            print(f'{key} - \t\t{win[key]} / {tot[key]} = {percentdict[key]}')
        elif key == 'Pair':
            print(f'{key} - \t\t\t{win[key]} / {tot[key]} = {percentdict[key]}')
        else:
            print(f'{key} - \t{win[key]} / {tot[key]} = {percentdict[key]}')

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

def handData():
    while True:
        # getting user input
        try: 
            shortdeck = input('Are you playing short deck? ')
            if shortdeck[0] != 'y' and shortdeck[0] != 'n': raise KeyError
            elif shortdeck[0] == 'y' : sd = True; deckLength=36
            elif shortdeck[0] == 'n' : sd = False; deckLength=52
        except KeyError or IndexError:
            print("Must 'y' or 'n''.")
            continue
        try:
            numdecks = 1 #int(input('How many decks should there be? ')) # dont want to ask how many decks right now 
            numboards = int(input('How many boards should be played? \n(8 Cards per board) '))
            numplayers = int(input('How many players should there be? '))
            numcards = int(input('How many cards should each player get? '))
        except:
            print("Must input a number.")
            continue
        if (numplayers*numcards + 8*numboards <= deckLength*numdecks):
            break
        else:
            print(f'There are not enough cards in {numdecks} deck(s) for that to work enter different numbers.')
            continue
    return sd, numboards, numplayers, numcards, numdecks

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
        try: 
            printStyle = input('How should the hand be shown? As a simulation or no print? ')
            printStyle = printStyle.lower()
            if printStyle[0] != 's' and printStyle[0] != 'n':
                raise KeyError
            elif printStyle[0] == 's':
                try: 
                    compress = (input("Do you want to print the values in a compressed way? (Y or N) ")).lower()
                    if compress[0] != 'y' and compress[0] != 'n': raise KeyError
                    elif compress[0] == 'y' : sp = True
                    elif compress[0] == 'n' : sp = False
                except:
                    print("Must 'y' or 'n''.")
                    continue
        except:
            print('Enter S for simulation or N for no print.')
            continue
        return handsAtaTime, printStyle, sp

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

    tothanddict = {'High Card':0, 'Pair':0, 'Two Pair':0, 'Three of a kind':0, 'Straight':0
                , 'Flush':0, 'Full House':0, 'Four of a kind':0, 'Straight Flush':0, 'Five of a kind':0}
    winninghanddict = {'High Card':0, 'Pair':0, 'Two Pair':0, 'Three of a kind':0, 'Straight':0
                    , 'Flush':0, 'Full House':0, 'Four of a kind':0, 'Straight Flush':0, 'Five of a kind':0}

    while con != 'n':
        if changeDets == 'y':

            find, handsAtaTime, sp, = seedfind()
            sd, numboards, numplayers, numcards, numdecks = handData()
            dead, wild = specialcards()

            while True:
                if find:
                    try: # asking user what hand they want to find with thier seed searching
                        print('What winning rank are you trying to find?')
                        length = len(Rankings.getHrank(sd))
                        if len(wild)==0: length-=1
                        for rank in range(length):
                            print(f'{rank+1} -> {Rankings.getHrank(sd)[rank]}')
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
                for rank in hand.getRanks():
                    tothanddict[rank]+=1
            numrounds += 1
            numhands += len(org.playerHands)

            for level in org.winningLevel:
                winninghanddict[level]+=1

            if find:
                if time.time()>cur+interval: # shows the user the prgram is running even if it is taking a long time
                    print(f'{(time.time()-start):.4} seconds elapsed')
                    cur+=interval
                if Rankings.getHrank(sd)[toFind-1] in org.winningLevel: # prints the hand with the winning rank of what the user wanted 
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