##### main algorithm that executes the temptation threshold imitation ####

import random
from Agent import *
from Temptation_Game import *
import functions as func


##### Set some parameters here #####
num_experiments = 100           # number of simulation runs to conduct
num_agents = 50                 # population size
random_initialization = False   # initial thresholds random or equidistant
min_dist = 0.01                 # distance between min/max thresholds in A for breaking condition to be fulfilled
RI = 'sucker'                   # imitator agent choice rule: 'sucker'/'random'/'average'/'rewarded'/'tempted'/'punished'


##### start a number of simulation runs #####
for experiment_id in range(num_experiments):

    #### set counters ####
    counter_sim_steps = 0
    counter_updates = 0

    ##### initialize the set of agents A as an array #####
    A = []
    for id_index in range(num_agents):
        new_agent = Agent(id_index)
        if random_initialization:
            new_threshold = random.random()
        else:
            new_threshold = id_index*1.0/num_agents
        new_agent.threshold = new_threshold
        A.append(new_agent)


    ##### run the simulation until the break condition is fulfilled #####
    break_condition = False
    while not break_condition:

        #### Part 1: Pairwise interaction ####

        # compute the interaction pairs
        P = func.random_pairs(A)

        # chose a random x value, and compute actions and payoffs for each interacting pair
        for pair in P:

            # choose a current x value between 0 and 1 and create a temptation game
            x = random.random()
            g = Temptation_Game(x)

            # set the given x value and the action for each agent of the given pair
            for agent in pair:
                agent.xValue = x
                if x < agent.threshold:
                    agent.action = 'C'
                else:
                    agent.action = 'D'

            # set payoff for each agent of the given pair
            agent_j = pair[0]
            agent_k = pair[1]
            agent_j.payoff = g.get_utility(agent_j.action, agent_k.action)
            agent_k.payoff = g.get_utility(agent_k.action, agent_j.action)


        #### Part 2: Threshold Imitation ####

        ### choose an imitator agent with respect to imitator agent choice rule RI

        # basic experiments' choice rules
        if RI == 'sucker':
            possible_imitator_agents = func.suckers(A)
        elif RI == 'random':
            possible_imitator_agents = A
        elif RI == 'average':
            possible_imitator_agents = func.agents_below_same_situation_average(A)
        # agent type choice rules for analysis
        elif RI == 'rewarded':
            possible_imitator_agents = func.rewarded_agents(A)
        elif RI == 'punished':
            possible_imitator_agents = func.punished_agents(A)
        elif RI == 'tempted':
            possible_imitator_agents = func.tempted_agents(A)


        # check if there exist change willing agents
        if len(possible_imitator_agents) > 0:

            # pick a random member from the change willing agents as imitator agent
            imitator_agent = func.random_member(possible_imitator_agents)

            # get all agents with a higher payoff than the imitator agent
            opponents_with_higher_payoffs = func.agents_with_higher_payoff(imitator_agent, A)

            # check if there are opponents with higher payoff
            if len(opponents_with_higher_payoffs) > 0:

                # choose randomly an example agent from the set of opponents with a higher payoff
                example_agent = func.random_member(opponents_with_higher_payoffs)

                # check if the two conditions hold:
                # (i) did the example agent behave differently
                # (ii) were example agent and imitator agent in the same situation, with respect to the imitator agent's threshold
                if imitator_agent.action != example_agent.action and func.is_in_same_situation(imitator_agent, example_agent):

                    # imitate the example agent's threshold as best as possible by coping his x value
                    imitator_agent.threshold = example_agent.xValue

                    # increase counter for updates
                    counter_updates += 1

        # increase counter for simulation steps
        counter_sim_steps += 1


        #### Part 3: Check if breaking condition is fulfilled

        threshold_array = []
        for agent in A:
            threshold_array.append(agent.threshold)

        if max(threshold_array)-min(threshold_array) < min_dist:
            break_condition = True


    ### print the results of the last simulation run ####
    print experiment_id, '\t', counter_sim_steps, '\t', counter_updates, '\t',
    print min(threshold_array), '\t', max(threshold_array), '\t', (min(threshold_array)+max(threshold_array))/2