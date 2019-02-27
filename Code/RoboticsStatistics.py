import os
import csv
import statistics as st
import collections as cs
from CSVRankings import csv_sheet

import pandas


def data_col(refcsv, cwda, csva, allteam):

    csvr = list()
    csvr = csv_sheet(refcsv, cwda, csva, allteam)
    matches = csvr[0]
    teams = csvr[1]
    team_scores = csvr[2]
    auto_scores = csvr[3]
    teleop_scores = csvr[4]
    endgame_scores = csvr[5]

    print('collecting data')
    print(team_scores)
    print(teams)


'''

All functions with "full" in front add the auto, teleop, and endgame 
As headers in the csv to be produced
For example, if median would result in
    median
bill 120

full median would result in:
    median  auto median  teleop median  endgame median
bill 120     35            32              40 
'''


def full_median(teams, team_scores, auto_scores, teleop_scores, endgame_scores):
    for teamn in teams:
        teams[teamn]['Median'] = st.median(team_scores[teamn])
        teams[teamn]['Auto Median'] = st.median(auto_scores[teamn])
        teams[teamn]['Teleop Median'] = st.median(teleop_scores[teamn])
        teams[teamn]['Endgame Median'] = st.median(endgame_scores[teamn])
        if len(team_scores['Gl' + teamn]) > 0:
            teams[teamn]['GlMedian'] = st.median(team_scores['Gl' + teamn])
            teams[teamn]['GlAuto Median'] = st.median(auto_scores['Gl' + teamn])
            teams[teamn]['GlTeleop Median'] = st.median(teleop_scores['Gl' + teamn])
            teams[teamn]['GlEndgame Median'] = st.median(endgame_scores['Gl' + teamn])

        else:
            teams[teamn]['GlMedian'] = 'NA'
            teams[teamn]['GlAuto Median'] = 'NA'
            teams[teamn]['GlTeleop Median'] = 'NA'
            teams[teamn]['GlEndgame Median'] = 'NA'

        if len(team_scores['Sl' + teamn]) > 0:
            teams[teamn]['SlMedian'] = st.median(team_scores['Sl' + teamn])
            teams[teamn]['SlAuto Median'] = st.median(auto_scores['Sl' + teamn])
            teams[teamn]['SlTeleop Median'] = st.median(teleop_scores['Sl' + teamn])
            teams[teamn]['SlEndgame Median'] = st.median(endgame_scores['Sl' + teamn])

        else:
            teams[teamn]['SlMedian'] = 'NA'
            teams[teamn]['SlAuto Median'] = 'NA'
            teams[teamn]['SlTeleop Median'] = 'NA'
            teams[teamn]['SlEndgame Median'] = 'NA'


def full_standard_dev(teams, team_scores, auto_scores, teleop_scores, endgame_scores):
    for teamn in teams:
        if len(team_scores[teamn]) > 1:

            teams[teamn]['StdDev.'] = st.stdev(team_scores[teamn])
            teams[teamn]['Auto StdDev.'] = st.stdev(auto_scores[teamn])
            teams[teamn]['Teleop StdDev.'] = st.stdev(teleop_scores[teamn])
            teams[teamn]['Endgame StdDev.'] = st.stdev(endgame_scores[teamn])

            if len(team_scores['Gl' + teamn]) <= 1:
                teams[teamn]['GlStdDev.'] = 'NA'
                teams[teamn]['GlAuto StdDev.'] = 'NA'
                teams[teamn]['GlTeleop StdDev.'] = 'NA'
                teams[teamn]['GlEndgame StdDev.'] = 'NA'
            else:
                teams[teamn]['GlStdDev.'] = st.stdev(team_scores['Gl' + teamn])
                teams[teamn]['GlAuto StdDev.'] = st.stdev(auto_scores['Gl' + teamn])
                teams[teamn]['GlTeleop StdDev.'] = st.stdev(teleop_scores['Gl' + teamn])
                teams[teamn]['GlEndgame StdDev.'] = st.stdev(endgame_scores['Gl' + teamn])

            if len(team_scores['Sl' + teamn]) <= 1:
                teams[teamn]['SlStdDev.'] = 'NA'
                teams[teamn]['SlAuto StdDev.'] = 'NA'
                teams[teamn]['SlTeleop StdDev.'] = 'NA'
                teams[teamn]['SlEndgame StdDev.'] = 'NA'
            else:
                teams[teamn]['SlStdDev.'] = st.stdev(team_scores['Sl' + teamn])
                teams[teamn]['SlAuto StdDev.'] = st.stdev(auto_scores['Sl' + teamn])
                teams[teamn]['SlTeleop StdDev.'] = st.stdev(teleop_scores['Sl' + teamn])
                teams[teamn]['SlEndgame StdDev.'] = st.stdev(endgame_scores['Sl' + teamn])
        else:
            teams[teamn]['StdDev.'] = 'NA'
            teams[teamn]['Auto StdDev.'] = 'NA'
            teams[teamn]['Teleop StdDev.'] = 'NA'
            teams[teamn]['Endgame StdDev.'] = 'NA'


def full_average(teams, team_scores, auto_scores, teleop_scores, endgame_scores):
    for teamn in teams:
        teamn2 = str(teamn)
        print(teams[teamn]['Team #'])
        teams[teamn]['Avg.'] = st.mean(team_scores[teamn])
        teams[teamn]['Auto Avg.'] = st.mean(auto_scores[teamn])
        teams[teamn]['Teleop Avg.'] = st.mean(teleop_scores[teamn])
        teams[teamn]['Endgame Avg.'] = st.mean(endgame_scores[teamn])
        if len(team_scores['Gl' + teamn]) <= 0:
            teams[teamn]['GlAvg.'] = 'NA'
            teams[teamn]['GlAuto Avg.'] = 'NA'
            teams[teamn]['GlTeleop Avg.'] = 'NA'
            teams[teamn]['GlEndgame Avg.'] = 'NA'
        else:
            teams[teamn]['GlAvg.'] = st.mean(team_scores['Gl' + teamn])
            teams[teamn]['GlAuto Avg.'] = st.mean(auto_scores['Gl' + teamn])
            teams[teamn]['GlTeleop Avg.'] = st.mean(teleop_scores['Gl' + teamn])
            teams[teamn]['GlEndgame Avg.'] = st.mean(endgame_scores['Gl' + teamn])

        if len(team_scores['Sl' + teamn]) <= 0:
            teams[teamn]['SlAvg.'] = 'NA'
            teams[teamn]['SlAuto Avg.'] = 'NA'
            teams[teamn]['SlTeleop Avg.'] = 'NA'
            teams[teamn]['SlEndgame Avg.'] = 'NA'
        else:
            teams[teamn]['SlAvg.'] = st.mean(team_scores['Sl' + teamn])
            teams[teamn]['SlAuto Avg.'] = st.mean(auto_scores['Sl' + teamn])
            teams[teamn]['SlTeleop Avg.'] = st.mean(teleop_scores['Sl' + teamn])
            teams[teamn]['SlEndgame Avg.'] = st.mean(endgame_scores['Sl' + teamn])



def full_medstd(teams, team_scores, auto_scores, teleop_scores, endgame_scores):
    for teamn in teams:
        # median + and - standard deviation for team scores
        if teams[teamn]['StdDev.'] == 'NA':
            teams[teamn]['Med-Std.'] = 'NA'
            teams[teamn]['Med+Std.'] = 'NA'
            teams[teamn]['GlMed-Std.'] = 'NA'
            teams[teamn]['GlMed+Std.'] = 'NA'
            teams[teamn]['SlMed-Std.'] = 'NA'
            teams[teamn]['SlMed+Std.'] = 'NA'
            teams[teamn]['AutoMed-Std.'] = 'NA'
            teams[teamn]['AutoMed+Std.'] = 'NA'
            teams[teamn]['GlAutoMed+Std.'] = 'NA'
            teams[teamn]['GlAutoMed-Std.'] = 'NA'
            teams[teamn]['SlAutoMed-Std.'] = 'NA'
            teams[teamn]['SlAutoMed+Std.'] = 'NA'
            teams[teamn]['TeleopMed-Std.'] = 'NA'
            teams[teamn]['TeleopMed+Std.'] = 'NA'
            teams[teamn]['GlTeleopMed+Std.'] = 'NA'
            teams[teamn]['GlTeleopMed-Std.'] = 'NA'
            teams[teamn]['SlTeleopMed-Std.'] = 'NA'
            teams[teamn]['SlTeleopMed+Std.'] = 'NA'
            teams[teamn]['EndgameMed-Std.'] = 'NA'
            teams[teamn]['EndgameMed+Std.'] = 'NA'
            teams[teamn]['GlEndgameMed+Std.'] = 'NA'
            teams[teamn]['GlEndgameMed-Std.'] = 'NA'
            teams[teamn]['SlEndgameMed-Std.'] = 'NA'
            teams[teamn]['SlEndgameMed+Std.'] = 'NA'
        elif teams[teamn]['Median'] == 'NA':
            teams[teamn]['Med-Std.'] = 'NA'
            teams[teamn]['Med+Std.'] = 'NA'
            teams[teamn]['AutoMed-Std.'] = 'NA'
            teams[teamn]['AutoMed+Std.'] = 'NA'
            teams[teamn]['GlMed-Std.'] = 'NA'
            teams[teamn]['GlMed+Std.'] = 'NA'
            teams[teamn]['SlMed-Std.'] = 'NA'
            teams[teamn]['SlMed+Std.'] = 'NA'
            teams[teamn]['GlAutoMed+Std.'] = 'NA'
            teams[teamn]['GlAutoMed-Std.'] = 'NA'
            teams[teamn]['SlAutoMed-Std.'] = 'NA'
            teams[teamn]['SlAutoMed+Std.'] = 'NA'
            teams[teamn]['TeleopMed-Std.'] = 'NA'
            teams[teamn]['TeleopMed+Std.'] = 'NA'
            teams[teamn]['GlTeleopMed+Std.'] = 'NA'
            teams[teamn]['GlTeleopMed-Std.'] = 'NA'
            teams[teamn]['SlTeleopMed-Std.'] = 'NA'
            teams[teamn]['SlTeleopMed+Std.'] = 'NA'
            teams[teamn]['EndgameMed-Std.'] = 'NA'
            teams[teamn]['EndgameMed+Std.'] = 'NA'
            teams[teamn]['GlEndgameMed+Std.'] = 'NA'
            teams[teamn]['GlEndgameMed-Std.'] = 'NA'
            teams[teamn]['SlEndgameMed-Std.'] = 'NA'
            teams[teamn]['SlEndgameMed+Std.'] = 'NA'
        else:
            teams[teamn]['Med-Std.'] = teams[teamn]['Median'] - teams[teamn]['StdDev.']
            teams[teamn]['Med+Std.'] = teams[teamn]['Median'] + teams[teamn]['StdDev.']

            if teams[teamn]['GlStdDev.'] == 'NA':
                teams[teamn]['GlMed-Std.'] = 'NA'
                teams[teamn]['GlMed+Std.'] = 'NA'
            elif teams[teamn]['GlMedian'] == 'NA':
                teams[teamn]['GlMed-Std.'] = 'NA'
                teams[teamn]['GlMed+Std.'] = 'NA'
            else:
                teams[teamn]['GlMed-Std.'] = teams[teamn]['GlMedian'] - teams[teamn]['GlStdDev.']
                teams[teamn]['GlMed+Std.'] = teams[teamn]['GlMedian'] + teams[teamn]['GlStdDev.']

            if teams[teamn]['SlStdDev.'] == 'NA':
                teams[teamn]['SlMed-Std.'] = 'NA'
                teams[teamn]['SlMed+Std.'] = 'NA'
            elif teams[teamn]['SlMedian'] == 'NA':
                teams[teamn]['SlMed-Std.'] = 'NA'
                teams[teamn]['SlMed+Std.'] = 'NA'
            else:
                teams[teamn]['SlMed-Std.'] = teams[teamn]['SlMedian'] - teams[teamn]['SlStdDev.']
                teams[teamn]['SlMed+Std.'] = teams[teamn]['SlMedian'] + teams[teamn]['SlStdDev.']

            # median + and - standard deviation for auto

            if teams[teamn]['Auto StdDev.'] == 'NA':
                teams[teamn]['AutoMed-Std.'] = 'NA'
                teams[teamn]['AutoMed+Std.'] = 'NA'

            elif teams[teamn]['Auto Median'] == 'NA':
                teams[teamn]['AutoMed-Std.'] = 'NA'
                teams[teamn]['AutoMed+Std.'] = 'NA'
            else:
                teams[teamn]['AutoMed-Std.'] = teams[teamn]['Auto Median'] - teams[teamn]['Auto StdDev.']
                teams[teamn]['AutoMed+Std.'] = teams[teamn]['Auto Median'] - teams[teamn]['Auto StdDev.']
                # for gold
                if teams[teamn]['GlAuto StdDev.'] == 'NA':
                    teams[teamn]['GlAutoMed+Std.'] = 'NA'
                    teams[teamn]['GlAutoMed-Std.'] = 'NA'

                elif teams[teamn]['GlAuto Median'] == 'NA':
                    teams[teamn]['GlAutoMed+Std.'] = 'NA'
                    teams[teamn]['GlAutoMed-Std.'] = 'NA'
                else:
                    teams[teamn]['GlAutoMed+Std.'] = teams[teamn]['GlAuto Median'] + teams[teamn]['GlAuto StdDev.']
                    teams[teamn]['GlAutoMed-Std.'] = teams[teamn]['GlAuto Median'] - teams[teamn]['GlAuto StdDev.']
                # for silver
                if teams[teamn]['SlAuto StdDev.'] == 'NA':
                    teams[teamn]['SlAutoMed+Std.'] = 'NA'
                    teams[teamn]['SlAutoMed-Std.'] = 'NA'

                elif teams[teamn]['SlAuto Median'] == 'NA':
                    teams[teamn]['SlAutoMed+Std.'] = 'NA'
                    teams[teamn]['SlAutoMed-Std.'] = 'NA'
                else:
                    teams[teamn]['SlAutoMed+Std.'] = teams[teamn]['SlAuto Median'] + teams[teamn]['SlAuto StdDev.']
                    teams[teamn]['SlAutoMed-Std.'] = teams[teamn]['SlAuto Median'] - teams[teamn]['SlAuto StdDev.']

            # median + and - standard deviation for teleop

            if teams[teamn]['Teleop StdDev.'] == 'NA':
                teams[teamn]['TeleopMed-Std.'] = 'NA'
                teams[teamn]['TeleopMed+Std.'] = 'NA'

            elif teams[teamn]['Teleop Median'] == 'NA':
                teams[teamn]['TeleopMed-Std.'] = 'NA'
                teams[teamn]['TeleopMed+Std.'] = 'NA'
            else:
                teams[teamn]['TeleopMed-Std.'] = teams[teamn]['Teleop Median'] - teams[teamn]['Teleop StdDev.']
                teams[teamn]['TeleopMed+Std.'] = teams[teamn]['Teleop Median'] - teams[teamn]['Teleop StdDev.']
                # for gold
                if teams[teamn]['GlTeleop StdDev.'] == 'NA':
                    teams[teamn]['GlTeleopMed+Std.'] = 'NA'
                    teams[teamn]['GlTeleopMed-Std.'] = 'NA'

                elif teams[teamn]['GlTeleop Median'] == 'NA':
                    teams[teamn]['GlTeleopMed+Std.'] = 'NA'
                    teams[teamn]['GlTeleopMed-Std.'] = 'NA'
                else:
                    teams[teamn]['GlTeleopMed+Std.'] = teams[teamn]['GlTeleop Median'] + teams[teamn][
                        'GlTeleop StdDev.']
                    teams[teamn]['GlTeleopMed-Std.'] = teams[teamn]['GlTeleop Median'] - teams[teamn][
                        'GlTeleop StdDev.']
                # for silver
                if teams[teamn]['SlTeleop StdDev.'] == 'NA':
                    teams[teamn]['SlTeleopMed+Std.'] = 'NA'
                    teams[teamn]['SlTeleopMed-Std.'] = 'NA'

                elif teams[teamn]['SlTeleop Median'] == 'NA':
                    teams[teamn]['SlTeleopMed+Std.'] = 'NA'
                    teams[teamn]['SlTeleopMed-Std.'] = 'NA'
                else:
                    teams[teamn]['SlTeleopMed+Std.'] = teams[teamn]['SlTeleop Median'] + teams[teamn][
                        'SlTeleop StdDev.']
                    teams[teamn]['SlTeleopMed-Std.'] = teams[teamn]['SlTeleop Median'] - teams[teamn][
                        'SlTeleop StdDev.']

            # median + and - standard deviation for endgame

            if teams[teamn]['Endgame StdDev.'] == 'NA':
                teams[teamn]['EndgameMed-Std.'] = 'NA'
                teams[teamn]['EndgameMed+Std.'] = 'NA'

            elif teams[teamn]['Endgame Median'] == 'NA':
                teams[teamn]['EndgameMed-Std.'] = 'NA'
                teams[teamn]['EndgameMed+Std.'] = 'NA'
            else:
                teams[teamn]['EndgameMed-Std.'] = teams[teamn]['Endgame Median'] - teams[teamn]['Endgame StdDev.']
                teams[teamn]['EndgameMed+Std.'] = teams[teamn]['Endgame Median'] - teams[teamn]['Endgame StdDev.']
                # for gold
                if teams[teamn]['GlEndgame StdDev.'] == 'NA':
                    teams[teamn]['GlEndgameMed+Std.'] = 'NA'
                    teams[teamn]['GlEndgameMed-Std.'] = 'NA'

                elif teams[teamn]['GlEndgame Median'] == 'NA':
                    teams[teamn]['GlEndgameMed+Std.'] = 'NA'
                    teams[teamn]['GlEndgameMed-Std.'] = 'NA'
                else:
                    teams[teamn]['GlEndgameMed+Std.'] = teams[teamn]['GlEndgame Median'] + teams[teamn][
                        'GlEndgame StdDev.']
                    teams[teamn]['GlEndgameMed-Std.'] = teams[teamn]['GlEndgame Median'] - teams[teamn][
                        'GlEndgame StdDev.']
                # for silver
                if teams[teamn]['SlEndgame StdDev.'] == 'NA':
                    teams[teamn]['SlEndgameMed+Std.'] = 'NA'
                    teams[teamn]['SlEndgameMed-Std.'] = 'NA'

                elif teams[teamn]['SlEndgame Median'] == 'NA':
                    teams[teamn]['SlEndgameMed+Std.'] = 'NA'
                    teams[teamn]['SlEndgameMed-Std.'] = 'NA'
                else:
                    teams[teamn]['SlEndgameMed+Std.'] = teams[teamn]['SlEndgame Median'] + teams[teamn][
                        'SlEndgame StdDev.']
                    teams[teamn]['SlEndgameMed-Std.'] = teams[teamn]['SlEndgame Median'] - teams[teamn][
                        'SlEndgame StdDev.']



def average(teams, team_scores, auto_scores):
    for teamn in teams:
        teamn2 = str(teamn)
        print(teams[teamn]['Team #'])
        teams[teamn]['Avg.'] = st.mean(team_scores[teamn])
        teams[teamn]['Auto Avg.'] = st.mean(auto_scores[teamn])

        if len(team_scores['Gl' + teamn]) <= 0:
            teams[teamn]['GlAvg.'] = 'NA'
            teams[teamn]['GlAuto Avg.'] = 'NA'

        else:
            teams[teamn]['GlAvg.'] = st.mean(team_scores['Gl' + teamn])
            teams[teamn]['GlAuto Avg.'] = st.mean(auto_scores['Gl' + teamn])

        if len(team_scores['Sl' + teamn]) <= 0:
            teams[teamn]['SlAvg.'] = 'NA'
            teams[teamn]['SlAuto Avg.'] = 'NA'

        else:
            teams[teamn]['SlAvg.'] = st.mean(team_scores['Sl' + teamn])
            teams[teamn]['SlAuto Avg.'] = st.mean(auto_scores['Sl' + teamn])


def median(teams, team_scores):
    for teamn in teams:
        teams[teamn]['Median'] = st.median(team_scores[teamn])
        if len(team_scores['Gl' + teamn]) > 0:
            teams[teamn]['GlMedian'] = st.median(team_scores['Gl' + teamn])
        else:
            teams[teamn]['GlMedian'] = 'NA'
        if len(team_scores['Sl' + teamn]) > 0:
            teams[teamn]['SlMedian'] = st.median(team_scores['Sl' + teamn])
        else:
            teams[teamn]['SlMedian'] = 'NA'


def standard_dev(teams, team_scores):
    for teamn in teams:
        if len(team_scores[teamn]) > 1:
            teams[teamn]['StdDev.'] = st.stdev(team_scores[teamn])
            if len(team_scores['Gl' + teamn]) > 1:
                teams[teamn]['GlStdDev.'] = st.stdev(team_scores['Gl' + teamn])
            else:
                teams[teamn]['GlStdDev.'] = 'NA'
            if len(team_scores['Sl' + teamn]) > 1:
                teams[teamn]['SlStdDev.'] = st.stdev(team_scores['Sl' + teamn])
            else:
                teams[teamn]['SlStdDev.'] = 'NA'
        else:
            teams[teamn]['StdDev.'] = 'NA'
            teams[teamn]['Gl' + teamn] = 'NA'
            teams[teamn]['Sl' + teamn] = 'NA'


def medstd(teams, team_scores):
    for teamn in teams:
        if teams[teamn]['StdDev.'] == 'NA':
            teams[teamn]['Med-Std.'] = 'NA'
            teams[teamn]['Med+Std.'] = 'NA'
        elif teams[teamn]['Median'] == 'NA':
            teams[teamn]['Med-Std.'] = 'NA'
            teams[teamn]['Med+Std'] = 'NA'
        else:
            teams[teamn]['Med-Std.'] = teams[teamn]['Median'] - teams[teamn]['StdDev.']
            teams[teamn]['Med-Std.'] = teams[teamn]['Median'] + teams[teamn]['StdDev.']
# Second-worst


'''
CCWM is how much a team contributed to the winning margin of the match
CCWM = (OPR-DPR)
DPR is how much, on average, a team will score against your alliance
'''


def dpr(matches, teams):
    nonmatch = 0
    for teamn in teams:

        ag_scores = list()  # list of scores against
        print("New Team Here")
        print(teams[teamn])
        for match in matches:
            r = int()
            try:
                if matches[match]['Blue'][teamn+'1']:
                    for score in matches[match]['Red']['Scores']:

                        ag_scores.append(int(score))

                    r = teamn
            except KeyError:
                try:
                    if matches[match]['Red'][teamn+'1']:

                        for score in matches[match]['Blue']['Scores']:

                            ag_scores.append(int(score))
                except KeyError:
                    nonmatch += 1

        teams[teamn]['DPR'] = st.mean(ag_scores)


'''
IMPORTANT: when this code was written, it was assumed you had individual scores.
This may change. when it does, name the Average to OPR
'''


def ccwm(teams):
    for teamn in teams:
        print(teams[teamn])
        teams[teamn]['CCWM'] = teams[teamn]['Avg.'] - teams[teamn]['DPR']


def apply_func(avg_full, median_full, std_full, medstd_full, teams, team_scores, auto_scores, teleop_scores, endgame_scores, default_d):
    print('Applying Function')
    if avg_full:
        default_d['GlAuto Avg.'] = 0
        default_d['GlTeleop Avg.'] = 0
        default_d['GlEndgame Avg.'] = 0
        default_d['SlAuto Avg.'] = 0
        default_d['SlTeleop Avg.'] = 0
        default_d['SlEndgame Avg.'] = 0
        full_average(teams, team_scores, auto_scores, teleop_scores, endgame_scores)
    else:
        average(teams, team_scores, auto_scores)

    if median_full or medstd_full:
        default_d['GlAuto Median'] = 0
        default_d['GlTeleop Median'] = 0
        default_d['GlEndgame Median'] = 0
        default_d['SlAuto Median'] = 0
        default_d['SlTeleop Median'] = 0
        default_d['SlEndgame Median'] = 0
        full_median(teams, team_scores, auto_scores, teleop_scores, endgame_scores)
    else:
        median(teams, team_scores)

    if std_full or medstd_full:
        default_d['GlAuto StdDev.'] = 0
        default_d['GlTeleop StdDev.'] = 0
        default_d['GlEndgame StdDev.'] = 0
        default_d['SlAuto StdDev.'] = 0
        default_d['SlTeleop StdDev.'] = 0
        default_d['SlEndgame StdDev.'] = 0
        full_standard_dev(teams, team_scores, auto_scores, teleop_scores, endgame_scores)
    else:
        standard_dev(teams, team_scores)

    if medstd_full:
        default_d['GlAutoM-Std.'] = 0
        default_d['GlTeleopM-Std.'] = 0
        default_d['GlEndgameM-Std.'] = 0
        default_d['GlAutoM+Std.'] = 0
        default_d['GlTeleopM+Std.'] = 0
        default_d['GlEndgameM+Std.'] = 0
        default_d['SlAutoM-Std.'] = 0
        default_d['SlTeleopM-Std.'] = 0
        default_d['SlEndgameM-Std.'] = 0
        default_d['SlAutoM+Std.'] = 0
        default_d['SlTeleopM+Std.'] = 0
        default_d['SlEndgameM+Std.'] = 0
        full_medstd(teams, team_scores, auto_scores, teleop_scores, endgame_scores)
    else:
        medstd(teams, team_scores)


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


def create_file(teams, cwd, csv2, default_d, default_gl, default_sl, metric, colormetric):
    if colormetric:
        gl = sorted(teams, key=lambda x: (teams[x]['Gl'+metric]), reverse=True)
        sl = sorted(teams, key=lambda x: (teams[x]['Sl'+metric]), reverse=True)
    else:
        y = sorted(teams, key=lambda x: (teams[x][metric]), reverse=True)
    print('ordering below')
    os.chdir(cwd)
    c = 1
    del default_gl['Picture']
    del default_sl['Picture']
    del default_d['Picture']
    if os.path.exists(csv2):  # deletes the rankings file if it exists
        os.remove(csv2)
    with open(csv2, 'w+', newline='') as f:  # creates a new file
        # checks to see if a metric can be sorted by side color
        if colormetric:
            # Gold Side
            w = csv.DictWriter(f, default_gl.keys(), extrasaction='ignore')  # i

            w.writeheader()
            while (c < len(gl)) and (c < 17):
                if teams[gl[c - 1]]['Picture'] == 'NA':
                    non = 'done'
                else:
                    teams[gl[c - 1]]['Team #'] = teams[gl[c - 1]]['Picture']

                print(teams[gl[c - 1]])
                w.writerow(teams[gl[c - 1]])
                c += 1
            c = 1
            # Silver Side

            w = csv.DictWriter(f, default_sl.keys(), extrasaction='ignore')  # i
            w.writeheader()
            while (c < len(sl)) and (c < 17):
                if teams[sl[c - 1]]['Picture'] == 'NA':
                    non = 'done'
                else:
                    teams[sl[c - 1]]['Team #'] = teams[sl[c - 1]]['Picture']
                print(teams[sl[c - 1]])
                w.writerow(teams[sl[c - 1]])
                c += 1
        else:
            w = csv.DictWriter(f, default_d.keys())  # i

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
    csva = "/CSV/SampleDatav2.csv"  # the csv's in question
    refcsv1 = "/CSV/ReferenceList1.csv"  # csv with some team names
    cwd2 = "CSV"  # the folder of the rankings csv
    csv2 = "CSV/Rankings.csv"  # The file that you want to place the rankings in.
    cwdpit = 'CSV'  # the pit scout location
    pit = 'CSV/Pit_Scouting.csv'  # pit scout csv
    pics1 = '/TeamPics/'  # the location of the teams pictures
    avg_full = False  # determines if the "full" function is called or not
    std_full = False
    median_full = False
    medstd_full = True
    teams = dict()  # The rows of the output csv
    team_scores = dict()  # the scores of each team
    auto_scores = dict()
    teleop_scores = dict()
    endgame_scores = dict()
    matches = dict()  # each match
    years = list()  # list of years to check
    teams_ord = cs.OrderedDict()

    metric = 'Median'
    '''
    the information in matches:
    
    brattain1+1 
    Blue
    blue margin
    blue total
    Blue teamn
    blue teamn
    win color
    Red
    '''

    years = ['2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009']
    default_d = {'Team #': 0,   # A Default team, updated with keys, used as the
                 'Name': 'NA',  # index for all of the keys a team would have
                 'DQ': 0,
                 'Best Score': 0,
                 'Worst Score': 0,
                 'Breakable': 'no',
                 'NumOfScores': 0,
                 'FullCrater': 'no',
                 'FullDepot': 'no',
                 'Avg.': 0,
                 'Auto Avg.': 0,
                 'GlAvg.': 0,
                 'GlAuto Avg.': 0,
                 'SlAvg.': 0,
                 'SlAuto Avg.': 0,
                 'CCWM': 0,
                 'DPR': 0,
                 'Median': 0,
                 'StdDev.': 0,
                 'Med-Std.': 0,
                 'Med+Std.': 0,
                 'GlMedian': 0,
                 'GlMed-Std.': 0,
                 'GlMed+Std.': 0,
                 'GlStdDev.': 0,
                 'SlMedian': 0,
                 'SlMed-Std.': 0,
                 'SlMed+Std.': 0,
                 'SlStdDev.': 0,
                 'Disconnects': 0,
                 'Preferred Side': 'None',
                 'Picture': ''
                 }
    default_gl = {'Team #': 0,   # A Default team, updated with keys, used as the
                  'Name': 'NA',  # index for all of the keys a team would have
                  'DQ': 0,
                  # 'Best Score': 0,
                  # 'Worst Score': 0,
                  # 'NumOfScores': 0,
                  # 'Avg.': 0,
                  # 'Auto Avg.': 0,
                  'Breakable': 'No',
                  'FullCrater': 'no',
                  'FullDepot': 'no',
                  'GlMedian': 0,
                  'GlMed-Std.': 0,
                  'GlMed+Std.': 0,
                  'GlStdDev.': 0,
                  'GlAvg.': 0,
                  'GlAuto Avg.': 0,
                  # 'CCWM': 0,
                  # 'DPR': 0,
                  'Median': 0,
                  'StdDev.': 0,
                  'Med-Std.': 0,
                  'Med+Std.': 0,
                  'Disconnects': 0,
                  'Preferred Side': 'None',
                  'Picture': ''
                  }
    default_sl = {'Team #': 0,   # A Default team, updated with keys, used as the
                  'Name': 'NA',  # index for all of the keys a team would have
                  'DQ': 0,
                  # 'Best Score': 0,
                  # 'Worst Score': 0,
                  # 'NumOfScores': 0,
                  # 'Avg.': 0,
                  # 'Auto Avg.': 0,
                  'Breakable': 'no',
                  'FullCrater': 'no',
                  'FullDepot': 'no',
                  'SlMedian': 0,
                  'SlMed-Std.': 0,
                  'SlMed+Std.': 0,
                  'SlStdDev.': 0,
                  'SlAvg.': 0,
                  'SlAuto Avg.': 0,
                  # 'CCWM': 0,
                  # 'DPR': 0,
                  'Median': 0,
                  'StdDev.': 0,
                  'Med-Std.': 0,
                  'Med+Std.': 0,
                  'Disconnects': 0,
                  'Preferred Side': 'None',
                  'Picture': ''
                  }

    # collects the data
    allteam = [matches, teams, team_scores, auto_scores, teleop_scores, endgame_scores]
    data_col(refcsv1, cwda, csva, allteam)

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
    if (metric == 'Median') or (metric == 'StdDev.'):
        colormetric = True
    else:
        colormetric = False
    create_file(teams, cwd, csv2, default_d, default_gl, default_sl, metric, colormetric)


if __name__ == '__main__':
    main()
