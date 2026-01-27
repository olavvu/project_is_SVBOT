from schnapsen.game import SchnapsenGamePlayEngine, Bot, PlayerPerspective, Move, RegularMove
from schnapsen.bots import RandBot, RdeepBot, BullyBot, MiniMaxBot, AlphaBetaBot
import random
from statistics import mean
import math
from scipy.stats import ttest_ind

engine = SchnapsenGamePlayEngine()

class SVBot(Bot):
    TRUMP_PENALTY = 10  

    def __init__(self, rand, name=None):
        super().__init__(name)
        self.rng = rand

    def get_move(self, perspective, leader_move):
        # Convert only regular moves
        valid_moves = []
        for move in perspective.valid_moves():
            if move.is_regular_move():
                valid_moves.append(move.as_regular_move())

        trump_suit = perspective.get_trump_suit()

        # If we start the trick then leader logic is used
        if leader_move is None:
            return self.choose_as_leader(perspective, valid_moves, trump_suit)
        # Otherwise follower logic
        else:
            return self.choose_as_follower(perspective, valid_moves, leader_move, trump_suit)

    def get_rank_points(self, perspective, card):
        scorer = perspective.get_engine().trick_scorer
        return scorer.rank_to_points(card.rank)

    def get_card_cost(self, perspective, card, trump_suit):
        """
        Cost = rank points + TRUMP_PENALTY if the card is trump.
        """
        cost = self.get_rank_points(perspective, card)
        if card.suit == trump_suit:
            cost += self.TRUMP_PENALTY
        return cost

    def lowest_cost_move(self, perspective, moves, trump_suit):
        lowest_move = None
        lowest_cost = None

        for move in moves:
            cost = self.get_card_cost(perspective, move.card, trump_suit)
            if lowest_cost is None or cost < lowest_cost:
                lowest_cost = cost
                lowest_move = move

        return lowest_move

    def beats(self, my_card, other_card, trump_suit):
        # if its same suit then higher rank wins
        if my_card.suit == other_card.suit:
            return my_card.rank.value > other_card.rank.value

        # Trump beats non-trump
        if my_card.suit == trump_suit and other_card.suit != trump_suit:
            return True

        return False


    def choose_as_leader(self, perspective, moves, trump_suit):

        trumps = []
        non_trumps = []
        good_non_trumps = []  # ACE, TEN, KING for example

        for m in moves:
            if m.card.suit == trump_suit:
                trumps.append(m)
            else:
                non_trumps.append(m)
                if m.card.rank.name in ["ACE", "TEN", "KING"]:
                    good_non_trumps.append(m)

        # If we have good non-trumps and trumps, compare cheapest of each
        if good_non_trumps and trumps:
            best_non_trump = self.lowest_cost_move(perspective, good_non_trumps, trump_suit)
            cheapest_trump = self.lowest_cost_move(perspective, trumps, trump_suit)

            cost_not_t = self.get_card_cost(perspective, best_non_trump.card, trump_suit)
            cost_trump = self.get_card_cost(perspective, cheapest_trump.card, trump_suit)

            # Pick the lower-cost option (trump or non-trump)
            if cost_trump < cost_not_t:
                return cheapest_trump
            return best_non_trump

        # Otherwise choose best available option
        if good_non_trumps:
            return self.lowest_cost_move(perspective, good_non_trumps, trump_suit)
        if non_trumps:
            return self.lowest_cost_move(perspective, non_trumps, trump_suit)

        # All are trump or no choice, so pick cheapest overall
        return self.lowest_cost_move(perspective, moves, trump_suit)

    def choose_as_follower(self, perspective, moves, leader_move, trump_suit):

        leader_card = leader_move.cards[0]

        winning_moves = []
        for m in moves:
            if self.beats(m.card, leader_card, trump_suit):
                winning_moves.append(m)

        # pick the lowest-cost winning card (trump or non-trump)
        if winning_moves:
            return self.lowest_cost_move(perspective, winning_moves, trump_suit)

        # dump the lowest-cost legal card
        return self.lowest_cost_move(perspective, moves, trump_suit)
