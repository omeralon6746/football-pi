"""
Program Name: user
By: Omer Alon
Date: 02/04/17
Program Version: 1.0.0
"""
import yaml
import information_server
from team_codes import TEAMS_DICT
import datetime


USERS_DATA = "users.yaml"


class User(object):

    def __init__(self, username):
        """Set the class's attributes."""
        self.__username = username
        self.__teams = []
        self.__user_games = []
        self.__information_source = information_server.InformationSource()

    def set_teams(self, picked_teams):
        """Set the teams' attribute and update the users file.


        Receives:
            picked_teams - A list that contains the teams
            that the user chose to follow on.
        """
        self.__teams = picked_teams
        with open(USERS_DATA, "a") as users_data:
            yaml.dump([{self.__username: picked_teams}], users_data, default_flow_style=False)

    def check_username(self):
        """
        Check if the username already exists in one of the saves.
        If it exists, restore the user's team to the team's attribute.


        Returns:
            check_exist - A bool that indicates if the username exists or not.
        """
        check_exist = False
        with open(USERS_DATA, "r") as users_file:
            users = yaml.load(users_file)
            if users:
                for user in users:
                    if self.__username in user.keys():
                        for value in user.values():
                            for team in value:
                                self.__teams.append(team)
                        check_exist = True
        return check_exist

    def get_teams(self):
        """Get the user's details teams.
        *********delete this if there is no use at the end of the project.

        Returns:
            self.__teams - A list of the user's teams.
        """
        return self.__teams

    def get_changes_categorized(self):
        new_games, ended_games, goals = self.__information_source.get_changes()
        return self.get_user_games(new_games), \
            self.get_user_games(ended_games), \
            self.get_user_games(goals)

    def get_user_games(self, games):
        """Check if the user's teams are on the given games updates that was found.


        Receives:
            games - A list of dictionaries that contains games

        Returns:
            A list of dictionaries that contains only the games that belong to the user's teams
        """
        return [game for game in games if game["homeTeamName"] in self.__teams
                or game["awayTeamName"] in self.__teams]

    def get_all_games(self):
        return self.__information_source.get_games(self.__teams)

    def get_games_categorized(self):
        live = self.__information_source.get_live_games()
        return self.get_finished_games(live), self.get_user_games(live), self.get_future_games(live)

    def get_finished_games(self, live):
        finished_games = [game for game in self.get_all_games() if game["status"] == "FINISHED"]
        for i in xrange(len(finished_games) - 1):
            finished_games[i] = User.choose_information(finished_games[i])
        return User.check_in_live(finished_games, live)

    def get_future_games(self, live):
        future_games = [game for game in self.get_all_games() if None in game["result"].values()
                        and game["status"] != "POSTPONED"]
        for i in xrange(len(future_games) - 1):
            future_games[i] = User.choose_information(future_games[i])
        return User.check_in_live(future_games, live)

    @staticmethod
    def check_in_live(games, live_games):
        for i in xrange(len(games) - 1):
            for live_game in live_games:
                if games[i]["homeTeamName"] == live_game["homeTeamName"] \
                        and datetime.datetime.strptime(games[i]["date"][:10], "%Y-%m-%d") == \
                        datetime.datetime.today().date():
                    games.remove(games[i])
        return games

    @staticmethod
    def choose_information(game):
        edited_game = {"date": game["date"],
                       "goalsHomeTeam": game["result"]["goalsHomeTeam"],
                       "goalsAwayTeam": game["result"]["goalsAwayTeam"]}
        try:
            edited_game["homeTeamName"] = TEAMS_DICT[game["homeTeamName"]]
        except KeyError:
            edited_game["homeTeamName"] = game["homeTeamName"]
        try:
            edited_game["awayTeamName"] = TEAMS_DICT[game["awayTeamName"]]
        except KeyError:
            edited_game["awayTeamName"] = game["awayTeamName"]
        return edited_game