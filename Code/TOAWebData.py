import os
import csv
import requests
import collections as cl


def main():
    data_csv = '/CSV/WAStateEvents.csv'  # csv for data
    api_key = 'bf4e3d409a68f3664d43df97e880bef840d35b7c3d7d3f1fa9b5e9c61d67ad98'
    headers = {'Content-Type': 'application/json',
               'X-TOA-Key': api_key, 'X-Application-Origin': 'TOAWebData.py'}
    URL1 = 'http://theorangealliance.org/api/event/1819-WA-PAS/matches'
    URL2 = 'http://theorangealliance.org/api/event/1819-WA-FEN/matches'


    event_table = dict()

    r1 = requests.get(url=URL1, headers=headers)
    print(r1.status_code)
    raw_pas = r1.json()
    print(type(raw_pas))
    print(raw_pas)
    all_teams = dict()
    x = 0
    while x < len(raw_pas):

        all_teams[raw_pas[x]['match_key']] = {
            'Event': 'Pasteur Interlague',
            'State': 'WA',
            'Date': '2018-12-15T00:00:00.000Z',
            'Match Code': raw_pas[x]['match_key'],
            'Red team 1': raw_pas[x]['participants'][0]['team_key'],
            'Red team 2': raw_pas[x]['participants'][1]['team_key'],
            'Blue team 1': raw_pas[x]['participants'][2]['team_key'],
            'Blue team 2': raw_pas[x]['participants'][3]['team_key'],
            'Red auto': raw_pas[x]['red_auto_score'],
            'Red teleop': raw_pas[x]['red_tele_score'],
            'Red endgame': raw_pas[x]['red_end_score'],
            'Red penalty': raw_pas[x]['red_penalty'],
            'Blue auto': raw_pas[x]['blue_auto_score'],
            'Blue teleop': raw_pas[x]['blue_tele_score'],
            'Blue endgame': raw_pas[x]['blue_end_score'],
            'Blue penalty': raw_pas[x]['blue_penalty']
        }
        if x == 1:
            default_d = {'Event': 'Pasteur Interlague',
                'State': 'WA',
                'Date': '2018-12-15T00:00:00.000Z',
                'Match Code': raw_pas[x]['match_key'],
                'Red team 1': raw_pas[x]['participants'][0]['team_key'],
                'Red team 2': raw_pas[x]['participants'][1]['team_key'],
                'Blue team 1': raw_pas[x]['participants'][2]['team_key'],
                'Blue team 2': raw_pas[x]['participants'][3]['team_key'],
                'Red auto': raw_pas[x]['red_auto_score'],
                'Red teleop': raw_pas[x]['red_tele_score'],
                'Red endgame': raw_pas[x]['red_end_score'],
                'Red penalty': raw_pas[x]['red_penalty'],
                'Blue auto': raw_pas[x]['blue_auto_score'],
                'Blue teleop': raw_pas[x]['blue_tele_score'],
                'Blue endgame': raw_pas[x]['blue_end_score'],
                'Blue penalty': raw_pas[x]['blue_penalty']}
        x += 1
    x = 0

    r2 = requests.get(url=URL2, headers=headers)
    print(r2.status_code)
    raw_fen = r2.json()
    print(type(raw_fen))
    print(raw_fen)

    while x < len(raw_fen):

        all_teams[raw_fen[x]['match_key']] = {
            'Event': 'Feynman Interleague',
            'State': 'WA',
            'Date': '2018-12-15T00:00:00.000Z',
            'Match Code': raw_fen[x]['match_key'],
            'Red team 1': raw_fen[x]['participants'][0]['team_key'],
            'Red team 2': raw_fen[x]['participants'][1]['team_key'],
            'Blue team 1': raw_fen[x]['participants'][2]['team_key'],
            'Blue team 2': raw_fen[x]['participants'][3]['team_key'],
            'Red auto': raw_fen[x]['red_auto_score'],
            'Red teleop': raw_fen[x]['red_tele_score'],
            'Red endgame': raw_fen[x]['red_end_score'],
            'Red penalty': raw_fen[x]['red_penalty'],
            'Blue auto': raw_fen[x]['blue_auto_score'],
            'Blue teleop': raw_fen[x]['blue_tele_score'],
            'Blue endgame': raw_fen[x]['blue_end_score'],
            'Blue penalty': raw_fen[x]['blue_penalty']
        }
        x += 1

    cwd = os.getcwd()
    os.chdir(cwd)
    os.chdir('..')
    match_num = 0
    create_file(all_teams, cwd, data_csv, default_d)


def create_file(all_teams, cwd, csv2, default_d):
    csv2 = os.getcwd() + csv2
    y = sorted(all_teams, key=lambda x: (all_teams[x]['State']), reverse=True)

    c = 1

    if os.path.exists(csv2):  # deletes the rankings file if it exists
        os.remove(csv2)
    with open(csv2, 'w+', newline='') as f:  # creates a new file
        w = csv.DictWriter(f, default_d.keys(), extrasaction='ignore')  # i

        w.writeheader()
        for team in all_teams:
            w.writerow(all_teams[y[c-1]])
            c += 1


if __name__ == '__main__':
    main()
