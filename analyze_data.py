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


def main():
# calls from SPOTIPY
    
    
    
# calls from MARVEL
    
    
    
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

