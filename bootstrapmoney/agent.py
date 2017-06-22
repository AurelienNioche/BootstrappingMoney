import numpy as np


class Traits:

    def __init__(self, production, production_difficulty, accepted_exchanges):
        self.production_difficulty = tuple(production_difficulty)
        self.production            = np.asarray(production)
        self.accepted_exchanges    = set(accepted_exchanges)

    @property
    def evolvable(self):
        """Evolvable traits are the old strategic traits"""
        return (("production", self.production) , ("accepted_exchanges", self.accepted_exchanges))


class Agent(object):

    name = "Agent"

    def __init__(self, traits, index, production_costs):
        self.traits  = traits
        self.index   = index
        self.n_goods = len(self.traits.production)
        self.costs = self.compute_costs(production_costs)

        # state variables
        self.stock     = np.zeros(self.n_goods, dtype=int)
        self.produced_goods = []
        self.consumed = 0
        self.fitness = 0


    def compute_costs(self, production_costs):
        """Compute the costs of production of an agent. This is the negative part of the fitness score"""
        c = 0
        for pcost_i, pdiff_i, p_i in zip(production_costs, self.traits.production_difficulty, self.traits.production):
            c += pcost_i * pdiff_i * p_i
        return c

    def __repr__(self):
        return 'Agent_{}'.format(self.index)

    def produce(self):
        self.stock += self.traits.production

    def consume(self):
        n_consumed = min(self.stock)  # note: `min` faster than `np.min` for small arrays
        self.stock[:]  -= n_consumed
        self.consumed += n_consumed

    def exchange(self, transaction):
        """Exchange a good for another (presumably with another agent)"""
        self.stock[transaction[0]] -= 1
        self.stock[transaction[1]] += 1

    def reset(self):
        self.stock[:] = 0
        self.consumed  = 0
        self.produce()
        self.consume()
