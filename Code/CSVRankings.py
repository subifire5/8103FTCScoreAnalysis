import os
import csv
import collections as cl
import pandas
import bs4
import numpy as np

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


def csv_sheet(refcsv, cwd, csv_location):

    total_scores = []  # the scores for each match
    auto_scores = []  # auto scores for each match
    teleop_scores = []  # teleop scores for each match
    endgame_scores = []  # endgame scores for each match
    raw_matches = dict()  # A dictionary of lists representing teams in a match
    matches = []  # a lists of lists, each representing a color in a match
    teams = dict()  # A dict of dicts that will hold the processed data of all teams
    opponent_score = []  # a list of lists, each representing the scores against a team in a match
    team_scores = dict()  # a dict of lists of lists team scores
    full_csv = []
    # Changes the directory to The Excel Folder
    os.chdir(cwd)
    os.chdir('..')
    cwd = os.getcwd()
    match_num = 0
    print(cwd)
    print(csv_location)
    csv_location = cwd + csv_location
    with open(csv_location) as csvFile:

        result_sheet = csv.DictReader(csvFile, delimiter=',')  # the sheet

        row_count = 0  # the row being iterated

        # The code will skip the first row with real data
        count=0
        team_nums = []
        for row in result_sheet:
            # if row_count > 0:
            count+=1
            print(count)

            '''
            A brief explanation
            
            each of the score lists is a list that has the scores of an alliance
            it is updated for each side of a match
            the red team's score is put in first, then the blue teams
            this is important for later
            
            the total_scores is the total score for an alliance
            that includes penalties
            
            The next part of the code accesses a dictionary of lists
            called "matches"
            the key to each list is a team's name
            Each list has the presence of a team on each alliance in a match
            red first then blue
            0 for not present, 1 for present
            so if a team was on the red alliance in a match and not present in another
            their list would look like:
            1
            0
            0
            0
            
            the program automatically adds two 0's to each team on record
            unless they play in that match
            
            if a team isn't on record the program will calculate how many 0's need to be added
            '''


            row_dict = dict(row)
            full_csv.append(row_dict)
            auto_scores.append(int(row_dict['Red auto']))
            auto_scores.append(int(row_dict['Blue auto']))
            teleop_scores.append(int(row_dict['Red teleop']))
            teleop_scores.append(int(row_dict['Blue teleop']))
            endgame_scores.append(int(row_dict['Red endgame']))
            endgame_scores.append(int(row_dict['Blue endgame']))
            scores = tally(row_dict)
            total_scores.append(scores[0])
            total_scores.append(scores[1])
            if row_dict['Red team 1'] in team_scores:
                team_scores[row_dict['Red team 1']]['Auto'].append(int(row_dict['Red auto']))
                team_scores[row_dict['Red team 1']]['Teleop'].append(int(row_dict['Red teleop']))
                team_scores[row_dict['Red team 1']]['Endgame'].append(int(row_dict['Red endgame']))
                team_scores[row_dict['Red team 1']]['Total'].append(scores[0])
            else:
                team_scores[row_dict['Red team 1']] = dict()
                team_scores[row_dict['Red team 1']]['Auto'] = [int(row_dict['Red auto'])]
                team_scores[row_dict['Red team 1']]['Teleop'] = [int(row_dict['Red teleop'])]
                team_scores[row_dict['Red team 1']]['Endgame'] = [int(row_dict['Red endgame'])]
                team_scores[row_dict['Red team 1']]['Total'] = [scores[0]]
            if row_dict['Red team 2'] in team_scores:
                team_scores[row_dict['Red team 2']]['Auto'].append(int(row_dict['Red auto']))
                team_scores[row_dict['Red team 2']]['Teleop'].append(int(row_dict['Red teleop']))
                team_scores[row_dict['Red team 2']]['Endgame'].append(int(row_dict['Red endgame']))
                team_scores[row_dict['Red team 2']]['Total'].append(scores[0])
            else:
                team_scores[row_dict['Red team 2']] = dict()
                team_scores[row_dict['Red team 2']]['Auto'] = [int(row_dict['Red auto'])]
                team_scores[row_dict['Red team 2']]['Teleop'] = [int(row_dict['Red teleop'])]
                team_scores[row_dict['Red team 2']]['Endgame'] = [int(row_dict['Red endgame'])]
                team_scores[row_dict['Red team 2']]['Total'] = [scores[0]]
            if row_dict['Blue team 1'] in team_scores:
                team_scores[row_dict['Blue team 1']]['Auto'].append(int(row_dict['Blue auto']))
                team_scores[row_dict['Blue team 1']]['Teleop'].append(int(row_dict['Blue teleop']))
                team_scores[row_dict['Blue team 1']]['Endgame'].append(int(row_dict['Blue endgame']))
                team_scores[row_dict['Blue team 1']]['Total'].append(scores[0])
            else:
                team_scores[row_dict['Blue team 1']] = dict()
                team_scores[row_dict['Blue team 1']]['Auto'] = [int(row_dict['Blue auto'])]
                team_scores[row_dict['Blue team 1']]['Teleop'] = [int(row_dict['Blue teleop'])]
                team_scores[row_dict['Blue team 1']]['Endgame'] = [int(row_dict['Blue endgame'])]
                team_scores[row_dict['Blue team 1']]['Total'] = [scores[1]]
            if row_dict['Blue team 2'] in team_scores:
                team_scores[row_dict['Blue team 2']]['Auto'].append(int(row_dict['Blue auto']))
                team_scores[row_dict['Blue team 2']]['Teleop'].append(int(row_dict['Blue teleop']))
                team_scores[row_dict['Blue team 2']]['Endgame'].append(int(row_dict['Blue endgame']))
                team_scores[row_dict['Blue team 2']]['Total'].append(scores[0])
            else:
                team_scores[row_dict['Blue team 2']] = dict()
                team_scores[row_dict['Blue team 2']]['Auto'] = [int(row_dict['Blue auto'])]
                team_scores[row_dict['Blue team 2']]['Teleop'] = [int(row_dict['Blue teleop'])]
                team_scores[row_dict['Blue team 2']]['Endgame'] = [int(row_dict['Blue endgame'])]
                team_scores[row_dict['Blue team 2']]['Total'] = [scores[1]]
            match_num += 2  # adds 2 each time because each match has a red and blue side
            # adding 0's and 1's
            '''
                        label which matches a team was in and which color
                        do this for the whole data set
                        then generate 1's and 0's accordingly
                        '''

            if row_dict['Red team 1'] in raw_matches:
                raw_matches[row_dict['Red team 1']].append('R'+str(row_dict['Match code']))
            else:
                team_nums.append(row_dict['Red team 1'])
                raw_matches[row_dict['Red team 1']] = []
                raw_matches[row_dict['Red team 1']].append('R' + str(row_dict['Match code']))
                teams[row_dict['Red team 1']] = dict()
                teams[row_dict['Red team 1']]['Team #'] = row_dict['Red team 1']

            if row_dict['Red team 2'] in raw_matches:
                raw_matches[row_dict['Red team 2']].append('R' + str(row_dict['Match code']))
            else:
                team_nums.append(row_dict['Red team 1'])
                raw_matches[row_dict['Red team 2']] = []
                raw_matches[row_dict['Red team 2']].append('R' + str(row_dict['Match code']))
                teams[row_dict['Red team 2']] = dict()
                teams[row_dict['Red team 2']]['Team #'] = row_dict['Red team 2']

            if row_dict['Blue team 1'] in raw_matches:
                raw_matches[row_dict['Blue team 1']].append('B' + str(row_dict['Match code']))
            else:
                team_nums.append(row_dict['Red team 1'])
                raw_matches[row_dict['Blue team 1']] = []
                raw_matches[row_dict['Blue team 1']].append('B' + str(row_dict['Match code']))
                teams[row_dict['Blue team 1']] = dict()
                teams[row_dict['Blue team 1']]['Team #'] = row_dict['Blue team 1']

            if row_dict['Blue team 2'] in raw_matches:
                raw_matches[row_dict['Blue team 2']].append('B' + str(row_dict['Match code']))
            else:
                team_nums.append(row_dict['Red team 1'])
                raw_matches[row_dict['Blue team 2']] = []
                raw_matches[row_dict['Blue team 2']].append('B' + str(row_dict['Match code']))
                teams[row_dict['Blue team 2']] = dict()
                teams[row_dict['Blue team 2']]['Team #'] = row_dict['Blue team 2']

            row_count += 1

        print('hello')

    with open(csv_location) as csvFile:
        team_order = []  # The order teams are placed into rows
        match_order = []  # the order matches (identified by match code) will be placed into the matrix
        result_sheet = csv.DictReader(csvFile, delimiter=',')  # the sheet
        sort_count = 0

        for arow in result_sheet:
            rowdic = dict(arow)
            match_order.append('R' + str(rowdic['Match code']))
            matches.append([])
            matches.append([])
            if sort_count == 0:
                for team in raw_matches:
                    if team not in team_order:
                        opponent_score.append([])
                        print(team)
                        team_order.append(team)
                    presentr = False
                    presentb = False
                    for pres in raw_matches[team]:
                        # checks if a team was blue or red in that match
                        if not presentr:
                            if ('R' + str(rowdic['Match code'])) == pres:
                                matches[sort_count].append(1)
                                presentr = True

                    if not presentr:
                        matches[sort_count].append(0)

                        for pres in raw_matches[team]:
                            # checks if a team was blue or red in that match
                            if not presentb:
                                if 'B' + str(rowdic['Match code']) == pres:
                                    matches[(sort_count + 1)].append(1)
                                    presentb = True

                    if not presentb:
                        matches[sort_count + 1].append(0)
            if sort_count != 0:
                num = 0
                while num < len(team_order):
                    presentr = False
                    presentb = False
                    for pres in raw_matches[team_order[num]]:
                        # checks if a team was blue or red in that match
                        if not presentr:
                            if ('R' + str(rowdic['Match code'])) == pres:
                                matches[sort_count].append(1)
                                presentr = True

                    if not presentr:
                        matches[sort_count].append(0)

                        for pres in raw_matches[team_order[num]]:
                            # checks if a team was blue or red in that match
                            if not presentb:
                                if 'B' + str(rowdic['Match code']) == pres:
                                    matches[(sort_count + 1)].append(1)
                                    presentb = True

                    if not presentb:
                        matches[sort_count + 1].append(0)
                    num += 1

            sort_count += 2



    # assigns team names to numbers

    # gets team names from refcxv
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
    print('auto shape')
    print(auto_scores)
    print(raw_matches)
    allteam = [matches, teams, total_scores, auto_scores, teleop_scores,
               endgame_scores, match_order, team_order, full_csv, raw_matches, team_scores]

    return allteam


def tally(row_dict):
    red_score = int(row_dict['Red auto']) + int(row_dict['Red teleop'])
    red_score += int(row_dict['Red endgame']) + int(row_dict['Blue penalty'])

    blue_score = int(row_dict['Blue auto']) + int(row_dict['Blue teleop'])
    blue_score += int(row_dict['Blue endgame']) + int(row_dict['Red penalty'])
    scores = [red_score, blue_score]
    return scores
