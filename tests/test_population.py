"""
Test if the Population class behavior
"""

import unittest

import numpy as np

import dotdot
from bootstrapmoney.population import Population


# def array2list(data):
#     """Replace np.array and array to lists in a complex data structure.
#
#     This function was written to easily check the equality of histories.
#     """
#     if isinstance(data, (list, tuple, array.array)):
#         return [array2list(e) for e in data]
#     elif isinstance(data, dict):
#         return {k: array2list(v) for k, v in data.items()}
#     elif isinstance(data, np.ndarray):
#         return data.tolist()
#     else:
#         return data


class PopulationTests(unittest.TestCase):
    """Test the Population class"""

    def test_possible_exchanges(self):
        """Test that possible exchanges are correctly generated"""

        parameters = {
            "n_goods": 3,
            "n_agents": 50,
            "p_mutation": 0.4,
            "mating_rate": 0.2
        }
        pop = Population(parameters)


        self.assertEqual(set(pop.all_possible_exchanges), set([(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]))

if __name__ == '__main__':
    unittest.main()
