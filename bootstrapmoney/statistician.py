import numpy as np


class Statistician:

    def __init__(self, params, model):

        self.n_goods = params["n_goods"]
        self.n_agents = params["n_agents"]
        
        self.mod = model

    def compute_stats(self):
        """Compute stats for keeping a trace of system dynamics"""

        # Keep a trace of fitness, number of producers per type of good and global production
        n_producers = np.zeros(self.n_goods)
        global_production = np.zeros(self.n_goods)

        for i in range(self.n_agents):

            production = self.mod.pop.agents[i].production
            for j in range(self.n_goods):
                if production[j] > 0:
                    n_producers[j] += 1
            global_production += production

        fitness = sum(self.mod.pop.agents_fitness) / self.n_agents

        # Keep a trace of production diversity
        production_diversity = [np.count_nonzero(a.production[:]) for a in self.mod.pop.agents]
        average_production_diversity = np.mean(production_diversity)

        # Keep a trace of strategies
        bu = self.mod.hist.back_up
        sum_direct, sum_indirect_0, sum_indirect_1, sum_indirect_2 = 0, 0, 0, 0

        for s_path, n_s in bu['n_strategies'][self.mod.t].items():

            if len(s_path) == 1:
                sum_direct += n_s

            elif len(s_path) == 2:

                if s_path[0][1] == 0:   # Get the last element of the first pair in the path
                    sum_indirect_0 += n_s

                elif s_path[0][1] == 1:
                    sum_indirect_1 += n_s

                elif s_path[0][1] == 2:
                    sum_indirect_2 += n_s

        # Make a back up
        bu["fitness"][self.mod.t] = fitness
        bu["production_diversity"][self.mod.t] = average_production_diversity
        bu["n_producers"][self.mod.t, :] = n_producers
        bu["production"][self.mod.t, :] = global_production
        bu["direct"][self.mod.t] = sum_direct
        bu["indirect_0"][self.mod.t] = sum_indirect_0
        bu["indirect_1"][self.mod.t] = sum_indirect_1
        bu["indirect_2"][self.mod.t] = sum_indirect_2
