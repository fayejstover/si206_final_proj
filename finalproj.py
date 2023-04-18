# Your names: Faye Stover, Agnes Mar, Chloe Emch

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

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            
    except FileNotFoundError:
        data = {}
        
    return data

url = "https://hp-api.onrender.com/api/characters"  
response = requests.get(url)

# Parse the response JSON data
data = json.loads(response.text)
print(data)


# main:
def main():




# test cases: 
    class TestHomework6(unittest.TestCase):



        
if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
