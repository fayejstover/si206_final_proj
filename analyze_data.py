import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import requests
import json

# implement functions here:

############## SPOTIPY API ###############


############### POKEMON API ###############
def get_bmr(db):
    bmr_lst = []
    names_tup = ()
    conn = sqlite3.connect(db)
    c = conn.cursor()
    
    result = c.execute('SELECT * FROM Pokemon')
    db_length = len(result.fetchall())

    for x in range(1,11):
        result = c.execute(f"SELECT height, weight FROM Pokemon WHERE id = {x}")
        height_weight = result.fetchall()

        bmr = 88.362 + (13.397 * height_weight[0][1]) + (4.799 * height_weight[0][0]) - (5.677 * 20)
        bmr_lst.append(bmr)
        res_names = c.execute(f"SELECT name FROM Pokemon WHERE id = {x}")
        names = res_names.fetchone()
        names_tup = names_tup + names
    conn.close()
    
    # making the visualization
    y_pos = np.arange(len(names_tup))
    plt.bar(y_pos, bmr_lst, align='center', alpha=0.5)
    plt.xticks(y_pos, names_tup)
    plt.ylabel('Pokemon BMR')
    plt.xlabel('Pokemon Name')
    plt.tick_params(axis='x', which='major', labelsize='5')
    plt.title('Top 10 Pokemon BMR')

    plt.show()

############ HARRY POTTER API ############


def get_house_counts(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    house_counts = {}
    
    for row in c.execute("SELECT house, COUNT(*) FROM characters GROUP BY house"):
        house_counts[row[0]] = row[1]
        
    conn.close()
    return house_counts


def create_visualization(db_file):
    house_counts = get_house_counts(db_file)
    
    labels = list(house_counts.keys())
    values = list(house_counts.values())
    
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title('Distribution of Hogwarts Houses')
    plt.show()
  
def read_data(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Retrieve the team, FT_PCT, and PTS columns from the NBAplayers table
    c.execute("SELECT team, FT_PCT, PTS FROM NBAplayers")
    rows = c.fetchall()
    
    # Separate the teams, FT_PCT, and PTS into separate lists
    teams = [row[0] for row in rows]
    ft_pct = [row[1] for row in rows]
    pts = [row[2] for row in rows]
    
    conn.close()
    
    return teams, ft_pct, pts



################# NBA API ################
############## EXTRA CREDIT ##############

def calculate_averages(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Get a list of all the unique teams
    c.execute("SELECT DISTINCT team FROM NBAplayers")
    teams = [row[0] for row in c.fetchall()]

    # Calculate the average FT_PCT and PTS for each team
    avg_ft_pct = []
    avg_pts = []
    for team in teams:
        c.execute("SELECT FT_PCT, PTS FROM NBAplayers WHERE team=?", (team,))
        rows = c.fetchall()
        ft_pct = [row[0] for row in rows]
        pts = [row[1] for row in rows]
        avg_ft_pct.append(sum(ft_pct) / len(ft_pct))
        avg_pts.append(sum(pts) / len(pts))

    conn.close()
    
    print("teams, avg_ft_pct, avg_pts: ")
    print(teams, avg_ft_pct, avg_pts)
    return teams, avg_ft_pct, avg_pts


def main():
# calls from SPOTIPY
    
    
    
# calls from POKEMON
get_bmr('finalproj.db')
        
    
# calls from HARRY POTTER
    db_file = 'hp_characters.db'
    create_visualization(db_file)
 

# ignore - made to stop compilation error
    '''
    labels = ["stuff 1", "stuff 2", "stuff 3", "stuff 4"]
    values = [3, 5, 7,  22]
            
    # Create a bar chart using matplotlib
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title(" title of stuff ")
    ax.set_xlabel(" x-axis title ")
    ax.set_ylabel(" y-axis title ")
    plt.show()
    '''

if __name__ == "__main__":
    main()

