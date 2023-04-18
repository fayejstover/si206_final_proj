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


conn = sqlite3.connect('hp_characters.db')
c = conn.cursor()

c.execute('SELECT * FROM characters')
rows = c.fetchall()
print(rows)

c.execute('SELECT house, COUNT(*) FROM characters GROUP BY house')
rows = c.fetchall()
print(rows)

conn.commit()
conn.close()


