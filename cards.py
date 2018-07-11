


class Card:

	def __init__(self, cost):
		self.cost = cost


	# permits nonsense like Copper() == Copper()
	# as opposed to having to do isinstance(Copper(), type(Copper()))

	# common use case:

	# for pile in piles:
	#		if pile and pile[0] == card:
	#			p.gain(pile.pop(0))

	# as opposed to 
	# if pile and isinstance(pile[0], type(card))


	def __eq__(self, value):
		return str(self) == str(value)


# metaprogramming this seems easy but low EV

class Cash(Card):

	def __init__(self, cost, cash):
		super().__init__(cost)
		self.cash = cash 

class Copper(Cash):

	def __init__(self):
		super().__init__(0, 1)


	def __str__(self):
		return "Copper"

class Silver(Cash):

	def __init__(self):
		super().__init__(3, 2)

	def __str__(self):
		return "Silver"

class Gold(Cash):

	def __init__(self):
		super().__init__(6, 3)

	def __str__(self):
		return "Gold"

class Victory(Card):

	def __init__(self, cost, vp):
		super().__init__(cost)

		#vp is a function of the gamestate (because Garden)
		#could move VP outside because duck typing?

		self.vp = vp

class Estate(Victory):

	def __init__(self):
		super().__init__(2, lambda g: 1)

	def __str__(self):
		return "Estate"

class Duchy(Victory):

	def __init__(self):
		super().__init__(5, lambda g: 3)

	def __str__(self):
		return "Duchy"

class Province(Victory):

	def __init__(self):
		super().__init__(8, lambda g: 	6)


	def __str__(self):
		return "Province"

class Curse(Victory):

	def __init__(self):
		super().__init__(0, lambda: -1)

	def __str__(self):
		return "Curse"

class Action(Card):

	def __init__(self, cost):

		# originally was self.action = action
		# but instead now relying on duck typing
		# because multiple inheritance is a fuck

		super().__init__(cost)

# could DSL the simple actions
# ie village.action = "+2 actions +1 draw"
# that sounds like fun but not incredibly useful
# except for code clutter

class Smithy(Action):

	def __init__(self):
		super().__init__(4)

	def __str__(self):
		return "Smithy"

	def action(self, g, p):
			p.drawN(3)

class Village(Action):

	def __init__(self):
		super().__init__(3)

	def __str__(self):
		return "Village"

	def action(self, g, p):
			g.actions += 2
			p.draw()

class Woodcutter(Action):

	def __init__(self):
		super().__init__(3)

	def __str__(self):
		return "Woodcutter"

	def action(self, g, p):
			g.buys += 1 
			g.cash += 2

class CouncilRoom(Action):

	def __init__(self):
		super().__init__(4)

	def __str__(self):
		return "Council Room"

	def action(self, g, p):
			g.buys += 1 
			p.drawN(3)

			# gets around "every other player" by reading it 
			# as "+3 cards, every player draws 1"
			for player in g.players:
				player.draw()

class Festival(Action):

	def __init__(self):
		super().__init__(5)

	def __str__(self):
		return "Festival"

	def action(self, g, p):
			g.actions += 2
			g.buys += 1 
			g.cash += 2

class Laboratory(Action):

	def __init__(self):
		super().__init__(5)

	def __str__(self):
		return "Laboratory"

	def action(g, p):
			p.drawN(2)
			g.actions += 1

class Market(Action):

	def __init__(self):
		super().__init__(5)

	def __str__(self):
		return "Market"

	def action(self, g, p):
		p.draw()
		p.actions += 1
		g.buys += 1
		g.cash += 1

class Chapel(Action):

	def __init__(self):
		super().__init__(2)

	def __str__(self):
		return "Chapel"

	def action(self, g, p):
		for card in p.chapelToTrash():
			p.trash(g, card)

class Cellar(Action):

	def __init__(self):
		super().__init__(2)

	def __str__(self):
		return "Cellar"

	def action(self, g, p):
		# need to know the length for later
		cards = p.cellarToDiscard()

		for card in cards:
			p.discardCard(card)
		p.drawN(len(cards))

		g.actions += 1 

class Chancellor(Action):

	def __init__(self):
		super().__init__(3)

	def __str__(self):
		return "Chancellor"

	def action(self, g, p):
		if p.chancellorDiscard():
			# could make a seperate player method for this
			# but a p.DeckToDiscard seems unnecessary
			# and p.XToY is too general	

			p.discard.extend(p.deck)
			p.deck = []

		g.cash += 2

class Feast(Action):

	def __init__(self):
		super().__init__(4)

	def __str__(self):
		return "Feast"

	def action(self, g, p):
		# card is non-null because Feast is not optional
		# after the action is played
		card = p.feastToGain()
		if card.cost <= 5:
			g.gain(p, card)
			p.trash(Feast())

class Moneylender(Action):

	def __init__(self):
		super().__init__(4)

	def __str__(self):
		return "Moneylender"

	def action(self, g, p):
		# non optional
		if Copper in p.hand:
			p.trash(Copper())
			g.cash += 3

class Remodel(Action):
	def __init__(self):
		super().__init__(4)

	def __str__(self):
		return "Remodel"

	def action(self, g, p):
		# nullity of card1 is nullity of p.hand because not optional 
		card1 = p.remodelToTrash()
		if p.hand:
			#if not p.hand then no go
			card2 = p.remodelToGain(card1.cost + 2)

			# verifying that player didn't fuck up
			# should add in an error here? or extend verification?
			if card2.cost <= card1.cost + 2:
				p.trash(g, card1)
				g.gain(p, card2)

class ThroneRoom(Action):

	def __init__(self):
		super().__init__(5)

	def __str__(self):
		return "Throne Room"

	def action(self, g, p):
		card = p.throneRoomCard(g)

		# if there exists an action in 
		if list(filter(lambda x: isinstance(x, Action), p.hand)):
			p.inPlay(g, card)
			card.action(g, p)
	

			card.action(g, p)
class Library(Action):

	def __init__(self):



		super().__init__(5, action)


	def __str__(self):

		return "Library"


	def action(self, g, p):

		droppedAction = []

		while len(p.hand) < 7:
				
			card = deck.pop(0)
			if isinstance(card, Action) and p.librarySetAside(g, card):
				droppedAction.append(card)
			else:
				p.hand.append(card)
		p.discard.extend(droppedAction)


class Mine(Action):

	def __init__(self):



		super().__init__(5, action)

	def __str__(self):
		return "Mine"

	def action(self, g, p):

		trashCard = p.mineTrash(g)
		if trashCard and isinstance(trashCard, Cash):
			gainCard = p.mineGain(g, trashCard.cost + 3)

			if gainCard and isinstance(gainCard, Cash) and gainCard.cost <= trashCard.cost + 3:

				g.gain(p, gainCard)


class Attack(Card):

	def __init__(self, *args):
		pass


class Witch(Action, Attack):

	def __init__(self):



		super().__init__(5, action)


	def __str__(self):
		return "Witch"


	def action(self, g, p):

		p.drawN(2)

		for player in g.players:
			if player != p:
				g.gain(player, Curse())

class Adventurer(Action):

	def __init__(self):

		
		super().__init__(6, action)

	def __str__(self):
		"Adventurer"


	def action(self, g, p):

		revealedNonCash = []
		cashRevealed = 0

		while cashRevealed < 2:
			revealCard = p.deck.pop(0)

			g.reveal(revealCard)

			if isinstance(revealCard, Cash):
				p.hand.append(revealCard)
				cashRevealed += 1
			else:
				revealedNonCash.append(revealCard)

		p.discard.extend(revealedNonCash)



