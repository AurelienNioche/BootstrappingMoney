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

        self.markets = dict([(i, []) for i in it.permutations(range(n_goods), r=2)])
        self.exchanges_types = [i for i in it.combinations(range(self.n_goods), r=2)]

        self.exchanges_labels = dict([(e, i) for i, e in enumerate(self.exchanges_types)])

        self.back_up = {
            "exchanges": np.zeros((self.n_generations, len(self.exchanges_types))),
            "n_exchanges": np.zeros(self.n_generations),
            "fitness": np.zeros(self.n_generations),
            "production_diversity": np.zeros(self.n_generations),
            "n_producers": np.zeros((self.n_generations, self.n_goods)),
            "n_goods_intervention": np.zeros((self.n_generations, self.n_goods)),
            "production": np.zeros((self.n_generations, self.n_goods)),
            "exchanges_labels": self.exchanges_labels,
            "exchanges_types": self.exchanges_types
        }

        self.g = None

    def run(self):

        for self.g in tqdm(range(self.n_generations)):

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

            a = Agent(
                n_goods=self.n_goods,
                # Assume an agent doesn't choose production preferences
                production_advantages=
                self.all_possible_production_advantages[i % len(self.all_possible_production_advantages)],
                production_costs=self.production_costs,
                u=self.u,
                idx=i,
                **self.get_agent_random_strategic_attributes()
            )
            agents.append(a)
            agent_idx += 1

        return agents

    def get_agent_random_strategic_attributes(self):

        return {
            "production": self.get_production(),
            "exchange_strategies": self.get_exchange_strategies()
        }

    def get_production(self):

        good_choice = np.random.choice(np.arange(self.n_goods), size=self.max_production)
        unique, counts = np.unique(good_choice, return_counts=True)
        production = np.zeros(self.n_goods, dtype=int)
        for value, count in zip(unique, counts):
            production[value] = count

        return production

    def get_exchange_strategies(self):

        exchange_strategies = np.zeros((self.n_goods, self.n_goods), dtype=object)
        for i in range(self.n_goods):
            for j in range(self.n_goods):
                if i != j:
                    exchange_strategies[i, j] = np.random.choice(self.get_possible_paths(i, j, self.n_goods))

        return exchange_strategies

    @staticmethod
    def get_possible_paths(departure_node, final_node, n_nodes):

        step_nodes = [i for i in range(n_nodes) if i not in [final_node, departure_node]]

        paths = [[(departure_node, final_node)]]

        for i in range(1, len(step_nodes) + 1):

            for j in it.permutations(step_nodes, r=i):
                node_list = [departure_node] + list(j) + [final_node]
                path = [(node_list[i], node_list[i + 1]) for i in range(len(node_list) - 1)]
                paths.append(path)

        return paths

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

            self.manage_exchanges()

            # Each agent consumes at the end of each round and adapt his behavior (or not).
            for i in market_agents:
                self.agents[i].consume()

    def manage_exchanges(self):

        for k in self.markets:
            self.markets[k] = []

        for agent in self.agents:
            agent_choice = agent.which_exchange_do_you_want_to_try()
            self.markets[agent_choice].append(agent.idx)

        success_idx = []
        for i, j in self.exchanges_types:

            a1 = self.markets[(i, j)]
            a2 = self.markets[(j, i)]
            min_a = int(min([len(a1), len(a2)]))

            if min_a:

                self.back_up["exchanges"][self.g, self.exchanges_labels[(i, j)]] += min_a
                self.back_up["n_exchanges"][self.g] += min_a

                for good in (i, j):
                    self.back_up["n_goods_intervention"][self.g, good] += min_a

                success_idx += list(np.random.choice(a1, size=min_a, replace=False))
                success_idx += list(np.random.choice(a2, size=min_a, replace=False))

        for idx in success_idx:
            agent = self.agents[idx]
            agent.proceed_to_exchange()

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

            production = self.agents[i].production
            for j in range(self.n_goods):
                if production[j] > 0:
                    n_producers[j] += 1
            global_production += production

        fitness /= self.n_agents

        # # Keep a trace of number of agents in market
        # self.back_up["n_market_agents"].append(len(self.market_agents))

        # Keep a trace of production diversity
        production_diversity = [sum(a.production[:] != 0) for a in self.agents]
        average_production_diversity = np.mean(production_diversity)

        # # Keep a trace of exchanges
        # for key in self.temp_back_up["exchanges"].keys():
        #     # Avoid division by zero
        #     if self.temp_back_up["n_exchanges"] > 0:
        #         self.temp_back_up["exchanges"][key] /= self.temp_back_up["n_exchanges"]
        #     else:
        #         self.temp_back_up["exchanges"][key] = 0

        # For back up
        self.back_up["fitness"][self.g] = fitness
        self.back_up["production_diversity"][self.g] = average_production_diversity
        self.back_up["n_producers"][self.g, :] = n_producers
        self.back_up["production"][self.g, :] = global_production

