import os
import csv
import collections as cl
import pandas
import bs4

# Autonomous Period

landedv = 30
sampledv = 25
claimedv = 15
parkedv = 10
max_auto = 80
max_auto2 = 105  # with double sample

# Driver Control

depotv = 2
landerv = 5

# End Game

hangingv = 50
part_in_craterv = 15
fully_in_craterv = 25


def csv_sheet(refcsv, cwd, csv_location, allteam):

    matches = allteam[0]
    teams = allteam[1]
    team_scores = allteam[2]
    auto_scores = allteam[3]
    teleop_scores = allteam[4]
    endgame_scores = allteam[5]
    # Changes the directory to The Excel Folder
    os.chdir(cwd)
    os.chdir('..')
    cwd = os.getcwd()

    print(cwd)
    print(csv_location)
    csv_location = cwd + csv_location
    with open(csv_location) as csvFile:

        result_sheet = csv.DictReader(csvFile, delimiter=',')  # the sheet

        row_count = 0  # the row being iterated

        # The code will skip the first row with real data
        count=0
        for row in result_sheet:
            # if row_count > 0:
            count+=1
            print(count)
            row_dict = dict(row)
            temp_scores1 = [int(row_dict['Total1']), int(row_dict['Auto1']),
                            int(row_dict['Teleop1']), int(row_dict['Endgame1'])]
            temp_scores2 = [int(row_dict['Total2']), int(row_dict['Auto2']),
                            int(row_dict['Teleop2']), int(row_dict['Endgame2'])]
            temp_score1 = int(row_dict['Total1'])
            temp_score2 = int(row_dict['Total2'])
            temp_teamn1 = row_dict['Team1']  # holds the number of the first team of an alliance being iterated
            temp_teamn2 = row_dict['Team2']  # holds the team # of team 2 in an alliance
            if 'ï»¿competition' in row_dict:
                temp_comp = 'ï»¿competition'
            else:
                temp_comp = 'Competition'
            temp_match = str(row_dict[temp_comp]) + str(row_dict['Match'])  # the competition plus the match number
            print(temp_match)
            print("printed once")
            temp_color = row_dict['Color']
            if temp_match in matches: # Checks to see if a match exists
                # updates the matches
                if temp_color == 'Blue':
                    matches[temp_match]['Blue'][temp_teamn1 + '1'] = True
                    matches[temp_match]['Blue'][temp_teamn2 + '1'] = True
                    if matches[temp_match]['Stats']['Filed'] == 2:
                        # checks if this is the last of a match
                        matches[temp_match]['Blue'][temp_teamn1] = int(row_dict['Total1'])
                        matches[temp_match]['Blue'][temp_teamn2] = int(row_dict['Total2'])
                        matches[temp_match]['Blue']['Total'] = int(row_dict['Total1']) + int(row_dict['Total2'])
                        matches[temp_match]['Stats']['Filed'] += 2
                        if matches[temp_match]['Blue']['Total'] > matches[temp_match]['Red']['Total']:
                            matches[temp_match]['Stats']['Win'] = 'Blue'
                            matches[temp_match]['Stats']['Margin'] = matches[temp_match]['Blue']['Total'] - \
                                matches[temp_match]['Red']['Total']

                        elif matches[temp_match]['Blue']['Total'] == matches[temp_match]['Red']['Total']:
                            matches[temp_match]['Stats']['Win'] = 'Tie'
                            matches[temp_match]['Stats']['Margin'] = 0
                        else:
                            matches[temp_match]['Stats']['Win'] = 'Red'
                            print(matches[temp_match]['Red']['Total'])
                            matches[temp_match]['Stats']['Margin'] = matches[temp_match]['Red']['Total'] -\
                                matches[temp_match]['Blue']['Total']

                    else:
                        matches[temp_match]['Blue'][temp_teamn1] = int(row_dict['Total1'])
                        matches[temp_match]['Blue'][temp_teamn2] = int(row_dict['Total2'])
                        matches[temp_match]['Blue']['Total'] = int(row_dict['Total1']) + int(row_dict['Total2'])
                        matches[temp_match]['Stats']['Filed'] += 1
                    matches[temp_match]['Blue']['Scores'].append(temp_score1)
                    matches[temp_match]['Blue']['Scores'].append(temp_score2)

                else:
                    matches[temp_match]['Red'][temp_teamn1 + '1'] = True
                    matches[temmp_match]['Red'][temp_teamn2 + '1'] = True
                    if matches[temp_match]['Stats']['Filed'] == 2:
                        # checks if this is the last of a match
                        matches[temp_match]['Red'][temp_teamn1] = int(row_dict['Total1'])
                        matches[temp_match]['Red'][temp_teamn2] = int(row_dict['Total2'])
                        matches[temp_match]['Red']['Total'] = int(row_dict['Total1']) + int(row_dict['Total2'])
                        matches[temp_match]['Stats']['Filed'] += 2
                        if matches[temp_match]['Blue']['Total'] > matches[temp_match]['Red']['Total']:
                            matches[temp_match]['Stats']['Win'] = 'Blue'
                            matches[temp_match]['Stats']['Margin'] = matches[temp_match]['Blue']['Total'] - \
                                                                     matches[temp_match]['Red']['Total']

                        elif matches[temp_match]['Blue']['Total'] == matches[temp_match]['Red']['Total']:
                            matches[temp_match]['Stats']['Win'] = 'Tie'
                            matches[temp_match]['Stats']['Margin'] = 0
                        else:
                            matches[temp_match]['Stats']['Win'] = 'Red'
                            matches[temp_match]['Stats']['Margin'] = matches[temp_match]['Red']['Total'] - \
                                                                     matches[temp_match]['Blue']['Total']
                    else:
                        matches[temp_match]['Red'][temp_teamn1] = int(row_dict['Total1'])
                        matches[temp_match]['Red'][temp_teamn2] = int(row_dict['Total2'])
                        matches[temp_match]['Red']['Total'] = int(row_dict['Total1']) + int(row_dict['Total2'])
                        matches[temp_match]['Stats']['Filed'] += 1
                    matches[temp_match]['Red']['Scores'].append(temp_score1)
                    matches[temp_match]['Red']['Scores'].append(temp_score2)

            else:
                if temp_color == 'Blue':
                    matches[temp_match] = {
                        'Blue': {temp_teamn1: int(row_dict['Total1']), temp_teamn2: int(row_dict['Total2']),
                                 'Total': int(row_dict['Total1']) + int(row_dict['Total2']), 'Scores': [temp_score1, temp_score2], temp_teamn1 +'1': True,
                                 temp_teamn2+'1': True},
                        'Stats': {'Filed': 2},
                        'Red': {'Total': 0, 'Scores': []}
                    }
                else:
                    matches[temp_match] = {
                        'Red': {temp_teamn1: int(row_dict['Total1']), temp_teamn2: int(row_dict['Total2']),
                                'Total': int(row_dict['Total1']) + int(row_dict['Total2']), 'Scores': [temp_score1, temp_score2],
                                temp_teamn1 + '1': True,
                                temp_teamn2 + '1': True},
                        'Stats': {'Filed': 2},
                        'Blue': {'Total': 0, 'Scores': []}
                    }

            if temp_teamn1 in teams:  # Checks to see if a team exists
                # edits a current team
                # updates scores and best/worst

                x= list()
                # CHANGE GOLD AND SIDE AS NEEDED
                # THIS IS THE FIRST PLACE WHERE PLACEHOLDERS HAVE BEEN PLACED
                # ASSUMES SILVER IF SIDE ISN'T 'gold'
                '''
                if row_dict['side'] == 'gold':
                    team_scores['Gl' + temp_teamn].append(temp_scores[0])
                    auto_scores['Gl' + temp_teamn].append(temp_scores[1])
                    teleop_scores['Gl' + temp_teamn].append(temp_scores[2])
                    endgame_scores['Gl' + temp_teamn].append(temp_scores[3])
                else:
                    team_scores['Sl' + temp_teamn].append(temp_scores[0])
                    auto_scores['Sl' + temp_teamn].append(temp_scores[1])
                    teleop_scores['Sl' + temp_teamn].append(temp_scores[2])
                    endgame_scores['Sl' + temp_teamn].append(temp_scores[3])
                '''
                team_scores[temp_teamn1].append(temp_scores1[0])
                auto_scores[temp_teamn1].append(temp_scores1[1])
                teleop_scores[temp_teamn1].append(temp_scores1[2])
                endgame_scores[temp_teamn1].append(temp_scores1[3])
                x = team_scores[temp_teamn1]

                teams[temp_teamn1]['Best Score'] = max(x)
                teams[temp_teamn1]['Worst Score'] = min(x)
                teams[temp_teamn1]['NumOfScores'] += 1
                if 'Name' not in teams[temp_teamn1] and 'name' in row_dict:
                    teams[temp_teamn1]['Name'] = row['name']
                if row_dict['Disconnects1?'] == '1':
                    teams[temp_teamn1]['Disconnects'] += 1

                # repeats for team 2

                team_scores[temp_teamn2].append(temp_scores2[0])
                auto_scores[temp_teamn2].append(temp_scores2[1])
                teleop_scores[temp_teamn2].append(temp_scores2[2])
                endgame_scores[temp_teamn2].append(temp_scores2[3])
                x = team_scores[temp_teamn2]

                teams[temp_teamn2]['Best Score'] = max(x)
                teams[temp_teamn2]['Worst Score'] = min(x)
                teams[temp_teamn2]['NumOfScores'] += 1

                if row_dict['Disconnects2?'] == '1':
                    teams[temp_teamn2]['Disconnects'] += 1

            # makes a new team
            else:
                # THIS IS THE SECOND POINT WHERE GOLD AND SIDE MAY VARY!!
                '''
                team_scores['Gl' + temp_teamn] = []
                auto_scores['Gl' + temp_teamn] = []
                teleop_scores['Gl' + temp_teamn] = []
                endgame_scores['Gl' + temp_teamn] = []
                team_scores['Sl' + temp_teamn] = []
                auto_scores['Sl' + temp_teamn] = []
                teleop_scores['Sl' + temp_teamn] = []
                endgame_scores['Sl' + temp_teamn] = []

                if row_dict['side'] == 'gold':
                    team_scores['Gl' + temp_teamn].append(temp_scores[0])
                    auto_scores['Gl' + temp_teamn].append(temp_scores[1])
                    teleop_scores['Gl' + temp_teamn].append(temp_scores[2])
                    endgame_scores['Gl' + temp_teamn].append(temp_scores[3])
                else:
                    team_scores['Sl' + temp_teamn].append(temp_scores[0])
                    auto_scores['Sl' + temp_teamn].append(temp_scores[1])
                    teleop_scores['Sl' + temp_teamn].append(temp_scores[2])
                    endgame_scores['Sl' + temp_teamn].append(temp_scores[3])
                '''
                team_scores[temp_teamn1] = [temp_scores1[0]]
                auto_scores[temp_teamn1] = [temp_scores1[1]]
                teleop_scores[temp_teamn1] = [temp_scores1[2]]
                endgame_scores[temp_teamn1] = [temp_scores1[3]]

                teams[temp_teamn1] = {'Team #': temp_teamn1,
                                      'Best Score': temp_scores1[0],
                                      'Worst Score': temp_scores1[0],
                                      'Disconnects': 0,
                                      'NumOfScores': 1,
                                      'Missed Hangs': 0
                                      }
                if row_dict['Disconnects1?'] == '1':
                    teams[temp_teamn1]['Disconnects'] += 1

                # Now with the second team

                team_scores[temp_teamn2] = [temp_scores2[0]]
                auto_scores[temp_teamn2] = [temp_scores2[1]]
                teleop_scores[temp_teamn2] = [temp_scores2[2]]
                endgame_scores[temp_teamn2] = [temp_scores2[3]]

                teams[temp_teamn2] = {'Team #': temp_teamn2,
                                      'Best Score': temp_scores2[0],
                                      'Worst Score': temp_scores2[0],
                                      'Disconnects': 0,
                                      'NumOfScores': 1,
                                      'Missed Hangs': 0
                                      }
                if row_dict['Disconnects2?'] == '1':
                    teams[temp_teamn2]['Disconnects'] += 1

            if row_dict['Parking1'] != 'H':
                teams[temp_teamn1]['Missed Hangs'] += 1
            if row_dict['Parking2'] != 'H':
                teams[temp_teamn2]['Missed Hangs'] += 1

            row_count += 1
    # Then it will
    # And saving specific scores and names together for processing

    # assigns team names to numbers

    cwd = os.getcwd()
    print('here')
    print(cwd)
    refcsv = cwd + refcsv
    with open(refcsv) as csvFile:

        result_sheet = csv.DictReader(csvFile, delimiter=',')  # the sheet

        # The code will skip the first row with real data
        print(teams)
        for row in result_sheet:
            # if row_count > 0:

            row_dict = dict(row)

            ref_teamn = row_dict['Team #']
            ref_name = row_dict['Name']
            for teamn in teams:
                try:
                    r = teams[teamn]['Name']
                except KeyError:

                    if teams[teamn]['Team #'] == ref_teamn:
                        teams[teamn]['Name'] = ref_name
                        print('successful')
                        break

    allteam = [matches, teams, team_scores, auto_scores, teleop_scores, endgame_scores]

    return allteam


