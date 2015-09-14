import random

"""
Horse - A single horse on the track. Holds the horses attributes and position.
"""

class Horse(object):
    number = -1             # jersey number
    power = 0               # weight (cheat factor)
    position = 0            # curPos on the track

    # This is called once per round. Roll dice, move horse.
    def step(self):
        self.position += random.randint(1, 50) * self.power

    def __str__(self):
        return self.number

"""
Holds horses; simulates their movement around the track.
"""
class Track(object):
    FINISH_POSITION = 10000
    horses = []
    def add_horse(self, h):
        self.horses.append(h)

    """
    Runs a race simulation. Returns a dictionary of winning horses.
    The key is horses number(1-5) and the value is the horse object.
    e.g.
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
            self.race_step()
            #state_str = ""
            for i, horse in enumerate(self.horses):    # loop through array that holds horses
                horse.step()						   # each horse takes a step in turn
                #state_str += "%s, " % horse.position   # saves curState of horses on track
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
            real_winners = {}   # dictionary for horses that (really) win
            max_distance = 0    # temp var for max
            winning_horse = -1  # store the winners number

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
        return winning_horses

    def race_step(self):
        pass


    def find_winners(self):
        pass

    # Remove all horses
    def reset(self):
        self.horses = None
        self.horses = []

