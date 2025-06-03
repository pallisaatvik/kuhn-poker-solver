# Class to represent a card
import random as rand
from copy import deepcopy

class Printer:
  def __init__(self, obj):
    self.target = obj
  def print_game():
    pass

class Card:
  CARD_VALUE = {
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
  def __init__(self, mode='kuhn'):
    self.cards = []
    if mode == 'kuhn':
      self.cards = [Card(0, i) for i in (11, 12, 13)]
    
    if mode == 'holdem':
      for suit in range(0, 4):
        for rank in range(2, 15):
          self.cards.append(Card(suit, rank))
    
    self.shuffle()

  def shuffle(self):
    rand.shuffle(self.cards)
    
  def deal(self):
    return self.cards.pop()
  
  def add(self, card):
    self.cards.append(card)

  def __repr__(self):
    return str(self.cards)
  
  __str__ = __repr__

class Player:
  def __init__(self, name, stack = 10):
    self.stack = stack
    self.cards = []
    self.name = name

  def get_stack(self):
    return self.stack

  def show_cards(self):
    return self.card

  def get_cards(self, cards):
    self.cards = cards

  def muck_cards(self):
    self.cards = []

  def ante(self, amount):
    self.stack -= amount
    self.validate_stack(amount)
  bet = ante

  def add_money(self, amount):
    self.stack += amount
  
  def validate_stack(self, amount):
    if self.stack < 0:
      raise Exception(f"Insufficient Money in Stack. Amt={self.stack}, req={amount}")


class StateAction:
  def __init__(self, game, player, action, state, amount=None):
    self.prev_state = None
    self.amount = amount
    self.player = Player

    match action:
      case 'A' | 'B' | 'C':
        player.ante(self.amount)
        game.add_to_pot(self.amount)
      case 'F':
        pass
      case 'X':
        pass

    if state:
      self.prev_state = state


class NullState:
  def __init__(self):
    pass

class KuhnPokerGame:
# TODO track folded players
  def __init__(self, stacks):
    #  In normal poker, small blind is [0], and button is [-1]
    self.players =  [Player(stack) for stack in stacks]
    self.in_hand =  {player: True for player in self.players}

    self.raise_amount = 0
    self.pot = 0
    self.last_state = NullState()
    self.rounds = [self.preflop, self.postflop]

  def play_hand(self):
    self.deck = Deck(mode='kuhn')

    for player in self.players:
      player.get_cards([self.deck.deal()]) 
    
    for game_round in self.rounds:
      game_round()

      # Check if only 1 player in hand
      if sum(self.in_hand.values()) == 1:
        self.end_hand()
        return

    self.showdown()
    self.end_hand()

  # Marks players as not in_hand if they have worse cards 
  # TODO make this scaleable
  def showdown(self):
    if self.players[0].show_cards()[0] > self.players[1].show_cards()[0]:
      self.in_hand[self.players[1]] = False
    if self.players[0].show_cards()[0] < self.players[1].show_cards()[0]:
      self.in_hand[self.players[0]] = False

  def end_hand(self):
    all_players = list(self.in_hand)
    true_players = []
    for player, state in all_players:
      player.muck_cards()
      if state:
        true_players.append(player)

    winnings = self.pot / len(true_players)
    
    for player in true_players:
      player.add_money(winnings)

  def preflop(self):
    for player in self.players:
      self.last_state = StateAction(self, player, 'A', self.last_state, 1)

  def postflop(self):
    for player in self.players:
      action = self.query_action()
      if len(action) == 2:
        self.raise_amount = action[1]
        self.last_state = StateAction(self, player, action[0], self.last_state, action[1])
      elif action == 'C':
        self.last_state = StateAction(self, player, action[0], self.last_state, self.raise_amount)
      else:
        self.last_state = StateAction(self, player, action, self.last_state)

  def query_action(self):
    action = input("Action: ")
    if action != 'B':
      return action
    print("Betting 1, because kuhn")
    return (action, 1)

  def add_to_pot(self, amount):
    self.pot += amount


if __name__ == '__main__':
  game = KuhnPokerGame(stacks=[10, 10])
  game.play_hand()  
  game.print_last_hand()



