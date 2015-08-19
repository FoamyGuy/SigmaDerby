import random
import time

import openpyxl

class Horse(object):
    number = -1
    power = 0
    position = 0

    def step(self):
        self.position += random.randint(1, 200) * self.power

    def __str__(self):
        return self.number

class Track(object):
    horses = []

    def add_horse(self, h):
        self.horses.append(h)

    def run_game(self):
        if len(self.horses) != 5:
            raise AttributeError

        has_winner = False

        winning_horses = {}
        while not has_winner:
            state_str = ""
            for i, horse in enumerate(self.horses):
                horse.step()
                state_str += "%s, " % horse.position
                if horse.position > 10000:
                    winning_horses[self.horses[i].number] = self.horses[i]
            #print state_str
            if len(winning_horses) >= 2:
                has_winner = True


        #print (winning_horses)
        if len(winning_horses) > 2:
            """
            all_winners = ""
            for h in winning_horses:
                all_winners += "%s," % (h)
            print(all_winners)
            """
            real_winners = {}
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


class Round(object):
    def generate_odds(self):
        all_outcomes = ["[1,2]", "[1,3]", "[1,4]", "[1,5]", "[2,3]"
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

        print odds_matrix


    def play(self):
        t = Track()
        for h in range(1,6):
            new_horse = Horse()
            new_horse.power = 2 + (h * .01)
            new_horse.number = h
            t.add_horse(new_horse)

        winners = t.run_game()
        return winners

if __name__ == "__main__":

    for i in range(1, 100):
        r = Round()
        r.generate_odds()


    """
    t = Track()
    tally = {}
    for game in range(1, 1000):
        for h in range(1, 6):
            new_horse = Horse()
            new_horse.power = 2 + (h * .01)
            new_horse.number = h
            t.add_horse(new_horse)

        winners = t.run_game()
        try:
            tally[str(winners.keys())] = tally[str(winners.keys())] + 1
        except KeyError:
            tally[str(winners.keys())] = 1
        t.reset()

    for pair in tally.keys():
        print ("%s: %s" % (pair, tally[pair]))

    """

