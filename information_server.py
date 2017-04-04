"""
Program Name: information_server
By: Omer Alon
Date: 01/04/17
Program Version: 1.0.0
"""
import requests
import changes


class InformationSource(object):
    LIVE_RESULTS_API = "http://soccer-cli.appspot.com/"
    OTHER_INFO_API = "http://api.football-data.org/v1/"

    def __init__(self):
        """Set the class's attributes."""
        self.__last_scores = []

    def get_changes(self):
        """Get the changes in the live games.


        Returns:
            changed - A list of lists that contains the updates on the live games.
        """
        old_scores = self.__last_scores
        new_scores = self.get_live_games()
        changed = changes.Changes(new_scores, old_scores).find_all_changes()
        return changed

    def get_live_games(self):
        """Get the live games.


        Returns:
            last_scores - A list of dictionaries, each containing information
            about the currently live games, in the following format:
            {'league': -,
            'goalsAwayTeam': -,
            'time': -,
            'homeTeamName': -,
            'awayTeamName': -,
            'goalsHomeTeam': -
            }
        """
        try:
            games = requests.get(self.LIVE_RESULTS_API).json()
        except ValueError:
            return self.get_live_games()
        # filter the live games
        self.__last_scores = [game for game in games['games'] if -1 not in game.values()]
        return self.__last_scores

    def get_team_league(team):
        """Get the team's league of a given team name.


        Receives:
            team - A string that contains a team.

        Returns:
            league - A string that contains the team's league.
        """
        pass