import numpy as np
from tqdm import tqdm
import itertools as it
import copy as cp
from agent import Agent


class Economy(object):

    def __init__(self, n_generations, n_periods_per_generation, n_goods, n_agents, n_reproduction_pairs, p_mutation):

        self.n_generations = n_generations
        self.n_periods_per_generation = n_periods_per_generation
        self.n_goods = n_goods
        self.n_agents = n_agents

        self.n_reproduction_pairs = n_reproduction_pairs

        self.p_mutation = p_mutation

        self.agents = self.create_agents()

        self.fitness = np.zeros(self.n_agents)

        self.diversity_quantity_mapping = self.create_diversity_quantity_mapping(n=n_goods, k=n_goods+1)

        # ----- For periodic backup ----- #

        self.exchanges = dict()
        for i in it.combinations(range(self.n_goods), r=2):
            self.exchanges[i] = 0
        self.n_exchange = 0
        self.average_fitness = 0

        # ---- For final backup ----- #
        self.back_up = {
            "exchanges": [],
            "n_exchanges": [],
            "fitness": [],
        }
        
    def run(self):

        for g in tqdm(range(self.n_generations)):

            self.prepare_new_generation()

            for p in range(self.n_periods_per_generation):

                self.time_step()

            self.make_a_backup()
            self.reproduce_agents()

        return self.back_up

    def prepare_new_generation(self):

        for i in range(self.n_agents):
            self.agents[i].produce(self.diversity_quantity_mapping)

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
        b = list(array_like)

        while True:

            error = 0

            first = np.random.permutation(a)
            second = np.random.permutation(b)
            pairs = zip(first, second)

            for i, j in pairs:

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
            production_preferences=np.random.permutation(np.arange(self.n_goods)),
            production_diversity=np.random.randint(1, self.n_goods + 1),
            goods_to_buy=np.random.choice(np.arange(self.n_goods), size=np.random.randint(0, self.n_goods + 1)),
            goods_to_sell=np.random.choice(np.arange(self.n_goods), size=np.random.randint(0, self.n_goods + 1)),
            idx=idx)

    def time_step(self):

        market_agents = [self.agents[i].idx for i in range(self.n_agents) if not self.agents[i].stock.any() == 0]

        # ---------- MANAGE EXCHANGES ----- #

        for i, j in self.derangement(market_agents):
            self.make_encounter(i, j)

        # Each agent consumes at the end of each round and adapt his behavior (or not).
        for i in market_agents:
            self.agents[i].consume()

    def make_encounter(self, i, j):
        
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

            self.exchanges[exchange] += 1
            self.n_exchange += 1

            # ---------------- #
    
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

            r = np.random.random()

            if r <= self.p_mutation:

                self.agents[to_be_changed] = self.create_single_agent(idx=to_be_changed)

            else:
                self.agents[to_be_changed] = cp.copy(self.agents[to_be_copied])
                self.agents[to_be_changed].idx = to_be_changed

        # --- FOR STATS AND RESET ---- #

        for i in range(self.n_agents):
            self.fitness[i] = self.agents[i].fitness
            self.agents[i].fitness = 0

    # --------------------------------------------------------------------------------------- #
    # --------------------------------- SAVING PART ----------------------------------------- #
    # --------------------------------------------------------------------------------------- #

    def make_a_backup(self):

        # Keep a trace from utilities
        average_fitness = sum(self.fitness)/self.n_agents

        # ----- FOR FUTURE BACKUP ----- #

        for key in self.exchanges.keys():
            # Avoid division by zero
            if self.n_exchange > 0:
                self.exchanges[key] /= self.n_exchange
            else:
                self.exchanges[key] = 0

        # For back up
        self.back_up["exchanges"].append(self.exchanges.copy())
        self.back_up["fitness"].append(average_fitness)
        self.back_up["n_exchanges"].append(self.n_exchange)

        self.reinitialize_backup_containers()

    def reinitialize_backup_containers(self):

        # Reinitialize fitness counter
        self.fitness[:] = 0

        # Containers for future backup
        for k in self.exchanges.keys():
            self.exchanges[k] = 0
        self.n_exchange = 0
