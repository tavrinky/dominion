
# TODO: Extend logging, verification

from ipdb import *
from players import *
from utils import *
from cards import *
from logger import *

class Game(object):

    def __init__(self, players):

        self.turn = 0 
        self.players = players

        self.actions = 0
        self.buys = 1
        self.cash = 0
        self.piles = []

        for card in [Copper(), Silver(), Gold(), Estate(), Duchy(), Province(), Smithy()]:
            self.piles.append(self.howManySetup(card) * [card])

        #tempted to make a more full fledged logger
        #should be able to reconstruct the game from the log
        self.log = Logger()
        self.trash = []
        self.inPlay = []

    def verifyBuy(self, p, card):
        self.log.add("\n\n" + self.playerName() + " attempted to buy a " + str(card))
        self.log.add("\nCurrent cash is " + str(self.cash))
        self.log.add("\nCard cost is " + str(card.cost))

        if self.isPile(card) and self.buys > 0 and card.cost <= self.cash:
            self.gain(p, card)
            self.log.add("\n" + self.playerName() + " successfully bought a " + str(card))

    def verifyPlayTreasures(self, p, card):
        if card in p.hand and isinstance(card, Cash):
            p.inPlay(self, card)
            self.cash += card.cash


    def veriyPlayActions(self, p, card):
        self.log.addMany(p.name, " is attempting to play", )
        if self.actions > 0 and isinstance(card, Action) and card in p.hand:
            p.inPlay(self, card)
            self.actions -= 1 
            card.action(self, p)

    def stepTurn(self):
        self.log.addMany("Beginning turn: ", self.turn, ": \n")
        self.actions = 0
        self.buys = 1
        self.cash = 0

        p = self.players[self.turn%len(self.players)]

        self.log.addMany("It is ", p.name, "'s turn\n")
        
        p.playActions(self)
        p.playTreasures(self)
        p.buy(self)
    
        self.endTurn(p)

        self.turn += 1

    def endTurn(self, p):
        p.discard.extend(self.inPlay)
        self.inPlay = []
        for card in p.hand:
            p.discardCard(card)
        p.drawN(5)

    def play(self):
        if not self.isWon():
            self.stepTurn()
            self.play()
        else:
            self.log.add("\nTHE GAME HAS BEEN WON")

    def isWon(self):
        existsProvincePile = False
        emptyPiles = 0
        for pile in self.piles:
            if pile:
                if isinstance(pile[0], Province):
                    existsProvincePile = True 
            else:
                emptyPiles += 1
        return (not existsProvincePile) or emptyPiles >= 3

    def isPile(self, card): 
        for pile in self.piles: 
            if card in pile: 
                return True 
        return False
        
    def howManySetup(self, card):
        numVictories = 8 if len(self.players) == 2 else 12

        d = { "Copper" : 60-7*len(self.players), 
        "Silver" : 40,
        "Gold" : 30,
        "Estate" : numVictories,
        "Duchy" : numVictories,
        "Province" : numVictories,
        "Smithy" : 10
        }
        return d[str(card)]

    def playerName(self):
        return "Player " + str(self.turn%len(self.players) + 1)

    def displayVP(self):
        for i in range(len(self.players)):
            string = "Player " 
            string += str(i + 1) 
            string += ": "

            vp = 0
            for card in self.players[i].cards():
                if isinstance(card, Victory):
                    vp += card.vp(self)

            string += str(vp)

            string += "\n"


            self.log.add(string)




    def howManyCards(self, player, card):
        inHand = len(list(filter(lambda c: c == card, player.hand)))
        inDeck = len(list(filter(lambda c: c == card, player.deck)))
        inDiscard = len(list(filter(lambda c: c == card, player.discard)))

        return inHand + inDeck + inDiscard


    def gain(self, p, card):
        for pile in self.piles:
            if pile and pile[0] == card:
                p.gain(pile.pop(0))
        
    def __str__(self):

        string = ""

        string += "Turn number "
        string += str(self.turn)
        string += "\n"

        string += "Players: \n"

        for p in self.players:
            string += str(p)

        string += "Actions: "
        string += str(self.actions)
        string += "\n"

        string += "Buys: "
        string += str(self.buys)
        string += "\n"

        string += "Cash: "
        string += str(self.cash)
        string += "\n"


        string += "Piles: \n"

        for pile in self.piles:
            if pile:
                string += pilestr(str(pile[0]), pile)

        return string 

    def devPlay(self, p, card):

        p.hand.append(card) 
        self.actions += 1

        self.playActions(p, card)

    def reveal(self, card):

        for player in self.players:
            player.onReveal(g, card)
            








