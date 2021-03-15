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
        self.assertEqual(helpers.euler_to_quaternion(0., 0., 0.), [0,0,0,1])
        x_axis_rot = helpers.euler_to_quaternion(1., 0., 0.)
        self.assertEqual([x_axis_rot[0], x_axis_rot[1]], [0., 0.])
        y_axis_rot = helpers.euler_to_quaternion(0., 1., 0.)
        self.assertEqual([y_axis_rot[1], y_axis_rot[2]], [0., 0.])
        z_axis_rot = helpers.euler_to_quaternion(0., 0., 1.)
        self.assertEqual([z_axis_rot[0], z_axis_rot[2]], [0., 0.])
        
        


if __name__ == '__main__':
    unittest.main()