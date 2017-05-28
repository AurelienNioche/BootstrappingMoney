from . import utils


class Economy(object):

    def __init__(self, params, population, history):
        self.population = population
        self.history    = history

    def time_step(self):
        """Update the economy by one time-step"""
        market_agents = self.population.sellers()

        if len(list(market_agents)) > 1:

            for a_i, a_j in utils.derangement(market_agents):
                self.meet(a_i, a_j)

            for a in market_agents:
                a.consume()

    def meet(self, a_i, a_j):
        """Agent a_i and a_j meet and exchange goods if they find an agreeable transaction."""
        transaction = None

        for x, y in a_i.accepted_exchanges:
            if (a_i.stock[x] > 1 and a_j.stock[y] > 1 and (y, x) in a_j.accepted_exchanges):
                transaction = (x, y)

        # # useful for debug
        # K = sorted(set(a_i.accepted_exchanges).intersection([(y, x) for x, y in a_j.accepted_exchanges]))
        # print('{}:{} <-> {}:{}: {} --- {}'.format(a_i.index, a_i.stock, a_j.index, a_j.stock, transaction, K))

        if transaction is not None: # exchange occurs
            a_i.exchange(transaction)
            a_j.exchange(list(reversed(transaction)))

            self.history.transaction_happens(a_i, a_j, transaction)
