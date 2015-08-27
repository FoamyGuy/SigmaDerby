from median import med

class Player(object):
    def __init__(self):
        self.credits = 0
        self.name = ""
        self.bets = {}


    def check_win(self, winners):
        winning_nums = []
        for horse in winners:
            winning_nums.append(horse)
        check_str = "[%s,%s]" % (winning_nums[0], winning_nums[1])
        if check_str in self.bets.keys():
            self.credits += self.bets[check_str]

            self.bets.clear()
            return True
        self.bets.clear()
        return False



class BigBob(Player):
    # Can bet multiple pairs
    # always bet the highest payouts
    def place_bets(self, payouts):
        self.bets.clear()
        for pair, payout in payouts.iteritems():
            if payout == max(payouts.values()):
                self.bets[pair] = payout

        self.credits -= len(self.bets)
        return self.bets


class CarefulCarl(Player):
    # Only bet on 1 pair.
    # Bet on one of the smallest payout
    def place_bets(self, payouts):
        self.bets.clear()
        for pair, payout in payouts.iteritems():
            if payout == min(payouts.values()):
                self.bets[pair] = payout
                self.credits -= len(self.bets)
                return self.bets


class AlloutAdam(Player):
    # Bet 1 credit on every outcome
    def place_bets(self, payouts):
        self.bets.clear()
        for pair, payout in payouts.iteritems():
            self.bets[pair] = payout

        self.credits -= len(self.bets)
        return self.bets


class MiddleMelanie(Player):
    # Bet 1 credit on the median pyout
    # can bet multiples
    def place_bets(self, payouts):
        med_payout = med(payouts.values())
        self.bets.clear()
        for pair, payout in payouts.iteritems():
            if payout == med_payout:
                self.bets[pair] = payout

        self.credits -= len(self.bets)

        return self.bets