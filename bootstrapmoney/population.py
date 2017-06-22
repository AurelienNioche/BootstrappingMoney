import numpy as np
import itertools as it

from .agent import Agent


class Population:

    def __init__(self, model, params):

        self.n_agents = params["n_agents"]
        self.mod = model

        self.agents = None

    def create_agents(self):

        self.agents = []

        agent_idx = 0

        for i in range(self.n_agents):

            a = Agent(
                n_goods=self.mod.eco.n_goods,
                # Assume an agent doesn't choose production preferences
                production_advantages=
                self.mod.eco.all_possible_production_advantages[i % len(self.mod.eco.all_possible_production_advantages)],
                production_costs=self.mod.eco.production_costs,
                u=self.mod.eco.u,
                idx=i,
                **self.get_agent_random_strategic_attributes()
            )
            self.agents.append(a)
            agent_idx += 1

    def get_agent_random_strategic_attributes(self):

        return {
            "production": self.get_production(),
            "exchange_strategies": self.get_exchange_strategies()
        }

    def get_production(self):

        good_choice = np.random.choice(np.arange(self.mod.eco.n_goods), size=self.mod.eco.max_production)
        unique, counts = np.unique(good_choice, return_counts=True)
        production = np.zeros(self.mod.eco.n_goods, dtype=int)
        for value, count in zip(unique, counts):
            production[value] = count

        return production

    def get_exchange_strategies(self):

        exchange_strategies = np.zeros((self.mod.eco.n_goods, self.mod.eco.n_goods), dtype=object)
        for i in range(self.mod.eco.n_goods):
            for j in range(self.mod.eco.n_goods):
                if i != j:
                    exchange_strategies[i, j] = np.random.choice(self.get_possible_paths(i, j, self.mod.eco.n_goods))

        return exchange_strategies

    @staticmethod
    def get_possible_paths(departure_node, final_node, n_nodes):

        step_nodes = [i for i in range(n_nodes) if i not in [final_node, departure_node]]

        paths = [[(departure_node, final_node)]]

        for i in range(1, len(step_nodes) + 1):

            for j in it.permutations(step_nodes, r=i):
                node_list = [departure_node] + list(j) + [final_node]
                path = [(node_list[i], node_list[i + 1]) for i in range(len(node_list) - 1)]
                paths.append(path)

        return paths

    def consume(self):

        for i in range(self.n_agents):
            self.agents[i].consume()

    def prepare_new_generation(self):
        """At the beginning of a new generation, 'reset' all agents, make them produce and consume if they are able to.
        """

        for i in range(self.n_agents):
            self.agents[i].reset()
            self.agents[i].produce()
            self.agents[i].consume()

        self.mod.eco.market_agents = list(range(self.n_agents))

    def end_generation(self):
        """At the end of generation, compute fitness for all agents."""

        for i in range(self.n_agents):
            self.agents[i].compute_fitness()
