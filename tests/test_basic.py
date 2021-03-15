# -*- coding: utf-8 -*-
import unittest
from .context import helpers
from .context import annotations
from .context import bicycle
from .context import human


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
    

    def test_file_or_url_load(self):
        url_annotations = annotations.load_json_from_file_url('https://jsonplaceholder.typicode.com/todos')
        self.assertEqual(len(url_annotations), 200)
        file_annotations = annotations.load_json_from_file_url('docs/example_annotations.json')
        self.assertEqual(len(file_annotations), 30)


    def test_parse_json(self):
        parsed_list = annotations.parse_annotations('docs/example_annotations.json')
        self.assertEqual(len(parsed_list), 30)
        self.assertIsInstance(parsed_list[0], bicycle.Bicycle)
        self.assertIsInstance(parsed_list[1], human.Human)


if __name__ == '__main__':
    unittest.main()
