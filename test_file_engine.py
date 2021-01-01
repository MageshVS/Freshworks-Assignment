import unittest
import os
from file_engine import FileEngine
import json

class Test(unittest.TestCase):

    def setUp(self):
        self.simple_file = FileEngine()
        self.sample_test_case ={"value": "test_object", "TimeToLive": 3000, "TimeStamp": "15:53:44"}
        with open("data_store.json", "r") as fr:
            with open("main_test.json", "w") as to:
                to.write(fr.read())

    def test_create_data(self):
        self.assertRaises(KeyError, self.simple_file.CreateDataEntry, "very-large-key-to-make-the-exception", "1")
        self.assertRaises(KeyError, self.simple_file.CreateDataEntry, "test1", "1")

    def test_read_file(self):
        self.assertRaises(KeyError, self.simple_file.read_file, "no_key_present")
        self.assertRaises(KeyError, self.simple_file.read_file, "key_expired")

        read_text = self.simple_file.read_file("test2")
        self.assertEqual(read_text, self.sample_test_case)

    def test_delete_data(self):
        self.assertRaises(KeyError, self.simple_file.read_file, "no_key_present")
        self.assertRaises(KeyError, self.simple_file.read_file, "key_expired")

        with open('main_test.json', "r") as fi:
            data = json.load(fi)

        pop = data.pop("test2", None)
        self.assertEqual(pop, self.sample_test_case)

    def tearDown(self):
        os.remove("main_test.json")

if __name__ == "__main__":
    unittest.main()
