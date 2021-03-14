# -*- coding: utf-8 -*-

from 3dAnnotations import annotations
import helpers

import unittest

'''
To have a complete set of manual tests,
all you need to do is make a list of all the features your application has,
the different types of input it can accept, and the expected results.
'''

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_euler_to_quaternion(self):
        assert True


if __name__ == '__main__':
    unittest.main()