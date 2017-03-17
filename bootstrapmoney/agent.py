import numpy as np


class Agent(object):

    name = "Agent"

    def __init__(self, traits, index):

        self.traits = traits
        self.index = index
        self.n_goods = len(self.traits['production_preferences'])

        # state variables
        self.stock = np.zeros(self.n_goods)
        self.production = np.zeros(self.n_goods)
        self.fitness = 0
        self.produced_goods = []

    def seller(self):
        return any(self.stock > 1)

    @property
    def accepted_exchanges(self):
        return self.traits['accepted_exchanges']

    def produce(self, diversity_quantity_mapping):
        prod_div   = self.traits['production_diversity']
        prod_prefs = self.traits['production_preferences']

        quantity_produced = diversity_quantity_mapping[prod_div]
        assert quantity_produced > 0, "At least a quantity of one is produced."
        self.produced_goods = np.array(prod_prefs[:prod_div])
        assert len(self.produced_goods) > 0, "At least one type of good is produced."

        self.production[:] = 0
        self.production[self.produced_goods] = quantity_produced
        self.stock += self.production

    def consume(self):
        n_consumed = np.min(self.stock)
        self.stock[:] -= n_consumed
        self.fitness  += n_consumed

    def exchange(self, transaction):
        """Exchange a good for another (presumably with another agent)"""
        self.stock[transaction[0]] -= 1
        self.stock[transaction[1]] += 1
