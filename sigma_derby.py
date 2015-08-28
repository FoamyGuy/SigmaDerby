import random
import time
from median import med
from players import BigBob, CarefulCarl, AlloutAdam, MiddleMelanie

"""
Horse - A single horse on the track. Holds the horses attributes and position.
"""
class Horse(object):
    number = -1             # jersey number
    power = 0               # weight (cheat factor)
    position = 0            # curPos on the track

    # This is called once per round. Roll dice, move horse.
    def step(self):
        self.position += random.randint(1, 200) * self.power

    def __str__(self):
        return self.number

"""
Holds horses; simulates their movement around the track.
"""
class Track(object):
    FINISH_POSITION = 1000
    horses = []
    def add_horse(self, h):
        self.horses.append(h)

    """
    Runs a race simulation. Returns a dictionary of winning horses.
    The key is horses number(1-5) and the value is the horse object.
    {4:<Horse.Object>
     2:<Horse.Object>}
    """
    def run_race(self):
        # If we don't have exactly 5 horses sound the alarms!
        if len(self.horses) != 5:
            raise AttributeError

        has_winner = False

        winning_horses = {}         # key: horse_number, value: horse object

        # Main race loop
        while not has_winner:
            state_str = ""
            for i, horse in enumerate(self.horses):    # loop through array that holds horses
                horse.step()						   # each horse takes a step in turn
                state_str += "%s, " % horse.position   # saves curState of horses on track
                if horse.position > self.FINISH_POSITION:     # Check if passed finish line.
                    winning_horses[self.horses[i].number] = self.horses[i]

            if len(winning_horses) >= 2:               # if at least 2 horses passed finish
                has_winner = True         			   # break out of race loop

        # Check to see if there was a "tie". (more than 2 crossed the finish line)
        if len(winning_horses) > 2:
            """
            We resolve ties by seeing which horse went further passed the finish line.
            If there is a tie on distance too, then highest numbered horse wins.
            """
            real_winners = {}				# dictionary for horses that (really) won
            max_distance = 0                # temp var for max
            winning_horse = -1              # store the winners number

            # Need to find the horse with highest position
            for horse in winning_horses.values():  # loop through winners
                if horse.position > max_distance:  # if my distance is longer than temp max
                    max_distance = horse.position  # change temp max to mine
                    winning_horse = horse.number   # set my number as winner

            # We've found one winner. Add her to the real_winners.
            real_winners[winning_horse] = winning_horses[winning_horse]

            #Remove her from all_winners so we can find the second highest position
            winning_horses.pop(winning_horse)

            max_distance = 0    # Reset temp max
            winning_horse = -1  # Reset winner number

            # Find the highest position again.
            for horse in winning_horses.values():   # loop through winners
                if horse.position > max_distance:   # if my distance is longer than temp max
                    max_distance = horse.position   # change temp max to mine
                    winning_horse = horse.number    # set my number as winner

            # Add our second winner to real_winners
            real_winners[winning_horse] = winning_horses[winning_horse]

            winning_horses = real_winners
        return real_winners

    # Remove all horses
    def reset(self):
        self.horses = None
        self.horses = []


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
    def play(weighted_powers):
        t = Track() # Make a new Track.
        t.reset()

        # Add 5 horses to it
        for h in range(1,6):
            new_horse = Horse()                     # Create a horse
            new_horse.power = weighted_powers[h-1]  # Set its power
            new_horse.number = h                    # Set its number
            t.add_horse(new_horse)                  # Add to the track

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
            # Mystical mathematic equation to turn potential value into a suitable power.
            # The gist of it is higher value -> lower power AND lower value -> higher power.
            values[i] = (1.1 - (cur_val / max_val)) * 5

            # Old mystical formula. Kept for posterity.
            #values[i] = (max_val + 10 - cur_val) / 500

        #print (values)
        return values

# Ladies and gentlemen... The main event of the evening.
if __name__ == "__main__":

    # Some stats holders
    tally = {}
    winnings_paid = []

    # Write down the time we start running simulations
    start_time = time.time()

    # Create some players
    bob = BigBob()
    bob.credits = 10000

    carl = CarefulCarl()
    carl.credits = 10000

    adam = AlloutAdam()
    adam.credits = 10000

    melanie = MiddleMelanie()
    melanie.credits = 10000

    # Play a bunch of rounds
    for game in range(1, 10000):
        # Generate a new set of payouts
        payouts = GameSimulator.generate_payouts()

        # From those payouts generate weighted_power values
        weighted_powers = GameSimulator.get_weighted_powers(payouts)

        # Let each player place their bets.
        bob.place_bets(payouts)
        carl.place_bets(payouts)
        adam.place_bets(payouts)
        melanie.place_bets(payouts)

        # BANG!! And Their Off!!
        winners = GameSimulator.play(weighted_powers)

        # Let each player check to see if they won anything.
        bob.check_win(winners)
        carl.check_win(winners)
        adam.check_win(winners)
        melanie.check_win(winners)

        # Store some statistics about this round.
        winnings_paid.append(payouts[str(winners.keys()).replace(' ', '')])
        try:
            tally[str(winners.keys())] = tally[str(winners.keys())] + 1
        except KeyError:
            tally[str(winners.keys())] = 1

    # Print a tally of how many times each pair of horses won a race.
    for pair in tally.keys():
        print ("%s: %s" % (pair, tally[pair]))

    # Highest possible payout (note: not guaranteed to have been played)
    print ("Highest payout: %s" % max(winnings_paid))

    # Lets see what the damage was
    print ("Bobs ending credits: %s" % bob.credits)
    print ("Carls ending credits: %s" % carl.credits)
    #print ("Adam ending credits: %s" % adam.credits)
    print ("Melanie ending credits: %s" % melanie.credits)

    # Wait, how long did that take?
    print ("Time = %s" % (time.time() - start_time))