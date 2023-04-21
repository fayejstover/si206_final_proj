# SI 206 FINAL PROJECT
# AGNES MAR, FAYE STOVER, CHLOE EMCH

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

def insert_RM_data(conn):
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS RickAndMorty (name TEXT UNIQUE, id INTEGER UNIQUE, status TEXT, species TEXT, gender TEXT)')
    c.execute('SELECT * FROM RickAndMorty WHERE id  = (SELECT MAX(id) FROM RickAndMorty)')

    data_dic = read_RM_api('https://rickandmortyapi.com/api/character')
    info = data_dic["info"]
    #db_length = c.execute('SELECT COUNT(*) FROM RickAndMorty').fetchone()[0]
    result = c.execute('SELECT COUNT(*) FROM RickAndMorty')
    db_length = result.fetchone()[0]
    page = min(db_length/20 + 1, 42) 
    data_dic = read_RM_api(f'https://rickandmortyapi.com/api/character/?page={page}')
    # print(data_dic)
    for character in data_dic["results"]:
        name = character["name"]
        my_id = character["id"]
        status = character["status"]
        species = character["species"]
        gender = character["gender"]
        c.execute("INSERT OR IGNORE INTO RickAndMorty (name, id, status, species, gender) VALUES (?,?,?,?,?)",(name, my_id, status, species, gender))
           
    conn.commit()
    


############## POKEMON API ########################################################################################################
def open_POKEMON_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    return conn

def read_POKEMON_api(url):
    req = requests.get(url)
    info = req.text
    text = json.loads(info)
    return text


def pokemon_data():
    conn = sqlite3.connect('finalproj.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Pokemon (name TEXT, id INTEGER, height INTEGER, weight INTEGER)')
    conn.commit()

    data_dic = read_POKEMON_api('https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0')
    result = c.execute('SELECT COUNT(*) FROM Pokemon')
    db_length = result.fetchone()[0]
    
    for x in range(db_length, db_length + 100, 25):
        data_slice = data_dic['results'][x:min(x+25, db_length+100)]
        for pokemon in data_slice:
            name = pokemon['name']
            url = pokemon['url']
            pokemon_api = read_POKEMON_api(url)
            height = pokemon_api['height']
            id = pokemon_api['id']
            weight = pokemon_api['weight']
            c.execute("INSERT OR IGNORE INTO Pokemon (name, id, height, weight) VALUES (?,?,?,?)",(name, id, height, weight))
    conn.commit()
    conn.close()

    

########## HARRY POTTER API ####################################################################################################
def get_HP_data():
    url = "https://hp-api.onrender.com/api/characters"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("error (1)")


def extract_HP_data(data, start, end):
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


def create_HP_table():
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


def insert_HP_data(start=0, end=100):
    conn = sqlite3.connect("finalproj.db")
    c = conn.cursor()

    data = get_HP_data()
    characters = extract_HP_data(data, start, end)

    c.executemany("INSERT INTO HarryPotterCharacters VALUES (?, ?, ?, ?)", characters)

    conn.commit()
    conn.close()

    
    
################# NBA API ##########################################################################################################
############## EXTRA CREDIT ########################################################################################################


def create_tables():
    """
    Create the two tables in the SQLite database
    """
    conn = sqlite3.connect('finalproj.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS NBAplayers
                 (PLAYER INTEGER PRIMARY KEY,
                  RANK INTEGER,
                  PLAYER_ED TEXT,
                  TEAM_ID INTEGER,
                  TEAM TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS NBAstats
                 (PLAYER INTEGER PRIMARY KEY,
                  PTS REAL,
                  REB REAL,
                  AST REAL,
                  STL REAL,
                  BLK REAL,
                  FGM REAL,
                  FGA REAL,
                  FTM REAL,
                  FTA REAL,
                  TOV REAL,
                  GP REAL)''')
    conn.commit()
    conn.close()

def insert_data():
    """
    Fetch data from the NBA API and insert it into the SQLite tables
    """
    url = "https://stats.nba.com/stats/leagueleaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2021-22&SeasonType=Regular+Season&StatCategory=PTS"
    response = requests.get(url)
    data = response.json()["resultSet"]["rowSet"]

    conn = sqlite3.connect('finalproj.db')
    c = conn.cursor()

    for row in data:
        player = row[0]
        rank = row[1]
        player_id = row[2]
        team_id = row[3]
        team = row[4]
        gp = row[5]
        fgm = row[7]
        fga = row[8]
        ftm = row[13]
        fta = row[14]
        reb = row[18]
        ast = row[19]
        stl = row[20]
        blk = row[21]
        tov = row[22]
        pts = row[23]

        c.execute("INSERT INTO NBAplayers (PLAYER, RANK, PLAYER_ID, TEAM_ID, TEAM) VALUES (?, ?, ?, ?, ?)",
                  (player, rank, player_id, team_id, team))
        c.execute("INSERT INTO NBAstats (PLAYER, PTS, REB, AST, STL, BLK, FGM, FGA, FTM, FTA, TOV, GP) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (player, pts, reb, ast, stl, blk, fgm, fga, ftm, fta, tov, gp))

    conn.commit()
    conn.close()



################# MAIN ##########################################################################################################

def main():
    # calls from RICK AND MORTY
    curr, conn = open_RM_database('finalproj.db')
    # conn.set_trace_callback(print)
    insert_RM_data(conn)
    conn.close()

    # calls from POKEMON
    poke_conn = open_POKEMON_database('finalproj.db')
    # poke_conn.set_trace_callback(print)
    pokemon_data()
    poke_conn.close()

    # calls from HARRY POTTER
    create_HP_table()
    hp_data = get_HP_data()
    extract_HP_data(hp_data, start=0, end=100)  
    insert_HP_data()

    # calls from NBA
    create_tables()
    insert_data()

if __name__ == "__main__":
    main()


