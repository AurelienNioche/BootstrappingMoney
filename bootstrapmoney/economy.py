from . import utils


class Economy(object):

    def __init__(self, params, population, history):
        self.population = population
        self.history    = history

    def time_step(self):
        """Update the economy by one time-step"""
        market_agents = [agent for agent in self.population.agents if any(agent.stock > 1)]

        if len(market_agents) > 1:
            for a_i, a_j in utils.derangement(market_agents):
                self.meet(a_i, a_j)

            for a in market_agents:
                a.consume()

    def meet(self, a_i, a_j):
        """Agent a_i and a_j meet and exchange goods if they find an agreeable transaction."""
        transaction = None

        for x, y in a_i.traits.accepted_exchanges:
            if (a_i.stock[x] > 1 and a_j.stock[y] > 1 and (y, x) in a_j.traits.accepted_exchanges):
                transaction = (x, y)
                break

        # # useful for debug
        # K = sorted(set(a_i.accepted_exchanges).intersection([(y, x) for x, y in a_j.accepted_exchanges]))
        # print('{}:{} <-> {}:{}: {} --- {}'.format(a_i.index, a_i.stock, a_j.index, a_j.stock, transaction, K))

        if transaction is not None: # exchange occurs
            self.exchange(a_i, a_j, transaction)
            self.history.transaction_happens(a_i, a_j, transaction)

    def exchange(self, a_i, a_j, transaction):
        """Complete the transation (x, y): `a_i` gives `x` to a_j, receives `y` from him."""
        x, y = transaction
        a_i.stock[x] -= 1
        a_j.stock[x] += 1
        a_i.stock[y] += 1
        a_j.stock[y] -= 1
