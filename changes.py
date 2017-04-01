"""
Program Name: changes
By: Omer Alon
Date: 01/04/17
Program Version: 1.0.0
"""


class Changes(object):

    def __init__(self, updated_games, old_games):
        self.__updated_games = updated_games
        self.__old_games = old_games

    def find_new_games(self):
        last_home_teams = [game['homeTeamName'] for game in self.__old_games]
        # get new games
        new_games = [game for game in self.__updated_games if game['homeTeamName']
                     not in last_home_teams]
        return new_games

    def find_finished_games(self):
        new_home_teams = [game['homeTeamName'] for game in self.__updated_games]
        # get finished games
        finished = [game for game in self.__old_games if game['homeTeamName']
                    not in new_home_teams]
        return finished

    def find_new_goals(self):
        new_goals = []
        for game in self.__old_games:
            for live_game in self.__updated_games:
                if live_game['homeTeamName'] == game['homeTeamName']:
                    if live_game['goalsHomeTeam'] != game['goalsHomeTeam'] \
                            or live_game['goalsAwayTeam'] != game['goalsAwayTeam']:
                        new_goals.append(((game['homeTeamName'],
                                           live_game['goalsHomeTeam'] - game['goalsHomeTeam']),
                                        (game['homeTeamName'],
                                         live_game['goalsAwayTeam'] - game['goalsAwayTeam'])))

        new_goals += [((game['homeTeamName'], game['goalsHomeTeam']),
                       (game['awayTeamName'], game['goalsAwayTeam']))
                      for game in self.find_new_games() if game['goalsAwayTeam'] != 0
                      or game['goalsAwaysTeam'] != 0]

        return new_goals