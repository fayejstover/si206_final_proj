import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import requests
import json


# implement functions here:

# Spotipy API


# Marvel API


# Harry Potter API

url = "https://hp-api.onrender.com/api/characters"
response = requests.get(url)

# Parse the response JSON data
data = json.loads(response.text)

print(data)


# main:
def main():
    # example code:
    print("Running main function")


# test cases: 
class TestHomework6(unittest.TestCase):
    # example test case:
    def test_example(self):
        self.assertEqual(1+1, 2)


if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
