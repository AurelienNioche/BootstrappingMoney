import itertools

import numpy as np


class History:

    def __init__(self, params):
        self.params = params
        self.n_goods  = self.params['n_goods']

        self.history = {
            "exchanges": [],
            "n_exchanges": [],
            "fitness": [],
            "production_diversity": [],
            "n_producers": [],
            "n_goods_intervention": [],
            "production": []
        }
        self.reset_period_history()

    def reset_period_history(self):
        self._period_history = {
            "exchanges": {(i, j): 0 for i, j in itertools.combinations(range(self.n_goods), r=2)},
            "n_exchanges": 0,
            "n_goods_intervention": [0 for _ in range(self.n_goods)]
        }

    def end_generation(self, agents):

        # Keep a trace of fitness
        fitness = 0
        n_producers       = np.zeros(self.n_goods)
        global_production = np.zeros(self.n_goods)
        for agent in agents:
            fitness += agent.fitness
            n_producers[agent.produced_goods] += 1
            global_production += agent.production
        fitness /= len(agents)

        # Keep a trace of production diversity
        average_production_diversity = np.mean([a.traits['production_diversity'] for a in agents])

        # Keep a trace of exchanges
        for key in self._period_history["exchanges"].keys():
            self._period_history["exchanges"][key] /= max(1, self._period_history["n_exchanges"])

        # For back up
        self.history["exchanges"].append(self._period_history["exchanges"])
        self.history["fitness"].append(fitness)
        self.history["n_exchanges"].append(self._period_history["n_exchanges"])
        self.history["production_diversity"].append(average_production_diversity)
        self.history["n_producers"].append(n_producers)
        self.history["n_goods_intervention"].append(self._period_history["n_goods_intervention"])
        self.history["production"].append(global_production)

        self.reset_period_history()

    def transaction_happens(self, agent1, agent2, transaction):
        """Record a transaction that just happened

        :param agent1: the agent giving `x`, receiving `y`
        :param agent2: the agent giving `y`, receiving `x`
        :param transaction:  a pair `(x, y)` with the good `x` and `y` being exchanged.
        """
        self._period_history["exchanges"][tuple(sorted(transaction))] += 1
        self._period_history["n_exchanges"] += 1
        for good in transaction:
            self._period_history["n_goods_intervention"][good] += 1
