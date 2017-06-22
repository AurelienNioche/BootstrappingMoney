import itertools as it

import numpy as np


class Economy(object):

    def __init__(self, model, params):

        self.n_goods = params["n_goods"]

        self.all_possible_exchanges = list(it.permutations(range(self.n_goods), r=2))
        self.all_possible_production_advantages = \
            np.random.permutation(
                list(it.permutations(params["production_difficulty"], r=self.n_goods))
            )
        self.production_costs = params["production_costs"]
        self.max_production = params["max_production"]
        self.u = params["utility"]

        self.markets = dict([(i, []) for i in it.permutations(range(self.n_goods), r=2)])
        self.exchanges_types = [i for i in it.combinations(range(self.n_goods), r=2)]

        self.exchanges_labels = dict([(e, i) for i, e in enumerate(self.exchanges_types)])

        self.mod = model

        self.g = 0

    def manage_exchanges(self):
        """Organize encounters between agents supposing that markets specialized in pairs of goods exist."""

        for k in self.markets:
            self.markets[k] = []

        for agent in self.mod.pop.agents:
            agent_choice = agent.which_exchange_do_you_want_to_try()
            self.markets[agent_choice].append(agent.idx)

        success_idx = []
        for i, j in self.exchanges_types:

            a1 = self.markets[(i, j)]
            a2 = self.markets[(j, i)]
            min_a = int(min([len(a1), len(a2)]))

            if min_a:

                self.mod.hist.back_up["exchanges"][self.g, self.exchanges_labels[(i, j)]] += min_a
                self.mod.hist.back_up["n_exchanges"][self.g] += min_a

                for good in (i, j):
                    self.mod.hist.back_up["n_goods_intervention"][self.g, good] += min_a

                success_idx += list(np.random.choice(a1, size=min_a))
                success_idx += list(np.random.choice(a2, size=min_a))

        for idx in success_idx:
            self.mod.pop.agents[idx].proceed_to_exchange()

    def compute_stats(self):
        """Compute stats for keeping a trace of system dynamics"""

        # Keep a trace of fitness, number of producers per type of good and global production
        fitness = 0
        n_producers = np.zeros(self.n_goods)
        global_production = np.zeros(self.n_goods)

        for i in range(self.mod.pop.n_agents):

            fitness += self.mod.pop.agents[i].fitness

            production = self.mod.pop.agents[i].production
            for j in range(self.n_goods):
                if production[j] > 0:
                    n_producers[j] += 1
            global_production += production

        fitness /= self.mod.pop.n_agents

        # Keep a trace of production diversity
        production_diversity = [sum(a.production[:] != 0) for a in self.mod.pop.agents]
        average_production_diversity = np.mean(production_diversity)

        # For back up
        self.mod.hist.back_up["fitness"][self.g] = fitness
        self.mod.hist.back_up["production_diversity"][self.g] = average_production_diversity
        self.mod.hist.back_up["n_producers"][self.g, :] = n_producers
        self.mod.hist.back_up["production"][self.g, :] = global_production

        self.g += 1

