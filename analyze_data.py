import matplotlib.pyplot as rmplt
import matplotlib.pyplot as pokeplt
import matplotlib.pyplot as hpplt
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
    rmplt.pie(y, labels = mylabels, colors=['lavender', 'bisque'])
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

    # making the visualization
    y_pos = np.arange(len(names_tup))
    pokeplt.bar(y_pos, bmr_lst, align='center', alpha=0.5)
    pokeplt.xticks(y_pos, names_tup)
    pokeplt.ylabel('Pokemon BMR')
    pokeplt.xlabel('Pokemon Name')
    pokeplt.tick_params(axis='x', which='major', labelsize='5')
    
    pokeplt.title('Top 10 Pokemon BMR')

    
    
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
    
    hpplt.show()


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

def read_NBA_data(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Retrieve the required columns from the NBAplayers table
    c.execute("SELECT PTS, REB, AST, STL, BLK, FGM, FGA, FTM, FTA, TOV, GP FROM NBAplayers")
    rows = c.fetchall()
    
    # Separate the data into separate lists and convert to float data type
    PTS = [float(row[0]) for row in rows]
    REB = [float(row[1]) for row in rows]
    AST = [float(row[2]) for row in rows]
    STL = [float(row[3]) for row in rows]
    BLK = [float(row[4]) for row in rows]
    FGM = [float(row[5]) for row in rows]
    FGA = [float(row[6]) for row in rows]
    FTM = [float(row[7]) for row in rows]
    FTA = [float(row[8]) for row in rows]
    TOV = [float(row[9]) for row in rows]
    GP = [float(row[10]) for row in rows]
    
    conn.close()
    
    return PTS, REB, AST, STL, BLK, FGM, FGA, FTM, FTA, TOV, GP


def calculate_PER(PTS, REB, AST, STL, BLK, FGM, FGA, FTM, FTA, TOV, GP):
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
    return PER


def top_5_PER_players(db_file):
    PTS, REB, AST, STL, BLK, FGM, FGA, FTM, FTA, TOV, GP = read_NBA_data(db_file)

    players = []
    for i in range(len(PTS)):
        player_stats = {}
        player_stats['name'] = 'Player ' + str(i+1)
        player_stats['PTS'] = PTS[i]
        player_stats['REB'] = REB[i]
        player_stats['AST'] = AST[i]
        player_stats['STL'] = STL[i]
        player_stats['BLK'] = BLK[i]
        player_stats['FGM'] = FGM[i]
        player_stats['FGA'] = FGA[i]
        player_stats['FTM'] = FTM[i]
        player_stats['FTA'] = FTA[i]
        player_stats['TOV'] = TOV[i]
        player_stats['GP'] = GP[i]
        player_stats['PER'] = calculate_PER(PTS[i], REB[i], AST[i], STL[i], BLK[i], FGM[i], FGA[i], FTM[i], FTA[i], TOV[i], GP[i])
        players.append(player_stats)

    players.sort(key=lambda x: x['PER'], reverse=True)

    top_5 = players[:5]
    return top_5


def create_NBA_visualization(db_file, conn):
    top_players = top_5_PER_players(db_file)

    player_names = [player['name'] for player in top_players]
    player_per = [player['PER'] for player in top_players]

    plt.bar(player_names, player_per)
    plt.xlabel('Player Names')
    plt.ylabel('PER Ratings')
    plt.title('Top 5 NBA Players by PER Rating')
    
    plt.show()


################# MAIN ##########################################################################################################


def main():
    db_file = 'finalproj.db'
    conn = sqlite3.connect(db_file)

    # calls from RICK AND MORTY

    # calls from POKEMON
    read_POKEMON_data(db_file)

    # calls from HARRY POTTER
    data, conn = read_HP_data(db_file)
    averages = calculate_HP(conn)
    create_HP_visualization(db_file)
    create_HP_visualization_2(db_file, conn)

    # calls from NBA
    top_5_PER_players(db_file)
    create_NBA_visualization(db_file, conn)

    conn.commit()
    conn.close()



if __name__ == "__main__":
    main()


