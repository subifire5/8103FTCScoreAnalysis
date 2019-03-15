import os
import csv
import statistics as st
import collections as cs
from CSVRankings import csv_sheet

import pandas
import numpy as np


def data_col(refcsv, cwda, csva):

    raw_data = csv_sheet(refcsv, cwda, csva)
    print(raw_data[0])
    print(raw_data[6])
    raw_matches = raw_data[0]
    teams = raw_data[1]

    total_scores = np.array(raw_data[2], dtype=np.float64)
    auto_scores = np.array(raw_data[3], dtype=np.float64)
    teleop_scores = np.array(raw_data[4], dtype=np.float64)
    endgame_scores = np.array(raw_data[5], dtype=np.float64)
    match_order = raw_data[6]  # the order of the matches, identifiable by match-code, are in the matrices
    team_order = raw_data[7]
    full_csv = raw_data[8]
    match_stats = raw_data[9]
    team_scores = raw_data[10]
    # appends as many empty lists as matches

    count = 1

    match_matrix = np.array(raw_matches, dtype=np.float64)
    print('collecting data')
    print(total_scores)
    print(raw_data[2])
    print(teams)
    matrices = [match_matrix, teams, total_scores, auto_scores, teleop_scores,
                endgame_scores, match_order, team_order, full_csv, match_stats, team_scores]
    return matrices


def opr(teams, matches, scores, team_order, **kwargs):
    # Transposing The match matrices
    print(scores)
    match_trp = matches.transpose()

    # The product of the transpose and the original
    matches_of_trp = (match_trp @ matches)
    print(matches_of_trp)
    print('next is score trp')
    # The product of the transpose and the scores
    score_trp = (match_trp @ scores)
    print(score_trp)
    '''
    The steps outlined above, create a transpose of the matches matrix
    then multiply both sides of the matches equation by the transpose
    on one side is the scores matrix and on the other is the matches matrix
    
    The equation is solved below using least squares
    
    the solutions are placed back into the dictionary by a team's position in the original matrix
    In other words, if a team was the furthest left column in the original matrix,
    they will be the first accounted for in the dictionary , and second out will the second from the left
    
    '''

    x, residuals, rank, s = np.linalg.lstsq(matches_of_trp, score_trp, rcond=None)
    solutions = list(x)  # a list of the solutions to this linear algebra
    print(solutions)
    count = 0

    # rounds to the nth_digit
    if 'nth_digit' in kwargs:
        solutions = np.around(solutions, kwargs['nth_digit'])

    # this code sorts through each team and inserts an OPR based on their team number
    while count < len(team_order):
        if 'section' in kwargs:
            section = kwargs['section']
            teams[team_order[count]][section + ' OPR'] = solutions[count]
        else:
            teams[team_order[count]]['OPR'] = solutions[count]
        count += 1
    print(teams)


def stdev(teams, team_scores, **kwargs):
    if 'section' in kwargs:
        section = kwargs['section']
    else:
        section = 'Total'
    if 'nth_digit' in kwargs:
        nth_digit = kwargs['nth_digit']
        rounding = True
    else:
        rounding = False
    for teamn in teams:
        temp_stdev = []
        if rounding:
            for score in team_scores[teamn][section]:
                temp_stdev.append(np.around(score, kwargs['nth_digit']))
        else:
            for score in team_scores[teamn][section]:
                temp_stdev.append(score)
        teams[teamn]['StdDev'] = st.stdev(temp_stdev)
    return teams


def median(teams, team_scores, **kwargs):
    if 'section' in kwargs:
        section = kwargs['section']
    else:
        section = 'Total'

    for teamn in teams:
        temp_median = []
        for score in team_scores[teamn][section]:
            temp_median.append(score)
        teams[teamn]['Median'] = st.median(temp_median)
    return teams


def medstd(teams, **kwargs):
    if 'nth_digit' in kwargs:
        nth_digit = kwargs['nth_digit']
        rounding = True
    else:
        rounding = False
    if rounding:
        for teamn in teams:
            if teams[teamn]['StdDev'] == 'NA':
                teams[teamn]['Med-Std'] = 'NA'
                teams[teamn]['Med+Std'] = 'NA'
            elif teams[teamn]['Median'] == 'NA':
                teams[teamn]['Med-Std'] = 'NA'
                teams[teamn]['Med+Std'] = 'NA'
            else:
                teams[teamn]['Med-Std'] = np.around(teams[teamn]['Median'] - teams[teamn]['StdDev'], nth_digit)
                teams[teamn]['Med+Std'] = np.around(teams[teamn]['Median'] + teams[teamn]['StdDev'], nth_digit)
    else:
        for teamn in teams:
            if teams[teamn]['StdDev'] == 'NA':
                teams[teamn]['Med-Std'] = 'NA'
                teams[teamn]['Med+Std'] = 'NA'
            elif teams[teamn]['Median'] == 'NA':
                teams[teamn]['Med-Std'] = 'NA'
                teams[teamn]['Med+Std'] = 'NA'
            else:
                teams[teamn]['Med-Std'] = teams[teamn]['Median'] - teams[teamn]['StdDev']
                teams[teamn]['Med+Std'] = teams[teamn]['Median'] + teams[teamn]['StdDev']

# Second-worst


def misc_score(teams, team_scores):
    for teamn in teams:
        temp_best = team_scores[teamn]['Total'][0]
        temp_worst = team_scores[teamn]['Total'][0]
        for score in team_scores[teamn]['Total']:
            print(team_scores)
            if temp_best < score:
                temp_best = score
            if temp_worst > score:
                temp_worst = score
        teams[teamn]['Best Score'] = temp_best
        teams[teamn]['Worst Score'] = temp_worst
        teams[teamn]['NumOfScores'] = len(team_scores[teamn]['Total'])
        print(teams[teamn])
    return teams


'''
CCWM is how much a team contributed to the winning margin of the match
CCWM = (OPR-DPR)
DPR is how much, on average, a team will score against your alliance
'''


def dpr(teams, full_csv, match_stats, **kwargs):
    nonmatch = 0

    for team in teams:
        count = 0
        temp_dpr = []
        while count < len(full_csv):

            codes = match_stats[team]
            for match_code in codes:
                color = list(match_code).pop(0)
                match_code = list(match_code)
                match_code.pop(0)
                match_code = ''.join(str(a) for a in match_code)

                if str(match_code) == full_csv[count]['Match code']:
                    print('found')
                    if color == 'R':
                        score = int(full_csv[count]['Blue auto']) + int(full_csv[count]['Blue teleop']) +\
                                int(full_csv[count]['Blue endgame']) + int(full_csv[count]['Red penalty'])
                        temp_dpr.append(score/2)
                    if color == 'B':
                        score = int(full_csv[count]['Red auto']) + int(full_csv[count]['Red teleop']) + \
                                int(full_csv[count]['Red endgame']) + int(full_csv[count]['Blue penalty'])
                        temp_dpr.append(score/2)

            count += 1
        teams[team]['DPR'] = np.mean(temp_dpr)
    print(teams)
    return teams


def ccwm(teams, **kwargs):
    if 'nth_digit' in kwargs:
        nth_digit = kwargs['nth_digit']
        rounding = True
    else:
        rounding = False
    for teamn in teams:
        if rounding:
            teams[teamn]['CCWM'] = np.around(teams[teamn]['OPR'] - teams[teamn]['DPR'], nth_digit)
        else:
            teams[teamn]['CCWM'] = teams[teamn]['OPR'] - teams[teamn]['DPR']


def scout(teams, cwdpit, pit):

    with open(pit) as csvFile:
        result_sheet = csv.DictReader(csvFile, delimiter=',')
        for row in result_sheet:
            # if row_count > 0:

            row_dict = dict(row)

            scoutn = row_dict['Team #']
            crater = row_dict['Full Auto Crater']
            depot = row_dict['Full Auto Depot']
            breakable = row_dict['Breakable']
            side = row_dict['Preferred Side']
            for teamn in teams:
                try:
                    r = teams[teamn]['FullCrater']
                except KeyError:

                    if teams[teamn]['Team #'] == scoutn:
                        teams[teamn]['FullCrater'] = crater
                        teams[teamn]['FullDepot'] = depot
                        teams[teamn]['Breakable'] = breakable
                        teams[teamn]['Preferred Side']  = side
                        break

# checks if they've been on silver or gold more
# if they have been on silver and gold the same amount, it will assume gold.


def dqs(teams):
    for teamn in teams:
        teams[teamn]['DQ'] = 0
        if teams[teamn]['Disconnects'] > 1:
            teams[teamn]['DQ'] += 1
        if teams[teamn]['Auto Avg.'] < 60:
            teams[teamn]['DQ'] += 1
        if teams[teamn]['Missed Hangs'] > 1:
            teams[teamn]['DQ'] += 1

        try:
            if teams[teamn]['Breakable'] == 'yes':
                teams[teamn]['DQ'] += 1
        except KeyError:
            print('Scout Sheet Missing ' + teamn)


'''

excel hyperlink formatting:
Each hyperlink will fit into a cell
=HYPERLINK("C:/bill/bob.txt", "bob")
bob.txt is the file it will link to
bob is what will show up in the cell

But python strings use quotes to denote when a str starts or ends
So how do you get quotes to show up?

to get around this there are two methods:

1. use '' for all programming uses, and "" for quotes you want to show up
    for example: 
    r = 'billy said "bob sucks"'
    print(r)
    billy said "bob sucks
    
2. triple quoting (when you need to use both types of quotes)
use """ and everything after that until another """ is text

    for example;
    r = """Bob: "The book says 'Ho ho ho!'" """
    print(r)
    Bob: "The book says 'Ho ho ho!'"

so: 
r = '=HYPERLINK("C:/bill/bob.txt", "bob")
r will now make the cell say bob and link to bob.txt


Alternatively: How to use .format

.format() is a function you can add to the end of a string to pass in non-string variables

for example:
r = '=HYPERLINK("{}", "{}").format(cwd, file)
or 
r= 'HYPERLINK("{x}", "{y}").format(x=cwd, y=file)

'''


def pics(teams, ploc):  # turns a teams pictures into an excel hyperlinks
    exten = '.jpg'
    cwd = os.getcwd()
    print('here')
    print(cwd)
    for teamn in teams:
        temp_num = teams[teamn]['Team #']
        pic_path = cwd+ploc+temp_num+exten

        #  pic_path = os.path.join(cwd, ploc, temp_num+exten)
        print(temp_num)
        print(pic_path)
        if os.path.isfile(pic_path):
            print('file found')
            #  x = '=HYPERLINK("' + pic_path + '","' + temp_num + ' ")'
            x= '=HYPERLINK("{}", "{}")'.format(pic_path, temp_num)
            teams[teamn]['Picture'] = x
        else:
            teams[teamn]['Picture'] = 'NA'
            print('File not found')


def create_file(teams, cwd, csv2, default_d,  metric):

    y = sorted(teams, key=lambda x: (teams[x][metric]), reverse=True)
    print('ordering below')
    print(os.getcwd())
    csv2 = os.getcwd() + csv2

    c = 1

    del default_d['Picture']
    if os.path.exists(csv2):  # deletes the rankings file if it exists
        os.remove(csv2)
    with open(csv2, 'w+', newline='') as f:  # creates a new file
        w = csv.DictWriter(f, default_d.keys(), extrasaction='ignore')  # i

        w.writeheader()
        while (c < len(y)) and (c < 17):
            if teams[y[c - 1]]['Picture'] == 'NA':
                non = 'done'
            else:
                teams[y[c - 1]]['Team #'] = teams[y[c - 1]]['Picture']
            del teams[y[c - 1]]['Picture']
            print(teams[y[c - 1]])
            w.writerow(teams[y[c - 1]])
            c += 1

# OPR


'''
Below is what is actually run
'''


def main():

    os.chdir("..")  # the folder where all program files are kept

    cwd = os.getcwd()
    print(cwd)

    cwda = "CSV"  # a location of the csv's you want.
    csva = "/CSV/OPRDataSet1.csv"  # the csv's in question
    refcsv1 = "/CSV/ReferenceList1.csv"  # csv with some team names
    ranking_cwd = "/CSV/"  # the folder of the rankings csv
    ranking_csv = "/CSV/Rankings.csv"  # The file that you want to place the rankings in.
    cwdpit = 'CSV'  # the pit scout location
    pit = 'CSV/Pit_Scouting.csv'  # pit scout csv
    pic_cwd = '/TeamPics/'  # the location of the teams pictures

    metric = 'OPR'

    years = ['2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009']
    default_d = {'Team #': 0,   # A Default team, updated with keys, used as the
                 'Name': 'NA',  # index for all of the keys a team would have
                 'DQ': 0,
                 'Best Score': 0,
                 'Worst Score': 0,
                 'NumOfScores': 0,
                 'OPR': 0,
                 'DPR': 0,
                 'CCWM': 0,
                 'Median': 0,
                 'StdDev': 0,
                 'Med-Std': 0,
                 'Med+Std': 0,
                 'Preferred Side': 'None',
                 'Picture': ''
                 }
    '''
    [match_matrix, teams, total_scores, auto_scores, teleop_scores,
                endgame_scores, match_order, team_order, raw_matches[0], full_csv, match_stats
    '''
    # collects the data
    data = data_col(refcsv1, cwda, csva)
    match_matrix = data[0]
    teams = data[1]
    total_scores = data[2]
    auto_scores = np.array(data[3], dtype=np.float64)
    teleop_scores = np.array(data[4], dtype=np.float64)
    endgame_scores = np.array(data[5], dtype=np.float64)
    match_order = data[6]
    team_order = data[7]
    full_csv = data[8]
    match_stats = data[9]
    team_scores = data[10]

    opr(teams, match_matrix, total_scores, team_order, nth_digit=2)
    opr(teams, match_matrix, auto_scores, team_order, section='Auto', nth_digit=2)
    opr(teams, match_matrix, teleop_scores, team_order, section='Teleop', nth_digit=2)
    opr(teams, match_matrix, endgame_scores, team_order, section='Endgame', nth_digit=2)
    dpr(teams, full_csv, match_stats, nth_digit=2)
    ccwm(teams, nth_digit=2)

    median(teams, team_scores, section='Auto')
    median(teams, team_scores)
    stdev(teams, team_scores, section='Auto', nth_digit=2)
    stdev(teams, team_scores, nth_digit=2)
    medstd(teams, nth_digit=2)
    pics(teams, pic_cwd)
    misc_score(teams, team_scores)
    create_file(teams, ranking_cwd, ranking_csv, default_d, metric)

    '''
    # applies the functions to the data
    apply_func(avg_full, median_full, std_full, medstd_full, teams, team_scores,
               auto_scores, teleop_scores, endgame_scores, default_d
               )
    # pref_side(teams, team_scores)
    dpr(matches, teams)
    ccwm(teams)
    scout(teams, cwdpit, pit)
    dqs(teams)

    #  get_name(teams, years)  Tabled Temporarily
    pics(teams, pics1)
    # creates the file

    create_file(teams, cwd, csv2, default_d, metric, colormetric)
    '''


if __name__ == '__main__':
    main()
