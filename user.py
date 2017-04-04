"""
Program Name: user
By: Omer Alon
Date: 02/04/17
Program Version: 1.0.0
"""


class User(object):

    def __init__(self, username):
        """Set the class's attributes."""
        self.__username = username
        self.__teams = None
        self.__leagues = None

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

    def create_user_data(self, new_user):
        """If it is new user, create a text file with the user's name and details.
           Else, update the existing file.


        Receives:
            new_user - A bool that indicates if the username is new or not.
        """
        pass

    def add_data(self, request):
        """Add to the user's file the requested information from the user.


        Receives:
            request - A string that contains the user's requested information.
        """

    def restore_data(self):
        """Restore the details of an existing user."""
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