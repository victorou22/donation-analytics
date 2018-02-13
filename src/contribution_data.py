from math import ceil, floor
import bisect

class ContributionData:
    """
    Class storing the datastructures assisting the calculations for the contributions from repeat donors
    Calculations include percentile, total amount of contributions, total number of contributions
    """

    def __init__(self):
        self.contribution_history = []
        self.running_total = 0

    def add_contribution(self, contribution):
        """
        Insert contribution into contribution history using a selection sort-like method to maintain sort

        :param contribution: value to be inserted
        :type contribution: int
        """
        bisect.insort(self.contribution_history, contribution)
    
    def calculate_percentile(self, percentile):
        """
        Calculate the percentile using the current running contribution history and the nearest-rank method

        :param percentile: input percentile to be used in calculation
        :type percentile: int
        :returns: the contribution associated with the input percentile
        :rtype: int
        """
        rank = percentile/100*len(self.contribution_history)
        if (rank % 1 >= 0.5) or rank < 0.5:
            rank = ceil(rank)
        else:
            rank = floor(rank)
        return self.contribution_history[rank - 1]

    def total_transactions(self):
        return len(self.contribution_history)

        