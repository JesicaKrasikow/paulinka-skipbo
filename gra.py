import random

from enum import IntEnum


class SkipBo:
    def __init__(self, players):
        self.players = players
        self.players_stack = [[], []]
        self.main_stack = []
        self.game_stacks = [[], [], [], []]
        self.players_hand = [[], []]
        self.discard_pile = [[[], [], [], []], [[], [], [], []]]
        self.tmp_deck = []


        standard_deck = [Card.ONE, Card.TWO, Card.THREE, Card.FOUR, Card.FIVE,
                         Card.SIX, Card.SEVEN, Card.EIGHT, Card.NINE, Card.TEN,
                         Card.ELEVEN, Card.TWELVE, Card.SKIPBO] * 12
        random.shuffle(standard_deck)
        self.main_stack = standard_deck

        for i in range(0, 5):
            self.players_stack[0].append(self.main_stack[0])
            self.main_stack = self.main_stack[1:]
            self.players_stack[1].append(self.main_stack[1])
            self.main_stack = self.main_stack[1:]

    def fill_hand(self, playerid):
        while len(self.players_hand[playerid]) < 5:
            self.players_hand[playerid].append(self.main_stack[0])
            self.main_stack = self.main_stack[1:]

    def move_from_hand(self, place, card, stack_id, player_id):
        if card not in self.players_hand[player_id]:
            print("Nie możesz użyć tej karty, gdyż nie ma jej w twej dłoni")
            return 1

        if place == Place.STACK:
            ret = self.verify(stack_id, card)
            if ret == 0:
                self.players_hand[player_id].remove(card)
                self.game_stacks[stack_id].append(card)
                self.clear_game_stack(stack_id)
                return 0
            else:
                return 1

        if place == Place.DISCARD:
            self.players_hand[player_id].remove(card)
            self.discard_pile[player_id][stack_id].append(card)
            self.clear_game_stack(stack_id)

        return 0

    def move_from_players(self, card, game_stack_id, player_id):
        if card != self.players_stack[player_id][-1]:
            print("Nie możesz użyć tej karty, gdyż nie ma jej na wierzchu twego stosu")
            return 1

        ret = self.verify(game_stack_id, card)
        if ret == 1:
            return 1

        del self.players_stack[player_id][-1]
        self.game_stacks[game_stack_id].append(card)
        self.clear_game_stack(game_stack_id)

        return 0

    def move_from_discard(self, card, game_stack_id, discard_pile_id, player_id):
        if card != self.discard_pile[player_id][discard_pile_id][-1]:
            print("Nie możesz użyć tej karty, gdyż nie ma jej na wierzchu twego stosu pomocniczego")
            return 1

        ret = self.verify(game_stack_id, card)
        if ret == 1:
            return 1

        del self.discard_pile[player_id][discard_pile_id][-1]
        self.game_stacks[game_stack_id].append(card)
        self.clear_game_stack(game_stack_id)

        return 0

    def verify(self, game_stack_id, card):
        # jeśli game_stack jest pusty, to można zacząć układać od karty 1 lub SKIPBO
        if not self.game_stacks[game_stack_id]:
            if card in [Card.ONE, Card.SKIPBO]:
                return 0
            else:
                print("Fałszywy ruch")
                return 1
        # jeśli game_stack ma karty, można położyć wyższą kartę lub SKIPBO
        else:
            if card == Card.SKIPBO:
                return 0
            # karta uzytkownika to nie SKIPBO
            top_card_game_stack = self.game_stacks[game_stack_id][-1]
            # karta SKIPBO się morfuje
            if top_card_game_stack == Card.SKIPBO:
                skipped = 0
                index = len(self.game_stacks[game_stack_id]) - 1
                # dopóki karta na stosie to SKIPBO,
                # czyli zajmujemy się przypadkiem, gdy użytkownik kładzie SKIPBO NA SKIPBO
                while self.game_stacks[game_stack_id][index] == Card.SKIPBO\
                        and index > 0:
                    index = index - 1
                    skipped = skipped + 1
                # jeżeli rzucana karta to ostatnia karta przed skipbo + ilość skipów + 1, to ok
                if card == self.game_stacks[game_stack_id][index] + skipped + 1:
                    return 0
                # ale to nie działa, gdy na stosie jest tylko SKIPBO, bo wtedy self.game_stacks[game_stack_id][index] + skipped + 1 = 14
                elif self.game_stacks[game_stack_id][index] + skipped + 1 == 14:
                    if card == Card.TWO:
                        return 0
                    else:
                        return 1
                        print("Fałszywy ruch")
                else:
                    print("Fałszywy ruch")
                    return 1
            # karta uzytkownika to nie SKIPBO i na gorze stosu nie lezy SKIPBO
            if card == top_card_game_stack + 1:
                return 0
            else:
                print("Fałszywy ruch")
                return 1

    def clear_game_stack(self, stack_id):
        if len(self.game_stacks[stack_id]) == 12:
            for card in self.game_stacks[stack_id]:
                self.tmp_deck.append(card)
            self.game_stacks[stack_id].clear()

        return 0


    @staticmethod
    def test_games():
        global test_game
        test_game = SkipBo(2)
        # Case 1: From hand to game stack
        test_game.players_hand[0] = [Card.ONE, Card.SKIPBO, Card.TWO, Card.FIVE, Card.FOUR]
        assert test_game.move_from_hand(Place.STACK, Card.THREE, 0, 0) is 1
        assert test_game.move_from_hand(Place.STACK, Card.ONE, 0, 0) is 0
        assert test_game.move_from_hand(Place.STACK, Card.TWO, 0, 0) is 0
        assert test_game.move_from_hand(Place.STACK, Card.FIVE, 0, 0) is 1
        assert test_game.move_from_hand(Place.STACK, Card.SKIPBO, 0, 0) is 0

        # Test na SKIPBO
        print("test skipbo...")
        assert test_game.move_from_hand(Place.STACK, Card.EIGHT, 0, 0) is 1
        assert test_game.move_from_hand(Place.STACK, Card.FIVE, 0, 0) is 1
        assert test_game.move_from_hand(Place.STACK, Card.FOUR, 0, 0) is 0
        test_game.game_stacks[0] = [Card.ONE, Card.TWO, Card.SKIPBO, Card.SKIPBO]
        test_game.players_hand[0] = [Card.ONE, Card.SKIPBO, Card.TWO, Card.FIVE, Card.FOUR]
        assert test_game.move_from_hand(Place.STACK, Card.FOUR, 0, 0) is 1
        assert test_game.move_from_hand(Place.STACK, Card.FIVE, 0, 0) is 0

        test_game.game_stacks[0] = []
        test_game.players_stack[0] = [Card.SKIPBO]
        test_game.players_hand[0] = [Card.TWO]
        assert test_game.move_from_players(Card.SKIPBO, 0, 0) is 0
        #assert test_game.move_from_hand(Place.STACK, Card.TWO, 0, 0) is 0

        # Case2: From hand to discard
        test_game.players_hand[0] = [Card.ONE, Card.SKIPBO, Card.TWO, Card.FIVE, Card.FOUR]
        assert test_game.move_from_hand(Place.DISCARD, Card.SKIPBO, 0, 0) is 0
        assert test_game.move_from_hand(Place.DISCARD, Card.TWO, 0, 0) is 0
        assert test_game.move_from_hand(Place.DISCARD, Card.THREE, 0, 0) is 1

        # Case3: From discard to game stack
        test_game.game_stacks[0] = [Card.ONE, Card.TWO, Card.SKIPBO]
        test_game.players_stack[0] = [Card.ONE, Card.SKIPBO, Card.TWO, Card.FIVE, Card.FOUR]
        test_game.discard_pile[0][0] = [Card.TWO, Card.FOUR]
        assert test_game.move_from_discard(Card.FOUR, 0, 0, 0) is 0
        assert test_game.move_from_discard(Card.FIVE, 0, 0, 0) is 1
        assert test_game.move_from_discard(Card.TWO, 0, 0, 0) is 1

        # Case4: From players stack to game stack
        test_game.players_stack[0] = [Card.FIVE, Card.SEVEN, Card.SIX, Card.SKIPBO, Card.FOUR]
        test_game.game_stacks[0] = [Card.ONE, Card.TWO, Card.THREE]
        assert test_game.move_from_players(Card.FOUR, 0, 0) is 0
        assert test_game.move_from_players(Card.SKIPBO, 0, 0) is 0
        assert test_game.move_from_players(Card.SEVEN, 0, 0) is 1
        assert test_game.move_from_players(Card.SIX, 0, 0) is 0

        # Case5: Clear game stack
        test_game.game_stacks[0] = [Card.ONE, Card.TWO, Card.SKIPBO, Card.FOUR, Card.FIVE, Card.SIX, Card.SEVEN,
                                    Card.EIGHT,
                                    Card.NINE, Card.TEN, Card.ELEVEN]
        test_game.players_hand[0] = [Card.SKIPBO]
        print(test_game.game_stacks[0])
        assert test_game.move_from_hand(Place.STACK, Card.SKIPBO, 0, 0) is 0
        #assert test_game.game_stacks[0] is []

        print("All fine!")


class Card(IntEnum):
    EMPTY = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    SKIPBO = 13


class Place(IntEnum):
    STACK = 1
    DISCARD = 2