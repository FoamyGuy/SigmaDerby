from median import med
from models import Track, Horse
import random


"""
GameSimulator - Represents the whole game.
It's broken into two main parts:
- generate payouts for the players to bet on
- run the race

NOTE: As of now the GameSimulator doesn't handle the bets.
Right now we are leaving that up to the player objects. Luckily
they are programs and therefore won't cheat. (unless they were programmed incorrectly).
"""

class GameSimulator(object):
    @staticmethod
    def generate_payouts():
        # All 10 possible winning outcomes
        all_outcomes = ["[1,2]", "[1,3]", "[1,4]", "[1,5]", "[2,3]",
                        "[2,4]", "[2,5]", "[3,4]", "[3,5]", "[4,5]"]

        # A giant bucket to hold a bunch of labeled ping pong balls.
        odds_choices = []

        # Fill the bucket with balls.
        # In  general there are more small numbers than big ones.
        # Tweak the amount of balls in order to play with average payout over time.
        for i in range(1, 1000): odds_choices.append(2)
        for i in range(1, 900): odds_choices.append(3)
        for i in range(1, 800): odds_choices.append(5)
        for i in range(1, 700): odds_choices.append(8)
        for i in range(1, 600): odds_choices.append(13)
        for i in range(1, 300): odds_choices.append(21)
        for i in range(1, 200): odds_choices.append(34)
        for i in range(1, 200): odds_choices.append(55)
        for i in range(1, 100): odds_choices.append(89)
        for i in range(1, 200): odds_choices.append(144)
        for i in range(1, 100): odds_choices.append(233)

        odds_matrix = {} # Dictionary to hold the payouts

        # Pick 10 balls, 1 for each possible outcome.
        for outcome in all_outcomes:
            odds_matrix[outcome] = random.choice(odds_choices)

        return odds_matrix

    @staticmethod
    def make_horses(weighted_powers):
        horses = []
        # Make 5 horses
        for h in range(1, 6):
            new_horse = Horse()                     # Create a horse
            new_horse.power = weighted_powers[h-1]  # Set its power
            new_horse.number = h                    # Set its number
            horses.append(new_horse)                  # Add to the track
        return horses


    @staticmethod
    def play(weighted_powers):
        t = Track() # Make a new Track.
        t.reset()

        new_horses = GameSimulator.make_horses(weighted_powers)

        # Add 5 horses to it
        for h in new_horses:
            t.add_horse(h)                  # Add to the track

        # Run the race and return results.
        return t.run_race()

    """
    Since this is a game designed to take money from the players, obviously we'll
    cheat a bit by skewing the odds so that horses that payout less are more
    likely to win than horses with large payouts.

    We will add up all of the possible payouts for each horse. This gives us a number
    roughly correlated to the horses potential monetary value.

     Then we'll give the horses with lower monetary values a higher power so they
     are more likely to win.
    """
    @staticmethod
    def get_weighted_powers(payouts):
        # everyone starts even.
        values = [0.2, 0.2, 0.2, 0.2, 0.2]

        # Loop through all of the payouts
        for pair in payouts.keys():

            # Tally up each horses potential value
            if "1" in pair:
                values[0] += payouts[pair]
            if "2" in pair:
                values[1] += payouts[pair]
            if "3" in pair:
                values[2] += payouts[pair]
            if "4" in pair:
                values[3] += payouts[pair]
            if "5" in pair:
                values[4] += payouts[pair]

        # Grab a few useful values
        max_val = max(values)
        min_val = min(values)
        med_value = med(values)

        for i, cur_val in enumerate(values):
            # Mystical mathematical equation to turn potential value into a suitable power.
            # The gist of it is higher value -> lower power AND lower value -> higher power.
            values[i] = (1.1 - (cur_val / max_val)) * 5

            # Old mystical formula. Kept for posterity.
            #values[i] = (max_val + 10 - cur_val) / 500

        #print (values)
        return values