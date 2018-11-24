import random


### returns a random member of the input array ###
def random_member(input_array):

    index = random.randint(0,len(input_array)-1)

    return input_array[index]


### returns randomly chosen pairs from an input array ###
def random_pairs(input_array):

    # make a copy of the input array to work with
    input_array_copy = []
    for entry in input_array:
        input_array_copy.append(entry)

    # create an array of pairs
    pair_array = []
    for pair_count in range(len(input_array)/2):
        index1 = random.randint(0,len(input_array_copy)-1)
        pair_member1 = input_array_copy.pop(index1)
        index2 = random.randint(0,len(input_array_copy)-1)
        pair_member2 = input_array_copy.pop(index2)
        pair_array.append([pair_member1,pair_member2])

    # return array of pairs
    return pair_array


### returns True, iff agent and opponent were in same situation with respect to agent's threshold ###
def is_in_same_situation(agent, opponent):

    return_boolean = False

    if agent.xValue < agent.threshold and opponent.xValue < agent.threshold:
        return_boolean = True
    elif agent.xValue > agent.threshold and opponent.xValue > agent.threshold:
        return_boolean = True

    return return_boolean


### returns the set of agents that have scored better than agent ###
def agents_with_higher_payoff(agent, agent_set):

    possible_agents = []

    for opponent in agent_set:
        if agent.payoff < opponent.payoff:
            possible_agents.append(opponent)

    return possible_agents


### returns all agents in agent_set that have scored below the average of all agents in the same situation ###
def agents_below_same_situation_average(agent_set):

    possible_agents = []

    for agent in agent_set:

        accumulated_payoff = 0.0
        num_opponents = 0

        for agent2 in agent_set:
            if is_in_same_situation(agent, agent2):

                accumulated_payoff += agent2.payoff
                num_opponents += 1

        average_payoff = -1.0
        if num_opponents > 0:
            average_payoff = accumulated_payoff/num_opponents

        if agent.payoff < average_payoff:
            possible_agents.append(agent)

    return possible_agents


### returns all agents in agent_set that were suckers in the last round: agents that scored -0.5 ###
def suckers(agent_set):

    possible_agents = []

    for agent in agent_set:
        if agent.payoff == -0.5:
            possible_agents.append(agent)

    return possible_agents


### returns all agents in agent_set that were punished in the last round: agents that scored 0.0 ###
def punished_agents(agent_set):

    possible_agents = []

    for agent in agent_set:
        if agent.payoff == 0.0:
            possible_agents.append(agent)

    return possible_agents


### returns all agents in agent_set that were rewarded in the last round: agents that cooperated and scored 0.5 ###
def rewarded_agents(agent_set):

    possible_agents = []

    for agent in agent_set:
        if agent.payoff == 0.5 and agent.action == 'C':
            possible_agents.append(agent)

    return possible_agents


### returns all agents in agent_set that were tempted in the last round: agents that defected and scored above 0.0 ###
def tempted_agents(agent_set):

    possible_agents = []

    for agent in agent_set:
        if agent.payoff > 0.0 and agent.action == 'D':
            possible_agents.append(agent)

    return possible_agents