from abc import ABC, abstractmethod
from random import shuffle
from time import sleep



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

        if suit in self.__class__.suits:
            self.suit = suit
        else:
            raise LookupError("Suit not found")

        if rank in self.__class__.ranks:
            self.rank = rank
        else:
            raise LookupError("Card initiation failed: check the card rank")
        self.soft, self.hard = self.value()
        
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
        self.number_of_players = 1
        self.dealer = Player("Dealer")
        self.max_players = 5
        self.users = []

    def add_player(self):
        if self.number_of_players < self.max_players:
            ask_player = input("Do you want to add a player(y/n): ")
            if ask_player == "y":
                player = Player(input("Please enter the player's name: "))
                self.users.append(player)
                print(f'{player.name} added!')
                self.number_of_players += 1
                Game.add_player(self)
            elif ask_player == "n":
                pass
            else:
                print("Please enter 'y' or 'n'.")
                Game.add_player(self)
        else:
            print("You reached maximum number of players!")
        if self.number_of_players == 1:
            print("No player joined the game.")
                

    def initial_deal(self):
        print("\n__________________________")
        print("Starting the game.")
        sleep(1)

        for i in range(2):
            self.dealer.hand.append(self.deck.deal())
            self.dealer.soft, self.dealer.hard = self.check_hand(self.dealer.hand)
            for user in self.users:
                user.hand.append(self.deck.deal())
                user.soft, user.hard = self.check_hand(user.hand)

    def show_status(self):
        print(f'{self.dealer.name}:  |  {str(self.dealer.hand[0][0])} of {str(self.dealer.hand[0][1])}  |  <card hidden>  |')
        for user in self.users:
            print(user.__repr__())

    def check_hand(self, hand):
        soft_sum = 0
        hard_sum = 0
        for h in hand:
            values = h[2].value()
            soft_sum += values[0]
            hard_sum += values[1]
        return [soft_sum, hard_sum]

    def ask_user(self, user: Player):
        user.__repr__()
        if user.soft == user.hard:
            print(f'Your total is {user.soft}')
        else:
            print(f'Your sums are - soft: {user.soft}, hard: {user.hard}')

        if user.soft == 21 or user.hard == 21:
            user.win = 1
            print("Blackjack!!! You won. \n")
            return None
        elif user.soft > 21 and user.hard > 21:
            user.win = 0
            print("You bust((( \n")
            return None
        elif user.soft < 21 or user.hard < 21:
            ask_player = input("Do you want another card(y/n): ")
            if  ask_player == "y":
                user.hand.append(self.deck.deal())
                user.soft, user.hard = self.check_hand(user.hand)
                self.ask_user(user)
            elif ask_player == "n":
                user.soft, user.hard = self.check_hand(user.hand)
            else:
                print("Please enter 'y' or 'n'.")
                self.ask_user(user)

    def ask_dealer(self):
        self.dealer.__repr__()
        # if self.dealer.soft == self.dealer.hard:
        #     print(f'Dealer`s total is {self.dealer.soft}')
        # else:
        #     print(f'Dealer`s sums are - soft: {self.dealer.soft}, hard: {self.dealer.hard}')

        # if self.dealer.soft == 21 or self.dealer.hard == 21:
        #     self.dealer.win = 1
        #     for user in self.users:
        #         if user.win is None:
        #             user.win = 0
        #     print("Blackjack!!! You won! \n")
        # elif self.dealer.soft > 16 and self.dealer.hard > 16:
        #     self.dealer.win = 0
        #     for user in self.users:
        #         if user.win is None:
        #             user.win = 1
        #     print("You bust((( \n")
        # elif self.dealer.soft <= 16 and self.dealer.hard <= 16:
        #     print("Opening a card")
        #     sh(self.deck)
        #     self.dealer.hand.append(self.deck[0])
        #     self.dealer.soft, self.dealer.hard = self.check_hand(self.dealer.hand)
        #     self.deck.pop(0)
        #     self.ask_dealer()
        # elif self.dealer.soft <= 16:
        #     print("Opening a card")
        #     sh(self.deck)
        #     self.dealer.hand.append(self.deck[0])
        #     self.dealer.soft, self.dealer.hard = self.check_hand(self.dealer.hand)
        #     self.deck.pop(0)
        #     self.ask_dealer()

        # def looping():
        #     soft_sum, _ = Game.check_hand(self, self.dealer.hand)
        #     print(self.dealer)

        #     print(f"Dealer's total is {soft_sum}")

        #     if soft_sum<=16:
        #         print("Opening a card")
        #         self.dealer.hand.append((self.deck.deal(), True))
        #         looping()
        #         sleep(1)
        #     else:
        #         self.dealer.soft = soft_sum
        #         if self.dealer.soft>=21:
        #             print("Dealer bust (((")
        #             self.dealer.win = 0

        # looping()


        print("____________________")
        print("Final Results are:")
        for player in self.users:
            if player.win == 0:
                print(f'\tPlayer {player.name} LOST(((')
            elif player.win == 1 or self.dealer.win == 0:
                player.win = 1
                self.dealer.win = 0
                print(f"\tPlayer {player.name} WIN!")
            else:
                if player.soft > self.dealer.soft or player.hard > self.dealer.soft:
                    player.win = 1
                    print(f"\tPlayer {player.name} WIN!")
                else:
                    player.win = 0
                    print(f'\tPlayer {player.name} LOST(((')
        print("_______________________________")

    def start_again(self):
        answer = input("\nDo you want to start again (y/n)? ")
        if  answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("Please enter 'y' or 'n'.")
            self.start_again()



def main():
    dec = Deck()
    game = Game(dec.deck)
    print("Welcome to Blackjack!")
    game.add_player()
    game.initial_deal()
    game.show_status() 
    for user in game.users:
        print("\n____________________________")
        print(f'Playing with {user.name}')
        game.ask_user(user)
    print("Dealer showing")
    game.ask_dealer()
    if game.start_again():
        main()
    print("Game over! Thanks. By!")


if __name__ == "__main__":
    main()