



class Card:

	def __init__(self, cost):
		self.cost = cost

	def __eq__(self, value):
		return str(self) == str(value)

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
		self.vp = vp

class Estate(Victory):

	def __init__(self):
		super().__init__(2, 1)

	def __str__(self):
		return "Estate"


class Duchy(Victory):

	def __init__(self):
		super().__init__(5, 3)

	def __str__(self):
		return "Duchy"


class Province(Victory):

	def __init__(self):
		super().__init__(8, 6)


	def __str__(self):
		return "Province"


class Curse(Victory):

	def __init__(self):
		super().__init__(0, -1)

	def __str__(self):
		return "Curse"

class Action(Card):

	def __init__(self, cost):
		super().__init__(cost)


class Smithy(Action):

	def __init__(self):

		super().__init__(4)


	def __str__(self):
		return "Smithy"


	def action(self, g, p):
			p.drawN(3)

class Village(Action):

	def __init__(self):

		

		super().__init__(3, action)

	def __str__(self):
		return "Village"

	def action(self, g, p):
			g.actions += 2
			p.draw()


class Woodcutter(Action):

	def __init__(self):

		

		super().__init__(3, action)

	def __str__(self):
		return "Woodcutter"

	def action(self, g, p):
			g.buys += 1 
			g.cash += 2


class CouncilRoom(Action):

	def __init__(self):

		

		super().__init__(4, action)

	def __str__(self):
		return "Council Room"

	def action(self, g, p):
			g.buys += 1 
			p.drawN(3)

			for player in g.players:
				player.draw()


class Festival(Action):

	def __init__(self):

		

		super().__init__(5, action)



	def __str__(self):

		return "Festival"

	def action(self, g, p):
			g.actions += 2
			g.buys += 1 
			g.cash += 2



class Laboratory(Action):

	def __init__(self):

		

		super().__init__(5, action)


	def __str__(self):
		return "Laboratory"

	def action(g, p):
			p.drawN(2)
			g.actions += 1

class Market(Action):

	def __init__(self):



		super().__init__(5, action)

	def __str__(self):
		return "Market"

	def action(self, g, p):
		p.draw()
		p.actions += 1
		g.buys += 1
		g.cash += 1


class Chapel(Action):

	def __init__(self):

		super().__init__(2, action)

	def __str__(self):
		return "Chapel"

	def action(self, g, p):
			for card in p.chapelToTrash():
				p.trash(card)


class Cellar(Action):

	def __init__(self):


		super().__init__(2, action)


	def __str__(self):

		return "Cellar"


	def action(g, p):
			cards = p.cellarToDiscard()

			for card in cards:
				p.discardCard(card)

			p.drawN(len(cards))

			g.actions += 1 
class Chancellor(Action):

	def __init__(self):

		def action(g, p):
			if p.chancellorDiscard():
				p.discard.extend(p.deck)
				p.deck = []

			g.cash += 2

		super().__init__(3, action)

	def __str__(self):
		return "Chancellor"


class Feast(Action):

	def __init__(self):

		def action(g, p):
			card = p.feastToGain()
			if card.cost <= 5:
				g.gain(p, card)
				p.trash(Feast())


		super().__init__(4, action)


	def __str__(self):

		return "Feast"



class Moneylender(Action):

	def __init__(self):

		def action(g, p):
			if p.moneylenderWillTrash() and Copper() in p.hand:
				p.trash(Copper())
				g.cash += 3

		super().__init__(4, action)


	def __str__(self):
		return "Moneylender"



class Remodel(Action):

	def __init__(self):

		def action(g, p):

			card1 = p.remodelToTrash()

			if p.hand:
				#if not p.hand then no go
				card2 = p.remodelToGain(card1.cost + 2)

				if card2.cost <= card1.cost + 2:
					p.trash(card1)
					g.gain(p, card2)




		super().__init__(4, action)


	def __str__(self):
		return "Remodel"



class ThroneRoom(Action):

	def __init__(self):

		def action(g, p):
			card = p.throneRoomCard(g)

			if card and card in p.hand:
				p.inPlay(g, card)
				card.action(g, p)
				card.action(g, p)
		
		super().__init__(5, action)

	def __str__(self):
		return "Throne Room"


class Library(Action):

	def __init__(self):

		def action(g, p):

			droppedAction = []

			while len(p.hand) < 7:
				
				card = deck.pop(0)
				if isinstance(card, Action) and p.librarySetAside(g, card):
					droppedAction.append(card)
				else:
					p.hand.append(card)

			p.discard.extend(droppedAction)


		super().__init__(5, action)


	def __str__(self):

		return "Library"


class Mine(Action):

	def __init__(self):

		def action(g, p):

			trashCard = p.mineTrash(g)
			if trashCard and isinstance(trashCard, Cash):
				gainCard = p.mineGain(g, trashCard.cost + 3)

				if gainCard and isinstance(gainCard, Cash) and gainCard.cost <= trashCard.cost + 3:

					g.gain(p, gainCard)

		super().__init__(5, action)

	def __str__(self):
		return "Mine"


class Attack(Card):

	def __init__(self, *args):
		pass


class Witch(Action, Attack):

	def __init__(self):

		def action(g, p):

			p.drawN(2)

			for player in g.players:
				if player != p:
					g.gain(player, Curse())

		super().__init__(5, action)


	def __str__(self):
		return "Witch"


class Adventurer(Action):

	def __init__(self):

		def action(g, p):

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

		super().__init__(6, action)

	def __str__(self):
		"Adventurer"


class 	



