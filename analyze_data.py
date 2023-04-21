import matplotlib.pyplot as rmplt
import matplotlib.pyplot as pokeplt
import matplotlib.pyplot as hpplt
import matplotlib.pyplot as nbaplt

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import sqlite3


# implement functions here:

############## RICK AND MORTY API #########################################################################################################
def read_RM_data(db):

    #calculations setup
    conn = sqlite3.connect(db)
    c = conn.cursor()
    result = c.execute('SELECT * FROM RickAndMorty')
    total = result.fetchall()
    gender = [row[4] for row in total]

    #calculate male percentages 
    male_count = (gender.count('Male') / len(gender)) * 100
    #calculate female percentages
    female_count = (gender.count('Female') / len(gender)) * 100


    #making the viz
    y = np.array([male_count, female_count])
    mylabels = ["Male", "Female"]
    rmplt.pie(y, labels = mylabels, colors=['lavender', 'bisque'], autopct='%1.1f%%')
    rmplt.title('Gender Breakdown of Rick and Morty Characters')
    rmplt.show() 

############### POKEMON API ###############################################################################################################

def read_POKEMON_data(db_file):
    bmr_lst = []
    names_tup = ()
    conn = sqlite3.connect(db_file)
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

    #making the visualization
    y_pos = np.arange(len(names_tup))
    pokeplt.bar(y_pos, bmr_lst, align='center', alpha=0.5)
    pokeplt.xticks(y_pos, names_tup)
    pokeplt.ylabel('Pokemon BMR')
    pokeplt.xlabel('Pokemon Name')
    pokeplt.tick_params(axis='x', which='major', labelsize='5')
    pokeplt.title('Top 10 Pokemon BMR')
    pokeplt.show()

    
    
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
    hpplt.bar(r1, student_averages, color='blue', width=bar_width, edgecolor='black', label='Average Student')
    hpplt.bar(r2, staff_averages, color='orange', width=bar_width, edgecolor='black', label='Average Staff')

    # Add labels, title, and legend
    hpplt.xlabel('House')
    hpplt.xticks([r + bar_width/2 for r in range(len(student_averages))], x_labels)
    hpplt.ylabel('Average Count')
    hpplt.title('Average Student and Staff Count by House')
    
    hpplt.legend()
    
    #hpplt.show()


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
    fig, ax = hpplt.subplots()
    ax.bar(r1, student_counts, color='blue', width=bar_width, edgecolor='black', label='Students')
    ax.bar(r2, staff_counts, color='orange', width=bar_width, edgecolor='black', label='Staff')

    # Add labels, title, and legend
    ax.set_xlabel('House')
    ax.set_ylabel('Count')
    ax.set_title('Counts of Students vs Staff in Each House')
    ax.set_xticks([r + bar_width/2 for r in range(len(student_counts))])
    ax.set_xticklabels(houses)
    ax.legend()
    
    hpplt.show()
    

################# NBA API ################################################################################################################
############## EXTRA CREDIT ##############################################################################################################

def get_NBA_data():
    """
    Retrieve a joined result set of NBAplayers and NBAstats tables based on the integer key player_id
    """
    conn = sqlite3.connect('finalproj.db')
    c = conn.cursor()
    c.execute("SELECT NBAplayers.PLAYER_ID, NBAstats.PTS, NBAstats.REB, NBAstats.AST, NBAstats.STL, NBAstats.BLK, NBAstats.FGM, NBAstats.FGA, NBAstats.FTM, NBAstats.FTA, NBAstats.TOV, NBAstats.GP \
                FROM NBAplayers \
                INNER JOIN NBAstats \
                ON NBAplayers.PLAYER_ID = NBAstats.PLAYER_ID \
                ORDER BY NBAstats.PTS DESC")
    rows = c.fetchall()
    conn.close()

    return rows



def calculate_PER(player_id, PTS, REB, AST, STL, BLK, FGM, FGA, FTM, FTA, TOV, GP):
    PTS = float(PTS)
    REB = float(REB)
    AST = float(AST)
    STL = float(STL)
    BLK = float(BLK)
    FGM = float(FGM)
    FGA = float(FGA)
    FTM = float(FTM)
    FTA = float(FTA)
    TOV = float(TOV)
    GP = float(GP)
    PER = (PTS + REB + AST + STL + BLK - (FGA - FGM) - (FTA - FTM) - TOV) / GP

    return (player_id, PER)


def create_NBA_visualization(db_file):
    # Retrieve NBA data from the database
    rows = get_NBA_data()

    # Calculate PER score for each player
    per_scores = []
    for row in rows:
        per_scores.append(calculate_PER(*row))

    # Sort players by PER score and select top 10
    top_10_players = sorted(per_scores, key=lambda x: x[1], reverse=True)[:10]

    # Extract player IDs and PER scores
    player_ids = [player_id for player_id, per_score in top_10_players]
    per_scores = [per_score for player_id, per_score in top_10_players]

    # Create bar chart
    nbaplt.bar(range(len(player_ids)), per_scores)
    nbaplt.xticks(range(len(player_ids)), player_ids)
    nbaplt.ylim(0, 1)
    nbaplt.xlabel('Player ID')
    nbaplt.ylabel('PER Score')
    nbaplt.title('Top 10 NBA Players by PER Score')
    nbaplt.show()



'''
def top_5_PER_players(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT NBAplayers.PLAYER_ID, NBAstats.PTS, NBAstats.REB, NBAstats.AST, NBAstats.STL, NBAstats.BLK, NBAstats.FGM, NBAstats.FGA, NBAstats.FTM, NBAstats.FTA, NBAstats.TOV, NBAstats.GP \
                FROM NBAplayers \
                INNER JOIN NBAstats \
                ON NBAplayers.PLAYER_ID = NBAstats.PLAYER_ID")
    rows = c.fetchall()

    per_scores = []

    for row in rows:
        print(f"Input values for player {row[0]}: PTS={row[1]}, REB={row[2]}, AST={row[3]}, STL={row[4]}, BLK={row[5]}, FGM={row[6]}, FGA={row[7]}, FTM={row[8]}, FTA={row[9]}, TOV={row[10]}, GP={row[11]}")
        per_scores.append(calculate_PER(*row))


    top_5_players = sorted(per_scores, key=lambda x: x[1], reverse=True)[:5]
    top_5_players_int = [(int(player_id), int(per_score)) for player_id, per_score in top_5_players]

    conn.close()

    print("top_5_players_int: ")
    print(top_5_players_int)
    return top_5_players_int
'''






################# MAIN ##########################################################################################################

def main():
    db_file = 'finalproj.db'
    conn = sqlite3.connect(db_file)

    # calls from RICK AND MORTY
    read_RM_data(db_file)

    # calls from POKEMON
    read_POKEMON_data(db_file)

    # calls from HARRY POTTER
    data, conn = read_HP_data(db_file)
    averages = calculate_HP(conn)
    create_HP_visualization(db_file)
    create_HP_visualization_2(db_file, conn)

    # calls from NBA
    create_NBA_visualization(db_file)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()


