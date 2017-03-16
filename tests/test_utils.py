import unittest

import numpy as np

import dotdot
import utils


class DerangementTests(unittest.TestCase):
    """Test the `derangement` function"""

    def test_derangement_1(self):
        """Test with one element: should throw a AssertionError"""
        a = [1]
        with self.assertRaises(AssertionError):
            utils.derangement(a, max_tries=1000)

    def test_derangement_1(self):
        """Test with the same repeating element: should throw a ValueError"""
        a = [1, 1]
        with self.assertRaises(ValueError):
            utils.derangement(a, max_tries=1000)

    def test_derangement_2(self):
        """Test with two elements"""
        a = [1, 2]
        for _ in range(1000):
            pairs = sorted(list(utils.derangement(a)))
            self.assertTrue(pairs[0][0] == 1 and pairs[0][1] == 2)
            self.assertTrue(pairs[1][0] == 2 and pairs[1][1] == 1)

    def test_derangement_3(self):
        """Test with two elements"""
        a = [1, 2, 3]
        for _ in range(1000):
            pairs = sorted(list(utils.derangement(a)))
            self.assertTrue(pairs[0][1] in [2, 3])
            self.assertTrue(pairs[1][1] in [1, 3])
            self.assertTrue(pairs[2][1] in [1, 2])

    def test_derangement_random(self):
        """Test with a random number of elements"""
        for _ in range(1000):
            n = np.random.randint(2, 1000)
            a = np.arange(n)
            pairs = list(utils.derangement(a))
            for i, j in pairs:
                self.assertTrue(i != j)


if __name__ == '__main__':
    unittest.main()
