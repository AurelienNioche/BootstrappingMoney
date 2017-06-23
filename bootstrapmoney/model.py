import numpy as np

from tqdm import tqdm

from . import economy, population, history, evolution, statistician


class Model:
    """Model class.

    Create the elements of the model, orchestrate their interaction, and keeps
    an history of the evolution of the economy.
    """

    def __init__(self, params):
        self.params = params

        np.random.seed(self.params['random_seed'])

        self.pop = population.Population(params=params, model=self)
        self.eco = economy.Economy(params=params, model=self)
        self.evo = evolution.Evolution(params=params, model=self)
        self.hist = history.History(model=self)
        self.stat = statistician.Statistician(model=self, params=params)

    def run(self):

        self.hist.setup()
        self.pop.setup()

        for self.t in tqdm(range(self.evo.n_generations)):

            self.pop.prepare_new_generation()

            for p in range(self.evo.n_periods_per_generation):

                self.eco.manage_exchanges()
                self.pop.consume()

            self.pop.end_generation()

            self.stat.compute_stats()
            self.evo.reproduce_agents()

        return self.hist.back_up
