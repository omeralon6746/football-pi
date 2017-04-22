"""
Program Name: user
By: Omer Alon
Date: 02/04/17
Program Version: 1.0.0
"""
import yaml
import information_server


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
        with open(USERS_DATA, 'a') as users_data:
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

    def get_goals_updates(self, goals_updates):
        """Check if the user's teams are on the goals updates that was found.


        Receives:
            goals_updates - A list of tuples that contains the updates on the new goal
            that was found.

        Returns:
            user_goals_updates - A list of tuples that contains the updates on the
            new goals that relevant to the user's choices.
        """


    def get_new_games_updates(self, new_games_updates):
        """Check if the user's teams are on the new games updates that was found.


        Receives:
            new_games_updates - A list of tuples that contains the updates on the new games
            that was found.

        Returns:
            user_new_games - A list of tuples that contains the updates on the
            new games that relevant to the user's choices.
        """
        pass

    def get_ended_games_updates(self, new_games_updates):
        """Check if the user's teams are on the ended games updates that was found.


        Receives:
            ended_games_updates - A list of tuples that contains the updates on the ended games
            that was found.

        Returns:
            user_ended_games - A list of tuples that contains the updates on the
            ended games that relevant to the user's choices.
        """
        pass

    def get_live_games(self, live_games):
        """Check if the user's teams are on the live games.


        Receives:
            live_games - A list of dictionaries, each containing information
            about the currently live games.

        Returns:
            self.__user_games - A list of dictionaries, each containing information
            about the currently live games of the user.
        """
        self.__user_games = []

        for team in self.__teams:
            for game in live_games:
                if team in game.values():
                    self.__user_games.append(game)
        return self.__user_games

    def get_all_games(self):
        return self.__information_source.get_games(self.__teams)

    def get_games_categorized(self):
        return self.get_finished_games(), self.get_current_games()

    def get_finished_games(self):
        return [game for game in self.get_all_games() if game["status"] == "FINISHED"]

    def get_current_games(self):
        return self.get_live_games(self.__information_source.get_live_games())