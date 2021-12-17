# from time import sleep
# from homework_2.lecture6 import Player, Deck
from abc import ABC, abstractmethod
from random import shuffle
import pandas as pd    



class CardABC(ABC):

    @abstractmethod
    def __repr__(self):
        pass
    
    @abstractmethod
    def value(self):
        pass



class DeckABC(ABC):

    @abstractmethod
    def create_deck(self):
        pass
    
    @abstractmethod
    def shuffle(self, deck):
        pass



class Card(CardABC):

    suits = {"♠", "♦", "♣", "♥"}
    ranks = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"}

    def __init__(self, suit, rank):
        super().__init__()
        self.rank = rank
        self.suit = suit
        self.suits = []
        self.ranks = []
        
    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def value(self):
        return None, None



class FaceCard(Card):

    # ranks = {"J", "Q", "K"}

    def __init__(self, suit, rank):
        super().__init__(suit, rank)
        self.soft = 10
        self.hard = 10
        self.suit = suit
        self.rank = rank
        self.ranks.append(self.rank)
        self.suits.append(self.suit)
    
    def value(self):
        return self.soft, self.hard



class AceCard(Card):

    # ranks = {"A"}

    def __init__(self, suit, rank):
        super().__init__(suit, rank)
        self.soft = 1
        self.hard = 11
        self.suit = suit
        self.rank = rank
        self.ranks.append(self.rank)
        self.suits.append(self.suit)

    def value(self):
        return self.soft, self.hard



class NumCard(Card):

    # ranks = {"2", "3", "4", "5", "6", "7", "8", "9", "10"}

    def __init__(self, suit, rank):
        super().__init__(suit, rank)
        self.hard = int(self.rank)
        self.soft = int(self.rank)
        self.suit = suit
        self.rank = rank
        self.ranks.append(self.rank)
        self.suits.append(self.suit)

    def value(self):
        return self.soft, self.hard



class Deck(DeckABC):
    def __init__(self):
        super().__init__()
        self.deck = []
        self.create_deck()
        self.shuffle(deck=self.deck)

    def __len__(self):
        return len(self.deck)

    def deal(self):
        return self.deck.pop()

    def create_deck(self):
        suits = {"♠", "♦", "♣", "♥"}
        
        for suit in suits:
            for rank in range(2, 11):
                numCard = NumCard(suit, str(rank))
                self.deck.append((str(rank), suit, numCard))
            for rank in {"J", "Q", "K"}:
                faceCard = FaceCard(suit, rank)
                self.deck.append((rank, suit, faceCard))
            aceCard = AceCard(suit, "A")
            self.deck.append(("A", suit, aceCard))

    @staticmethod
    def shuffle(deck):
        shuffle(deck)



class Player(object):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.hand = []
        self.win = None
        self.soft = None
        self.hard = None
    
    def __repr__(self):
        representation = self.name + ":  |  "
        for card in self.hand:
            representation += card[2].__repr__() + "  |  "
        return representation



class Game(object):
    def __init__(self, deck):
        super().__init__()
        self.deck = deck
        self.dealer = Player("Dealer")
        self.user = Player("Player")
        self.result_user = 0
        self.result_dealer = 0


    def initial_deal(self):
        for i in range(2):
            self.dealer.hand.append(self.deck.pop())
            self.user.hand.append(self.deck.pop())
        self.dealer.soft, self.dealer.hard = self.check_hand(self.dealer.hand)
        self.user.soft, self.user.hard = self.check_hand(self.user.hand)

    def check_hand(self, hand):
        soft_sum = 0
        hard_sum = 0
        for h in hand:
            values = h[2].value()
            soft_sum += values[0]
            hard_sum += values[1]
        return [soft_sum, hard_sum]

    def ask_user(self, parametre):
        if self.user.soft <= parametre:
            self.user.hand.append(self.deck.pop())
            self.user.soft, self.user.hard = self.check_hand(self.user.hand)
            self.ask_user(parametre=parametre)
        else:
            if self.user.soft > 21:
                self.result_user = self.user.soft
            else:
                self.result_user = self.user.soft if self.user.hard > 21 else max(self.user.soft, self.user.hard)
                

    def ask_dealer(self):
        if self.dealer.soft <= 16:
            self.dealer.hand.append(self.deck.pop())
            self.dealer.soft, self.dealer.hard = self.check_hand(self.dealer.hand)
            self.ask_dealer()
        else:
            if self.dealer.soft > 21:
                self.result_dealer = self.dealer.soft
            else:
                self.result_dealer = self.dealer.soft if self.dealer.hard > 21 else max(self.dealer.soft, self.dealer.hard)
        


def simulate(parameter):
        dec = Deck()
        game = Game(dec.deck)
        game.initial_deal()
        game.ask_user(parameter=parameter)
        game.ask_dealer()
        
        if game.result_user > 21:
            return 3
        elif game.result_user < 21 and game.result_dealer > 21:
            return 2
        else:
            if game.result_user < game.result_dealer:
                return 1
            else:
                return 0

def main():
    result_dict = {}
    for i in range(1, 21):
        result = simulate(parametre=i)
        result_dict[i] = result
    
if __name__ == "__main__":
    main()
