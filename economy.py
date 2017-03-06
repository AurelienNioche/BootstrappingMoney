import itertools as it

import numpy as np
from tqdm import tqdm

import utils
from agent import Agent


class Economy(object):

    def __init__(self, n_generations, n_periods_per_generation, n_goods, n_agents,
                 p_mutation, random_seed):

        np.random.seed(random_seed)
        self.n_generations = n_generations
        self.n_periods_per_generation = n_periods_per_generation
        self.n_goods = n_goods
        self.n_agents = n_agents

        self.p_mutation = p_mutation

        self.agents = self.create_agents()

        self.diversity_quantity_mapping = self.create_diversity_quantity_mapping(n=n_goods)
        print("Diversity quantity mapping:", self.diversity_quantity_mapping)

        self.market_agents = None

        # ---- For final backup ----- #
        self.back_up = {
            "exchanges": [],
            "n_exchanges": [],
            "fitness": [],
            "production_diversity": [],
            "n_producers": [],
            "n_market_agents": [],
            "n_exchanges_t": []
        }

        # ----- For periodic backup ----- #

        self.temp_back_up = {
            "exchanges": dict([((i, j), 0) for i, j in it.combinations(range(n_goods), r=2)]),
            "n_exchanges": 0
        }

    def run(self):

        for g in tqdm(range(self.n_generations)):

            self.prepare_new_generation()

            for p in range(self.n_periods_per_generation):

                self.time_step()

            self.make_a_backup()
            self.reproduce_agents()

        return self.back_up

    @staticmethod
    def create_diversity_quantity_mapping(n):
        mapping = [round(n*i**2/j) for (i, j) in zip(range(1, n+1), range(n+1, 1, -1))] + [0]
        mapping.reverse()
        return mapping


    def create_agents(self):

        agents = []

        agent_idx = 0

        for i in range(self.n_agents):

            a = self.create_single_agent(i)

            agents.append(a)
            agent_idx += 1

        return agents

    def create_single_agent(self, idx):

        return Agent(
            n_goods=self.n_goods,
            # Assume an agent doesn't choose production preferences
            production_preferences=np.random.permutation(np.arange(self.n_goods)),
            idx=idx,
            **self.get_agent_random_strategic_attributes()
        )

    def get_agent_random_strategic_attributes(self):

        return {
            "production_diversity": np.random.randint(1, self.n_goods + 1),
            "goods_to_buy": np.random.choice(np.arange(self.n_goods),
                                             size=np.random.randint(1, self.n_goods + 1), replace=False),
            "goods_to_sell": np.random.choice(np.arange(self.n_goods),
                                              size=np.random.randint(1, self.n_goods + 1), replace=False)
        }

    def prepare_new_generation(self):

        for i in range(self.n_agents):
            self.agents[i].stock[:] = 0
            self.agents[i].fitness = 0
            self.agents[i].produce(self.diversity_quantity_mapping)
            self.agents[i].consume()

        self.market_agents = [i for i in range(self.n_agents)]

    def time_step(self):

        market_agents = [i for i in self.market_agents if max(self.agents[i].stock) > 1]

        # ---------- MANAGE EXCHANGES ----- #

        n_exchanges_t = 0   # For stats
        for i, j in utils.derangement(market_agents):
            n_exchanges_t += self.make_encounter(i, j)

        # Each agent consumes at the end of each round and adapt his behavior (or not).
        for i in market_agents:
            self.agents[i].consume()

        # ----------------- #
        # ---- STATS ------ #

        self.back_up["n_exchanges_t"].append(n_exchanges_t)

        # ---------------- #
        # ---------------- #

    def make_encounter(self, i, j):

        exchange_takes_place = 0

        possible_exchange_i = {(x, y) for x, y in it.product(self.agents[i].goods_to_sell, self.agents[i].goods_to_buy)
                               if x != y and self.agents[i].stock[x] > 1}
        possible_exchange_j = {(y, x) for x, y in it.product(self.agents[j].goods_to_sell, self.agents[j].goods_to_buy)
                               if x != y and self.agents[j].stock[x] > 1}

        points_of_agreement = possible_exchange_i.intersection(possible_exchange_j)

        if len(points_of_agreement):

            exchange = [i for i in points_of_agreement][np.random.choice(len(points_of_agreement))]

            # ...exchange occurs
            self.agents[i].proceed_to_exchange(exchange)
            self.agents[j].proceed_to_exchange((exchange[1], exchange[0]))

            # ----------------- #
            # ---- STATS ------ #

            self.temp_back_up["exchanges"][tuple(sorted(exchange))] += 1
            self.temp_back_up["n_exchanges"] += 1
            exchange_takes_place = 1

            # ---------------- #
            # ---------------- #
        return exchange_takes_place

    # --------------------------------------------------------------------------------------- #
    # --------------------------- EVOLUTIONARY PART ----------------------------------------- #
    # --------------------------------------------------------------------------------------- #

    def reproduce_agents(self):

        selected_to_be_copied, selected_to_be_changed = self.procedure_of_selection()

        for to_be_copied, to_be_changed in zip(selected_to_be_copied, selected_to_be_changed):

            self.procedure_of_reproduction(to_be_copied, to_be_changed)

    def procedure_of_selection(self):

        selected_to_be_copied, selected_to_be_changed = [], []

        data = dict()

        for a in np.random.permutation(self.agents):
            prod_pref = tuple(a.production_preferences)
            if prod_pref not in data.keys():
                data[prod_pref] = {
                    "idx": [],
                    "fitness": []
                }
            data[prod_pref]["idx"].append(a.idx)
            data[prod_pref]["fitness"].append(a.fitness)

        for prod_pref in data.keys():

            if len(data[prod_pref]["idx"]) > 1:

                selected_to_be_copied.append(
                    data[prod_pref]["idx"][
                        np.argmax(data[prod_pref]["fitness"])
                    ]
                )

                selected_to_be_changed.append(
                    data[prod_pref]["idx"][
                        np.argmin(data[prod_pref]["fitness"])
                    ]
                )

        return selected_to_be_copied, selected_to_be_changed

    def procedure_of_reproduction(self, to_be_copied, to_be_changed):

        good_attributes = self.agents[to_be_copied].get_strategic_attributes()
        random_attributes = self.get_agent_random_strategic_attributes()

        r = np.random.random(len(good_attributes))

        for idx, key in enumerate(good_attributes.keys()):

            if r[idx] <= self.p_mutation:

                setattr(self.agents[to_be_changed], key, random_attributes[key])

            else:
                setattr(self.agents[to_be_changed], key, good_attributes[key])

    # --------------------------------------------------------------------------------------- #
    # --------------------------------- SAVING PART ----------------------------------------- #
    # --------------------------------------------------------------------------------------- #

    def make_a_backup(self):

        # Keep a trace of fitness
        fitness = 0
        n_producers = np.zeros(self.n_goods)
        for i in range(self.n_agents):
            fitness += self.agents[i].fitness
            produced_goods = self.agents[i].get_produced_goods()
            for j in produced_goods:
                n_producers[j] += 1

        fitness /= self.n_agents

        # Keep a trace of number of agents in market
        self.back_up["n_market_agents"].append(len(self.market_agents))

        # Keep a trace of production diversity
        average_production_diversity = np.mean([a.production_diversity for a in self.agents])

        # Keep a trace of exchanges
        for key in self.temp_back_up["exchanges"].keys():
            # Avoid division by zero
            if self.temp_back_up["n_exchanges"] > 0:
                self.temp_back_up["exchanges"][key] /= self.temp_back_up["n_exchanges"]
            else:
                self.temp_back_up["exchanges"][key] = 0

        # For back up
        self.back_up["exchanges"].append(self.temp_back_up["exchanges"].copy())
        self.back_up["fitness"].append(fitness)
        self.back_up["n_exchanges"].append(self.temp_back_up["n_exchanges"])
        self.back_up["production_diversity"].append(average_production_diversity)
        self.back_up["n_producers"].append(n_producers)

        self.reinitialize_backup_containers()

    def reinitialize_backup_containers(self):

        # Containers for future backup
        for k in self.temp_back_up["exchanges"].keys():
            self.temp_back_up["exchanges"][k] = 0
        self.temp_back_up["n_exchanges"] = 0
