import numpy as np


class History:

    def __init__(self, model):

        self.back_up = {}
        self.mod = model

    def setup(self):

        self.back_up.update(
            {
                "exchanges": np.zeros((self.mod.evo.n_generations, len(self.mod.eco.exchanges_types))),
                "n_exchanges": np.zeros(self.mod.evo.n_generations),
                "fitness": np.zeros(self.mod.evo.n_generations),
                "production_diversity": np.zeros(self.mod.evo.n_generations),
                "n_producers": np.zeros((self.mod.evo.n_generations, self.mod.eco.n_goods)),
                "n_goods_intervention": np.zeros((self.mod.evo.n_generations, self.mod.eco.n_goods)),
                "production": np.zeros((self.mod.evo.n_generations, self.mod.eco.n_goods)),
                "exchanges_labels": self.mod.eco.exchanges_labels,
                "exchanges_types": self.mod.eco.exchanges_types
            }
        )
