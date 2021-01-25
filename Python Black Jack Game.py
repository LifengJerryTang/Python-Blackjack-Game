import random

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ("Two," "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}

playing = True


class Card:

    # This is the constructor of the Card class
    def __init__(self, suit, rank):

        self.suit = suit
        self.rank = rank

    # This method returns a string representation of a Card instance
    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    # This is the constructor of the Deck class
    # Stores Card instances for every suits and ranks to an array
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append((Card(suit, rank)))

    # This method returns a string representation of a Deck instance
    def __str__(self):
        deck_composition = ''
        for card in self.deck:
            deck_composition += '\n' + card.__str__()

        return "The deck has: " + deck_composition

    # shuffles the deck array, which contains Card instances for every suits and ranks
    def shuffle(self):
        random.shuffle(self.deck)

    # returns a Card instance from the deck array for dealing
    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:

    # Constructs a Hand instance
    # Params:
        # cards: the Card instances that a player currently has
        # value: total value of the all Card instances
        # aces:  number of aces
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    # Adds a Card instance
    def add_card(self,card):
        # card passed in from Deck.deal() --> single card (suit, rank)
        self.cards.append(card)
        self.value += values[card.rank]

        # Track Aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        # If total value > 21 AND I STILL HAVE AN ACE
        # Than change my ace to a 1 instead of an 11
        while self.value > 21 and self.aces:

            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self, total = 100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Please enter your bet amount: "))

        except ValueError:

            print("ERROR!! Please enter an integer amount: ")
            continue

        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed ", chips.total)

            else:
                break


def hit(deck, hand):

    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):

    global playing

    while True:
        x = input('Hit or Stand? Enter h or s ')

        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print("Player Stands; Dealer's Turn")
            playing = False

        else:
            print("Sorry, I did not understand that. Please enter either h or s: ")
            continue

        break


def player_busts(player, dealer, chips):
    print("BUST PLAYER!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("PLAYER WINS!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("PLAYER WINS! DEALER BUSTED")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("DEALER WINS!")
    chips.lose_bet()


def push(player, dealer):
    print("Dealer and player tie! PUSH")


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)

def main():

    global playing

    while True:

        The_Deck = Deck()
        The_Deck.shuffle()

        player = Hand()
        player.add_card(The_Deck.deal())
        player.add_card(The_Deck.deal())

        dealer = Hand()
        dealer.add_card(The_Deck.deal())
        dealer.add_card(The_Deck.deal())

        chips = Chips()
        take_bet(chips)

        print("\n")
        show_some(player, dealer)

        while playing:

            hit_or_stand(The_Deck, player)

            show_some(player, dealer)

            if player.value > 21:
                player_busts(player, dealer, chips)

                break

        if player.value <= 21:

            while dealer.value < player.value:
                hit(The_Deck, dealer)

            show_all(player, dealer)

        if dealer.value > 21:
            dealer_busts(player, dealer, chips)

        elif dealer.value > player.value:
            dealer_wins()

        elif dealer.value < player.value:
            player_wins(player, dealer, chips)

        else:
            push(player, dealer)

        print("\n Player total chips are at {}".format(chips.total))

        new_game = input("Would you like to play again? y/n: ")

        if new_game[0].lower() == 'y':
            playing = True
            continue

        else:
            print("Thank you for playing! Good game!")
            break


if __name__ == "__main__":
    main()
