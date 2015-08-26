
import random
import time


class Horse(object):
    number = -1             # jersey number
    power = 0               # weight
    position = 0            # curPos on the track

# This is called once per round. Roll dice, move horse.
    def step(self):
        self.position += random.randint(1, 200) * self.power

    def __str__(self):
        return self.number


# Holds horses; simulates movement around the track.
class Track(object):
    horses = []
    def add_horse(self, h):
        self.horses.append(h)

# Runs the simulation.
    def run_game(self):
        if len(self.horses) != 5:
            raise AttributeError

        has_winner = False

        winning_horses = {}         # a list of keys and values
        while not has_winner:
            state_str = ""
            for i, horse in enumerate(self.horses):    # loop through array that holds horses
                horse.step()						   # each horse takes a step in turn
                state_str += "%s, " % horse.position   # saves curState of horses on track
                if horse.position > 1000:             # determine winner
                    winning_horses[self.horses[i].number] = self.horses[i]
            #print state_str
            if len(winning_horses) >= 2:               # if at least 2 horses passed finish
                has_winner = True         			   # break out of game loop


        #print (winning_horses)
        if len(winning_horses) > 2:
            """
            all_winners = ""
            for h in winning_horses:
                all_winners += "%s," % (h)
            print(all_winners)
            """
            real_winners = {}				# a dictionary for horses that won
            max_distance = 0
            winning_horse = -1
            for horse in winning_horses.values():
                if horse.position > max_distance:
                    max_distance = horse.position
                    winning_horse = horse.number

            real_winners[winning_horse] = winning_horses[winning_horse]
            winning_horses.pop(winning_horse)

            max_distance = 0
            winning_horse = -1
            for horse in winning_horses.values():
                if horse.position > max_distance:
                    max_distance = horse.position
                    winning_horse = horse.number

            real_winners[winning_horse] = winning_horses[winning_horse]

            winning_horses = real_winners

            """
            all_winners = ""
            for h in winning_horses:
                all_winners += "%s," % (h)
            print(all_winners)
            print("=====")
            """

        return winning_horses

    def reset(self):
        self.horses = None
        self.horses = []


# A round of play
class GameSimulator(object):
    @staticmethod
    def generate_payouts():
        all_outcomes = ["[1,2]", "[1,3]", "[1,4]", "[1,5]", "[2,3]",
                        "[2,4]", "[2,5]", "[3,4]", "[3,5]", "[4,5]"]
        odds_choices = []

        for i in range(1, 1000): odds_choices.append(2)
        for i in range(1, 900): odds_choices.append(3)
        for i in range(1, 800): odds_choices.append(5)
        for i in range(1, 700): odds_choices.append(8)
        for i in range(1, 600): odds_choices.append(13)
        for i in range(1, 500): odds_choices.append(21)
        for i in range(1, 400): odds_choices.append(34)
        for i in range(1, 300): odds_choices.append(55)
        for i in range(1, 200): odds_choices.append(89)
        for i in range(1, 200): odds_choices.append(144)
        for i in range(1, 200): odds_choices.append(233)

        #print odds_choices
        odds_matrix = {}
        for outcome in all_outcomes:
            odds_matrix[outcome] = random.choice(odds_choices)

        return odds_matrix

    @staticmethod
    def play(weighted_powers):


        t = Track()
        t.reset()
        for h in range(1,6):
            new_horse = Horse()
            new_horse.power = weighted_powers[h-1]
            new_horse.number = h
            t.add_horse(new_horse)

        return t.run_game()


    @staticmethod
    def get_weighted_powers(payouts):
        values = [0.0, 0.0, 0.0, 0.0, 0.0]
        for pair in payouts.keys():

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


        max_val = max(values)

        for i, cur_val in enumerate(values):
            values[i] = (max_val + 10 - cur_val) / 500

        return values


if __name__ == "__main__":
    tally = {}

    winnings_paid = []

    start_time = time.time()

    for game in range(1, 10000):

        payouts = GameSimulator.generate_payouts()
        weighted_powers = GameSimulator.get_weighted_powers(payouts)
        #print(payout)

        winners = GameSimulator.play(weighted_powers)

        winnings_paid.append(payouts[str(winners.keys()).replace(' ', '')])
        #print("Winners %s. Bet pays: %s" % (winners.keys(), payouts[str(winners.keys()).replace(' ', '')]))
        try:
            tally[str(winners.keys())] = tally[str(winners.keys())] + 1
        except KeyError:
            tally[str(winners.keys())] = 1

    for pair in tally.keys():
        print ("%s: %s" % (pair, tally[pair]))

    print ("Highest payout: %s" % max(winnings_paid))

    print ("Time = %s" % (time.time() - start_time))