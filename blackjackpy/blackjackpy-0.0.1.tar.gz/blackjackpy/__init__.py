import random


class Card:
    def __init__(self, num):
        self.suit = num // 13 + 1
        self.rank = num % 13 + 1

    def point(self):
        return min(10, self.rank)

    def __str__(self):
        n = self.rank * 2
        r = " A 2 3 4 5 6 7 8 910 J Q K"[n - 2 : n]
        s = "(" + "DHSC"[self.suit - 1] + ")"
        return r + s


class Owner:
    def __init__(self):
        self.hands = []

    def draw(self, bj):
        self.hands.append(bj.pop())

    def sequence(self, hide=False):
        s = "".join(str(cd) for cd in self.hands)
        return (s[:5] + " *(*)" + s[10:]) if hide else s

    def point(self):
        p = sum(cd.point() for cd in self.hands)
        for cd in self.hands:
            if cd.rank == 1 and p + 10 <= 21:
                p += 10
        return p


class Player(Owner):
    def ask(self):
        print("Draw? (y/n) ", end="")
        return input()

    def act(self, bj):
        while self.point() <= 20:
            bj.show(True)
            s = ""
            while s != "y" and s != "n":
                s = self.ask()
            if s == "n":
                break
            self.draw(bj)


class Dealer(Owner):
    def act(self, bj):
        while self.point() <= 16:
            self.draw(bj)


class Blackjack:
    def __init__(self, seed=None):
        self.cards = [Card(i) for i in range(52)]
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.cards)
        self.player = Player()
        self.dealer = Dealer()

    def start_game(self):
        for _ in range(2):
            self.player.draw(self)
            self.dealer.draw(self)
        self.player.act(self)
        player_point = self.player.point()
        self.message = "You lose."
        if player_point <= 21:
            self.dealer.act(self)
            dealer_point = self.dealer.point()
            if player_point == dealer_point:
                self.message = "Draw."
            elif dealer_point >= 22 or dealer_point < player_point:
                self.message = "You win."
        self.show(False)
        print(self.message)

    def show(self, hide):
        p = self.player.point()
        s = self.player.sequence()
        print(f"Player({p:2}): {s}")
        p = "--" if hide else self.dealer.point()
        s = self.dealer.sequence(hide)
        print(f"Dealer({p:2}): {s}")

    def pop(self):
        return self.cards.pop(0)


def main():
    Blackjack().start_game()
