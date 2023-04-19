import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import requests
import json


# implement functions here:

############## RICK AND MORTY API #################################################################################################

def open_RM_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def read_RM_api(url):
    req = requests.get(url)
    info = req.text
    text = json.loads(info)
    return text

def insert_RM_data():
    conn = sqlite3.connect('finalproj.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS RickAndMorty (name TEXT, id INTEGER, status TEXT, species TEXT, gender TEXT)')
    conn.commit()

    data_dic = read_RM_api('https://rickandmortyapi.com/api/character')
    info = data_dic["info"]
    total_pages = info["pages"]
    # db_length = c.execute('SELECT COUNT(*) FROM RickAndMorty').fetchone()[0]

    for page in range(1, min(total_pages + 1, 5)):
        data_dic = read_RM_api(f'https://rickandmortyapi.com/api/character/?page={page}')
        for character in data_dic["results"]:
            name = character["name"]
            id = character["id"]
            status = character["status"]
            species = character["species"]
            gender = character["gender"]
            c.execute("INSERT OR IGNORE INTO RickAndMorty (name, id, status, species, gender) VALUES (?,?,?,?,?)",(name, id, status, species, gender))

    conn.commit()
    conn.close()
    


############## POKEMON API ########################################################################################################
def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def read_api(url):
    req = requests.get(url)
    info = req.text
    text = json.loads(info)
    return text

def pokemon_data():
    conn = sqlite3.connect('finalproj.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Pokemon (name TEXT, id INTEGER, height INTEGER, weight INTEGER)')
    conn.commit()

    data_dic = read_api('https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0')
    result = c.execute('SELECT COUNT(*) FROM Pokemon')
    db_length = result.fetchone()[0]
    
    for x in range(db_length, db_length + 25):
        name = data_dic['results'][x]['name']
        url = data_dic['results'][x]['url']
        pokemon_api = read_api(url)
        height = pokemon_api['height']
        id = pokemon_api['id']
        weight = pokemon_api['weight']
        c.execute("INSERT OR IGNORE INTO Pokemon (name, id, height, weight) VALUES (?,?,?,?)",(name, id, height, weight))
    conn.commit()
    conn.close()

    

########## HARRY POTTER API ####################################################################################################
def get_hp_data():
    url = "https://hp-api.onrender.com/api/characters"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("error (1)")


def extract_hp_data(data, start, end):
    characters = []
    for i, character in enumerate(data):
        if i < start:
            continue
        if i >= end:
            break
        row = (
            str(character["name"]),
            str(character["house"]),
            str(character["hogwartsStudent"]),
            str(character["hogwartsStaff"])
        )
        characters.append(row)
    return characters



def create_hp_table():
    conn = sqlite3.connect("finalproj.db")
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS HarryPotterCharacters")
    c.execute("""
        CREATE TABLE HarryPotterCharacters (
            name TEXT,
            house TEXT,
            hogwartsStudent TEXT,
            hogwartsStaff TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_hp_data(start=0, end=100):
    conn = sqlite3.connect("finalproj.db")
    c = conn.cursor()

    data = get_hp_data()
    characters = extract_hp_data(data, start, end)

    c.executemany("INSERT INTO HarryPotterCharacters VALUES (?, ?, ?, ?)", characters)

    conn.commit()
    conn.close()

    
    
 
################# NBA API ##########################################################################################################
############## EXTRA CREDIT ########################################################################################################
'''
def get_nba_data():
    url = "https://stats.nba.com/stats/leagueleaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2021-22&SeasonType=Regular+Season&StatCategory=PTS"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("error (1)")

def extract_nba_data(data):
    players = []
    for player in data["resultSet"]["rowSet"]:
        try:
            name = str(player[2])
            team = str(player[4])
            ft_pct = str(player[15])
            pts = str(player[23])
            eff = str(player[24])
            
            row = (name, team, ft_pct, pts, eff)
            players.append(row)
        except IndexError:
            pass
    return players


def create_nba_table():
    conn = sqlite3.connect("finalproj.db")
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS NBAplayers")
    c.execute("""
        CREATE TABLE NBAplayers (
            PLAYER TEXT,
            TEAM TEXT,
            FT_PCT TEXT,
            PTS TEXT,
            EFF TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_nba_data(players):
    conn = sqlite3.connect("finalproj.db")
    c = conn.cursor()
    c.executemany("INSERT INTO NBAplayers VALUES (?, ?, ?, ?, ?)", players)

    conn.commit()
    conn.close()
'''

################# MAIN ##########################################################################################################

def main():
    
    # calls from RICK AND MORTY
    cur, conn = open_RM_database('finalproj.db')
    insert_RM_data()
    conn.close()
    
    # calls from POKEMON
    open_database('Pokemon')
    read_api('https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0')
    pokemon_data()
    
    # calls from HARRY POTTER
    create_hp_table()
    hp_data = get_hp_data()
    hp_characters = extract_hp_data(hp_data, start=0, end=100)  # Provide start and end arguments
    insert_hp_data()
    pokemon_data()
    insert_RM_data()

    
    # retrieve the data from the database
    conn = sqlite3.connect("finalproj.db")
    c = conn.cursor()
    c.execute("SELECT * FROM HarryPotterCharacters")
    rows = c.fetchall()
    conn.close()

    # calls from NBA
    #q_data = get_nba_data()
    #quotes = extract_nba_data(q_data)
    #create_nba_table()
    #insert_nba_data(quotes)


if __name__ == "__main__":
    main()
