import math
import random
import time
from cards import *

# Settings
NUM_PLAYERS = 6
BLIND = 2
CHIPS = 100

# Computer Bets
MAX_VAL = 1135.2
SPREAD = 0.15
FOLD_POINT = 4
RAISE_POINT = 12


def print_header():
    sleep = SPEED / 5
    big_text = f"""
    {quads} {quads} {quads} {quads} {quads} {quads} {quads} {half}
         _________ _______           _______  _______         
         \__   __/(  ____ \|\     /|(  ___  )(  ____ \        
            ) (   | (    \/( \   / )| (   ) || (    \/        
            | |   | (__     \ (_) / | (___) || (_____         
            | |   |  __)     ) _ (  |  ___  |(_____  )        
            | |   | (       / ( ) \ | (   ) |      ) |        
            | |   | (____/\( /   \ )| )   ( |/\____) |        
            )_(   (_______/|/     \||/     \|\_______)                         
              _______  _        ______     _  _______  _______ 
    |\     /|(  ___  )( \      (  __  \   ( )(  ____ \(       )
    | )   ( || (   ) || (      | (  \  )  |/ | (    \/| () () |
    | (___) || |   | || |      | |   ) |     | (__    | || || |
    |  ___  || |   | || |      | |   | |     |  __)   | |(_)| |
    | (   ) || |   | || |      | |   ) |     | (      | |   | |
    | )   ( || (___) || (____/\| (__/  )     | (____/\| )   ( |
    |/     \|(_______)(_______/(______/      (_______/|/     \|

   {quads} {quads} {quads} {quads} {quads} {quads} {quads} {half}                                         
    """
 
    print(f"{quads} {quads} {quads} {quads} {quads} {quads} {quads} {half}")
    time.sleep(sleep)
    print("     _________ _______           _______  _______")
    time.sleep(sleep)
    print("     \__   __/(  ____ \|\     /|(  ___  )(  ____ \ ")
    time.sleep(sleep)
    print("        ) (   | (    \/( \   / )| (   ) || (    \/")
    time.sleep(sleep)
    print("        | |   | (__     \ (_) / | (___) || (_____")
    time.sleep(sleep)
    print("        | |   |  __)     ) _ (  |  ___  |(_____  )")
    time.sleep(sleep)
    print("        | |   | (       / ( ) \ | (   ) |      ) |")
    time.sleep(sleep)
    print("        | |   | (____/\( /   \ )| )   ( |/\____) |  ")
    time.sleep(sleep)
    print("        )_(   (_______/|/     \||/     \|\_______)\n")
    time.sleep(sleep * 4)
    print("          _______  _        ______     _  _______  _______ ")
    time.sleep(sleep)
    print("|\     /|(  ___  )( \      (  __  \   ( )(  ____ \(       )")
    time.sleep(sleep)
    print("| )   ( || (   ) || (      | (  \  )  |/ | (    \/| () () |")
    time.sleep(sleep)
    print("| (___) || |   | || |      | |   ) |     | (__    | || || |")
    time.sleep(sleep)
    print("|  ___  || |   | || |      | |   | |     |  __)   | |(_)| |")
    time.sleep(sleep)
    print("| (   ) || |   | || |      | |   ) |     | (      | |   | |")
    time.sleep(sleep)
    print("| )   ( || (___) || (____/\| (__/  )     | (____/\| )   ( |")
    time.sleep(sleep)
    print("|/     \|(_______)(_______/(______/      (_______/|/     \|\n")
    print(f"{quads} {quads} {quads} {quads} {quads} {quads} {quads} {half}\n")
    time.sleep(sleep)


class PokerHand(Hand):
    def subset(self, combo: list):
        """Returns a subset hand of just the cards
            listed in the combo list.
        """
        new = PokerHand([])
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

    def superscore(self, board):
        five_choose_three = [
            [0, 1, 2],
            [0, 1, 3],
            [0, 1, 4],
            [1, 2, 3],
            [1, 2, 4],
            [2, 3, 4]
        ]

        five_choose_four = [
            [0, 1, 2, 3],
            [0, 1, 2, 4],
            [0, 1, 3, 4],
            [0, 2, 3, 4],
            [1, 2, 3, 4]
        ]

        # In comparing, the board gets you no advantage
        max_score = 0
        b = PokerHand(board)

        # If they play just one card...
        for card in range(2):
            for combo in five_choose_four:
                c = b.subset(combo)
                h = HoldemHand([self.cards[card]])
                s = h.score(c)
                if s > max_score:
                    max_score = s
        
        # If they play both cards...
        for combo in five_choose_three:
            c = b.subset(combo)
            h = HoldemHand(self.cards)
            s = h.score(c)
            if s > max_score:
                max_score = s

        return max_score


class HoldemHand(PokerHand):
    """ Scores a 5-card hand numerically, with a maximum score 
        of 1135.2 for a Spades Royal Flush.
    """
    def score(self, board) -> float:
        if (self.size == 2):
            cards = [self.cards[0], self.cards[1], board.cards[0],
                    board.cards[1], board.cards[2]]
        elif (self.size == 1):
            cards = [self.cards[0], board.cards[0], board.cards[1], 
                    board.cards[2], board.cards[3]]
        else:
            cards = [board.cards[0], board.cards[1], board.cards[2],
                    board.cards[3], board.cards[4]]
        vals = [cards[0].value, cards[1].value, cards[2].value,
                cards[3].value, cards[4].value]
        vals_set = list(set(vals))
        suits = [cards[0].suit, cards[1].suit, cards[2].suit,
                cards[3].suit, cards[4].suit]
        suits_set = set(suits)
        
        # Royal Flush
        if (set(vals) == {10, 11, 12, 13, 14}) and (len(suits_set) == 1):
            return 1135 + (suits[0] / 5)
        
        # Straight Flush
        elif (len(vals_set) == 5) and (max(vals) - min(vals) == 4) and (len(suits_set) == 1):
            return 1120 + max(vals) + (suits[0] / 5)
        
        # Wheel Straight Flush
        elif (set(vals) == {2, 3, 4, 5, 14}) and (len(suits_set) == 1):
            return 1125 + (suits[0] / 5)
        
        # Four of Kind
        elif (vals.count(vals_set[0]) == 4):
            return 1110 + vals_set[0]

        elif (vals.count(vals_set[1]) == 4):
            return 1110 + vals_set[1]

        # Full House
        elif (vals.count(vals_set[0]) == 2) and (vals.count(vals_set[1]) == 3):
            return 900 + (vals_set[1] * 14) + vals_set[0]
        
        elif (vals.count(vals_set[1]) == 2) and (vals.count(vals_set[0]) == 3):
            return 900 + (vals_set[0] * 14) + vals_set[1]
        
        # Flush
        elif (len(suits_set) == 1):
            m = max(vals)
            vals.remove(m)
            n = max(vals)
            vals.pop(vals.index(n))
            return 700 + (m * 14) + n + (max(vals) / 15)
        
        # Straight
        elif (len(vals_set) == 5) and (max(vals) - min(vals) == 4):
            top = vals.index(max(vals))
            return 760 + max(vals) + (suits[top] / 5)
        
        # Wheel Straight
        elif (len(vals_set) == 5) and (set(vals) == {2, 3, 4, 5, 14}):
            top = vals.index(5)
            return 765 + (suits[top] / 5)
        
        # Three of a Kind
        elif (vals.count(vals_set[0]) == 3):
            m = vals_set[0]
            vals.remove(m)
            vals.remove(m)
            vals.remove(m)
            n = max(vals)
            vals.pop(vals.index(n))
            return 560 + (m * 14) + n + (max(vals) / 15)
        
        elif (vals.count(vals_set[1]) == 3):
            m = vals_set[1]
            vals.remove(m)
            vals.remove(m)
            vals.remove(m)
            n = max(vals)
            vals.pop(vals.index(n))
            return 560 + (m * 14) + n + (max(vals) / 15)
        
        elif (vals.count(vals_set[2]) == 3):
            m = vals_set[2]
            vals.remove(m)
            vals.remove(m)
            vals.remove(m)
            n = max(vals)
            vals.pop(vals.index(n))
            return 560 + (m * 14) + n + (max(vals) / 15)
        
        # Two Pair
        elif (vals.count(vals_set[0]) == 2) and (vals.count(vals_set[1]) == 2):
            m1 = max(vals_set[0], vals_set[1])
            m2 = min(vals_set[0], vals_set[1])
            n = vals_set[2]
            return 380 + (m1 * 14) + m2 + (n / 15)
        
        elif (vals.count(vals_set[0]) == 2) and (vals.count(vals_set[2]) == 2):
            m1 = max(vals_set[0], vals_set[2])
            m2 = min(vals_set[0], vals_set[2])
            n = vals_set[1]
            return 380 + (m1 * 14) + m2 + (n / 15)
        
        elif (vals.count(vals_set[1]) == 2) and (vals.count(vals_set[2]) == 2):
            m1 = max(vals_set[1], vals_set[2])
            m2 = min(vals_set[1], vals_set[2])
            n = vals_set[0]
            return 380 + (m1 * 14) + m2 + (n / 15)
        
        # Pair
        elif (vals.count(vals_set[0]) == 2):
            m = vals_set[0]
            vals.remove(m)
            vals.remove(m)
            n = max(vals)
            vals.pop(vals.index(n))
            return 200 + (m * 14) + n + (max(vals) / 15)
        
        elif (vals.count(vals_set[1]) == 2):
            m = vals_set[1]
            vals.remove(m)
            vals.remove(m)
            n = max(vals)
            vals.pop(vals.index(n))
            return 200 + (m * 14) + n + (max(vals) / 15)
        
        elif (vals.count(vals_set[2]) == 2):
            m = vals_set[2]
            vals.remove(m)
            vals.remove(m)
            n = max(vals)
            vals.pop(vals.index(n))
            return 200 + (m * 14) + n + (max(vals) / 15)
        
        elif (vals.count(vals_set[3]) == 2):
            m = vals_set[3]
            vals.remove(m)
            vals.remove(m)
            n = max(vals)
            vals.pop(vals.index(n))
            return 200 + (m * 14) + n + (max(vals) / 15)
        
        # High Card
        else:
            m = max(vals)
            vals.remove(m)
            n = max(vals)
            vals.pop(vals.index(n))
            return (m * 14) + n + max(vals) / 14
    
    """ Scores a 2-card holdem hand numerically using the 
        Chen formula for opening hands.
    """
    def chen(self) -> int:
        vals = [self.cards[0].value, self.cards[1].value]
        high = max(vals)
        result = 0
        if high == 14:
            result += 10
        elif high == 13:
            result += 8
        elif high == 12:
            result += 7
        elif high == 13:
            result += 6
        else:
            result += high / 2

        # Multiply pairs by 2
        if vals[0] == vals[1]:
            result = max(5, 2 * result)
        
        # Add 2 points if suited
        if self.cards[0].suit == self.cards[1].suit:
            result += 2
        
        # Subtract points if gap between values
        if abs(vals[0] - vals[1]) > 1:
            if abs(vals[0] - vals[1]) == 2:
                result -= 1
            elif abs(vals[0] - vals[1]) == 3:
                result -= 2
            elif abs(vals[0] - vals[1]) == 4:
                result -= 4
            else:
                result -= 5
        
        # Add 1 point for 0 or 1 card gap below Q
        if abs(vals[0] - vals[1]) in [1, 2] and high <= 11:
            result += 1

        return math.ceil(result)
        

    """ Names a 5-card hand. """
    def name(self, board) -> str:
        if (self.size == 2):
            cards = [self.cards[0], self.cards[1], board.cards[0],
                    board.cards[1], board.cards[2]]
        elif (self.size == 1):
            cards = [self.cards[0], board.cards[0], board.cards[1], 
                    board.cards[2], board.cards[3]]
        else:
            cards = [board.cards[0], board.cards[1], board.cards[2],
                    board.cards[3], board.cards[4]]
        vals = [cards[0].value, cards[1].value, cards[2].value,
                cards[3].value, cards[4].value]
        vals_set = list(set(vals))
        suits = [cards[0].suit, cards[1].suit, cards[2].suit,
                cards[3].suit, cards[4].suit]
        suits_set = set(suits)
        
        # Royal Flush
        if (set(vals) == {10, 11, 12, 13, 14}) and (len(suits_set) == 1):
            return "a Royal Flush"
        
        # Straight Flush
        elif (len(vals_set) == 5) and (max(vals) - min(vals) == 4) and (len(suits_set) == 1):
            return "a Straight Flush"
        
        # Wheel Straight Flush
        elif (set(vals) == {2, 3, 4, 5, 14}) and (len(suits_set) == 1):
            return "a Straight Flush"
        
        # Four of Kind
        elif (vals.count(vals_set[0]) == 4):
            return "Four of a Kind"

        elif (vals.count(vals_set[1]) == 4):
            return "Four of a Kind"

        # Full House
        elif (vals.count(vals_set[0]) == 2) and (vals.count(vals_set[1]) == 3):
            return "a Full House"
        
        elif (vals.count(vals_set[1]) == 2) and (vals.count(vals_set[0]) == 3):
            return "a Full House"
        
        # Flush
        elif (len(suits_set) == 1):
            return "a Flush"
        
        # Straight
        elif (len(vals_set) == 5) and (max(vals) - min(vals) == 4):
            return "a Straight"
        
        # Wheel Straight
        elif (len(vals_set) == 5) and (set(vals) == {2, 3, 4, 5, 14}):
            return "a Straight"
        
        # Three of a Kind
        elif (vals.count(vals_set[0]) == 3):
            return "Three of a Kind"
        
        elif (vals.count(vals_set[1]) == 3):
            return "Three of a Kind"
        
        elif (vals.count(vals_set[2]) == 3):
            return "Three of a Kind"
        
        # Two Pair
        elif (vals.count(vals_set[0]) == 2) and (vals.count(vals_set[1]) == 2):
            return "Two Pair"
        
        elif (vals.count(vals_set[0]) == 2) and (vals.count(vals_set[2]) == 2):
            return "Two Pair"
        
        elif (vals.count(vals_set[1]) == 2) and (vals.count(vals_set[2]) == 2):
            return "Two Pair"
        
        # Pair
        elif (vals.count(vals_set[0]) == 2):
            return f"a Pair of {long_value_dict[vals_set[0]]}s"
        
        elif (vals.count(vals_set[1]) == 2):
            return f"a Pair of {long_value_dict[vals_set[1]]}s"
        
        elif (vals.count(vals_set[2]) == 2):
            return f"a Pair of {long_value_dict[vals_set[2]]}s"
        
        elif (vals.count(vals_set[3]) == 2):
            return f"a Pair of {long_value_dict[vals_set[3]]}s"
        
        # High Card
        else:
            m = max(vals)
            return f"{long_value_dict[m]} High"


class Holdem():
    def __init__(self, players: int, blind, chips):
        self.players = players
        self.blind = blind
        self.reserves = [chips for _ in range(players)]
        self.chips = chips

    def setup(self, first=True):
        # Print obnoxious header
        print("\nNow playing...\n")
        print_header()

        # Shuffle the deck
        d = Deck()
        d.shuffle()
        self.deck = d
        self.board = PokerHand([])
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
        print(f"Little Blind: ${self.blind}")
        if (self.order == 0):
            print("You are the Little Blind")
        elif (self.order == 1):
            print("You are the Big Blind")
        else:
            print(f"You are player #{self.order + 1}")
        time.sleep(SPEED * 4)

    def active_players(self):
        return self.active.count(True)

    def deal(self):
        cards = [[] for p in range(self.players)]
        for i in range(2):
            for p in range(self.players):
                c = self.deck.draw()
                cards[p].append(c)
        
        self.hands = [HoldemHand(h) for h in cards]
    
    def show(self):
        print(f"Current Pot:    ${self.pot}")
        print(f"Your stakes:    ${self.stakes[self.order]}")
        print(f"Your reserves:  ${self.reserves[self.order]}")
        if self.board.size > 0:
            print("\n\nThe board:")
            self.board.print_hand()

        print("\n\nYour hand:")
        self.hands[self.order].print_hand()
        print()
    
    def computer_bet(self, player, leading):
        # Determine remaining possible cards
        remaining = Deck()
        for card in self.hands[player].cards:
            remaining.remove(card)
        for card in self.board.cards:
            remaining.remove(card)

        ratio = leading / (leading + self.pot)
        lower_bound = 1 - ratio - SPREAD
        upper_bound = 1 - ratio + SPREAD
        total_score = 0

        # Opening bet: Use Chen's formula
        if self.board.size == 0:
            score_chen = self.hands[player].chen()
            if score_chen <= FOLD_POINT:
                # Fold
                return 0

            elif score_chen > FOLD_POINT and score_chen < RAISE_POINT:
                # Call
                if self.reserves[player] < leading:
                    # Out of money, fold
                    return 0
                return leading

            else:
                # Raise
                target_bet = leading * 2
                if self.reserves[player] < leading:
                    # Out of money, fold
                    return 0
                elif self.reserves[player] < target_bet:
                    # All in
                    return self.reserves[player]
                else:
                    # Raise
                    return target_bet

        if self.board.size == 3:
            for i, card_i in enumerate(remaining.cards[:-1]):
                for card_j in remaining.cards[i + 1:]:
                    h = PokerHand(self.hands[player].cards)
                    b = self.board.cards.copy()
                    b.append(card_i)
                    b.append(card_j)
                    total_score += h.superscore(b)
            # 52 - 5 cards in play, 47 choose 2
            total_score /= 1081
            score_ratio = total_score / MAX_VAL
        
        elif self.board.size == 4:
            for card_i in remaining.cards:
                h = PokerHand(self.hands[player].cards)
                b = self.board.cards.copy()
                b.append(card_i)
                total_score += h.superscore(b)
            # 52 - 6 cards in play, 46 cards left
            total_score /= 46
            score_ratio = total_score / MAX_VAL

        if score_ratio <= lower_bound:
            # Fold
            return 0
        
        elif score_ratio > lower_bound and score_ratio < upper_bound:
            if self.reserves[player] < leading:
                # Out of money, fold
                return 0
            else:
                # Call
                return leading
        
        else:
            target_bet = min(leading * 2, self.pot)
            if self.reserves[player] < leading:
                # Out of money, fold
                return 0
            elif self.reserves[player] < target_bet:
                # All in
                return self.reserves[player]
            else:
                # Raise
                return target_bet

    def first_bet(self):
        print(f"\n\n{blue}{stars}")
        print("                   FIRST ROUND OF BETTING")
        print(f"{stars}{reset}")
        self.show()

        high = self.blind * 2
        self.bets = [0 for _ in range(self.players)]
        for p in range(self.players):
            time.sleep(SPEED * 2)
            if p == 0 and self.order != 0:
                print(f"PLAYER 1: Little Blind of ${self.blind}")
                self.bets[0] = self.blind
                self.reserves[0] -= self.blind
            
            elif p == 0 and self.order == 0:
                print(f"You Bet ${self.blind} as the Little Blind")
                self.bets[0] = self.blind
                self.reserves[0] -= self.blind
            
            elif p == 1 and self.order != 1:
                print(f"PLAYER 2: Big Blind of ${self.blind * 2}")
                self.bets[1] = self.blind * 2
                self.reserves[1] -= self.blind * 2
            
            elif p == 1 and self.order == 1:
                print(f"You Bet ${self.blind * 2} as the Big Blind")
                self.bets[1] = self.blind * 2
                self.reserves[1] -= self.blind * 2

            # Your Bet
            elif p == self.order:
                print(f"\n{blue}YOUR TURN")
                print(f"[F to Fold, C to Call ${high}, or R to Raise]{reset}")
                bet = input("Enter your choice: ")

                while bet.lower() not in ["f", "c", "r"]:
                    print(f"{red}ERROR: Invalid play. Please try again.{reset}")
                    bet = input("Enter your choice: ")

                if bet in ["f", "F"]:
                    self.active[p] = False
                elif bet in ["c", "C"]:
                    self.bets[p] = high
                    self.reserves[p] -= high
                elif bet in ["r", "R"]:
                    new_bet = input("Enter your raise: $")
                    n = int(new_bet)
                    while n <= high or n > self.reserves[p]:
                        print(f"{red}ERROR: Invalid raise. Please try again.{reset}")
                        new_bet = input("Enter your raise: $")

                    self.bets[p] = n
                    self.reserves[p] -= n
                    high = n
                print()

            # Computer Bet
            elif self.active[p]:
                bet = self.computer_bet(p, high)
                if bet < high:
                    print(f"PLAYER {p + 1}: Fold")
                    self.active[p] = False

                elif bet == high:
                    print(f"PLAYER {p + 1}: Call")
                    self.bets[p] = bet
                    self.reserves[p] -= bet
                
                elif bet > high:
                    print(f"PLAYER {p + 1}: Raise to ${bet}")
                    high = bet
                    self.bets[p] = bet
                    self.reserves[p] -= bet
            
            else:
                print(f"PLAYER {p + 1}: (Folded)")

        # Final calls if raised
        for p in range(self.players):

            # Your Bet
            if p == self.order and self.active[p] and self.bets[p] < high:
                time.sleep(SPEED * 2)
                print(f"\n{blue}YOUR TURN")
                print(f"[F to Fold, C to Call ${high}]{reset}")
                bet = input("Enter your choice: ")

                while bet not in ["f", "F", "c", "C"]:
                    print(f"{red}ERROR: Invalid play. Please try again.{reset}")
                    bet = input("Enter your choice: ")

                if bet in ["f", "F"]:
                    self.active[p] = False
                elif bet in ["c", "C"]:
                    self.reserves[p] -= high - self.bets[p]
                    self.bets[p] = high

                print()

            # Computer Bet
            elif self.active[p] and self.bets[p] < high:
                time.sleep(SPEED * 2)
                bet = self.computer_bet(p, high)
                if bet < high:
                    print(f"PLAYER {p + 1}: Fold")
                    self.active[p] = False

                elif bet >= high:
                    print(f"PLAYER {p + 1}: Call")
                    self.reserves[p] -= high - self.bets[p]
                    self.bets[p] = bet

        self.stakes = [s + self.bets[i] for i, s in enumerate(self.stakes)]
        self.pot += sum(self.bets)

    def additional_bet(self, round: int):
        print(f"\n\n{blue}{stars}")
        if round == 2:
            print("                   SECOND ROUND OF BETTING")
        elif round == 3:
            print("                   THIRD ROUND OF BETTING")
        print(f"{stars}{reset}")
        self.show()

        high = 0
        self.bets = [0 for _ in range(self.players)]
        for p in range(self.players):
            time.sleep(1)

            # Your Bet
            if p == self.order and self.active[p]:
                print(f"\n{blue}YOUR TURN")
                if high == 0:
                    print(f"[F to Fold, C to Check, or R to Raise]{reset}")
                else:
                    print(f"[F to Fold, C to Call ${high}, or R to Raise]{reset}")

                bet = input("Enter your choice: ")
                if bet in ["f", "F"]:
                    self.active[p] = False
                elif bet in ["c", "C"]:
                    self.bets[self.order] = high
                    self.reserves[p] -= high
                elif bet in ["r", "R"]:
                    new_bet = input("Enter your raise: $")                    
                    n = int(new_bet)
                    while n <= high or n > self.reserves[p]:
                        print(f"{red}ERROR: Invalid raise. Please try again.{reset}")
                        new_bet = input("Enter your raise: $")

                    self.bets[self.order] = n
                    high = n
                    self.reserves[p] -= n
                print()

            # Computer Bet
            elif self.active[p]:
                if self.reserves[p] <= 0:
                    print(f"PLAYER {p + 1}: Bankrupt")
                    self.active[p] = False

                bet = self.computer_bet(p, high)
                if bet < high or bet > self.reserves[p]:
                    print(f"PLAYER {p + 1}: Fold")
                    self.active[p] = False

                elif bet == high:
                    print(f"PLAYER {p + 1}: Call")
                    self.bets[p] = bet
                    self.reserves[p] -= bet
                
                elif bet > high:
                    print(f"PLAYER {p + 1}: Raise to ${bet}")
                    high = bet
                    self.bets[p] = bet
                    self.reserves[p] -= bet
        
        # Final calls if raised
        for p in range(self.players):
            time.sleep(SPEED * 2)

            # Your Bet
            if p == self.order and self.active[p] and self.bets[p] < high:
                print(f"\n{blue}YOUR TURN")
                print(f"[F to Fold, C to Call ${high}]{reset}")
                bet = input("Enter your choice: ")

                while bet not in ["f", "F", "c", "C"]:
                    print(f"{red}ERROR: Invalid play. Please try again.{reset}")
                    bet = input("Enter your choice: ")

                if bet in ["f", "F"]:
                    self.active[p] = False
                elif bet in ["c", "C"]:
                    self.reserves[p] -= high - self.bets[p]
                    self.bets[p] = high

                print()

            # Computer Bet
            elif self.active[p] and self.bets[p] < high:
                bet = self.computer_bet(p, high)
                if bet < high:
                    print(f"PLAYER {p + 1}: Fold")
                    self.active[p] = False

                elif bet >= high:
                    print(f"PLAYER {p + 1}: Call")
                    self.reserves[p] -= high - self.bets[p]
                    self.bets[p] = bet

        self.stakes = [s + self.bets[i] for i, s in enumerate(self.stakes)]
        self.pot += sum(self.bets)

    def superscore(self, player: int):
        """Determines the highest score possible for a player,
        given their hand and the full board.
        Returns the cards used, winning board card combination, and score.
        """
        five_choose_three = [
            [0, 1, 2],
            [0, 1, 3],
            [0, 1, 4],
            [1, 2, 3],
            [1, 2, 4],
            [2, 3, 4]
        ]

        five_choose_four = [
            [0, 1, 2, 3],
            [0, 1, 2, 4],
            [0, 1, 3, 4],
            [0, 2, 3, 4],
            [1, 2, 3, 4]
        ]

        full_board = [0, 1, 2, 3, 4]

        # If they play the board...
        blank_hand = HoldemHand([])
        max_score = blank_hand.score(self.board)
        winning_combo = full_board
        cards_used = -1

        # If they play just one card...
        for card in range(2):
            for combo in five_choose_four:
                b = self.board.subset(combo)
                h = HoldemHand([self.hands[player].cards[card]])
                s = h.score(b)
                if s > max_score:
                    max_score = s
                    winning_combo = combo
                    cards_used = card
        
        # If they play both cards...
        for combo in five_choose_three:
            b = self.board.subset(combo)
            s = self.hands[player].score(b)
            if s > max_score:
                max_score = s
                winning_combo = combo
                cards_used = 2

        return (cards_used, winning_combo, max_score)

    def reveal(self):
        print(f"\n\n{blue}{stars}")
        print("                       FINAL RESULTS")
        print(f"{stars}{reset}")

        # Select Winner
        scores = []
        combos = []
        hands = []
        for p in range(self.players):
            if not self.active[p]:
                scores.append(0)
                combos.append(None)
                hands.append(None)
            
            else:
                h, combo, s = self.superscore(p)
                scores.append(s)
                combos.append(combo)
                hands.append(h)
        
        winner = scores.index(max(scores))
        
        # Reveal Standing
        if self.active[self.order]:
            b = self.board.subset(combos[self.order])
            used = hands[self.order]
        else:
            used, combo, s = self.superscore(self.order)
            b = self.board.subset(combo)
        
        # Find Our Hand's Name
        if used == -1:
            hand = HoldemHand([])
        elif used == 2:
            hand = self.hands[self.order]
        else:
            hand = HoldemHand([self.hands[self.order].cards[used]])
        n = hand.name(b)
        if winner == self.order:
            print_winner()
            print(f"\nHooray! You won with {n}!")
            print(f"Your winnings: ${self.pot}")
            self.reserves[self.order] += self.pot
            self.pot = 0

        elif not self.active[self.order]:
            print(f"\nUnfortunately, you folded with {n}.")
            lost = self.stakes[self.order]
            if lost == 0:
                print("Fortunately, you did not bet anything.")
            else:
                print(f"You lost your bet of ${lost}.")
        else:
            print(f"\nUnfortunately, you lost with only {n}.")
            lost = self.stakes[self.order]
            if lost == 0:
                print("Fortunately, you did not bet anything.")
            else:
                print(f"You lost your bet of ${lost}.")

        # Refresh on your hand and the board
        if self.board.size > 0:
            print("\n\nThe board:")
            self.board.print_hand()

        print("\n\nYour hand:")
        self.hands[self.order].print_hand()
        print()
        
        # Reveal Hands
        for p in range(self.players):
            if p != self.order:
                c0 = self.hands[p].cards[0].short_name()
                c1 = self.hands[p].cards[1].short_name()
                if not self.active[p]:
                    print(f"PLAYER {p + 1}: {c0} {c1} (Folded)")
                elif p == winner:
                    print(f"PLAYER {p + 1}: {c0} {c1} (Winner)")
                    self.reserves[p] += self.pot
                    self.pot = 0
                else:
                    print(f"PLAYER {p + 1}: {c0} {c1}")

    def play(self, first=True):
        self.setup(first=first)
        self.deal()
        self.first_bet()
        
        # Flop
        for _ in range(3):
            c = self.deck.draw()
            self.board.add(c)
        time.sleep(SPEED * 2)
        if self.active_players() > 1:
            self.additional_bet(2)

        # Turn
        c = self.deck.draw()
        self.board.add(c)
        time.sleep(SPEED * 2)
        if self.active_players() > 1:
            self.additional_bet(3)

        # River
        c = self.deck.draw()
        self.board.add(c)

        self.reveal()

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
    g = Holdem(NUM_PLAYERS, BLIND, CHIPS)
    g.play()
