# Class to represent a card
import random as rand
from copy import deepcopy


class Card:
  mapping = {
    0: "Spade",
    1: "Diamond", 
    2: "Heart", 
    3: "Club",
    11: "Jack", 
    12: "Queen", 
    13: "King", 
    14: "Ace" }
  
  def __init__(self, suit, rank):
    # Spade, Diamond, Heart, Club
    self.suit = suit
    # 2 - 10, 11 (J), 12 (Q), 13 (K), 14 (A)
    self.rank = rank
  
  def __eq__(self, other):
    return self.suit == other.suit and self.rank == other.rank
  
  def __gt__(self, other):
    return self.rank > other.rank

  def __repr__(self):
    return f"{self.mapping[self.rank] if self.rank > 10 else self.rank} of {self.mapping[self.suit]}"

class Deck:
  def __init__(self, cards=None):
    self.cards = []
    if cards:
      self.cards = cards
  
  def shuffle(self):
    rand.shuffle(self.cards)
    
  
  def deal(self):
    return self.cards.pop()
  
  def add(self, card):
    self.cards.append(card)

  def __repr__(self):
    return str(self.cards)
  
  __str__ = __repr__

class State:
  def __init__(self, cards=None):
    # Current stage:
    #   0 is p1 action
    #   1 is p2 action
    #   2 is p1 action upon p2 bet
    self.stage = 0
    
    # if theres an active bet
    self.active_bet = False
    self.pot = 2

    # List of actions so far
    self.action_list = []





class Game:
  def __init__(self, action=None):
    pass

  def start(self):
    # Shuffle and deal
    self.deck = Deck([Card(0, i) for i in (12, 13, 14)])
    rand.shuffle(self.deck)

    p1_card = self.deck.deal()
    p2_card = self.deck.deal()
    
    self.state = State(cards=(p1_card, p2_card))


  def utility(self):
    return self.pot * 3
    # positive is the amount p1 wins, negative is the amount p2 wins
    pass

  def actions(self):
    if self.turn == 0:
      for action in ['X', 'B']:
        return 

    if self.turn == 1:
      pass




if __name__ == '__main__':
  card = [Card(0, i) for i in (12, 13, 14)]

  print(card[1] < card[0])
  print(card[1] > card[0])
  print(card[1] == card[0])  
  


