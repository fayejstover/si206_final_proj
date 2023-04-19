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


def get_data():
    url = "https://hp-api.onrender.com/api/characters"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("error (1)")


def extract_data(data):
    characters = []
    for character in data:
        row = (
            str(character["name"]),
            str(character["house"]),
            str(character["wand"]),
            str(character["patronus"])
        )
        characters.append(row)
    return characters


def create_table():
    conn = sqlite3.connect("hp_characters.db")
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS characters")
    c.execute("""
        CREATE TABLE characters (
            name TEXT,
            house TEXT,
            wand TEXT,
            patronus TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_data(characters):
    conn = sqlite3.connect("hp_characters.db")
    c = conn.cursor()

    c.executemany("INSERT INTO characters VALUES (?, ?, ?, ?)", characters)

    conn.commit()
    conn.close()




# test cases: 
class TestHomework6(unittest.TestCase):

    def test_example(self):
        self.assertEqual(1+1, 2)


def main():
# calls from SPOTIPY
    
    
    
# calls from MARVEL
    
    
    
# calls from HARRY POTTER
    data = get_data()
    characters = extract_data(data)
    create_table()
    insert_data(characters)

    conn = sqlite3.connect("hp_characters.db")
    c = conn.cursor()

    c.execute("SELECT * FROM characters")
    rows = c.fetchall()
    
    print(rows)
    conn.close()
    

if __name__ == "__main__":
    main()
