import math
import random
import time
from cards import *

# Settings
NUM_PLAYERS = 6
CHIPS = 100
DECKS = 6

GAP = "   "


def print_header():
    sleep = SPEED / 5
    big_text = f"""
    {quads} {quads} {quads} {quads} {quads} {quads} {quads} {half}
             ______   __                 __       
            |_   _ \ [  |               [  |  _   
              | |_) | | |  ,--.   .---.  | | / ]  
              |  __'. | | `'_\ : / /'`\] | '' <   
             _| |__) || | // | |,| \__.  | |`\ \  
            |_______/[___]\'-;__/'.___.'[__|  \_] 
                                                
                        _____              __           
                       |_   _|            [  |  _       
                         | | ,--.   .---.  | | / ]      
                     _   | |`'_\ : / /'`\] | '' <       
                    | |__' |// | |,| \__.  | |`\ \      
                    `.____.'\'-;__/'.___.'[__|  \_]     
                                                
   {quads} {quads} {quads} {quads} {quads} {quads} {quads} {half}                                         
    """
 
    print(f"{quads} {quads} {quads} {quads} {quads} {quads} {quads} {half}")
    time.sleep(sleep)
    print("      ______   __                 __       ")
    time.sleep(sleep)
    print("     |_   _ \ [  |               [  |  _   ")
    time.sleep(sleep)
    print("       | |_) | | |  ,--.   .---.  | | / ]  ")
    time.sleep(sleep)
    print("       |  __'. | | `'_\ : / /'`\] | '' <   ")
    time.sleep(sleep)
    print("      _| |__) || | // | |,| \__.  | |`\ \  ")
    time.sleep(sleep)
    print("     |_______/[___]\'-;__/ '.___.'[__|  \_]\n")
    time.sleep(sleep * 4)
    print("                    _____              __  ")
    time.sleep(sleep)
    print("                   |_   _|            [  |  _  ")
    time.sleep(sleep)
    print("                     | | ,--.   .---.  | | / ]  ")
    time.sleep(sleep)
    print("                 _   | |`'_\ : / /'`\] | '' <   ")
    time.sleep(sleep)
    print("                | |__' |// | |,| \__.  | |`\ \  ")
    time.sleep(sleep)
    print("                `.____.'\'-;__/ '.___.'[__|  \_]\n")
    print(f"{quads} {quads} {quads} {quads} {quads} {quads} {quads} {half}\n")
    time.sleep(sleep)


class BlackjackHand(Hand):
    def subset(self, combo: list):
        """Returns a subset hand of just the cards
            listed in the combo list.
        """
        new = Blackjack([])
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

    def print_hands(self, other):
        suits = [suit_dict[c.suit] for c in self.cards]
        vals = [value_dict[c.value] for c in self.cards]
        suits.extend([suit_dict[c.suit] for c in other.cards])
        vals.extend([value_dict[c.value] for c in other.cards])
        for _ in range(self.size):
            print(" _____ ", end=" ")
        print(GAP, end="")
        for _ in range(other.size):
            print(" _____ ", end=" ")
        print()

        for i in range(self.size):
            print(f"|{suits[i]}    |", end=" ")
        print(GAP, end="")
        for i in range(other.size):
            print(f"|{suits[i + self.size]}    |", end=" ")
        print()

        for i in range(self.size):
            if self.cards[i].suit in [2, 3]:
                print(f"|  {red}{vals[i]}{reset}  |", end=" ")
            else:
                print(f"|  {vals[i]}  |", end=" ")
        print(GAP, end="")
        for i in range(other.size):
            if other.cards[i].suit in [2, 3]:
                print(f"|  {red}{vals[i + self.size]}{reset}  |", end=" ")
            else:
                print(f"|  {vals[i + self.size]}  |", end=" ")
        print()

        for i in range(self.size):
            print(f"|    {suits[i]}|", end=" ")
        print(GAP, end="")
        for i in range(self.size):
            print(f"|    {suits[i + self.size]}|", end=" ")
        print()

        for _ in range(self.size):
            print(" ----- ", end=" ")
        print(GAP, end="")
        for _ in range(self.size):
            print(" ----- ", end=" ")
        print()

    def score(self):
        total = 0
        for card in self.cards:
            if card.value in [11, 12, 13]:
                total += card.value
            # All Aces start as high
            elif card.value == 14:
                total += 11
            elif card.value <= 10:
                total += card.value

        # Determine which Aces are low
        for card in self.cards:
            if card.value == 14 and total > 21:
                total -= 10
        
        if total > 21:
            return 0
        return total


class Blackjack():
    def __init__(self, players: int, chips):
        self.players = players
        self.reserves = [chips for _ in range(players)]
        self.chips = chips

    def setup(self, first=True):
        # Print obnoxious header
        print("\nNow playing...\n")
        print_header()

        # Shuffle the deck
        d = Deck(decks=DECKS)
        d.shuffle()
        self.deck = d
        self.board = Hand([])
        self.pot = 0

        # Assign roles
        if first:
            self.order = random.randint(0, self.players - 1)
        else:
            self.reserves.append(self.reserves.pop(0))
            self.order = (self.order - 1) % self.players
        self.active = [True for _ in range(self.players)]
        self.stakes = [0 for _ in range(self.players)]
        time.sleep(SPEED)
        print(f"\nNumber of players: {self.players}")
        print(f"You are player #{self.order + 1}\n")
        time.sleep(SPEED * 4)

    def deal(self):
        self.hands = []
        for _ in range(self.players):
            c1 = self.deck.draw()
            c2 = self.deck.draw()
            self.hands.append(BlackjackHand([c1, c2]))

        c1 = self.deck.draw()
        c2 = self.deck.draw()
        self.dealer = BlackjackHand([c1, c2])
            
    def show(self):
        print(f"Current Pot:    ${self.pot}")
        print(f"Your stakes:    ${self.stakes[self.order]}")
        print(f"Your reserves:  ${self.reserves[self.order]}")
        
        print("\n\nThe dealer's hand:")
        self.dealer.print_hand()

        print("\n\nThe table:")
        hands = list(range(self.players))
        hands.remove(self.order)
        hands = [h for h in hands if self.active[h]]
        for i in range(math.floor(len(hands) / 2)):
            hand1 = hands[2 * i]
            hand2 = hands[(2 * i) + 1]
            print(f"\nPlayer {hand1 + 1}: {GAP * 3} Player {hand2 + 1}:")
            other = self.hands[hand2]
            self.hands[hand1].print_hands(other)

        if len(hands) % 2 == 1:
            print(f"\nPlayer {hands[-1] + 1}:")
            self.hands[hands[-1]].print_hand()

        print("\n\nYour hand:")
        self.hands[self.order].print_hand()
        print()

    def play(self, first=True):
        self.setup(first=first)

        self.deal()
        self.show()

        # Parlay?
        print(blue, end="")
        if self.reserves[self.order] <= 0:
            print("\nYou are out of money. Better luck next time!")
            print(reset)
        else:
            print("\nWant to parlay?")
            print(f"[Y for Yes, N for No]{reset}")
            a = input("Enter your choice: ")
            if a.lower() in ["y", "yes"]:
                self.play(first=False)
            else:
                amt = self.reserves[self.order]
                print(yellow, end="")
                if self.reserves[self.order] < self.chips:
                    print(f"\nThank you for playing, you're leaving with ${amt}.")
                else:
                    print(f"\nCongratulations! You're leaving with ${amt}.")
                print(reset, end="")


if __name__ == "__main__":
    g = Blackjack(NUM_PLAYERS, CHIPS)
    g.play()