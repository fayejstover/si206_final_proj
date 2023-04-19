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


def main():
# calls from SPOTIPY
    
    
    
# calls from MARVEL
    
    
    
# calls from HARRY POTTER
 

# ignore - made to stop compilation error

    labels = ["stuff 1", "stuff 2", "stuff 3", "stuff 4"]
    values = [3, 5, 7, 22]
    
    # Create a bar chart using matplotlib
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title(" title of stuff ")
    ax.set_xlabel(" x-axis title ")
    ax.set_ylabel(" y-axis title ")
    plt.show()


if __name__ == "__main__":
    main()

