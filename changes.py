"""
Program Name: changes
By: Omer Alon
Date: 01/04/17
Program Version: 1.0.0
"""


class Changes(object):

    def __init__(self, updated_games, old_games):
        """Set the class's attributes."""
        self.__updated_games = updated_games
        self.__old_games = old_games

    def find_new_games(self):
        """Find new games that started.


        Returns:
            new_games - A list of dictionaries that contains
            the new games that started.
        """
        last_home_teams = [game['homeTeamName'] for game in self.__old_games]
        # get new games
        new_games = [game for game in self.__updated_games if game['homeTeamName']
                     not in last_home_teams]
        return new_games

    def find_finished_games(self):
        """Find the games that finished.


        Returns:
            finished - A list of dictionaries that contains
            the games that finished
        """
        new_home_teams = [game['homeTeamName'] for game in self.__updated_games]
        # get finished games
        finished = [game for game in self.__old_games if game['homeTeamName']
                    not in new_home_teams]
        return finished

    def find_new_goals(self):
        """Find new goals on the live games.


        Returns:
            new_games - A list of tuples that contains
            the new goals on the live games.
        """
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

    def find_all_changes(self):
        """Find updates on new games, finished games and goals.
        *********delete this if there is no use at the end of the project.

        Returns:
            changes - A list of lists that contains the new updates.
        """
        return [self.find_new_games(),
                self.find_finished_games(), self.find_new_goals()]