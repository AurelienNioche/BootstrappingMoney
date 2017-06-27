import numpy as np


class Agent(object):

    name = "Agent"

    def __init__(self, production, production_difficulty, exchange_strategies, idx,
                 model):

        # For identifying the agent (mainly useful for debug purpose
        self.idx = idx

        # Strategic traits
        self.production = np.asarray(production, dtype=int)
        self.production_difficulty = np.asarray(production_difficulty)
        self.exchange_strategies = exchange_strategies

        # Model and parameters of the model
        self.mod = model
        self.n_goods = model.eco.n_goods
        self.u = model.eco.u
        self.production_costs = model.eco.production_costs
        self.exchange_cost = model.eco.exchange_cost

        # Attributes that will evolve inside a generation
        self.n_consumption = 0
        self.n_exchange = 0
        self.fitness = 0
        self.stock = np.zeros(self.n_goods, dtype=int)

        # For current exchange
        self.exchange = None

        # For current strategy
        self.current_strategy = None
        self.involved = False
        self.goal = None
        self.step = 0

    def produce(self):
        """
        Increase stock by your amount of production
        :return:
        """

        self.stock += self.production

    def which_exchange_do_you_want_to_try(self):

        self.n_exchange += 1

        if not self.involved:

            min_stock = min(self.stock)
            self.goal = np.random.choice(np.arange(self.n_goods)[self.stock == min_stock])

            max_stock = max(self.stock)
            to_be_sold = np.random.choice(np.arange(self.n_goods)[self.stock == max_stock])

            self.current_strategy = self.exchange_strategies[(to_be_sold, self.goal)]

            # For backup
            ex_hist = self.mod.hist.back_up["n_strategies"][self.mod.t]
            ex_hist[self.current_strategy] = ex_hist.get(self.current_strategy, 0) + 1

            self.step = 0
            self.involved = True

        self.exchange = self.current_strategy[self.step]

        return self.exchange

    def consume(self):
        """
        For consuming, agent needs to have a unit of each good
        :return:
        """

        n_consumption_t = min(self.stock)
        if n_consumption_t:
            self.stock[:] -= n_consumption_t
            self.n_consumption += n_consumption_t

    def proceed_to_exchange(self):
        """
        Decrease of one unit for the good given, increase by one for the good obtained.
        If goal of current strategy is reached, agent is not involved anymore in a strategy.
        He will choose a new one for the next time step.
        Otherwise, he goes to the next exchange step prescribed by the current strategy
        :return:
        """

        self.stock[self.exchange[0]] -= 1
        self.stock[self.exchange[1]] += 1

        if self.exchange[1] == self.goal:
            self.involved = False

        else:
            self.step += 1

    def compute_fitness(self):

        """
        Fitness is composed of two parts: one counts as negative, the other counts as positive.
         Positive is based on consumption.
         Negative is based on production and exchange.
        :return:
        """

        pos = self.u * self.n_consumption
        neg = sum(self.production * self.production_costs * self.production_difficulty) \
            + self.n_exchange * self.exchange_cost

        self.fitness = \
            pos - neg

        return self.fitness

    def reset(self):

        self.stock[:] = 0
        self.fitness = 0
        self.n_consumption = 0
        self.n_exchange = 0
        self.involved = False
