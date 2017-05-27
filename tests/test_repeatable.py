"""
Test if the run are repeatable, i.e., successive runs yield the same results, given a fixed
random seed.
"""

import unittest
import array

import numpy as np

import dotdot
from bootstrapmoney import Model


def array2list(data):
    """Replace np.array and array to lists in a complex data structure.

    This function was written to easily check the equality of histories.
    """
    if isinstance(data, (list, tuple, array.array)):
        return [array2list(e) for e in data]
    elif isinstance(data, dict):
        return {k: array2list(v) for k, v in data.items()}
    elif isinstance(data, np.ndarray):
        return data.tolist()
    else:
        return data


class RepeatableTests(unittest.TestCase):
    """Test repeatability"""

    def test_repeatable(self):
        """Test that two 50-steps runs yield the same history"""

        def run(seed):
            """Return the history of a run"""
            parameters = {
                "random_seed": seed,
                "n_generations": 50,
                "n_periods_per_generation": 10,
                "n_goods": 3,
                "n_agents": 50,
                "p_mutation": 0.4,
                "mating_rate": 0.2
            }
            model = Model(parameters)
            model.run()
            return model.history.history

        self.assertEqual(array2list(run(0)), array2list(run(0)))

if __name__ == '__main__':
    unittest.main()
