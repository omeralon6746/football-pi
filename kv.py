"""
Program Name: kv
By: Omer Alon
Date: 02/04/17
Program Version: 1.0.0
"""
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from screen import ScreenNew, ScreenManager
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
from kivy.app import runTouchApp
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.widget import Widget
import datetime
import threading
import pandas
from sys import exit
from team_codes import *


Builder.load_string('''

<LoginScreen>:
    RelativeLayout:
        Label:
            text: "Football Pi"
            pos: 0, 200
            font_size: "64sp"
        TextInput:
            pos_hint: {"x": 0.25, "y": 0.5}
            size_hint: 0.5, 0.07
            multiline: False
            hint_text: "Enter Your Name"
            padding_x: 150
            id: username
            on_text: root.update_input_padding(self), app.click()
            on_text_validate: root.check_username(self)

<TeamName>:
    text_size: self.size

<CheckButton>:
    size_hint_y: None
    size_hint_x: None
    height: 24
    width: 24
    background_normal: "button-before-check.png"
    background_down: "button-after-check-2.png"
    on_press: root.add_remove_team(), app.click()

<ButtonNew>:
    background_normal: "button-before-press.png"
    background_down: "button-after-press.png"
    border: 20, 20, 20, 20

<HomeScreen>:
    app: app
    bar: bar
    pos_hint_x: .03
    grid: layout
    BoxLayout:
        orientation: 'horizontal'
        size_hint: 1, 1
        height: 50
        width: 800
        pos: 0, 480 - self.height
        id: bar
        cols: 4
        ButtonNew:
            text: "Home"
            on_press: app.click()
        ButtonNew:
            text: "Preferences"
            on_press: app.set_screen("team_selection"), app.click()
        ButtonNew:
            text: "About"
            on_press: app.click()
        ButtonNew:
            text: "Exit"
            on_press: app.click(), exit()
    ScrollView:
        size_hint: 1, None
        size: 800, 480 - bar.height
        GridLayout:
            id: layout
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            Label:
                height: 15
                size_hint_y: None


<TeamSelectionScreen>:
    layout: layout
    bar: bar
    pos_hint_x: .03
    GridLayout:
        pos: 0, 480 - self.height
        id: bar
        size_hint: 1, 1
        spacing: 10
        width: 800
        height: 50
        cols: 2
        Label:
            text: "Pick the teams you would like to follow"
            bold: True
            size_hint_x: None
            width: 0.7 * 800
        ButtonNew:
            text: "Done"
            on_press: app.end_team_selection_screen(root.selected_teams), app.click()

    ScrollView:
        size_hint: 1, None
        size: 800, 480 - bar.height
        GridLayout:
            padding: 20, 0
            width: 800
            id: layout
            cols: 2
            spacing: 20
            size_hint_y: None
            height: self.minimum_height


<GameLabel@Label>:
    canvas:
        Color:
            rgb: 0, 1, 0
        Rectangle:
            pos: self.pos
            size: self.width, 2
        Rectangle:
            pos: self.x, self.y + self.height
            size: self.width, 2
        Rectangle:
            pos: self.pos
            size: 2, self.height
        Rectangle:
            pos: self.x + self.width - 2, self.y
            size: 2, self.height
    ''')


class TeamName(Label):
    pass


class ButtonNew(Button):
    pass


class GameLabel(Label):
    pass


class HomeScreen(ScreenNew):

    def __init__(self, app, **kwargs):
        """Set the class's attributes."""
        super(HomeScreen, self).__init__(**kwargs)
        self.__game_labels = []
        self.__app = app

    def update(self):
        """Update the home screen according to the user's live updates."""
        self.grid.add_widget(Label(
            text="Loading...", height=50, size_hint_y=None))
        # get the finished, live and future matches of the user
        finished, live, future = self.app.user.get_games_categorized()
        self.refresh_screen(finished, live, future)
        while True:
            while self.app.screen == "home":
                new_games, ended_games, new_goals_games, updated = \
                    self.app.user.get_changes_categorized()
                # if only the minutes changed, present the updated
                if not (new_games or ended_games or new_goals_games):
                    for i in xrange(len(updated)):
                        if updated[i]["time"] != live[i]["time"]:
                            self.change_minutes(updated)
                            break
                else:
                    # check if the changes working(not necessary)
                    for game in ended_games:
                        finished.append(game)
                        # present on screen!
                    for game in new_games:
                        future = [future_game for future_game in future
                                  if future_game[HOME] !=
                                  game[HOME] or future_game["date"] !=
                                  datetime.datetime.today()]
                        # present on screen!
                    for game in new_goals_games:
                        print "present on screen!"
                    # update the screen according to the changes
                    self.refresh_screen(finished, updated, future)
                live = updated

    def add_game(self, game, type_time):
        """Present a live game on the screen.


        Receives:
            game - A dictionary that contains the game information.
        """
        # present the minute
        time_label = GameLabel(text=str(game["%s" % type_time]),
                               height=30, size_hint_y=None)
        self.grid.add_widget(time_label)
        # present the score and teams' names
        label = GameLabel(text="{0:>33}{1:11}{2:<5}{3:<5}{4:<11}{5:<6}".format(
            game[HOME], " ", game[HOME_GOALS],
            "-", game[AWAY_GOALS], game[AWAY]),
            font_name="Inconsolata-Bold.ttf", padding_x=0,
            height=25, width=480, size_hint_y=None)
        label.bind(size=label.setter("text_size"))
        self.grid.add_widget(label)
        self.grid.add_widget(Label(height=50, size_hint_y=None))
        self.__game_labels.append(time_label)

    def change_minutes(self, live):
        """Change the minutes of the live games.


        Receives:
            live - A list of dictionaries that contains the live games.
        """
        for i in xrange(len(live)):
            self.__game_labels[i].text = live[i]["time"]
            self.__game_labels[i].texture_update()

    def refresh_screen(self, finished, live, future):
        """Clear the screen and present the updated information.


        Receives:
            live - A list of dictionaries that contains the live games.
        """
        self.grid.clear_widgets()
        self.grid.add_widget(Label(height=15, size_hint_y=None))
        # if there are no live games, print a message
        if live or future or finished:
            self.grid.add_widget(Label(
                text="Finished matches", height=30, size_hint_y=None))
            for finished_game in finished:
                finished_game[HOME] = \
                    self.__app.special_names(finished_game[HOME])
                finished_game[AWAY] = \
                    self.__app.special_names(finished_game[AWAY])
                self.add_game(finished_game, "date")
            self.grid.add_widget(Label(
                text="Live matches", height=30, size_hint_y=None))
            for live_game in live:
                live_game[HOME] = self.__app.special_names(live_game[HOME])
                live_game[AWAY] = self.__app.special_names(live[AWAY])
                self.add_game(live_game, "time")
            self.grid.add_widget(Label(
                text="Future matches", height=30, size_hint_y=None))
            for future_game in future:
                future_game[HOME] = self.__app.special_names(future_game[HOME])
                future_game[AWAY] = self.__app.special_names(future_game[AWAY])
                self.add_game(future_game, "date")
        else:
            self.grid.add_widget(Label(
                text="There are currently no live games for your teams"))


class CheckButton(ToggleButton):
    def __init__(self, team, root, **kwargs):
        """Set the class's attributes."""
        super(CheckButton, self).__init__(**kwargs)
        self.__team = team
        self.__root = root

    def add_remove_team(self):
        self.__root.add_remove_team(self.__team)


class TeamSelectionScreen(ScreenNew):
    def __init__(self, app, teams, **kwargs):
        """Set the class's attributes."""
        super(TeamSelectionScreen, self).__init__(**kwargs)
        self.__selected_teams = []
        self.__app = app
        # special team names
        for team in teams:
            show_team = self.__app.special_names(team)
            self.layout.add_widget(CheckButton(team, self))
            self.layout.add_widget(TeamName(text=show_team))

    @property
    def selected_teams(self):
        return self.__selected_teams

    def add_remove_team(self, team):
        """If a button is pressed, add/remove the team that the button points on.


        Receives:
            team - A string that contains the team
                   that the pressed button points on.
        """
        if team in self.__selected_teams:
            self.__selected_teams.remove(team)
        else:
            self.__selected_teams.append(team)

        print self.__selected_teams


class LoginScreen(Screen):
    def __init__(self, app, **kwargs):
        """Set the class's attributes."""
        super(LoginScreen, self).__init__(**kwargs)
        self.__app = app

    @staticmethod
    def update_input_padding(text_input):
        """Set the text to the middle of the screen."""
        if text_input.text != "":
            text_width = text_input._get_text_width(
                text_input.text,
                text_input.tab_width,
                text_input._label_cached
            )
            text_input.padding_x = (text_input.width - text_width) / 2
        else:
            # manually calculated padding
            text_input.padding_x = 143

    def check_username(self, text_input):
        """Get the user's input"""
        if text_input.text == "":
            text_input.hint_text = "Please enter something!"
            # manually calculated padding
            text_input.padding_x = 118
        else:
            self.__app.update_username(text_input.text)


class ScreenManagerNew(ScreenManager):
    def __init__(self, app, teams, **kwargs):
        """Set the class's attributes."""
        Window.size = (800, 480)
        super(ScreenManagerNew, self).__init__(**kwargs)
        self.__app = app
        self.home_screen = HomeScreen(app, name="home")
        self.add_widget(LoginScreen(app, name="login"))
        self.add_widget(TeamSelectionScreen(app, teams, name="team_selection"))
        self.add_widget(self.home_screen)
