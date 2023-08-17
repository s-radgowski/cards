import random
import time

# Formatting
SPEED = 0.5
stars = "*" * 58
red = "\033[0;31m"
blue = "\033[0;34m"
yellow = "\033[0;33m"
reset = "\033[0m"


value_dict = {
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "T",
    11: "J",
    12: "Q",
    13: "K",
    14: "A"
}

long_value_dict = {
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "Jack",
    12: "Queen",
    13: "King",
    14: "Ace"
}

suit_dict = {
    1: "♣",
    2: f"{red}♦{reset}",
    3: f"{red}♥{reset}",
    4: "♠"
}

quads = f"♣ {red}♦{reset} ♠ {red}♥{reset}"
half = f"♣ {red}♦{reset}"


class Card():
    def __init__(self, value: int, suit: int):
        if value > 14 or value < 2:
            raise ValueError("Invalid Card Value")
        self.value = value
        if suit > 4 or suit < 1:
            raise ValueError("Invalid Suit")
        self.suit = suit
    
    def __str__(self):
        val = value_dict[self.value]
        if self.suit == 1:
            return f"{val} ♣"
        elif self.suit == 2:
            return f"{val} ♦"
        elif self.suit == 3:
            return f"{val} ♥"
        else:
            return f"{val} ♠"
    
    def __repr__(self):
        val = long_value_dict[self.value]
        if self.suit == 1:
            return f"{val} of Clubs"
        elif self.suit == 2:
            return f"{val} of Diamonds"
        elif self.suit == 3:
            return f"{val} of Hearts"
        else:
            return f"{val} of Spades"

    def __lt__(self, other):
        if self.value < other.value:
            return True
        elif self.value == other.value:
            return self.suit < other.suit
        return False

    def __gt__(self, other):
        if self.value > other.value:
            return True
        elif self.value == other.value:
            return self.suit < other.suit
        return False

    def __eq__(self, other):
        return (self.value == other.value) and (self.suit == other.suit)

    def print_card(self):
        print(" _____")
        print(f"|{suit_dict[self.suit]}    |")
        print(f"|  {value_dict[self.value]}  |")
        print(f"|    {suit_dict[self.suit]}|")
        print(" -----")

    def short_name(self) -> str:
        if self.suit in [2, 3]:
            val = f"{red}{value_dict[self.value]}{reset}"
        else:
            val = value_dict[self.value]
        return val + suit_dict[self.suit]


class Deck():
    def __init__(self, decks=1):
        self.cards = []
        for _ in range(decks):
            for i in range(2, 15):
                for j in range(1, 5):
                    self.cards.append(Card(i, j))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def remaining(self):
        return len(self.cards)
    
    def draw(self):
        if self.remaining() == 0:
            return None

        c = self.cards[0]
        self.cards.pop(0)
        return c

    def remove(self, c: Card):
        self.cards.remove(c)
    
    def replace(self, c: Card):
        self.cards.append(c)


class Hand():
    def __init__(self, cards: list):
        self.cards = cards
        self.size = len(cards)
    
    def add(self, c: Card):
        self.cards.append(c)
        self.size += 1

    def subset(self, combo: list):
        """Returns a subset hand of just the cards
            listed in the combo list.
        """
        new = Hand([])
        for i in combo:
            if not isinstance(i, int):
                raise TypeError("Subset must use integer indices")
            new.add(self.cards[i])
        return new

    def print_hand(self):
        suits = [suit_dict[c.suit] for c in self.cards]
        vals = [value_dict[c.value] for c in self.cards]
        for _ in range(self.size):
            print(" _____ ", end=" ")
        print()
        for i in range(self.size):
            print(f"|{suits[i]}    |", end=" ")
        print()
        for i in range(self.size):
            if self.cards[i].suit in [2, 3]:
                print(f"|  {red}{vals[i]}{reset}  |", end=" ")
            else:
                print(f"|  {vals[i]}  |", end=" ")
        print()
        for i in range(self.size):
            print(f"|    {suits[i]}|", end=" ")
        print()
        for _ in range(self.size):
            print(" ----- ", end=" ")
        print()


def print_winner():
    sleep = SPEED / 4
    big_text = f"""
             _________ _        _        _______  _______  _ 
    |\     /|\__   __/( (    /|( (    /|(  ____ \(  ____ )( )
    | )   ( |   ) (   |  \  ( ||  \  ( || (    \/| (    )|| |
    | | _ | |   | |   |   \ | ||   \ | || (__    | (____)|| |
    | |( )| |   | |   | (\ \) || (\ \) ||  __)   |     __)| |
    | || || |   | |   | | \   || | \   || (      | (\ (   (_)
    | () () |___) (___| )  \  || )  \  || (____/\| ) \ \__ _ 
    (_______)\_______/|/    )_)|/    )_)(_______/|/   \__/(_)                                        
    """
    print(f"{yellow}          _________ _        _        _______  _______  _ ")
    time.sleep(sleep)
    print(" |\     /|\__   __/( (    /|( (    /|(  ____ \(  ____ )( )")
    time.sleep(sleep)
    print(" | )   ( |   ) (   |  \  ( ||  \  ( || (    \/| (    )|| |")
    time.sleep(sleep)
    print(" | | _ | |   | |   |   \ | ||   \ | || (__    | (____)|| |")
    time.sleep(sleep)
    print(" | |( )| |   | |   | (\ \) || (\ \) ||  __)   |     __)| |")
    time.sleep(sleep)
    print(" | || || |   | |   | | \   || | \   || (      | (\ (   (_)")
    time.sleep(sleep)
    print(" | () () |___) (___| )  \  || )  \  || (____/\| ) \ \__ _ ")
    time.sleep(sleep)
    print(f" (_______)\_______/|/    )_)|/    )_)(_______/|/   \__/(_){reset}\n")
    time.sleep(sleep * 3)
