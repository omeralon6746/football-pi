"""
Program Name: main_project
By: Omer Alon
Date: 08/03/17
Program Version: 1.0.0
"""
import information_server
import user
import os
import kv
import threading
from kivy.app import App


class Main(App):
    def __init__(self, **kwargs):
        """Set the class's attributes."""
        super(Main, self).__init__(**kwargs)
        self.__user = None
        self.__screen_manager = kv.ScreenManagerNew(self, information_server.InformationSource.get_all_teams())
        self.screen = "login"

    @property
    def user(self):
        return self.__user

    def build(self):
        # set window size
        return self.__screen_manager

    def end_team_selection_screen(self, selected_teams):
        """Set the new user's teams


        Receives:
            selected_teams - A list of the teams that the user chose.
        """
        self.__user.set_teams(selected_teams)
        # move to the next screen: home
        self.set_screen("home")

    def update_username(self, username):
        """Create the user object.


        Receives:
            username - A string that contains the user name.
        """
        self.__user = user.User(username)
        # if the username is already exists, skip team selection screen
        if self.__user.check_username():
            self.set_screen("home")
        else:
            self.set_screen("team_selection")

    def set_screen(self, screen_name):
        """Move to the next screen.


        Receives:
            screen_name - A string that contains the name of the screen that need to be show.
        """
        self.screen = screen_name
        if screen_name == "home":
            thread = threading.Thread(target=self.__screen_manager.home_screen.update)
            thread.daemon = True
            thread.start()
        self.__screen_manager.current = screen_name


if __name__ == '__main__':
    Main().run()
