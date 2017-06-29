import itertools as it

import numpy as np


class Economy(object):

    def __init__(self, model, params):

        self.n_goods = len(params["production_costs"])

        self.all_possible_exchanges = list(it.permutations(range(self.n_goods), r=2))
        self.all_possible_production_difficulty = \
            list(it.permutations(params["production_difficulty"], r=self.n_goods))
        self.production_costs = params["production_costs"]
        self.max_production = params["max_production"]
        self.u = params["utility"]
        self.exchange_cost = params["exchange_cost"]

        self.markets = {i: [] for i in it.permutations(range(self.n_goods), r=2)}
        self.exchanges_types = [i for i in it.combinations(range(self.n_goods), r=2)]

        self.exchanges_labels = {e: i for i, e in enumerate(self.exchanges_types)}

        self.mod = model

    # @profile
    def manage_exchanges(self):
        """Organize encounters between agents supposing that markets specialized in pairs of goods exist."""

        for k in self.markets:
            self.markets[k] = []

        for agent in self.mod.pop.agents:
            if sum(agent.stock) > self.n_goods:
                agent_choice = agent.which_exchange_do_you_want_to_try()
                self.markets[agent_choice].append(agent.idx)

        for i, j in self.exchanges_types:

            market = [self.markets[(i, j)], self.markets[(j, i)]]
            n = [len(i) for i in market]
            arg_sorted = np.argsort(n)
            min_n = n[arg_sorted[0]]

            if min_n:

                self.mod.hist.back_up["exchanges"][self.mod.t, self.exchanges_labels[(i, j)]] += min_n
                self.mod.hist.back_up["n_exchanges"][self.mod.t] += min_n

                for good in (i, j):
                    self.mod.hist.back_up["n_goods_intervention"][self.mod.t, good] += min_n

                # Select randomly agents in the part the most populated of the market
                for idx in np.random.choice(market[arg_sorted[-1]], size=min_n, replace=False):
                    self.mod.pop.agents[idx].proceed_to_exchange()

                for idx in market[arg_sorted[0]]:
                    self.mod.pop.agents[idx].proceed_to_exchange()
