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
        super(Main, self).__init__(**kwargs)
        self.__user = None
        self.__screen_manager = kv.ScreenManagerNew(self, information_server.InformationSource.get_all_teams())


    @property
    def user(self):
        return self.__user

    def build(self):
        # set window size
        return self.__screen_manager

    def end_team_selection_screen(self, selected_teams):
        self.__user.set_teams(selected_teams)
        self.set_screen("home")

    def update_username(self, username):
        self.__user = user.User(username)
        if self.__user.check_username():
            self.set_screen("home")
        else:
            self.set_screen("team_selection")

    def set_screen(self, screen_name):
        if screen_name == "home":
            thread = threading.Thread(target=self.__screen_manager.home_screen.update)
            thread.daemon = True
            thread.start()

        self.__screen_manager.current = screen_name


if __name__ == '__main__':
    Main().run()
