import numpy as np


class Agent(object):

    name = "Agent"

    def __init__(self, production_preferences, production_diversity, goods_to_sell, goods_to_buy, n_goods, idx):

        self.production_preferences = production_preferences
        self.production_diversity = production_diversity

        self.goods_to_sell = goods_to_sell
        self.goods_to_buy = goods_to_buy

        self.n_goods = n_goods

        self.idx = idx

        self.stock = np.zeros(self.n_goods)

        self.fitness = 0
        self.produced_goods = []

    def produce(self, diversity_quantity_mapping):

        quantity_produced = diversity_quantity_mapping[self.production_diversity]
        assert quantity_produced, "At least a quantity of one is produced."
        self.produced_goods = self.production_preferences[:self.production_diversity]
        assert len(self.produced_goods), "At least one type of good is produced."

        prod = np.zeros(self.n_goods)
        prod[self.produced_goods] = quantity_produced

        self.stock += prod

    def consume(self):

        n_consumption = np.min(self.stock)

        self.stock[:] -= n_consumption
        self.fitness += n_consumption

    def proceed_to_exchange(self, exchange):

        self.stock[exchange[0]] -= 1
        self.stock[exchange[1]] += 1

    def get_strategic_attributes(self):

        all_attr = vars(self).copy()

        for i in ["n_goods", "stock", "fitness", "produced_goods", "production_preferences", "idx"]:
            all_attr.pop(i)

        return all_attr

    def get_produced_goods(self):

        return self.produced_goods


def create_agent(n_goods=3, idx=0):

    return Agent(
        n_goods=n_goods,
        production_preferences=np.random.permutation(np.arange(n_goods)),
        production_diversity=np.random.randint(1, n_goods + 1),
        goods_to_buy=np.random.choice(np.arange(n_goods), size=np.random.randint(1, n_goods + 1), replace=False),
        goods_to_sell=np.random.choice(np.arange(n_goods), size=np.random.randint(1, n_goods + 1), replace=False),
        idx=idx)


if __name__ == "__main__":

    a = create_agent()
    print(vars(a))