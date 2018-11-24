class Temptation_Game:

    ####### constructor #######

    def __init__(self, x_value):
        # set payoff matrix
        self.payoff_matrix = [[0.5,-0.5],[x_value, 0.0]]

    ######## get method #########

    def get_utility(self, action1, action2):

        if action1 == 'C' and action2 == 'C':
            payoff_value = self.payoff_matrix[0][0]
        elif action1 == 'C' and action2 == 'D':
            payoff_value = self.payoff_matrix[0][1]
        elif action1 == 'D' and action2 == 'C':
            payoff_value = self.payoff_matrix[1][0]
        elif action1 == 'D' and action2 == 'D':
            payoff_value = self.payoff_matrix[1][1]

        return payoff_value