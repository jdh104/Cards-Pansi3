#!/usr/bin/env python3
    # indent size

from random import choice, randrange
from enum import Enum
from pansi import pfstr, printf

__author__ = "Jonah Haney"
__version__ = "2018.5.12"
__all__ = ["Rank", "Suit", "Card", "Packet", "Deck"]

class Rank(Enum):
	PREMIUM = "Premium Card"
	ACE = "Ace"
	TWO = "Deuce"
	THREE = "Trey"
	FOUR = "Four"
	FIVE = "Five"
	SIX = "Six"
	SEVEN = "Seven"
	EIGHT = "Eight"
	NINE = "Nine"
	TEN = "Ten"
	JACK = "Jack"
	QUEEN = "Queen"
	KING = "King"
	LJOKER = "Low Joker"
	HJOKER = "High Joker"

class Suit(Enum):
	SUITLESS = ""
	SPADE = "Spade"
	DIAMOND = "Diamond"
	CLUB = "Club"
	HEART = "Heart"

class const(Enum):
	FRENCH_RANKS = [Rank.ACE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING]
	FACE_RANKS = [Rank.JACK, Rank.QUEEN, Rank.KING]
	ROYAL_RANKS = [Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE]
	NUM_RANKS = [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN]
	FRENCH_SUITS = [Suit.SPADE, Suit.DIAMOND, Suit.CLUB, Suit.HEART]
	RED_SUITS = [Suit.HEART, Suit.DIAMOND]
	BLACK_SUITS = [Suit.SPADE, Suit.CLUB]

def copy(obj):
	try:
		return obj.__copy__()
	except:
		raise TypeError("copy was passed a non-copiable object")

class Card:
	def __init__(self, rank=None, suit=None, fromrankset=const.FRENCH_RANKS.value, fromsuitset=const.FRENCH_SUITS.value):
		if rank == None: 
			try:
				self.rank = choice(fromrankset)
				if not isinstance(self.rank, Rank):
					raise Exception()
			except:
				raise TypeError("`fromrankset` must be a set of Rank enums.")
		else:
			if isinstance(rank, Rank):
				self.rank = rank
			else:
				try:
					self.rank = list(Rank)[int(rank)]
				except:
					raise TypeError("Card rank must be a valid Rank enum, or a valid numeric ID (0-15).")
		if self.rank == Rank.LJOKER or self.rank == Rank.HJOKER or self.rank == Rank.PREMIUM:
			self.suit = Suit.SUITLESS
		elif suit == None:
			try:
				self.suit = choice(fromsuitset)
				if not isinstance(self.suit, Suit):
					raise Exception()
			except:
				raise TypeError("`fromsuitset` must be a set of Suit enums.")
		else:
			if isinstance(suit, Suit):
				self.suit = suit
			else:
				try:
					self.suit = list(Rank)[int(rank)]
				except:
					raise TypeError("Card suit must be a valid Suit enum, or a valid numeric ID (0-4).")
	
	def __copy__(self):
		return Card(rank=self.rank, suit=self.suit)

	def __pfstr__(self):
		if self.suit == None:
			return "{BOLD}" + self.rank.value + "{RSET_STYLE}"
		elif self.suit == Suit.HEART:
			return "{BOLD}{FCLR,250,10,10}" + self.rank.value + "{RSET_STYLE} of Hearts"
		elif self.suit == Suit.DIAMOND:
			return "{BOLD}{FCLR,250,250,50}" + self.rank.value + "{RSET_STYLE} of Diamonds"
		elif self.suit == Suit.SPADE:
			return "{BOLD}{FCLR,10,10,250}" + self.rank.value + "{RSET_STYLE} of Spades"
		elif self.suit == Suit.CLUB:
			return "{BOLD}{FCLR,10,250,10}" + self.rank.value + "{RSET_STYLE} of Clubs"
		else:
			return str(self)  # patch potential extension holes 

	def __str__(self):
		if self.suit == None:	
			return self.rank.value
		else:
			return self.rank.value + " of " + self.suit.value + "s"

class Packet:
	def __init__(self):
		self.cards = []

	def __copy__(self):
		p = Packet()
		for c in self.cards:
			p.append(copy(c))
		return p

	def __pfstr__(self):
		f = ""
		for i in range(len(self.cards)):
			f += pfstr(self.cards[i])
			if i+1 != len(self.cards):
				f += "\n"
		return f

	def __len__(self):
		return len(self.cards)

	def __str__(self):
		s = ""
		for i in range(len(self.cards)):
			s += str(self.cards[i])
			if i+1 != len(self.cards):
				s += "\n"
		return s

	def append(self, newcard):
		if not isinstance(newcard, Card):
			raise TypeError("`newcard` must be an instance of Card.")
		else:
			self.cards.append(newcard)
	
	def cut(self, index=None):
		if not index:
			if len(self.cards) > 1:
				index = len(self.cards) // 2
			else:
				raise ValueError("Cannot cut a packet with 1 or 0 cards.")
		elif index >= len(self.cards):
			raise ValueError("Not enough cards to cut at index of " + str(index) + "\n\tonly have " + str(len(self.cards)) + " cards in packet.")
		p = Packet()
		for c in self.cards[-index:]:
			p.append(c)
		self.cards = self.cards[:-index]
		return p

	def extend(self, packet):
		if not isinstance(packet, Packet):
			raise TypeError("`packet` must be an instance of Packet.")
		else:
			self.cards.extend(packet.cards)

	def get(self, index):
		try:
			return self.cards[index]
		except ValueError as err:
			raise err

	def insert(self, index, newcard):
		if not isinstance(newcard, Card):
			raise TypeError("`newcard` must be an instance of Card.")
		elif index >= len(self) or index < 0:
			raise ValueError("index out of bounds.")
		else:
			try:
				self.cards.insert(index, newcard)
			except:
				raise TypeError("`index` must be an integer.")
	
	def join(self, packet):
		if not isinstance(packet, Packet):
			raise TypeError("`packet` must be an instance of Packet.")
		else:
			self.cards.extend(packet.cards)
			packet.cards = []

	def remove(self, card):
		if not isinstance(card, Card):
			raise TypeError("`card` must be an instance of Card.")
		else:
			try:
				self.cards.remove(card)
			except ValueError as err:
				raise err

class Deck:
	def __init__(self, suitset=const.FRENCH_SUITS, rankset=const.FRENCH_RANKS, copies=1, empty=False, cardlist=None):
		if copies < 1:
			raise ValueError("`copies` must be a non-zero positive integer.")
		elif empty:
			self.packets = []
		else:
			self.packets = [Packet() for _ in range(copies)]
			for p in self.packets:
				if cardlist:
					for c in cardlist:
						if isinstance(c, Card):
							p.append(c)
						else:
							raise TypeError("`cardlist` must be a list of cards (c'mon now).")
				else:
					for s in suitset.value:
						for r in rankset.value:
							p.append(Card(rank=r, suit=s))

	def __copy__(self):
		d = Deck(empty=True)
		for p in self.packets:
			d.append(copy(p))
		return d

	def __pfstr__(self):
		f = ""
		for i in range(len(self.packets)):
			f += pfstr(self.packets[i])
			if i+1 < len(self.packets):
				f += "\n{BOLD}-----------------{RSET_STYLE}\n"
		return f
				
	def __len__(self):
		l = 0
		for p in self.packets:
			l += len(p)
		return l

	def __str__(self):
		s = ""
		for i in range(len(self.packets)):
			s += str(self.packets[i])
			if i+1 < len(self.packets):
				s += "\n-----------------\n"
		return s

	def append(self, newpacket):
		if not isinstance(newpacket, Packet):
			raise TypeError("`newpacket` must be an instance of Packet.")
		else:
			self.packets.append(newpacket)
		return self

	def copy(self):
		return

	def cut(self, index=None):
		"""Cut the top-most packet in two, at `index` and append the new packet to `self.packets`"""
		self.packets.append(self.packets[len(self.packets)-1].cut(index))
		return self

	def extend(self, newdeck):
		if not isinstance(newdeck, Deck):
			raise TypeError("`newdeck` must be an instance of Deck.")
		else:
			for p in copy(newdeck).packets:
				self.packets.append(p)
		return self

	def join_all(self):
		for p in self.packets[1:]:
			self.packets[0].join(p)
			self.packets.remove(p)
		return self

	def pharo(self):
		return self.riffle(maxclump=1)
		
	def riffle(self, maxclump=2):
		if maxclump < 1:
			raise ValueError("Clumping constraint must be a positive integer.\n\tmaxclump: " + str(maxclump))
		elif len(self.packets) > 2:
			raise RuntimeError("Deck must be joined (or in exactly two packets) to riffle")
		else:
			if len(self.packets) == 1:
				self.cut()

			# Begin riffle algorithm here
			marker, r = 0, 1
			for c in range(len(self.packets[1].cards)):
				try:
					self.packets[0].insert(marker, self.packets[1].get(c))
				except ValueError:
					self.packets[0].cards.extend(self.packets[1].cards[c:])
					del self.packets[1]
					return self
				if r == 1:
					r = randrange(1, maxclump+1) * choice([1,-1])
					if r < 0:
						marker -= r - 1
						r = 1
					else:
						marker += 2
				else:
					r -= 1
					marker += 1
			del self.packets[1]
			return self

def test():
	d = Deck()
	d.extend(Deck(cardlist=[Card() for _ in range(52)]))
	d.pharo().riffle(maxclump=6).riffle(maxclump=4).riffle()
	printf(d)
