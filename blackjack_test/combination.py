# want to instead make this a black jack situational quiz game
# needs a lot of rework

import random as r
from flask import Flask, render_template, request

app = Flask(__name__)

# picture dimensions
WIDTH = 33
HEIGHT = 45
scale_factor = 5

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
        if val == 10:
            self.image_name = f'10{self.Suit[0]}'.lower()
        else:
            self.image_name = f'{str(self.Val)[0]}{self.Suit[0]}'.lower()
    def get_image_name(self):
        return self.image_name
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

class Shoe():
    def __init__(self):
        self.deck = list()
        self.dealer = Hand([])
        self.players = list()

        suits = ['s', 'h', 'c', 'd']
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
        for decks in range(3):
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

def get_correct_play(playersHand : Hand, dealersTopCard : Card):

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

    if catagory == 'Hard':
        return hardDict[playersHand.getValue()][dealersTopCard.getValnum()]

    if catagory == 'Soft':
        return softDict[playersHand.getValue()-11][dealersTopCard.getValnum()]
    
    if catagory == 'Pair':
        splitAction = pairDict[playersHand.getValue()/2][dealersTopCard.getValnum()]
        if splitAction == 'Split':
            return splitAction
        else:
            return hardDict[playersHand.getValue()][dealersTopCard.getValnum()]

def create_image_placeholders(s:Shoe):
    d_images = [x.get_image_name() for x in s.dealer.getCards()]
    p_images = []
    if len(s.players)==1:
        p_images = [x.get_image_name() for x in s.players[0].getCards()]
    else:
        for p in s.players:
            temp_images = [x.get_image_name() for x in p.getCards()]
            p_images.append(temp_images)
    return d_images, p_images

def decide_actions(s:Shoe):
    actions = ['Hit', 'Stand', 'Double']
    p_cards = s.players[0].getCards()
    if len(p_cards)==2 and p_cards[0].getValnum() == p_cards[1].getValnum():
        actions.append('Split')
    return actions

def correct_hand(s:Shoe, mode:int):
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

@app.route('/')
def home():
    # application defaults to this function
    return render_template('init_game.html', gameModes = [1,2,3,4])

@app.route('/chosen_Mode', methods = ["POST"])
def game_choice():
    global mode 
    global s # the shoe
    # integer representing the game mode
    mode = int(request.form.get('action')) 

    while True:
        s = Shoe() # make a shoe
        s.shuffle() # shuffle it
        s.deal() # deal it
        # if player has blackjack skip iteration since there is nothing for them to do
        if (s.players[0].getValue() == 21):
            continue
        break
    
    if mode in [2, 3, 4]:
        correct_hand(s, mode)
    
    d_images, p_images = create_image_placeholders(s)
    actions = decide_actions(s)

    return render_template('play.html', 
                           dealer_cards = [d_images[0], 'backred'],
                           player_cards = [p_images], actions = actions, 
                           w=WIDTH*scale_factor, h=HEIGHT*scale_factor)

@app.route('/action_result', methods=["POST"])
def action_result():
    user_action = request.form.get('action')
    correct_action = get_correct_play(s.players[0], s.dealer.getCards()[0])

    stats[1]+=1
    if user_action == correct_action:
        result_string = 'That is Correct!'
        stats[0]+=1
    else:
        result_string = f'That is incorrect, the correct action was to {correct_action}.'
    
    d_images, p_images = create_image_placeholders(s)
        
    return render_template('result.html', res_string = result_string,
                           dealer_cards = [d_images[0], 'backred'],
                           player_cards = [p_images], 
                           options = ['New Hand', 'Change Settings', 'Quit'], 
                           w=WIDTH*scale_factor, h=HEIGHT*scale_factor)

@app.route('/next_choice', methods=["POST"])
def next_choice():
    choice = request.form.get('action')
    print(choice)
    if choice == 'Quit':
        return render_template('quit.html', 
                               stats = stats)
    elif choice == 'Change':
        return render_template('init_game.html', gameModes = [1,2,3,4])
    else: # choice == 'New Hand'
        while True:
            global s
            s = Shoe() # make a shoe
            s.shuffle() # shuffle it
            s.deal() # deal it
            # if player has blackjack skip iteration since there is nothing for them to do
            if (s.players[0].getValue() == 21):
                continue
            break
    
        if mode in [2, 3, 4]:
            correct_hand(s, mode)

        d_images, p_images = create_image_placeholders(s)
        actions = decide_actions(s)

        return render_template('play.html', 
                               dealer_cards = [d_images[0], 'backred'],
                               player_cards = [p_images], actions = actions, 
                               w=WIDTH*scale_factor, h=HEIGHT*scale_factor)

if __name__ == '__main__':
    # run the flask app
    global stats 
    stats = [0,0]
    app.run(debug=True)
    # this then goes to the home function
