import numpy as np


class Evolution:

    def __init__(self, model, params):

        self.mod = model
        self.n_generations = params["n_generations"]
        self.n_periods_per_generation = params["n_periods_per_generation"]
        self.mating_rate = params["mating_rate"]
        self.p_mutation = params["p_mutation"]

    def reproduce_agents(self):
        """Reproduce agents using a process of 'natural' selection."""

        selected_to_be_copied, selected_to_be_changed = self.procedure_of_selection()

        for to_be_copied, to_be_changed in zip(selected_to_be_copied, selected_to_be_changed):

            self.procedure_of_reproduction(to_be_copied, to_be_changed)

    def procedure_of_selection(self):
        """Select agents to reproduce.

        One part of agents will be selected to be copied, an another part to be changed.

        Pairs of agents (one to reproduce, one to replace) are created between agents with the same
        production preferences.
        """

        selected_to_be_copied, selected_to_be_changed = [], []

        # ---- #

        data = dict()

        for a in np.random.permutation(self.mod.pop.agents):  # Permutation is important in case of equal fitness
            prod_advantage = tuple(a.production_advantages)
            if prod_advantage not in data.keys():
                data[prod_advantage] = {
                    "idx": [],
                    "fitness": []
                }
            data[prod_advantage]["idx"].append(a.idx)
            data[prod_advantage]["fitness"].append(a.fitness)

        # ---- #

        prod_advantages = np.random.permutation(self.mod.eco.all_possible_production_advantages)

        for i in range(int(self.mating_rate * self.mod.pop.n_agents)):

            prod_advantage = tuple(prod_advantages[i % len(prod_advantages)])

            if len(data[prod_advantage]["idx"]) > 1:

                idx_with_best_fitness = np.argmax(data[prod_advantage]["fitness"])
                idx_with_worse_fitness = np.argmin(data[prod_advantage]["fitness"])

                selected_to_be_copied.append(
                    data[prod_advantage]["idx"][
                        idx_with_best_fitness
                    ]
                )

                selected_to_be_changed.append(
                    data[prod_advantage]["idx"][
                        idx_with_worse_fitness
                    ]
                )

                for j, idx in enumerate([idx_with_best_fitness, idx_with_worse_fitness]):
                    data[prod_advantage]["fitness"].pop(idx - j)
                    data[prod_advantage]["idx"].pop(idx - j)

        return selected_to_be_copied, selected_to_be_changed

    def procedure_of_reproduction(self, to_be_copied, to_be_changed):
        """Agents with the worse fitness 'imitate' agents with best fitness, copying certain attributes.
        However, this copy can be 'mutated' in a way to maintain variability (here 'mutated' means randomly picked)
        """

        good_attributes = self.mod.pop.agents[to_be_copied].get_strategic_attributes()
        random_attributes = self.mod.pop.get_agent_random_strategic_attributes()

        r = np.random.random(len(good_attributes))

        for idx, key in enumerate(good_attributes.keys()):

            if r[idx] <= self.p_mutation:

                setattr(self.mod.pop.agents[to_be_changed], key, random_attributes[key])

            else:
                setattr(self.mod.pop.agents[to_be_changed], key, good_attributes[key])