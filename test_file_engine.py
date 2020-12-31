import unittest
import os
from file_engine import FileEngine
import json


class Test(unittest.TestCase):

    def setUp(self):
        self.simple_file = FileEngine()
        self.sample_test_case = {"value": "test_object", "TimeToLive": 2000, "CurrentTime": "20:37:26"}
        with open("main.json", "r") as fr:
            with open("main_test.json", "w") as to:
                to.write(fr.read())

    def test_read_file(self):
        read_text = self.simple_file.read_file("test1")
        self.assertEqual(read_text, self.sample_test_case)

    def test_delete_data(self):
        with open('main_test.json', "r") as fi:
            data = json.load(fi)

        pop = data.pop("test1", None)
        self.assertEqual(pop, self.sample_test_case)

    def tearDown(self):
        os.remove("main_test.json")

suite = unittest.TestLoader().loadTestsFromTestCase(Test)
unittest.TextTestRunner(verbosity=1).run(suite)
