import itertools as it

import numpy as np
from tqdm import tqdm

import utils
from agent import Agent


class Economy(object):

    def __init__(self, n_generations, n_periods_per_generation, n_goods, n_agents,
                 production_advantages, production_costs, u, max_production,
                 p_mutation, mating_rate, random_seed):

        np.random.seed(random_seed)
        self.n_generations = n_generations
        self.n_periods_per_generation = n_periods_per_generation
        self.n_goods = n_goods
        self.n_agents = n_agents

        self.p_mutation = p_mutation
        self.n_mating = int(mating_rate * self.n_agents)

        # --- For agent creation --- #
        self.all_possible_exchanges = list(it.permutations(range(self.n_goods), r=2))
        self.all_possible_production_advantages = \
            np.random.permutation(
                list(it.permutations(production_advantages, r=self.n_goods))
            )
        self.production_costs = production_costs
        self.max_production = max_production
        self.u = u

        self.agents = self.create_agents()

        self.market_agents = None

        # ---- For final backup ----- #
        self.back_up = {
            "exchanges": [],
            "n_exchanges": [],
            "fitness": [],
            "production_diversity": [],
            "n_producers": [],
            # "n_market_agents": [],
            # "n_exchanges_t": [],
            "n_goods_intervention": [],
            "production": []
        }

        # ----- For periodic backup ----- #

        self.temp_back_up = {
            "exchanges": dict([((i, j), 0) for i, j in it.combinations(range(n_goods), r=2)]),
            "n_exchanges": 0,
            "n_goods_intervention": dict([(i, 0) for i in range(self.n_goods)])
        }

    def run(self):

        for g in tqdm(range(self.n_generations)):

            self.prepare_new_generation()

            for p in range(self.n_periods_per_generation):

                self.time_step()

            for i in range(self.n_agents):
                self.agents[i].compute_fitness()

            self.make_a_backup()
            self.reproduce_agents()

        return self.back_up

    # --------------------------------------------------------------------------------------- #
    # --------------------------- AGENT CREATION PART --------------------------------------- #
    # --------------------------------------------------------------------------------------- #

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
            production_advantages=
            self.all_possible_production_advantages[idx % len(self.all_possible_production_advantages)],
            production_costs=self.production_costs,
            u=self.u,
            idx=idx,
            **self.get_agent_random_strategic_attributes()
        )

    def get_agent_random_strategic_attributes(self):

        production = np.random.randint(0, self.max_production+1, size=self.n_goods)

        accepted_exchanges = [tuple(i) for i in np.random.permutation(
            self.all_possible_exchanges)[:np.random.randint(1, len(self.all_possible_exchanges))]]

        return {
            "production": production,
            "accepted_exchanges": accepted_exchanges
        }

    # ---------------------------------------------------------------------------- #

    def prepare_new_generation(self):

        for i in range(self.n_agents):
            self.agents[i].reset()
            self.agents[i].produce()
            self.agents[i].consume()

        self.market_agents = [i for i in range(self.n_agents)]

    def time_step(self):

        market_agents = [i for i in self.market_agents if max(self.agents[i].stock) > 1]

        if len(market_agents) > 1:

            # ---------- MANAGE EXCHANGES ----- #

            # n_exchanges_t = 0   # For stats
            for i, j in utils.derangement(market_agents):
                # n_exchanges_t += self.make_encounter(i, j)
                self.make_encounter(i, j)

            # Each agent consumes at the end of each round and adapt his behavior (or not).
            for i in market_agents:
                self.agents[i].consume()

            # # ----------------- #
            # # ---- STATS ------ #
            #
            # self.back_up["n_exchanges_t"].append(n_exchanges_t)
            #
            # # ---------------- #
            # # ---------------- #

    def make_encounter(self, i, j):

        # exchange_takes_place = 0
        exchange = None

        for x, y in self.agents[i].accepted_exchanges:

            if self.agents[i].stock[x] > 1 \
                    and self.agents[j].stock[y] > 1 \
                    and (y, x) in self.agents[j].accepted_exchanges:

                exchange = (x, y)

        if exchange is not None:

            # ...exchange occurs
            self.agents[i].proceed_to_exchange(exchange)
            self.agents[j].proceed_to_exchange((exchange[1], exchange[0]))

            # ----------------- #
            # ---- STATS ------ #

            self.temp_back_up["exchanges"][tuple(sorted(exchange))] += 1
            self.temp_back_up["n_exchanges"] += 1
            for e in exchange:
                self.temp_back_up["n_goods_intervention"][e] += 1
            # exchange_takes_place = 1

            # ---------------- #
            # ---------------- #

        # return exchange_takes_place

    # --------------------------------------------------------------------------------------- #
    # --------------------------- EVOLUTIONARY PART ----------------------------------------- #
    # --------------------------------------------------------------------------------------- #

    def reproduce_agents(self):

        selected_to_be_copied, selected_to_be_changed = self.procedure_of_selection()

        for to_be_copied, to_be_changed in zip(selected_to_be_copied, selected_to_be_changed):

            self.procedure_of_reproduction(to_be_copied, to_be_changed)

    def procedure_of_selection(self):

        selected_to_be_copied, selected_to_be_changed = [], []

        # ---- #

        data = dict()

        for a in np.random.permutation(self.agents):  # Permutation is important in case of equal fitness
            prod_advantage = tuple(a.production_advantages)
            if prod_advantage not in data.keys():
                data[prod_advantage] = {
                    "idx": [],
                    "fitness": []
                }
            data[prod_advantage]["idx"].append(a.idx)
            data[prod_advantage]["fitness"].append(a.fitness)

        # ---- #

        prod_advantages = np.random.permutation(self.all_possible_production_advantages)

        for i in range(self.n_mating):

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
        global_production = np.zeros(self.n_goods)

        for i in range(self.n_agents):

            fitness += self.agents[i].fitness

            production = self.agents[i].get_production()
            for j in range(self.n_goods):
                if production[j] > 0:
                    n_producers[j] += 1
            global_production += production

        fitness /= self.n_agents

        # # Keep a trace of number of agents in market
        # self.back_up["n_market_agents"].append(len(self.market_agents))

        # Keep a trace of production diversity
        production_diversity = [sum(a.production != 0) for a in self.agents]
        average_production_diversity = np.mean(production_diversity)

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
        self.back_up["n_goods_intervention"].append(self.temp_back_up["n_goods_intervention"].copy())
        self.back_up["production"].append(global_production)

        self.reinitialize_backup_containers()

    def reinitialize_backup_containers(self):

        # Containers for future backup
        for dic in [self.temp_back_up["exchanges"], self.temp_back_up["n_goods_intervention"]]:
            for k in dic.keys():
                dic[k] = 0
        self.temp_back_up["n_exchanges"] = 0
