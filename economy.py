import numpy as np
from tqdm import tqdm
import itertools as it
from agent import Agent


class Economy(object):

    def __init__(self, n_generations, n_periods_per_generation, n_goods, n_agents, reproduction_proportion,
                 p_mutation, random_seed):

        np.random.seed(random_seed)
        self.n_generations = n_generations
        self.n_periods_per_generation = n_periods_per_generation
        self.n_goods = n_goods
        self.n_agents = n_agents

        self.n_reproduction_pairs = int(reproduction_proportion * n_agents)

        self.p_mutation = p_mutation

        self.agents = self.create_agents()

        self.diversity_quantity_mapping = self.create_diversity_quantity_mapping(n=n_goods, k=n_goods*2+1)
        print("Diversity quantity mapping:", self.diversity_quantity_mapping)

        # ---- For final backup ----- #
        self.back_up = {
            "exchanges": [],
            "n_exchanges": [],
            "fitness": [],
            "n_market_agents": [],
            "production_diversity": [],
            "n_exchanges_t": []
        }

        # ----- For periodic backup ----- #

        self.temp_back_up = {
            "exchanges": dict([((i, j), 0) for i, j in it.combinations(range(n_goods), r=2)]),
            "n_exchanges": 0,
            "fitness": 0,
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
    def create_diversity_quantity_mapping(n, k):

        # k is the squared root of the quantity produced if you produce only one type of good

        a = - (k - 1) / (n - 1)
        b = (k * n - 1) / (n - 1)

        f = lambda x: a * x + b

        mapping = [0]

        for i in range(1, n + 1):
            mapping.append(int(f(i)) ** 2)

        return mapping

    @staticmethod
    def derangement(array_like):

        a = list(array_like)

        while True:

            error = 0

            first = np.random.permutation(a)
            second = np.random.permutation(a)

            for i, j in zip(first, second):

                if i == j:
                    error = 1
                    break
            if not error:
                pairs = zip(first, second)
                break

        return pairs

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
            idx=idx, **self.get_agent_random_strategic_attributes())

    def get_agent_random_strategic_attributes(self):

        return {
            "production_preferences": np.random.permutation(np.arange(self.n_goods)),
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

    def time_step(self):

        n_exchanges_t = 0

        market_agents = [self.agents[i].idx for i in range(self.n_agents) if max(self.agents[i].stock) > 1]

        # -- STATS -- #
        self.back_up["n_market_agents"].append(len(market_agents))

        # ---------- MANAGE EXCHANGES ----- #

        for i, j in self.derangement(market_agents):
            n_exchanges_t += self.make_encounter(i, j)

        # Each agent consumes at the end of each round and adapt his behavior (or not).
        for i in market_agents:
            self.agents[i].consume()

        self.back_up["n_exchanges_t"].append(n_exchanges_t)

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

            # ---- STATS ------ #

            exchange = tuple(sorted(exchange))

            self.temp_back_up["exchanges"][exchange] += 1
            self.temp_back_up["n_exchanges"] += 1

            exchange_takes_place = 1

            # ---------------- #
        return exchange_takes_place
    
    # --------------------------------------------------------------------------------------- #
    # --------------------------- EVOLUTIONARY PART ----------------------------------------- #
    # --------------------------------------------------------------------------------------- #

    def reproduce_agents(self):

        reproduction_pairs = \
            np.random.choice(np.arange(self.n_agents), size=(self.n_reproduction_pairs, 2), replace=False)

        for i, j in reproduction_pairs:

            if self.agents[i].fitness > self.agents[j].fitness:

                to_be_copied = i
                to_be_changed = j

            elif self.agents[i].fitness < self.agents[j].fitness:

                to_be_copied = i
                to_be_changed = j

            else:
                continue

            good_attributes = self.agents[to_be_copied].get_strategic_attributes()
            random_attributes = self.get_agent_random_strategic_attributes()

            r = np.random.random(len(good_attributes))

            for idx, key in enumerate(good_attributes.keys()):

                if r[idx] <= self.p_mutation:

                    setattr(self.agents[to_be_changed], key, random_attributes[key])

                else:
                    setattr(self.agents[to_be_changed], key, good_attributes[key])

        # --- FOR STATS AND RESET ---- #

        for i in range(self.n_agents):
            self.temp_back_up["fitness"] += self.agents[i].fitness

    # --------------------------------------------------------------------------------------- #
    # --------------------------------- SAVING PART ----------------------------------------- #
    # --------------------------------------------------------------------------------------- #

    def make_a_backup(self):

        # Keep a trace of fitness
        average_fitness = self.temp_back_up["fitness"]/self.n_agents

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
        self.back_up["fitness"].append(average_fitness)
        self.back_up["n_exchanges"].append(self.temp_back_up["n_exchanges"])
        self.back_up["production_diversity"].append(average_production_diversity)

        self.reinitialize_backup_containers()

    def reinitialize_backup_containers(self):

        # Containers for future backup
        for k in self.temp_back_up["exchanges"].keys():
            self.temp_back_up["exchanges"][k] = 0
        self.temp_back_up["n_exchanges"] = 0
        self.temp_back_up["fitness"] = 0
