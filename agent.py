import numpy as np


class Agent(object):

    name = "Agent"

    def __init__(self, u, production, production_advantages, accepted_exchanges, production_costs, n_goods, idx):

        self.n_goods = n_goods
        self.idx = idx
        self.stock = np.zeros(self.n_goods, dtype=int)

        self.production = np.asarray(production, dtype=int)
        self.production_advantages = np.asarray(production_advantages)
        self.production_costs = np.asarray(production_costs)

        self.accepted_exchanges = accepted_exchanges

        self.u = u

        self.n_consumption = 0
        self.fitness = 0

    def produce(self):

        self.stock += self.production

    def consume(self):

        n_consumption_t = min(self.stock)

        self.stock[:] -= n_consumption_t
        self.n_consumption += n_consumption_t

    def proceed_to_exchange(self, exchange):

        self.stock[exchange[0]] -= 1
        self.stock[exchange[1]] += 1

    def get_strategic_attributes(self):

        str_attributes = {
            "production": self.production,
            "accepted_exchanges": self.accepted_exchanges
        }

        return str_attributes

    def compute_fitness(self):

        pos = self.u * self.n_consumption
        neg = 0
        for i in range(self.n_goods):
            neg += self.production[i] * self.production_costs[i] * self.production_advantages[i]

        self.fitness = \
            pos - neg

    def get_production(self):

        return self.production

    def reset(self):

        self.stock[:] = 0
        self.fitness = 0
        self.n_consumption = 0

if __name__ == "__main__":

    pass
