import itertools

import numpy as np

from .agent import Agent, Traits


class Population:

    def __init__(self, params):
        self.params = params

        self.n_goods          = params['n_goods']
        self.n_agents         = params['n_agents']
        self.p_mutation       = params['p_mutation']
        self.production_costs = params['production_costs']
        self.n_mating         = int(params['mating_rate'] * self.n_agents) #FIXME incoherent formula

        self.all_possible_exchanges = list(itertools.permutations(range(self.n_goods), r=2))
        self.all_possible_production_difficulties = list(itertools.permutations(self.params['production_difficulty']))
        np.random.shuffle(self.all_possible_production_difficulties)

        self.create_population()

    def __len__(self):
        return len(self.agents)

    def create_population(self):
        """Create the population of agents."""
        self.agents = []
        for index in range(self.n_agents):
            evolvable = self._random_evolvable_traits()
            production_difficulty = self.all_possible_production_difficulties[index % len(self.all_possible_production_difficulties)]
            traits = Traits(evolvable['production'], production_difficulty, evolvable['accepted_exchanges'])
            self.agents.append(Agent(traits, index, self.params['production_costs']))

    def _random_evolvable_traits(self):
        """Create a random agent's traits."""
        production = np.random.randint(0, self.params['max_production'] + 1, size=self.n_goods)
        np.random.shuffle(self.all_possible_exchanges)
        accepted_exchanges = self.all_possible_exchanges[:np.random.randint(1, len(self.all_possible_exchanges))]

        return {"production": production, "accepted_exchanges": accepted_exchanges}


        ## Evolutionary functions ##

    def reset_agents(self):
        """Reset the state of all agents. Called to prepare each new generation."""
        for agent in self.agents:
            agent.reset()

    #@profile
    def evolve_agents(self):
        """Evolve the population of agents."""
        for agent_to_reproduce, agent_to_replace in self.agents_selection():
            self.reproduce(agent_to_reproduce, agent_to_replace.index)

    def agents_selection(self):
        """Select agents to reproduce through mutation and agents to replace.

        Pairs of agents (one to reproduce, one to replace) are created between agents with the same
        production preferences.
        """
        for agent in self.agents:
            agent.fitness = agent.consumed * self.params['utility'] - agent.costs

        prod_diff_sets = {} # sets of agents with the same production preferences.
        for agent in self.agents: # important in case of equal fitness #HUGH?
            prod_diff_sets.setdefault(agent.traits.production_difficulty, [])
            prod_diff_sets[agent.traits.production_difficulty].append(agent)
        prod_diff_sets = list(prod_diff_sets.values()) # converting to lists
        np.random.shuffle(prod_diff_sets)
        for agent_set in prod_diff_sets:
            agent_set.sort(key=lambda agent: agent.fitness)
        # prod_diff_sets = [agent_set.sort(key=lambda agent: agent.fitness) for agent_set in prod_diff_sets]

        # only self.n_mating agents will evolve
        mutation_counts = [0 for _ in prod_diff_sets]
        #print(self.n_mating)
        for i in range(self.n_mating):
            j = i % len(prod_diff_sets)
            if len(prod_diff_sets[j]) > mutation_counts[j]:
                mutation_counts[j] += 1

        #print(mutation_counts)

        reproduction_pairs = []
        for agent_set, mutation_count in zip(prod_diff_sets, mutation_counts):
            agents_to_imitate  = agent_set[-mutation_count:]
            agents_to_replace = agent_set[:mutation_count]
            reproduction_pairs.extend(zip(agents_to_imitate, agents_to_replace))

        return reproduction_pairs

    #@profile
    def reproduce(self, agent, index):
        """Reproduce an agent through replacements of random attributes.

        :param agent:  the agent to be reproduced.
        :param index:  the destination index for the new agent.
        """
        new_traits = self._random_evolvable_traits()

        for key, value in agent.traits.evolvable:
            if np.random.random() > self.p_mutation:  # we keep this trait from the source agent.
                new_traits[key] = value

        traits = Traits(new_traits['production'], agent.traits.production_difficulty,
                        new_traits['accepted_exchanges'])

        self.agents[index].traits = traits
        self.agents[index].compute_costs(self.production_costs)

        # self.agents[index] = Agent(traits, index, self.params['production_costs'])
