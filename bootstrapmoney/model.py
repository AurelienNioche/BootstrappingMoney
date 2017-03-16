import numpy as np

from tqdm import tqdm

from . import economy, population


class Model:
    """Model class.

    Create the elements of the model, orchestrate their interaction, and keeps
    an history of the evolution of the economy.
    """

    def __init__(self, params):
        self.params = params

        np.random.seed(self.params['random_seed'])
        self.population = population.Population(params)
        self.economy    = economy.Economy(params, self.population)

    def run(self):
        for _ in tqdm(range(self.n_generations)):
            self.population.reset_agents()
            for p in range(self.params['n_periods_per_generation']):
                self.economy.update()
            self.population.evolve_agents()
