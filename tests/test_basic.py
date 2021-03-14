# -*- coding: utf-8 -*-
import unittest
from .context import helpers
from .context import annotations

'''
To have a complete set of manual tests,
all you need to do is make a list of all the features your application has,
the different types of input it can accept, and the expected results.
'''

class BasicTests(unittest.TestCase):
    """Basic test cases."""

    def test_euler_to_quaternion(self):
        #import pdb
        #pdb.set_trace()
        assert (helpers.euler_to_quaternion(0., 0., 1.) == [0,0,0,1]), 'message'
        


if __name__ == '__main__':
    unittest.main()