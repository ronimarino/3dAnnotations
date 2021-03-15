# -*- coding: utf-8 -*-
import unittest
import json
from .context import annotations



class AdvancedTests(unittest.TestCase):
    """Advanced test cases."""


    def test_convert_json(self):
        annotations.convert_json('docs/example_annotations.json', 'docs/test_output.json')
        test_converted_json = '0'
        correct_converted_json = '1'
        with open('docs/test_output.json') as input_json_file:
            test_converted_json = json.load(input_json_file)
        with open('docs/example_output.json') as input_json_file:
            correct_converted_json = json.load(input_json_file)
        
        self.assertEqual(test_converted_json, correct_converted_json)


if __name__ == '__main__':
    unittest.main()
