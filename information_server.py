"""
Program Name: information_server
By: Omer Alon
Date: 01/04/17
Program Version: 1.0.0
"""
import requests
import changes
import time
import calendar
import datetime
from team_codes import *


class InformationSource(object):
    LIVE_RESULTS_API = "http://soccer-cli.appspot.com/"
    OTHER_INFO_API = "http://api.football-data.org/v1/"
    HEADERS = {"X-Auth-Token": "7796fc8dfc6740048cf8ebb80c3f3108"}

    def __init__(self):
        """Set the class"s attributes."""
        self.__last_scores = []

    def get_changes(self):
        """Get the changes in the live games.


        Returns:
            changed - A list of lists that contains the updates on the live games.
        """
        old_scores = self.__last_scores
        new_scores = self.get_live_games()
        changed = changes.Changes(new_scores, old_scores).find_all_changes()
        return changed[0], changed[1], changed[2]

    def get_live_games(self):
        """Get the live games.


        Returns:
            last_scores - A list of dictionaries, each containing information
            about the currently live games, in the following format:
            {"goalsAwayTeam": -,
             "time": -,
             "homeTeamName": -,
             "awayTeamName": -,
             "goalsHomeTeam": -
            }
        """
        try:
            games = requests.get(self.LIVE_RESULTS_API, headers=InformationSource.HEADERS).json()
        except ValueError:
            return self.get_live_games()
        # filter the live games
        self.__last_scores = [game for game in games["games"]
                              if -1 not in game.values() and "FT" not in game.values()]
        for game in self.__last_scores:
            del game["league"]
        return self.__last_scores

    @staticmethod
    def get_all_teams():
        """Get all the available teams from the teams' file.


        Returns:
            teams - A list that contains the available teams.
        """
        with open("teams.txt") as teams_list:
            for i, team in enumerate(teams_list.read().splitlines()):
                if team and i != 0:
                    yield team

    @staticmethod
    def get_games(user_teams):
        """Get a user's team and return all the games that they played.


        Receives:
            user_teams - A list that contains the names of the user's teams.

        Returns:
            old_games - A list of dictionaries of the finished games of the teams.
        """
        all_games = []
        for team in user_teams:
            all_games += InformationSource.get_team_games(team)
        delete_duplicates = []
        for game in all_games:
            game["date"] = InformationSource.convert_to_local_time(game["date"])
        for game in all_games:
            if game in delete_duplicates:
                all_games.remove(game)
            try:
                if TEAMS_DICT[game["homeTeamName"]] in user_teams and TEAMS_DICT[game["awayTeamName"]] in user_teams:
                    delete_duplicates.append(game)
            except KeyError:
                pass
        print "duplicates: %r" % delete_duplicates
        print all_games
        return sorted(all_games, key=lambda fixture: fixture["date"])

    @staticmethod
    def get_team_games(team):
        team_code = TEAM_CODES[team]
        team_games = requests.get("%s/teams/%d/fixtures" % (InformationSource.OTHER_INFO_API, team_code),
                                  headers=InformationSource.HEADERS).json()

        try:
            return team_games["fixtures"]
        except KeyError:
            time.sleep(50)
            return InformationSource.get_team_games(team)

    @staticmethod
    def convert_to_local_time(timestamp):
        timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        timestamp = calendar.timegm(timestamp.timetuple())
        return datetime.datetime.fromtimestamp(timestamp)

    @staticmethod
    def remove_duplicates(games):
        pass
        # for game in games:
        #     counter = 0
        #     for fixture in games:
        #         if game["date"] == fixture["date"] and game["homeTeamName"] == fixture["homeTeamName"]:
        #             counter += 1
        #     if counter > 1:
        #         games.remove(game)