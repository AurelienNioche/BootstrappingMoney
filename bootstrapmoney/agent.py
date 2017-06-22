import numpy as np


class Agent(object):

    name = "Agent"

    def __init__(self, u, production, production_advantages, exchange_strategies, production_costs, n_goods, idx):

        self.n_goods = n_goods
        self.idx = idx
        self.stock = np.zeros(self.n_goods, dtype=int)

        self.production = np.asarray(production, dtype=int)
        self.production_advantages = np.asarray(production_advantages)
        self.production_costs = np.asarray(production_costs)

        self.exchange_strategies = exchange_strategies

        self.u = u

        self.n_consumption = 0
        self.fitness = 0

        self.exchange = None

        self.involved = False
        self.goal = None
        self.current_strategy = None
        self.step = 0

    def produce(self):

        self.stock += self.production

    def which_exchange_do_you_want_to_try(self):

        if not self.involved:

            min_stock = min(self.stock)
            self.goal = np.random.choice(np.arange(self.n_goods)[self.stock == min_stock])

            max_stock = max(self.stock)
            to_be_sold = np.random.choice(np.arange(self.n_goods)[self.stock == max_stock])

            self.current_strategy = self.exchange_strategies[to_be_sold, self.goal]
            assert self.current_strategy != 0, "Stocks should not be empty!"

            self.step = 0
            self.involved = True

        self.exchange = self.current_strategy[self.step]

        return self.exchange

    def consume(self):

        n_consumption_t = min(self.stock)
        if n_consumption_t:
            self.stock[:] -= n_consumption_t
            self.n_consumption += n_consumption_t

    def proceed_to_exchange(self):

        self.stock[self.exchange[0]] -= 1
        self.stock[self.exchange[1]] += 1

        if self.exchange[1] == self.goal:
            self.involved = False

        else:
            self.step += 1

    def get_strategic_attributes(self):

        return {
            "production": self.production,
            "exchange_strategies": self.exchange_strategies
        }

    def compute_fitness(self):

        pos = self.u * self.n_consumption
        neg = sum([self.production[i] * self.production_costs[i] * self.production_advantages[i]
                   for i in range(self.n_goods)])

        self.fitness = \
            pos - neg

    def reset(self):

        self.stock[:] = 0
        self.fitness = 0
        self.n_consumption = 0
        self.involved = False

