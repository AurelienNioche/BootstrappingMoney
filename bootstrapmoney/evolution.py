import numpy as np


class Evolution:

    def __init__(self, model, params):

        self.mod = model
        self.n_agents = params["n_agents"]
        self.n_generations = params["n_generations"]
        self.n_periods_per_generation = params["n_periods_per_generation"]
        self.mating_rate = params["mating_rate"]
        self.p_mutation = params["p_mutation"]

    def reproduce_agents(self):
        """Reproduce agents using a process of 'natural' selection."""

        selected_to_be_copied, selected_to_be_changed = self.procedure_of_selection()
        self.procedure_of_reproduction(selected_to_be_copied, selected_to_be_changed)

    # @profile
    def procedure_of_selection(self):
        """Select agents to reproduce.

        One part of agents will be selected to be copied, an another part to be changed.

        Pairs of agents (one to reproduce, one to replace) are created between agents with the same
        production difficulties.
        """

        selected_to_be_copied, selected_to_be_changed = [], []

        tup_possible_production_difficulty = list(self.mod.pop.sorted_idx_per_production_difficulty.keys())

        data = {
            tuple(i): {"idx": [], "fitness": []}
            for i in self.mod.eco.all_possible_production_difficulty
        }

        for prod_difficulty in tup_possible_production_difficulty:

            idx = np.random.permutation(self.mod.pop.sorted_idx_per_production_difficulty[prod_difficulty])

            sorted_idx = np.argsort(self.mod.pop.agents_fitness[idx])
            data[prod_difficulty]["idx"] = idx[sorted_idx]
            data[prod_difficulty]["fitness"] = self.mod.pop.agents_fitness[idx[sorted_idx]]

        # ---- #

        np.random.shuffle(tup_possible_production_difficulty)

        n_prod_difficulties = len(tup_possible_production_difficulty)

        for i in range(int(self.mating_rate * self.n_agents)):

            prod_difficulty = tup_possible_production_difficulty[i % n_prod_difficulties]

            if len(data[prod_difficulty]["idx"]) > 1:

                selected_to_be_copied.append(
                    data[prod_difficulty]["idx"][-1]
                )

                selected_to_be_changed.append(
                    data[prod_difficulty]["idx"][0]
                )

                data[prod_difficulty]["fitness"] = data[prod_difficulty]["fitness"][1: -1]
                data[prod_difficulty]["idx"] = data[prod_difficulty]["idx"][1: -1]

        return selected_to_be_copied, selected_to_be_changed

    # @profile
    def procedure_of_reproduction(self, selected_to_be_copied, selected_to_be_changed):
        """Agents with the worse fitness 'imitate' agents with best fitness, copying certain attributes.
        However, this copy can be 'mutated' in a way to maintain variability (here 'mutated' means randomly picked)
        """
        n = len(selected_to_be_copied)
        r = np.random.random((n, len(self.mod.pop.random_attribute)))

        for i, (to_be_copied, to_be_changed) in enumerate(zip(selected_to_be_copied, selected_to_be_changed)):

            for idx, key in enumerate(self.mod.pop.random_attribute):

                if r[i, idx] <= self.p_mutation:

                    setattr(self.mod.pop.agents[to_be_changed], key, self.mod.pop.random_attribute[key]())

                else:
                    setattr(self.mod.pop.agents[to_be_changed], key, self.mod.pop.agents[to_be_copied].__getattribute__(key))
