
import time
from players import BigBob, CarefulCarl, AlloutAdam, MiddleMelanie
from GameSimulator import GameSimulator


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