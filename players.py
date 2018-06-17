

from random import shuffle

from game import *
from cards import *
from utils import *



class Player(object):

	def __init__(self):
		self.hand = []
		self.discard = []

		self.deck = [Copper() for i in range(7)]
		
		self.deck.extend(Estate() for i in range(3))

		shuffle(self.deck)
		self.drawN(5)



	def draw(self):

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
		self.discard.append(card)


	def discardCard(self, card):
		self.hand.remove(card)
		self.discard.append(card)

	def playTreasures(self, g):
		treasures = list(filter(lambda card: isinstance(card, Cash), self.hand))


		for treasure in treasures:
			g.playTreasures(self, treasure)


	def __str__(self):
		string = ""

		string += pilestr("Hand", self.hand)
		string += pilestr("Deck", self.deck)
		string += pilestr("Discard", self.discard)



	

		return string



	def cards(self):
		return flatten([self.deck, self.hand, self.discard])


	def allThe(self, cards):
		clist = []

		for card in cards:
			correct = filter(lambda n: n == card, self.hand)
			clist.extend(correct)

		return clist


	def trash(self, g, card):
		p.hand.remove(card)
		g.trash.append(card)


	def inPlay(self, g, card):
		self.hand.remove(card)
		g.inPlay.append(card)



class BMPlayer(Player):

	def __init__(self):
		super().__init__()

	def buy(self, g):

		d = [(8, Province()), (6, Gold()), (3, Silver())]

		for cost, card in d:

			if cost <= g.cash:
			

				g.buy(self, card)
				


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

	def moneylenderWillTrash(self):

		return Copper() in self.hand

	def remodelToTrash(self):
		if hand:
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



	def onReveal(self, g, card):
		pass


class BMSmithyPlayer(BMPlayer):

	def __init__(self):
		super().__init__()


	def buy(self, g):

		smithycount = len(list(filter(lambda n: n == Smithy(), self.cards())))

		d = [(8, Province()), (6, Gold()), (4, Smithy()), (3, Silver())]

		for cost, card in d:
			if card != Smithy() or smithycount < 1:
				if cost <= g.cash:
			 
					g.buy(self, card)

	def playActions(self, g):

		if g.actions and Smithy() in self.hand:
			g.playActions(self, Smithy())
