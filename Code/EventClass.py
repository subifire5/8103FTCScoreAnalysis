import os
import csv
import collections as cl
import pandas
import bs4
import numpy as np


class Event:

    def __init__(self):
        self.total_scores = []  # the scores for each match
        self.auto_scores = []  # auto scores for each match
        self.teleop_scores = []  # teleop scores for each match
        self.endgame_scores = []  # endgame scores for each match
        self.raw_matches = dict()  # A dictionary of lists representing teams in a match
        self.matches = []  # a lists of lists, each representing a color in a match
        self.teams = dict()  # A dict of dicts that will hold the processed data of all teams
        self.opponent_score = []  # a list of lists, each representing the scores against a team in a match
        self.team_scores = dict()  # a dict of lists of lists team scores
        self. team_nums = []
        self.full_csv = []
        self.match_num = 0
        self.team_order = []  # The order teams are placed into rows
        self.match_order = []  # the order matches (identified by match code) will be placed into the matrix
        self.sort_count = 0
        self.num = 0
        self.match_matrix = dict()
        self.match_stats = dict()



