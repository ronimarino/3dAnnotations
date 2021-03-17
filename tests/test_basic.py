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

    
    def test_generate_dicts(self):
        parsed_list = annotations.parse_annotations('docs/example_annotations.json')
        bike = parsed_list[0]
        person = parsed_list[1]
        test_bike_dict = {
          "BICYCLE_ID": 0,
          "POSITION": [
            6.214051078965763,
            -1.6141740617314968,
            -1.1567630666763957
          ],
          "ORIENTATION": [
            -0.005390844858319934,
            0.004885218172705003,
            0.8069478741049281,
            0.5905778542348636
          ],
          "SIZE": [
            0.38506336808139396,
            1.7546858722619847,
            1.12662733359948
          ],
          "STATUS": 0,
          "RIDER": 1,
          "TYPE": 0
        }
        test_human_dict = {
          "HUMAN_ID": 1,
          "POSITION": [
            6.08933372191161,
            -1.6203931711134456,
            -0.8208160370426799
          ],
          "ORIENTATION": [
            -0.005390844858319934,
            0.004885218172705003,
            0.8069478741049281,
            0.5905778542348636
          ],
          "SIZE": [
            0.5008161429394367,
            0.8935028422787278,
            1.586688306599624
          ],
          "WEARS_HELMET": 0,
          "AGE": 0
        }
        bike_dict = bike.generate_bicycle_dict()
        human_dict = person.generate_human_dict()
        helpers.assertDictAlmostEqual(self, test_bike_dict, bike_dict)
        helpers.assertDictAlmostEqual(self, test_human_dict, human_dict)




if __name__ == '__main__':
    unittest.main()
