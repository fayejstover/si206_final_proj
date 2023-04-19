import matplotlib.pyplot as plt
import numpy as np
import os
import sqlite3
import unittest
import requests
import json


# implement functions here:

############## SPOTIPY API ###############################################################################################################


############### POKEMON API ###############################################################################################################

def read_POKEMON_data(db):
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

    
    
############ HARRY POTTER API ############################################################################################################

def read_HP_data(db_file):
    conn = sqlite3.connect(db_file)
    data = {}
    # Query 
    for row in conn.execute("SELECT house FROM HarryPotterCharacters"):
        house = row[0]
        if house in data:
            data[house] += 1
        else:
            data[house] = 1
    conn.commit()
    return data, conn


'''
read in the proper data needed for 
calculate and visualization functions
'''
def calculate_HP(conn):
    student_counts = {}
    staff_counts = {}
    house_counts = []

    # Query
    for row in conn.execute("SELECT house, hogwartsStudent, hogwartsStaff FROM HarryPotterCharacters"):
        house = row[0]
        is_student = row[1]
        is_staff = row[2]

        # count students in house
        if is_student == "True":
            if house in student_counts:
                student_counts[house] += 1
            else:
                student_counts[house] = 1
                
        # count staff in house
        if is_staff == "True":
            if house in staff_counts:
                staff_counts[house] += 1
            else:
                staff_counts[house] = 1

    for house in student_counts.keys():
        student_count = student_counts.get(house, 0)
        staff_count = staff_counts.get(house, 0)
        total_count = student_count + staff_count

        house_counts.append({
            "House": house,
            "total Student": student_count,
            "total Staff": staff_count,
            "AverageStudent": student_count / total_count,
            "AverageStaff": staff_count / total_count
        })

    return house_counts


'''
take the found dictionary     
    {"House": "Slytherin", 
    "AverageStudent": ##, 
    "AverageStaff": ##}
make a side by side bar chart using matplotlib that has:
the x-axis as the different houses
te y-axis as the average hogwartsStudent and average hogwartsStaff
'''
def create_HP_visualization(db_file):
    conn = sqlite3.connect(db_file)
    house_counts = calculate_HP(conn)
    conn.close()

    x_labels = [hc['House'] for hc in house_counts]
    student_averages = [hc['AverageStudent'] for hc in house_counts]
    staff_averages = [hc['AverageStaff'] for hc in house_counts]

    # Set the bar width
    bar_width = 0.4

    # Set the positions of the bars on the x-axis
    r1 = range(len(student_averages))
    r2 = [x + bar_width for x in r1]

    # Create the bar chart
    plt.bar(r1, student_averages, color='blue', width=bar_width, edgecolor='black', label='Average Student')
    plt.bar(r2, staff_averages, color='orange', width=bar_width, edgecolor='black', label='Average Staff')

    # Add labels, title, and legend
    plt.xlabel('House')
    plt.xticks([r + bar_width/2 for r in range(len(student_averages))], x_labels)
    plt.ylabel('Average Count')
    plt.title('Average Student and Staff Count by House')
    plt.legend()

    

def create_HP_visualization_2(db_file, conn):
    house_counts = calculate_HP(conn)

    houses = [hc["House"] for hc in house_counts]
    student_counts = [hc["total Student"] for hc in house_counts]
    staff_counts = [hc["total Staff"] for hc in house_counts]

    # Set the bar width
    bar_width = 0.4

    # Set the positions of the bars on the x-axis
    r1 = range(len(student_counts))
    r2 = [x + bar_width for x in r1]

    # Create the bar chart
    fig, ax = plt.subplots()
    ax.bar(r1, student_counts, color='blue', width=bar_width, edgecolor='black', label='Students')
    ax.bar(r2, staff_counts, color='orange', width=bar_width, edgecolor='black', label='Staff')

    # Add labels, title, and legend
    ax.set_xlabel('House')
    ax.set_ylabel('Count')
    ax.set_title('Counts of Students vs Staff in Each House')
    ax.set_xticks([r + bar_width/2 for r in range(len(student_counts))])
    ax.set_xticklabels(houses)
    ax.legend()
    
    

################# NBA API ################################################################################################################
############## EXTRA CREDIT ##############################################################################################################
'''
def read_NBA_data(db_file):
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

def calculate_NBA_averages(db_file):
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
'''

################# MAIN ##########################################################################################################

def main():
    db_file = 'finalproj.db'

    # calls from SPOTIPY

    # calls from POKEMON
    read_POKEMON_data(db_file)

    # calls from HARRY POTTER
    data, conn = read_HP_data(db_file)
    averages = calculate_HP(conn)
    create_HP_visualization(db_file)
    create_HP_visualization_2(db_file, conn)

    conn.commit()
    conn.close()

    plt.show()
    
    # calls from NBA
    #read_NBA_data(db_file)
    #calculate_NBA_averages(db_file)

if __name__ == "__main__":
    main()
