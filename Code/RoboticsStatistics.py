import os
import csv
import statistics as st
import collections as cs
import EventClass as ec
from CSVRankings import csv_sheet

import pandas
import numpy as np


def data_col(refcsv, cwda, csva, refcsv2):

    raw_events = csv_sheet(refcsv, cwda, csva, refcsv2)
    events = dict()
    for ev in raw_events:
        events[ev] = ec.Event()
        events[ev].raw_matches = raw_events[ev].raw_matches
        events[ev].matches = raw_events[ev].matches
        events[ev].teams = raw_events[ev].teams

        events[ev].total_scores = np.array(raw_events[ev].total_scores, dtype=np.float64)
        events[ev].auto_scores = np.array(raw_events[ev].auto_scores, dtype=np.float64)
        events[ev].teleop_scores = np.array(raw_events[ev].teleop_scores, dtype=np.float64)
        events[ev].endgame_scores = np.array(raw_events[ev].endgame_scores, dtype=np.float64)
        events[ev].match_order = raw_events[ev].match_order  # the order of the matches,
        # identifiable by match-code, are in the matrices
        events[ev].team_order = raw_events[ev].team_order
        events[ev].full_csv = raw_events[ev].full_csv
        events[ev].match_stats = raw_events[ev].match_stats
        events[ev].team_scores = raw_events[ev].team_scores
        # appends as many empty lists as matches

        count = 1

        events[ev].match_matrix = np.array(events[ev].matches, dtype=np.float64)


    nyc = 'NYC FIRST Tech Challenge Qualifier 6'
    return events


def opr(ev, **kwargs):
    if 'section' in kwargs:
        section = kwargs['section']
        if section == 'Auto':
            scores = ev.auto_scores
        elif section == 'Teleop':
            scores = ev.teleop_scores
        elif section == 'Endgame':
            scores = ev.endgame_scores
    else:
        scores = ev.total_scores

    # Transposing The match matrices
    match_trp = ev.match_matrix.transpose()

    # The product of the transpose and the original
    matches_of_trp = (match_trp @ ev.match_matrix)

    # The product of the transpose and the scores
    score_trp = (match_trp @ scores)
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
    while count < len(ev.team_order):
        if 'section' in kwargs:
            section = kwargs['section']
            ev.teams[ev.team_order[count]][section + ' OPR'] = solutions[count]
        else:
            ev.teams[ev.team_order[count]]['OPR'] = solutions[count]
        count += 1


def stdev(ev, **kwargs):
    if 'section' in kwargs:
        section = kwargs['section']
    else:
        section = 'Total'
    if 'nth_digit' in kwargs:
        nth_digit = kwargs['nth_digit']
        rounding = True
    else:
        rounding = False
    for teamn in ev.teams:
        temp_stdev = []
        if rounding:
            for score in ev.team_scores[teamn][section]:
                temp_stdev.append(np.around(score, kwargs['nth_digit']))
        else:
            for score in ev.team_scores[teamn][section]:
                temp_stdev.append(score)
        ev.teams[teamn]['StdDev'] = st.stdev(temp_stdev)
    return ev.teams


def median(ev, **kwargs):
    if 'section' in kwargs:
        section = kwargs['section']
    else:
        section = 'Total'

    for teamn in ev.teams:
        temp_median = []
        for score in ev.team_scores[teamn][section]:
            temp_median.append(score)
        ev.teams[teamn]['Median'] = st.median(temp_median)
    return ev.teams


def medstd(ev, **kwargs):
    if 'nth_digit' in kwargs:
        nth_digit = kwargs['nth_digit']
        rounding = True
    else:
        rounding = False
    if rounding:
        for teamn in ev.teams:
            if ev.teams[teamn]['StdDev'] == 'NA':
                ev.teams[teamn]['Med-Std'] = 'NA'
                ev.teams[teamn]['Med+Std'] = 'NA'
            elif ev.teams[teamn]['Median'] == 'NA':
                ev.teams[teamn]['Med-Std'] = 'NA'
                ev.teams[teamn]['Med+Std'] = 'NA'
            else:
                ev.teams[teamn]['Med-Std'] = np.around(ev.teams[teamn]['Median'] - ev.teams[teamn]['StdDev'], nth_digit)
                ev.teams[teamn]['Med+Std'] = np.around(ev.teams[teamn]['Median'] + ev.teams[teamn]['StdDev'], nth_digit)
    else:
        for teamn in ev.teams:
            if ev.teams[teamn]['StdDev'] == 'NA':
                ev.teams[teamn]['Med-Std'] = 'NA'
                ev.teams[teamn]['Med+Std'] = 'NA'
            elif ev.teams[teamn]['Median'] == 'NA':
                ev.teams[teamn]['Med-Std'] = 'NA'
                ev.teams[teamn]['Med+Std'] = 'NA'
            else:
                ev.teams[teamn]['Med-Std'] = ev.teams[teamn]['Median'] - ev.teams[teamn]['StdDev']
                ev.teams[teamn]['Med+Std'] = ev.teams[teamn]['Median'] + ev.teams[teamn]['StdDev']

# Second-worst


def misc_score(ev):
    for teamn in ev.teams:
        temp_best = ev.team_scores[teamn]['Total'][0]
        temp_worst = ev.team_scores[teamn]['Total'][0]
        for score in ev.team_scores[teamn]['Total']:
            if temp_best < score:
                temp_best = score
            if temp_worst > score:
                temp_worst = score
        ev. teams[teamn]['Best Score'] = temp_best
        ev.teams[teamn]['Worst Score'] = temp_worst
        ev.teams[teamn]['NumOfScores'] = len(ev.team_scores[teamn]['Total'])
    return ev.teams


'''
CCWM is how much a team contributed to the winning margin of the match
CCWM = (OPR-DPR)
DPR is how much, on average, a team will score against your alliance
'''


def dpr(ev, **kwargs):
    nonmatch = 0
    for team in ev.teams:
        count = 0
        temp_dpr = []
        while count < len(ev.full_csv):

            codes = ev.match_stats[team]
            for match_code in codes:
                color = list(match_code).pop(0)
                match_code = list(match_code)
                match_code.pop(0)
                match_code = ''.join(str(a) for a in match_code)

                if str(match_code) == ev.full_csv[count]['Match code']:
                    if color == 'R':

                        score = int(ev.full_csv[count]['Blue auto']) + int(ev.full_csv[count]['Blue teleop']) +\
                                int(ev.full_csv[count]['Blue endgame']) + int(ev.full_csv[count]['Red penalty'])

                        temp_dpr.append(score/2)
                    if color == 'B':
                        score = int(ev.full_csv[count]['Red auto']) + int(ev.full_csv[count]['Red teleop']) + \
                                int(ev.full_csv[count]['Red endgame']) + int(ev.full_csv[count]['Blue penalty'])
                        temp_dpr.append(score/2)

            count += 1
        ev.teams[team]['DPR'] = np.mean(temp_dpr)
    return ev.teams


def ccwm(ev, **kwargs):
    if 'nth_digit' in kwargs:
        nth_digit = kwargs['nth_digit']
        rounding = True
    else:
        rounding = False
    for teamn in ev.teams:
        if rounding:
            ev.teams[teamn]['CCWM'] = np.around(ev.teams[teamn]['OPR'] - ev.teams[teamn]['DPR'], nth_digit)
        else:
            ev.teams[teamn]['CCWM'] = ev.teams[teamn]['OPR'] - ev.teams[teamn]['DPR']


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


def pics(ev, ploc):  # turns a teams pictures into an excel hyperlinks
    exten = '.jpg'
    cwd = os.getcwd()
    for teamn in ev.teams:
        temp_num = ev.teams[teamn]['Team #']
        pic_path = cwd+ploc+temp_num+exten

        #  pic_path = os.path.join(cwd, ploc, temp_num+exten)
        if os.path.isfile(pic_path):
            print('file found')
            #  x = '=HYPERLINK("' + pic_path + '","' + temp_num + ' ")'
            x= '=HYPERLINK("{}", "{}")'.format(pic_path, temp_num)
            ev.teams[teamn]['Picture'] = x
        else:
            ev.teams[teamn]['Picture'] = 'NA'


def create_file(all_teams, cwd, csv2, default_d,  metric):
    y = sorted(all_teams, key=lambda x: (all_teams[x][metric]), reverse=True)
    csv2 = os.getcwd() + csv2

    c = 1

    del default_d['Picture']
    if os.path.exists(csv2):  # deletes the rankings file if it exists
        os.remove(csv2)
    with open(csv2, 'w+', newline='') as f:  # creates a new file
        w = csv.DictWriter(f, default_d.keys(), extrasaction='ignore')  # i

        w.writeheader()
        while (c < len(y)) and (c < 100):
            if all_teams[y[c - 1]]['Picture'] == 'NA':
                non = 'done'
            else:
                all_teams[y[c - 1]]['Team #'] = all_teams[y[c - 1]]['Picture']
            del all_teams[y[c - 1]]['Picture']
            w.writerow(all_teams[y[c - 1]])
            c += 1

# OPR


'''
Below is what is actually run
'''


def main():

    os.chdir("..")  # the folder where all program files are kept

    cwd = os.getcwd()

    cwda = "CSV"  # a location of the csv's you want.
    csva = "/CSV/WAStateRREvents.csv"  # the csv's in question
    refcsv1 = "/CSV/ReferenceList1.csv"  # csv with some team names
    ranking_cwd = "/CSV/"  # the folder of the rankings csv
    ranking_csv = "/CSV/Rankings.csv"  # The file that you want to place the rankings in.
    cwdpit = 'CSV'  # the pit scout location
    pit = 'CSV/Pit_Scouting.csv'  # pit scout csv
    pic_cwd = '/TeamPics/'  # the location of the teams pictures
    all_teams = dict()
    metric = 'OPR'
    specific_teams = True  # look at only specific teams?
    spec_csv = '/CSV/WAStateRoverRuckus.csv'  # csv of teams you want to look for
    spec_teams = []  # list of teams to look for
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
    if specific_teams:
        cwd = os.getcwd()
        match_num = 0
        spec_csv = cwd + spec_csv
        with open(spec_csv) as csvFile:
            result_sheet = csv.DictReader(csvFile, delimiter=',')  # the sheet

            for row in result_sheet:
                row_dict = dict(row)
                spec_teams.append(row_dict['Number'])


    # collects the data
    events = data_col(refcsv1, cwda, csva, spec_csv)
    nyc = 'NYC FIRST Tech Challenge Qualifier 6'

    for ev in events:

        opr(events[ev], nth_digit=2)
        opr(events[ev], section='Auto', nth_digit=2)
        opr(events[ev], section='Teleop', nth_digit=2)
        opr(events[ev], section='Endgame', nth_digit=2)
        dpr(events[ev], nth_digit=2)
        ccwm(events[ev], nth_digit=2)

        median(events[ev], section='Auto')
        median(events[ev])
        stdev(events[ev], section='Auto', nth_digit=2)
        stdev(events[ev], nth_digit=2)
        medstd(events[ev], nth_digit=2)
        pics(events[ev], pic_cwd)
        misc_score(events[ev])
        for team in events[ev].teams:
            if team in all_teams:
                all_teams[team][ev] = events[ev].teams[team]
            else:
                all_teams[team] = dict()
                all_teams[team][ev] = events[ev].teams[team]
    for teamn in all_teams:
        instances = len(all_teams[teamn])
        if instances == 1:
            all_teams[teamn]['Final'] = dict()
            for ev in all_teams[teamn]:
                if ev != 'Final':
                    all_teams[teamn]['Final'] = all_teams[teamn][ev]
        else:
            temp_stats = dict()
            count = 0
            all_teams[teamn]['Final'] = dict()
            for ev in all_teams[teamn]:
                if count == 0:
                    all_teams[teamn]['Final'] = all_teams[teamn][ev]
                    for stat in all_teams[teamn][ev]:
                        print(stat)
                        if stat != 'Team #' and stat != 'Name' and stat != 'Picture':
                            temp_stats[stat] = []
                for stat in temp_stats:
                    temp_stats[stat].append(all_teams[teamn][ev][stat])
            for stat in temp_stats:
                if stat == 'Median':
                    all_teams[teamn]['Final'][stat] = np.median(temp_stats[stat])
                elif stat == 'Best Score' or stat == 'Worst Score':
                    temp_best = temp_stats[stat][0]
                    temp_worst = temp_stats[stat][0]
                    for score in temp_stats[stat]:
                            if temp_best < score:
                                temp_best = score
                            if temp_worst > score:
                                temp_worst = score
                            all_teams[teamn]['Final']['Best Score'] = temp_best
                            all_teams[teamn]['Final']['Worst Score'] = temp_worst
                elif stat == 'NumOfScores':
                    all_teams[teamn]['Final']['NumOfScores'] = sum(temp_stats['NumOfScores'])
                else:
                    all_teams[teamn]['Final'][stat] = np.around(temp_stats[stat])

    total_teams = dict()
    for teamn in all_teams:
        total_teams[teamn]=dict()
        total_teams[teamn] = all_teams[teamn]['Final']
    print(total_teams)
    chosen_teams = dict()

    for teamn in total_teams:
        if teamn in spec_teams:
            chosen_teams[teamn] = total_teams[teamn]
    with open(spec_csv) as csvFile:

        result_sheet = csv.DictReader(csvFile, delimiter=',')  # the sheet
        # The code will skip the first row with real data

        for row in result_sheet:
            # if row_count > 0:

            row_dict = dict(row)

            ref_teamn = row_dict['Number']
            ref_name = row_dict['Name']
            for teamn in chosen_teams:
                try:
                    r = chosen_teams[teamn]['Name']
                except KeyError:

                    if chosen_teams[teamn]['Team #'] == ref_teamn:
                        chosen_teams[teamn]['Name'] = ref_name
                        break
    create_file(chosen_teams, ranking_cwd, ranking_csv, default_d, metric)

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
