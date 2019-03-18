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

        for row in result_sheet:
            # if row_count > 0:

            row_dict = dict(row)

            temp_scores = score_up(row_dict)  # a list of the scores from sections of match.
            temp_score = temp_scores[0]  # holds the score of a team from a match
            temp_teamn = row_dict['team']  # holds the number of the team being iterated
            if 'ï»¿competition' in row_dict:
                temp_comp = 'ï»¿competition'
            else:
                temp_comp = 'competition'
            temp_match = row_dict[temp_comp] + row_dict['match']  # the competition plus the match number

            temp_color = row_dict['color']
            if temp_match in matches: # Checks to see if a match exists
                # updates the matches
                if temp_color == 'Blue':
                    matches[temp_match]['Blue'][temp_teamn + '1'] = True
                    if matches[temp_match]['Stats']['Filed'] == 3:  # checks if this is the last of a match
                        matches[temp_match]['Blue'][temp_teamn] = temp_score
                        matches[temp_match]['Blue']['Total'] += temp_score
                        matches[temp_match]['Stats']['Filed'] += 1
                        if matches[temp_match]['Blue']['Total'] > matches[temp_match]['Red']['Total']:
                            matches[temp_match]['Stats']['Win'] = 'Blue'
                            matches[temp_match]['Stats']['Margin'] = matches[temp_match]['Blue']['Total'] - \
                                matches[temp_match]['Red']['Total']

                        elif matches[temp_match]['Blue']['Total'] == matches[temp_match]['Red']['Total']:
                            matches[temp_match]['Stats']['Win'] = 'Tie'
                            matches[temp_match]['Stats']['Margin'] = 0
                        else:
                            matches[temp_match]['Stats']['Win'] = 'Red'
                            matches[temp_match]['Stats']['Margin'] = matches[temp_match]['Red']['Total'] -\
                                matches[temp_match]['Blue']['Total']
                    else:
                        matches[temp_match]['Blue'][temp_teamn] = temp_score
                        matches[temp_match]['Blue']['Total'] += temp_score
                        matches[temp_match]['Stats']['Filed'] += 1
                    matches[temp_match]['Blue']['Scores'].append(temp_score)

                else:
                    matches[temp_match]['Red'][temp_teamn + '1'] = True

                    if matches[temp_match]['Stats']['Filed'] == 3:  # checks if this is the last of a match
                        matches[temp_match]['Red'][temp_teamn] = temp_score
                        matches[temp_match]['Red']['Total'] += temp_score
                        matches[temp_match]['Stats']['Filed'] += 1
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

                        matches[temp_match]['Red'][temp_teamn] = temp_score
                        matches[temp_match]['Red']['Total'] += temp_score
                        matches[temp_match]['Stats']['Filed'] += 1
                    matches[temp_match]['Red']['Scores'].append(temp_score)

            else:
                if temp_color == 'Blue':
                    matches[temp_match] = {
                        'Blue': {temp_teamn: temp_score, 'Total': temp_score, 'Scores': [temp_score],
                                 temp_teamn+'1': True},
                        'Stats': {'Filed': 1},
                        'Red': {'Total': 0, 'Scores': []}
                    }
                else:
                    matches[temp_match] = {
                        'Red': {temp_teamn: temp_score, 'Total': temp_score, 'Scores': [temp_score],
                                temp_teamn+'1': True},
                        'Stats': {'Filed': 1},
                        temp_teamn: True,
                        'Blue': {'Total': 0, 'Scores': []}
                    }

            if temp_teamn in teams:  # Checks to see if a team exists
                # edits a current team
                # updates scores and best/worst

                x= list()
                # CHANGE GOLD AND SIDE AS NEEDED
                # THIS IS THE FIRST PLACE WHERE PLACEHOLDERS HAVE BEEN PLACED
                # ASSUMES SILVER IF SIDE ISN'T 'gold'


                team_scores[temp_teamn].append(temp_scores[0])
                auto_scores[temp_teamn].append(temp_scores[1])
                teleop_scores[temp_teamn].append(temp_scores[2])
                endgame_scores[temp_teamn].append(temp_scores[3])
                x = team_scores[temp_teamn]

                teams[temp_teamn]['Best Score'] = max(x)
                teams[temp_teamn]['Worst Score'] = min(x)
                teams[temp_teamn]['NumOfScores'] += 1
                if 'Name' not in teams[temp_teamn] and 'name' in row_dict:
                    teams[temp_teamn]['Name'] = row['name']


            # makes a new team
            else:
                # THIS IS THE SECOND POINT WHERE GOLD AND SIDE MAY VARY!!



                team_scores[temp_teamn] = [temp_scores[0]]
                auto_scores[temp_teamn] = [temp_scores[1]]
                teleop_scores[temp_teamn] = [temp_scores[2]]
                endgame_scores[temp_teamn] = [temp_scores[3]]

                teams[temp_teamn] = {'Team #': temp_teamn,
                                     'Best Score': temp_scores[0],
                                     'Worst Score': temp_scores[0],
                                     'Disconnects': 0,
                                     'NumOfScores': 1,
                                     'Missed Hangs': 0
                                     }


                if 'name' in row_dict:
                    teams[temp_teamn]['Name'] = row['name']
            if row_dict['hanging'] == 0:
                teams[temp_teamn]['Missed Hangs'] += 1

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


def score_up(row_dict):
    # adds up the scores for all three sections of the game, then returns a list
    tempin_score = 0  # total score
    auto_score = 0  # auto score
    teleop_score = 0  # teleop score
    endgame_score = 0  # endgame score
    score_list = list()  # list of the above scores in that order

    auto_score += landedv*int(row_dict['landed'])
    auto_score += sampledv*int(row_dict['sampled'])
    auto_score += claimedv*int(row_dict['claimed'])
    auto_score += parkedv*int(row_dict['parked'])

    tempin_score += auto_score

    teleop_score += landerv*int(row_dict['lander'])
    teleop_score += depotv*int(row_dict['depot'])

    tempin_score += teleop_score

    endgame_score += hangingv*int(row_dict['hanging'])
    endgame_score += part_in_craterv*int(row_dict['partincrater'])
    endgame_score += fully_in_craterv*int(row_dict['fullyincrater'])

    tempin_score += endgame_score

    score_list.append(tempin_score)
    score_list.append(auto_score)
    score_list.append(teleop_score)
    score_list.append(endgame_score)
    print(score_list)
    return score_list
