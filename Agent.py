class Agent:

    ####### constructor #######

    def __init__(self, id):

        # set initial values
        self.id = id
        self.threshold = 0.0
        self.action = 'D'
        self.payoff = 0.0
        self.xValue = 0.0