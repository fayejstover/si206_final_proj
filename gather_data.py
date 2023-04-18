import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import requests
import json


# implement functions here:

############## SPOTIPY API ###############


############### MARVEL API ###############


############ HARRY POTTER API ############


url = "https://hp-api.onrender.com/api/characters"
rows = 25

def get_data_from_api():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def create_database():
    conn = sqlite3.connect('hp_characters.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE characters
                (id INTEGER PRIMARY KEY,
                 name TEXT,
                 house TEXT,
                 patronus TEXT)''')
    conn.commit()
    conn.close()

def insert_data(data):
    conn = sqlite3.connect('hp_characters.db')
    c = conn.cursor()
    for row in data:
        c.execute('''INSERT INTO characters (name, house, patronus)
                     VALUES (?, ?, ?)''', (row['name'], row['house'], row['patronus']))
    conn.commit()
    conn.close()

def gather_data():
    num_rows = 0
    while num_rows < 100:
        data = get_data_from_api()
        if data:
            insert_data(data)
            num_rows += len(data)
            if num_rows >= 100 or num_rows % rows == 0:
                break
        else:
            print("error lol (2)")
            break



# test cases: 

class TestHomework6(unittest.TestCase):

    def test_example(self):
        self.assertEqual(1+1, 2)





if __name__ == "__main__":
    # calls from SPOTIPY
    
    
    
    # calls from MARVEL
    
    
    
    # calls from HARRY POTTER
    create_database()
    gather_data()

