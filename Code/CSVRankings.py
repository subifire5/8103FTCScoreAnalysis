import os
import csv
import collections as cl
import pandas
import bs4
import numpy as np
import EventClass as ec

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


def csv_sheet(refcsv, cwd, csv_location, refcsv2):
    events = dict()
    # Changes the directory to The Excel Folder
    '''
    1. you need to make code more efficient
    To do this, process each event (i.e. tesla interlagues, tesla qualifierrs)
    as a seperate event rather than the entire set of matches as one huge table
    get the OPR, DPR, etc of each team multiple times like that, and then
    average out their stats from each competitin

    this means you make multipel instances of each team, one for each event they were at
    it also means calculating hte linear algebra will be done with only around 30 matches at a time.
    '''
    os.chdir(cwd)
    os.chdir('..')
    cwd = os.getcwd()
    match_num = 0
    csv_location = cwd + csv_location
    with open(csv_location) as csvFile:

        result_sheet = csv.DictReader(csvFile, delimiter=',')  # the sheet

        row_count = 0  # the row being iterated

        # The code will skip the first row with real data
        count = 0
        team_nums = []
        for row in result_sheet:
            row_dict = dict(row)
            ev = row_dict['Event']  # a placeholder for the name of an event
            r1 = row_dict['Red team 1']
            r2 = row_dict['Red team 2']
            b1 = row_dict['Blue team 1']
            b2 = row_dict['Blue team 2']
            rau = row_dict['Red auto']
            rte = row_dict['Red teleop']
            ren = row_dict['Red endgame']
            bau = row_dict['Blue auto']
            bte = row_dict['Blue teleop']
            ben = row_dict['Blue endgame']
            maco = row_dict['Match code']
            try:
                events[ev].full_csv.append(row_dict)
                events[ev].auto_scores.append(int(rau))
                events[ev].auto_scores.append(int(bau))
                events[ev].teleop_scores.append(int(rte))
                events[ev].teleop_scores.append(int(bte))
                events[ev].endgame_scores.append(int(ren))
                events[ev].endgame_scores.append(int(ben))
                scores = tally(row_dict)
                events[ev].total_scores.append(scores[0])
                events[ev].total_scores.append(scores[1])

            except KeyError:
                events[ev] = ec.Event()
                events[ev].full_csv.append(row_dict)
                events[ev].auto_scores.append(int(rau))
                events[ev].auto_scores.append(int(bau))
                events[ev].teleop_scores.append(int(rte))
                events[ev].teleop_scores.append(int(bte))
                events[ev].endgame_scores.append(int(ren))
                events[ev].endgame_scores.append(int(ben))
                scores = tally(row_dict)
                events[ev].total_scores.append(scores[0])
                events[ev].total_scores.append(scores[1])

            # if row_count > 0:
            count += 1

            '''
            A brief explanation2

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

            if row_dict['Red team 1'] in events[ev].team_scores:
                events[ev].team_scores[r1]['Auto'].append(int(rau))
                events[ev].team_scores[r1]['Teleop'].append(int(rte))
                events[ev].team_scores[r1]['Endgame'].append(int(ren))
                events[ev].team_scores[r1]['Total'].append(scores[0])
                events[ev].match_stats[r1].append('R'+maco)
            else:
                events[ev].team_scores[r1] = dict()
                events[ev].team_scores[r1]['Auto'] = []
                events[ev].team_scores[r1]['Teleop'] = []
                events[ev].team_scores[r1]['Endgame'] = []
                events[ev].team_scores[r1]['Total'] = []
                events[ev].match_stats[r1] = ['R'+maco]
                events[ev].team_scores[r1]['Auto'].append(int(rau))
                events[ev].team_scores[r1]['Teleop'].append(int(rte))
                events[ev].team_scores[r1]['Endgame'].append(int(ren))
                events[ev].team_scores[r1]['Total'].append(scores[0])

            if row_dict['Red team 2'] in events[ev].team_scores:
                events[ev].team_scores[r2]['Auto'].append(int(rau))
                events[ev].team_scores[r2]['Teleop'].append(int(rte))
                events[ev].team_scores[r2]['Endgame'].append(int(ren))
                events[ev].team_scores[r2]['Total'].append(scores[0])
                events[ev].match_stats[r2].append('R'+maco)
            else:
                events[ev].team_scores[r2] = dict()
                events[ev].team_scores[r2]['Auto'] = []
                events[ev].team_scores[r2]['Teleop'] = []
                events[ev].team_scores[r2]['Endgame'] = []
                events[ev].team_scores[r2]['Total'] = []
                events[ev].match_stats[r2] = ['R'+maco]
                events[ev].team_scores[r2]['Auto'].append(int(rau))
                events[ev].team_scores[r2]['Teleop'].append(int(rte))
                events[ev].team_scores[r2]['Endgame'].append(int(ren))
                events[ev].team_scores[r2]['Total'].append(scores[0])

            if row_dict['Blue team 1'] in events[ev].team_scores:
                events[ev].team_scores[b1]['Auto'].append(int(bau))
                events[ev].team_scores[b1]['Teleop'].append(int(bte))
                events[ev].team_scores[b1]['Endgame'].append(int(ben))
                events[ev].team_scores[b1]['Total'].append(scores[0])
                events[ev].match_stats[b1].append('B'+maco)
            else:
                events[ev].team_scores[b1] = dict()
                events[ev].team_scores[b1]['Auto'] = []
                events[ev].team_scores[b1]['Teleop'] = []
                events[ev].team_scores[b1]['Endgame'] = []
                events[ev].team_scores[b1]['Total'] = []
                events[ev].match_stats[b1] = ['B'+maco]
                events[ev].team_scores[b1]['Auto'].append(int(bau))
                events[ev].team_scores[b1]['Teleop'].append(int(bte))
                events[ev].team_scores[b1]['Endgame'].append(int(ben))
                events[ev].team_scores[b1]['Total'].append(scores[0])

            if row_dict['Blue team 2'] in events[ev].team_scores:
                events[ev].team_scores[b2]['Auto'].append(int(bau))
                events[ev].team_scores[b2]['Teleop'].append(int(bte))
                events[ev].team_scores[b2]['Endgame'].append(int(ben))
                events[ev].team_scores[b2]['Total'].append(scores[0])
                events[ev].match_stats[b2].append('B'+maco)
            else:
                events[ev].team_scores[b2] = dict()
                events[ev].team_scores[b2]['Auto'] = []
                events[ev].team_scores[b2]['Teleop'] = []
                events[ev].team_scores[b2]['Endgame'] = []
                events[ev].team_scores[b2]['Total'] = []
                events[ev].match_stats[b2] = ['B'+maco]
                events[ev].team_scores[b2]['Auto'].append(int(bau))
                events[ev].team_scores[b2]['Teleop'].append(int(bte))
                events[ev].team_scores[b2]['Endgame'].append(int(ben))
                events[ev].team_scores[b2]['Total'].append(scores[0])
            events[ev].match_num += 2  # adds 2 each time because each match has a red and blue side
            # adding 0's and 1's
            '''
                        label which matches a team was in and which color
                        do this for the whole data set
                        then generate 1's and 0's accordingly
                        '''

            if row_dict['Red team 1'] in events[ev].raw_matches:
                events[ev].raw_matches[r1].append('R' + str(maco))
            else:
                events[ev].team_nums.append(r1)
                events[ev].raw_matches[r1] = []
                events[ev].raw_matches[r1].append('R' + str(maco))
                events[ev].teams[r1] = dict()
                events[ev].teams[r1]['Team #'] = r1

            if row_dict['Red team 2'] in events[ev].raw_matches:
                events[ev].raw_matches[r2].append('R' + str(maco))
            else:
                events[ev].team_nums.append(r2)
                events[ev].raw_matches[r2] = []
                events[ev].raw_matches[r2].append('R' + str(maco))
                events[ev].teams[r2] = dict()
                events[ev].teams[r2]['Team #'] = r2

            if row_dict['Blue team 1'] in events[ev].raw_matches:
                events[ev].raw_matches[b1].append('B' + str(maco))
            else:
                events[ev].team_nums.append(b1)
                events[ev].raw_matches[b1] = []
                events[ev].raw_matches[b1].append('B' + str(maco))
                events[ev].teams[b1] = dict()
                events[ev].teams[b1]['Team #'] = b1

            if row_dict['Blue team 2'] in events[ev].raw_matches:
                events[ev].raw_matches[b2].append('B' + str(maco))
            else:
                events[ev].team_nums.append(b2)
                events[ev].raw_matches[b2] = []
                events[ev].raw_matches[b2].append('B' + str(maco))
                events[ev].teams[b2] = dict()
                events[ev].teams[b2]['Team #'] = b2

            row_count += 1
        for ev in events:
            print('teams in general')
            print(events[ev].teams)

    with open(csv_location) as csvFile:
        result_sheet = csv.DictReader(csvFile, delimiter=',')  # the sheet
        for arow in result_sheet:
            rowdic = dict(arow)
            ev = rowdic['Event']  # a placeholder for the name of an event
            r1 = rowdic['Red team 1']
            r2 = rowdic['Red team 2']
            b1 = rowdic['Blue team 1']
            b2 = rowdic['Blue team 2']
            rau = rowdic['Red auto']
            rte = rowdic['Red teleop']
            ren = rowdic['Red endgame']
            bau = rowdic['Blue auto']
            bte = rowdic['Blue teleop']
            ben = rowdic['Blue endgame']
            maco = rowdic['Match code']

            events[ev].match_order.append('R' + str(maco))
            events[ev].matches.append([])
            events[ev].matches.append([])
            if events[ev].sort_count == 0:
                for team in events[ev].raw_matches:
                    if team not in events[ev].team_order:
                        events[ev].opponent_score.append([])
                        events[ev].team_order.append(team)
                    presentr = False
                    presentb = False
                    for pres in events[ev].raw_matches[team]:
                        # checks if a team was blue or red in that match
                        if not presentr:
                            if ('R' + str(maco)) == pres:
                                events[ev].matches[events[ev].sort_count].append(1)
                                presentr = True

                    if not presentr:
                        events[ev].matches[events[ev].sort_count].append(0)

                        for pres in events[ev].raw_matches[team]:
                            # checks if a team was blue or red in that match
                            if not presentb:
                                if 'B' + str(maco) == pres:
                                    events[ev].matches[(events[ev].sort_count + 1)].append(1)
                                    presentb = True

                    if not presentb:
                        events[ev].matches[events[ev].sort_count + 1].append(0)
            if events[ev].sort_count != 0:
                events[ev].num = 0
                while events[ev].num < len(events[ev].team_order):
                    presentr = False
                    presentb = False
                    for pres in events[ev].raw_matches[events[ev].team_order[events[ev].num]]:
                        # checks if a team was blue or red in that match
                        if not presentr:
                            if ('R' + str(maco)) == pres:
                                events[ev].matches[events[ev].sort_count].append(1)
                                presentr = True

                    if not presentr:
                        events[ev].matches[events[ev].sort_count].append(0)

                        for pres in events[ev].raw_matches[events[ev].team_order[events[ev].num]]:
                            # checks if a team was blue or red in that match
                            if not presentb:
                                if 'B' + str(rowdic['Match code']) == pres:
                                    events[ev].matches[(events[ev].sort_count + 1)].append(1)
                                    presentb = True

                    if not presentb:
                        events[ev].matches[events[ev].sort_count + 1].append(0)
                    events[ev].num += 1

            events[ev].sort_count += 2
    for ev in events:
        print('here')
        print(events[ev].matches)

    # assigns team names to numbers

    # gets team names from refcxv
    cwd = os.getcwd()
    refcsv = cwd + refcsv
    with open(refcsv) as csvFile:

        result_sheet = csv.DictReader(csvFile, delimiter=',')  # the sheet
        en = row_dict['Event']  # a placeholder for the name of an event

        # The code will skip the first row with real data

        for row in result_sheet:
            # if row_count > 0:

            row_dict = dict(row)

            ref_teamn = row_dict['Team #']
            ref_name = row_dict['Name']
            for teamn in events[ev].teams:
                try:
                    r = events[ev].teams[teamn]['Name']
                except KeyError:

                    if events[ev].teams[teamn]['Team #'] == ref_teamn:
                        events[ev].teams[teamn]['Name'] = ref_name
                        break


    return events


def tally(row_dict):
    red_score = int(row_dict['Red auto']) + int(row_dict['Red teleop'])
    red_score += int(row_dict['Red endgame']) + int(row_dict['Blue penalty'])

    blue_score = int(row_dict['Blue auto']) + int(row_dict['Blue teleop'])
    blue_score += int(row_dict['Blue endgame']) + int(row_dict['Red penalty'])
    scores = [red_score, blue_score]
    return scores

