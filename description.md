# Decision model.

* `g` goods. (default `g = 3`). `G` = [0, 1, ..., g-1]
* `n` agents. An agent is composed of
    * `S`: exchanges strategies (x, y) for x, y in G (with x != y)
    * `D`: difficulty of production of each good
    * `P`: production strategy
* shared by all agents:
    * `C`: production costs
    * `e`: exchange costs
    * `m`: max production

* `‎γ` generations
* `ρ` period (i.e. number of tentative of exchanges) per generation.
* `α` mutation rate
* `β` mating rate
