import numpy as np


class Agent(object):

    name = "Agent"

    def __init__(self, production_preferences, production_diversity, accepted_exchanges, n_goods, idx):

        self.production_preferences = production_preferences
        self.production_diversity = production_diversity

        self.accepted_exchanges = accepted_exchanges

        self.n_goods = n_goods

        self.idx = idx

        self.stock = np.zeros(self.n_goods)

        self.fitness = 0
        self.produced_goods = []
        self.production = np.zeros(self.n_goods)

    def produce(self, diversity_quantity_mapping):

        quantity_produced = diversity_quantity_mapping[self.production_diversity]
        assert quantity_produced, "At least a quantity of one is produced."
        self.produced_goods = self.production_preferences[:self.production_diversity]
        assert len(self.produced_goods), "At least one type of good is produced."

        self.production[:] = 0
        self.production[self.produced_goods] = quantity_produced

        self.stock += self.production

    def consume(self):

        n_consumption = np.min(self.stock)

        self.stock[:] -= n_consumption
        self.fitness += n_consumption

    def proceed_to_exchange(self, exchange):

        self.stock[exchange[0]] -= 1
        self.stock[exchange[1]] += 1

    def get_strategic_attributes(self):

        all_attr = vars(self).copy()

        for i in ["n_goods", "stock", "fitness", "produced_goods", "production", "production_preferences", "idx"]:
            all_attr.pop(i)

        return all_attr

    def get_production_stats(self):

        return self.produced_goods, self.production

if __name__ == "__main__":

    pass
