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
        """Set the class's attributes."""
        self.__last_scores = []

    def get_changes(self):
        """Get the changes in the live matches.


        Returns:
            changed - A list of lists that contains
                      the updates on the live matches.
        """
        old_scores = self.__last_scores
        new_scores = self.get_live_matches()
        # get the live matches changes
        changed = changes.Changes(new_scores, old_scores).find_all_changes()
        return changed[0], changed[1], changed[2]

    def get_live_matches(self):
        """Get the live matches.


        Returns:
            last_scores - A list of dictionaries, each containing information
            about the currently live matches, in the following format:
            {"goalsAwayTeam": -,
             "time": -,
             "homeTeamName": -,
             "awayTeamName": -,
             "goalsHomeTeam": -
            }
        """
        try:
            matches = requests.get(self.LIVE_RESULTS_API,
                                   headers=InformationSource.HEADERS).json()
        except ValueError:
            return self.get_live_matches()
        # filter the live matches
        self.__last_scores = [match for match in matches[MATCHES] if -1 not in
                              match.values() and
                              FINAL_TIME not in match.values()]
        for match in self.__last_scores:
            del match["league"]
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
    def get_matches(user_teams):
        """Get a user's teams and return all the matches that they played.


        Receives:
            user_teams - A list that contains the names of the user's teams.

        Returns:
            A list of dictionaries of the user teams' matches.
        """
        all_matches = []
        for team in user_teams:
            # get the matches of specific team from the information server
            all_matches += InformationSource.get_team_matches(team)
        without_duplications = []
        for match in all_matches:
            match[DATE] = InformationSource.convert_to_local_time(match[DATE])
        for match in all_matches:
            if match not in without_duplications:
                without_duplications.append(match)
        # sort the matches by date
        return sorted(without_duplications, key=lambda fixture: fixture[DATE])

    @staticmethod
    def get_team_matches(team):
        """Get all the team's matches.


        Receives:
            team - A string that contains the name of the team.


        Returns:
            A list of dictionaries that contains all the team's matches.
        """
        team_code = TEAM_CODES[team]
        try:
            team_matches = requests.get(
                "%s/teams/%d/fixtures" % (
                    InformationSource.OTHER_INFO_API, team_code),
                headers=InformationSource.HEADERS).json()
        except ValueError:
            return InformationSource.get_team_matches(team)
        # sleep time because of the request limit on the information server
        try:
            return team_matches["fixtures"]
        except KeyError:
            time.sleep(50)
            return InformationSource.get_team_matches(team)

    @staticmethod
    def convert_to_local_time(timestamp):
        """Convert to the time in Israel.



        Receives:
            timestamp - A string that contains the time of a match.


        Receives:
            A datetime object that contains the time of the match in Israel.
        """
        timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        timestamp = calendar.timegm(timestamp.timetuple())
        return datetime.datetime.fromtimestamp(timestamp)

    @property
    def last_scores(self):
        """Get the last scores."""
        return self.__last_scores
