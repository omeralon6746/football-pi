"""
Program Name: user
By: Omer Alon
Date: 02/04/17
Program Version: 1.0.0
"""
import yaml


USERS_DATA = "users.yaml"


class User(object):

    def __init__(self, username):
        """Set the class's attributes."""
        self.__username = username
        self.__teams = []
        self.__leagues = []

    def set_teams(self, picked_teams):
        """Set the teams' attribute.


        Receives:
            picked_teams - A list that contains the teams
            that the user chose to follow on.
        """
        self.__teams = picked_teams

    def set_leagues(self, picked_leagues):
        """Set the leagues' attribute.


        Receives:
            picked_leagues - A list that contains the leagues
            that the user chose to follow on.
        """
        self.__leagues = picked_leagues

    def check_username(self):
        """Check if the username already exists in one of the saves.


        Receives:
            username - A string that contains the user's name that was entered by the user.

        Returns:
            check_exist - A bool that indicates if the username exists or not.
        """
        check_exist = False
        with open(USERS_DATA, "r") as users_file:
            users = yaml.load(users_file)
            for user in users:
                if self.__username in user.keys():
                    check_exist = True
        return check_exist

    def create_user_data(self, new_user):
        """If it is new user, create a text file with the user's name and details.
           Else, update the existing file.


        Receives:
            new_user - A bool that indicates if the username is new or not.
        """
        if new_user:
            with open(self.__username + ".txt", "w") as name:
                name.write("teams:\r\n\r\n")

    def add_data(self, f):
        """Add to the user's file the requested information from the user.


        Receives:
            request - A string that contains the user's requested information.
        """
        for team in self.__teams:
            f.write(team + "\r\n\r\n")
        f.write("leagues\r\n\r\n")
        for league in self.__leagues:
            f.write(league + "\r\n\r\n")

    def restore_data(self):
        """Restore the details of an existing user.******************************************"""
        pass

    def get_details(self):
        """Get the user's details(teams and leagues).


        Returns:
            details - A list of two lists that contains the teams and the leagues.
        """
        details = None
        details.append(self.__teams)
        details.append(self.__leagues)
        return details