

from random import shuffle

from game import *
from cards import *
from utils import *

#TODO: 21
#Safeguard? How much energy do you even spend against "illegal" Player classes?
#Sim them

class Player(object):

    def __init__(self):

        # should be moved into game 
        self.hand = []
        self.discard = []

        # tempting to make init cards into args 
        # but nah

        self.deck = [Copper() for i in range(7)]
        
        self.deck.extend(Estate() for i in range(3))

        # otherwise always a 5-2 split
        shuffle(self.deck)
        self.drawN(5)

        self.name = "Player"

    def draw(self):

        # if there is no deck, shuffle discard, becomes deck
        # if there is no discard and there is no deck, no change in state

        if not self.deck:
            self.deck = self.discard[:]
            self.discard = []
            shuffle(self.deck)

        if self.deck:
            self.hand.append(self.deck.pop(0))

    def drawN(self, n):
        if n <= 0:
            return None
        else:
            self.draw()
            self.drawN(n-1)

    def gain(self, card):
        # Do I keep this?
        # Pro: Abstraction, if I need to change this
        # Con: API isn't total

        self.discard.append(card)


    def discardCard(self, card):
        # tempted to make a util method
        # filter and replace
        # on xs ys p n
        # find the first n zs in xs such that p, remove them from xs, and insert them into ys
        self.hand.remove(card)
        self.discard.append(card)

    def playTreasures(self, g):
        # why is filter lazy
        # when everything else is strict
        treasures = list(filter(lambda card: isinstance(card, Cash), self.hand))
        for treasure in treasures:
            g.verifyPlayTreasures(self, treasure)

    def __str__(self):
        string = ""

        string += pilestr("Hand", self.hand)
        string += pilestr("Deck", self.deck)
        string += pilestr("Discard", self.discard)

        return string

    def cards(self):
        # would do 
        # return self.deck.extend(self.hand).extend(self.discard)
        # but this is mutable :c
        return flatten([self.deck, self.hand, self.discard])


    def allThe(self, cards):
        clist = []
        for card in cards:
            correct = filter(lambda n: n == card, self.hand)
            clist.extend(correct)
        return clist


    def trash(self, g, card):
        # see discardCard
        p.hand.remove(card)
        g.trash.append(card)


    def inPlay(self, g, card):
        # see discardCard
        self.hand.remove(card)
        g.inPlay.append(card)

class BMPlayer(Player):
    # Just a tester

    def __init__(self, name = None):
        super().__init__()
        if name: 
            self.name = name 
        else: 
            self.name = "BMPlayer"

    def buy(self, g):
        d = [(8, Province()), (6, Gold()), (3, Silver())]
        for cost, card in d:
            if cost <= g.cash:
                g.verifyBuy(self, card)
                
    def playActions(self, g):
        pass

    def chapelToTrash(self):
        return self.allThe([Estate(), Curse()])

    def cellarToDiscard(self):
        return self.allThe([Estate(), Curse(), Copper()])

    def chancellorDiscard(self):
        return True

    def feastToGain(self):
        return Duchy()

    def remodelToTrash(self):
        if self.hand:
            cheapest = self.hand[0]
            for card in self.hand:
                if card.cost < cheapest.cost :
                    cheapest = card 

            return cheapest

    def remodelToGain(self, cost):
        if cost >= 3:
            return Silver()
        return Copper()

    def throneRoomCard(self, g):
        card = input()
        return eval(card)

    def librarySetAside(self, g, card):
        return True



class BMSmithyPlayer(BMPlayer):
    def __init__(self, name = None):
        super().__init__()
        if name: 
            self.name = name
        else: 
            self.name = "BMSmithyplayer"

    def buy(self, g):
        smithycount = len(list(filter(lambda n: n == Smithy(), self.cards())))
        d = [(8, Province()), (6, Gold()), (4, Smithy()), (3, Silver())]
        for cost, card in d:
            if card != Smithy() or smithycount < 1:
                if cost <= g.cash:
                    g.verifyBuy(self, card)

    def playActions(self, g):
        if g.actions and Smithy() in self.hand:
            g.verifyPlayActions(self, Smithy())
