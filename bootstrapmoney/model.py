import numpy as np

from tqdm import tqdm

from . import economy, population, history


class Model:
    """Model class.

    Create the elements of the model, orchestrate their interaction, and keeps
    an history of the evolution of the economy.
    """

    def __init__(self, params):
        self.params = params

        np.random.seed(self.params['random_seed'])
        self.history    = history.History(params)
        self.population = population.Population(params)
        self.economy    = economy.Economy(params, self.population, self.history)

    def run(self):
        for t_gen in tqdm(range(self.params['n_generations'])):
            self.population.reset_agents()
            for p in range(self.params['n_periods_per_generation']):
                self.economy.time_step()
            self.history.end_generation(self.population.agents)
            self.population.evolve_agents()
