import numpy as np


class Traits:

    def __init__(self, production, production_difficulty, accepted_exchanges):
        self.production_difficulty = tuple(production_difficulty)
        self.production            = np.asarray(production)
        self.accepted_exchanges    = np.asarray(accepted_exchanges)

    @property
    def evolvable(self):
        """Evolvable traits are the old strategic traits"""
        return {"production": self.production,
                "accepted_exchanges": self.accepted_exchanges}


class Agent(object):

    name = "Agent"

    def __init__(self, traits, index):
        self.traits  = traits
        self.index   = index
        self.n_goods = len(self.traits.production)

        # state variables
        self.stock     = np.zeros(self.n_goods, dtype=int)
        self.produced_goods = []
        self.consummed = 0

    def __repr__(self):
        return 'Agent_{}'.format(self.index)

    def seller(self):
        return any(self.stock > 1)

    @property
    def accepted_exchanges(self):
        return self.traits.accepted_exchanges

    def produce(self):
        self.stock += self.traits.production

    def consume(self):
        n_consumed = np.min(self.stock)
        self.stock[:]  -= n_consumed
        self.consummed += n_consumed

    def exchange(self, transaction):
        """Exchange a good for another (presumably with another agent)"""
        self.stock[transaction[0]] -= 1
        self.stock[transaction[1]] += 1

    def reset(self):
        self.stock[:] = 0
        self.consummed  = 0
        self.produce()
        self.consume()
