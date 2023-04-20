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
    return conn


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

def get_NBA_data():
    url = "https://stats.nba.com/stats/leagueleaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2021-22&SeasonType=Regular+Season&StatCategory=PTS"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("error (2)")

def extract_NBA_data(data):
    players = []
    for player in data["resultSet"]["rowSet"]:
        try:
            name = str(player[2])
            team = str(player[4])
            pts = str(player[23])
            reb = str(player[18])
            ast = str(player[19])
            stl = str(player[20])
            blk = str(player[21])
            fgm = str(player[11])
            fga = str(player[12])
            ftm = str(player[14])
            fta = str(player[15])
            tov = str(player[22])
            gp = str(player[6])

            row = (name, team, pts, reb, ast, stl, blk, fgm, fga, ftm, fta, tov, gp)
            players.append(row)
        except IndexError:
            pass
    return players

def create_NBA_table():
    conn = sqlite3.connect("finalproj.db")
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS NBAplayers")
    c.execute("""
        CREATE TABLE NBAplayers (
            PLAYER TEXT,
            TEAM TEXT,
            PTS TEXT,
            REB TEXT,
            AST TEXT,
            STL TEXT,
            BLK TEXT,
            FGM TEXT,
            FGA TEXT,
            FTM TEXT,
            FTA TEXT,
            TOV TEXT,
            GP TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_NBA_data(players):
    conn = sqlite3.connect("finalproj.db")
    c = conn.cursor()
    c.executemany("INSERT INTO NBAplayers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", players)

    conn.commit()
    conn.close()


################# MAIN ##########################################################################################################

def main():
    
    # calls from RICK AND MORTY
    rm_conn = open_RM_database('finalproj.db')
    insert_RM_data()
    rm_conn.close()
    
    # calls from POKEMON
    poke_conn = open_POKEMON_database('finalproj.db')
    pokemon_data()
    poke_conn.close()
    
    # calls from HARRY POTTER
    create_HP_table()
    hp_data = get_HP_data()
    extract_HP_data(hp_data, start=0, end=100)  
    insert_HP_data()

    conn = sqlite3.connect("finalproj.db")
    c = conn.cursor()
    c.execute("SELECT * FROM HarryPotterCharacters")
    rows = c.fetchall()
    conn.close()

    # calls from NBA
    data = get_NBA_data()
    players = extract_NBA_data(data)
    create_NBA_table()
    insert_NBA_data(players)


if __name__ == "__main__":
    main()


