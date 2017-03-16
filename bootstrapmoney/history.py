

class History:

    def __init__(self, params):
        self.params = params

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
            produced_goods, production = self.agents[i].get_production_stats()
            for j in produced_goods:
                n_producers[j] += 1
            global_production += production

        fitness /= self.n_agents

        # # Keep a trace of number of agents in market
        # self.back_up["n_market_agents"].append(len(self.market_agents))

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
        self.back_up["n_goods_intervention"].append(self.temp_back_up["n_goods_intervention"].copy())
        self.back_up["production"].append(global_production)

        self.reinitialize_backup_containers()

    def reinitialize_backup_containers(self):

        # Containers for future backup
        for dic in [self.temp_back_up["exchanges"], self.temp_back_up["n_goods_intervention"]]:
            for k in dic.keys():
                dic[k] = 0
        self.temp_back_up["n_exchanges"] = 0

    def transaction_happens(self):
        """A transaction as just happened

        :param transaction:  a pair `(x, y)` with the good `x` and `y` being exchanged.
        """
        # stats
        self.temp_back_up["exchanges"][tuple(sorted(exchange))] += 1
        self.temp_back_up["n_exchanges"] += 1
        for e in exchange:
            self.temp_back_up["n_goods_intervention"][e] += 1
