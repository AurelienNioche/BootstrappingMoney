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

    def produce(self, diversity_quantity_mapping):

        quantity_produced = diversity_quantity_mapping[self.production_diversity]
        assert quantity_produced, "At least a quantity of one is produced."
        produced_goods = self.production_preferences[:self.production_diversity]
        assert len(produced_goods), "At least one type of good is produced."

        prod = np.zeros(self.n_goods)
        prod[produced_goods] = quantity_produced

        self.stock += prod

    def consume(self):

        while self.stock.all() >= 1:

            self.stock[:] -= 1
            self.fitness += 1

    def proceed_to_exchange(self, exchange):

        self.stock[exchange[0]] -= 1
        self.stock[exchange[1]] += 1

    def get_strategy(self):

        all_attr = vars(self)
        for i in ["n_goods", "stock"]:
            all_attr.pop(i)


def create_agent(n_goods=3, idx=0):

    return Agent(
        n_goods=n_goods,
        production_preferences=np.random.permutation(np.arange(n_goods)),
        production_diversity=np.random.randint(1, n_goods + 1),
        goods_to_buy=np.random.choice(np.arange(n_goods), size=np.random.randint(0, n_goods + 1)),
        goods_to_sell=np.random.choice(np.arange(n_goods), size=np.random.randint(0, n_goods + 1)),
        idx=idx)


if __name__ == "__main__":


    a = create_agent()
    print(vars(a))