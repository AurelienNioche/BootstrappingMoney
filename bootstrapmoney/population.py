import numpy as np
import itertools as it

from .agent import Agent


class Population:

    def __init__(self, model, params):

        self.n_agents = params["n_agents"]
        self.n_goods = len(params["production_costs"])
        self.p_direct = params["p_direct"]

        self.mod = model

        self.agents = []
        self.possible_exchange_strategies = {}

        self.random_attribute = {
            "production": self.random_production,
            "exchange_strategies": self.random_exchange_strategies
        }

        self.agents_fitness = np.zeros(self.n_agents)

        self.sorted_idx_per_production_difficulty = None
        self.p_exchange_strategies = None

    def setup(self):

        self.sorted_idx_per_production_difficulty = {
            tuple(i): []
            for i in self.mod.eco.all_possible_production_difficulty
        }
        self.create_possible_exchange_strategies()
        self.create_p_exchange_strategies()
        self.create_agents()

    def create_agents(self):
        """
        Create population.
        Each agent have particular production difficulties (or facilities).
        Each agent 'chooses' (he will be selected on this basis) his production strategy and exchange strategies.
        :return:
        """

        possible_prod_difficulty = np.random.permutation(self.mod.eco.all_possible_production_difficulty)

        for i in range(self.n_agents):

            prod_difficulty = possible_prod_difficulty[i % len(self.mod.eco.all_possible_production_difficulty)]

            self.sorted_idx_per_production_difficulty[tuple(prod_difficulty)].append(i)

            a = Agent(
                # Assume an agent doesn't choose production preferences (i.e. what is the more easy for him).
                production_difficulty=prod_difficulty,
                # Assume an agent 'chooses' his production strategy.
                production=self.random_production(),
                # Assume an agent 'chooses' his exchange strategies.
                exchange_strategies=self.random_exchange_strategies(),
                model=self.mod,
                idx=i
            )
            self.agents.append(a)

    def random_production(self):
        """"Production is one of the two traits of agents that will evolve.
        Here is a method to generate it randomly.
        """
        good_choice = np.random.choice(np.arange(self.n_goods), size=self.mod.eco.max_production)
        unique, counts = np.unique(good_choice, return_counts=True)
        production = np.zeros(self.n_goods, dtype=int)
        for value, count in zip(unique, counts):
            production[value] = count

        return production

    def random_exchange_strategies(self):
        """Exchange strategies are one of the two traits of agents that will evolve.
        Here is a method to generate it randomly.
        """
        exchange_strategies = {}
        for i, j in it.permutations(range(self.n_goods), r=2):
            exchange_strategies[(i, j)] = np.random.choice(
                self.possible_exchange_strategies[(i, j)],
                p=self.p_exchange_strategies)

        return exchange_strategies

    def create_possible_exchange_strategies(self):
        """Create all possible exchange strategies.
        It will be used for choosing a particular set of exchange strategies."""

        for i, j in it.permutations(range(self.n_goods), r=2):
            self.possible_exchange_strategies[(i, j)] = self.get_possible_paths(i, j)

    def create_p_exchange_strategies(self):

        self.p_exchange_strategies = [self.p_direct, ] + \
            [(1 - self.p_direct) / (len(self.possible_exchange_strategies[(0, 1)]) - 1), ] \
             * (len(self.possible_exchange_strategies[(0, 1)]) - 1)

    def get_possible_paths(self, i, j):

        paths = [((i, j),)]
        for k in range(self.n_goods):
            if k not in [i, j]:
                paths.append(
                    ((i, k), (k, j))
                )
        return paths

    def consume(self):
        """Make all agents consume their goods."""
        for agent in self.agents:
            agent.consume()

    def prepare_new_generation(self):
        """At the beginning of a new generation, 'reset' the stock of all agents.
        Agents then produce goods, and consume them if they are able to.
        """
        for agent in self.agents:
            agent.reset()
            agent.produce()
            agent.consume()

    def end_generation(self):
        """At the end of generation, compute fitness for all agents."""
        self.agents_fitness[:] = [agent.compute_fitness() for agent in self.agents]
