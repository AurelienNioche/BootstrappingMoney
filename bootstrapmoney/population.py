import itertools

import numpy as np


def create_diversity_quantity_mapping(n):

    mapping = [1]

    f = lambda x: 2 * (x + 1) ** 2

    for raw, diversity in enumerate(range(n - 1, 0, -1)):
        previous_quantity_of_production = mapping[-1] * (diversity + 1)
        result = round((previous_quantity_of_production + f(raw)) / diversity)
        mapping.append(result)
    mapping.append(0)
    mapping.reverse()

    return mapping



class Population:

    def __init__(self, params, p_mutation, mating_rate):
        self.params = params

        self.n_agents   = params['n_agents']
        self.p_mutation = params['p_mutation']
        self.n_mating   = int(mating_rate * self.n_agents)

        self.all_possible_exchanges = [tuple(p) for p in itertools.permutations(range(self.n_goods), r=2))]
        self.all_possible_production_preferences = np.random.permutation(
            tuple(p) for p in itertools.permutations(range(self.n_goods), r=self.n_goods))

        self.agents = self.create_population()

        self.diversity_quantity_mapping = create_diversity_quantity_mapping(self.n_goods)

    def __len__(self):
        return self.n_agents

    def sellers(self):
        """Agents that have more than one instance of at least one good.""""
        return (agent for agent in self.agents if agent.seller())

    def create_population(self):
        self.agents = [self.create_agent(index) for index in range(len(self))]

    def create_agent(self, index, traits=None):
        """Create an agent with random traits"""
        if traits is None:
            traits = self._random_traits()
        return Agent(traits, index=index)

    def _random_traits(self, index):
        """Create a random agent's traits."""


        n_accepted_exchanges = np.random.randint(1, len(self.all_possible_exchanges))
        accepted_exchanges = np.random.permutation(self.all_possible_exchanges)[:n_accepted_exchanges]

        production_preferences = self.all_possible_production_preferences[index % len(self.all_possible_production_preferences)]

        return {'production_preferences': production_preferences,
                'production_diversity': np.random.randint(1, self.n_goods + 1),
                'accepted_exchanges': accepted_exchanges}


        ## Evolutionary functions ##

    def reset_agents(self, diversity_quantity_mapping):
        """Reset the state of all agents. Called to prepare each new generation."""
        for agent in self.agents:
            agent.stock[:] = 0
            agent.fitness  = 0
            agent.produce(self.diversity_quantity_mapping)
            agent.consume()

    def evolve_agents(self):
        """Evolve the population of agents."""
        for agent_to_reproduce, agent_to_replace in self.agents_selection():
            self.reproduce(agent_to_reproduce, agent_to_replace.index)

    def agents_selection(self):
        """Select agents to reproduce through mutation and agents to replace.

        Pairs of agents (one to reproduce, one to replace) are created between agents with the same
        production preferences.
        """
        selected_to_be_copied, selected_to_be_changed = [], []

        prod_pref_sets = {} # sets of agents with the same production preferences.
        for a in self.agents: # important in case of equal fitness #HUGH?
            prod_pref_sets.setdefault(a.production_preferences, [])
            prod_pref_sets[a.production_preferences].append(a)
        prod_pref_sets = list(prod_pref_sets.values()) # converting to lists


        # only self.n_mating sets will evolve, with a probability proportional to their size
        sets_to_evolve = np.random.choice(prod_pref_sets, size=self.n_mating,
                                          p=[len(e)/len(self) for e in prod_pref_sets])

        reproduction_pairs = []
        for agent_set in sets_to_evolve:
            agent_set.sort(key=lambda x: x.fitness)
            reproduction_pairs.extend(zip(np.random.permutation(agent_set[:-len(agent_set)//2]),
                                          np.random.permutation(agent_set[len(agent_set)//2:]))
        return reproduction_pairs

    def reproduce(self, agent, index):
        """Reproduce an agent through replacements of random attributes.

        :param agent:  the agent to be reproduced.
        :param index:  the destination index for the new agent.
        """
        new_traits = self._random_traits()
        p_mutate = np.random.random(len(agent.traits))

        for key, p_i in zip(agent.traits.keys(), p_mutate):
            if p_i > self.p_mutation: # we keep this trait from the source agent.
                new_traits[key] = agent.traits[key]

        self.agents[index] = self.create_agent(index, traits=new_traits)
