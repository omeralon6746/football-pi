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
            on_text: root.update_input_padding(self), app.audio(app.CLICK_SOUND)
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
    on_press: root.add_remove_team(), app.audio(app.CLICK_SOUND)

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
            text: "Live"
            on_press: app.audio(app.CLICK_SOUND), root.show_live()
        ButtonNew:
            text: "Future Matches"
            on_press: app.audio(app.CLICK_SOUND), root.show_future()
        ButtonNew:
            text: "Finished Matches"
            on_press: app.audio(app.CLICK_SOUND), root.show_finished()
        ButtonNew:
            text: "About"
            on_press: app.audio(app.CLICK_SOUND)
        ButtonNew:
            text: "Exit"
            on_press: app.audio(app.CLICK_SOUND), exit()
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
            on_press: app.end_team_selection_screen(root.selected_teams), app.audio(app.CLICK_SOUND)

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


<MatchLabel@Label>:
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


class MatchLabel(Label):
    pass


class HomeScreen(ScreenNew):
    NO_LIVE_MATCHES = "There are currently no live matches for your teams"
    NO_FUTURE_MATCHES = "There are no future matches for your teams"
    NO_FINISHED_MATCHES = "There are no finished matches for your teams"
    FONT = "Inconsolata-Bold.ttf"
    LOADING = "Loading..."

    def __init__(self, app, **kwargs):
        """Set the class's attributes."""
        super(HomeScreen, self).__init__(**kwargs)
        self.__finished = []
        self.__live = []
        self.__future = []
        self.__user_place = "live"
        self.__match_labels = []
        self.__app = app

    def update(self):
        """Update the home screen according to the user's live updates."""
        self.grid.add_widget(Label(
            text=self.LOADING, height=50, size_hint_y=None))
        # get the finished, live and future matches of the user
        self.__finished, self.__live, self.__future =\
            self.app.user.get_matches_categorized()
        self.show_live()
        while True:
            new_matches, ended_matches, new_goals_matches, updated = \
                self.app.user.get_changes_categorized()
            # if only the minutes changed, present the updated
            if not (new_matches or ended_matches or new_goals_matches):
                for i in xrange(len(updated)):
                    if updated[i][TIME] != self.__live[i][TIME]:
                        self.change_minutes(updated)
                        break
                self.__live = updated
            else:
                for match in ended_matches:
                    self.__finished.append(match)
                    # present on screen!
                for match in new_matches:
                    self.__future = [future_match for future_match in
                                     self.__future if future_match[HOME] !=
                                     match[HOME] or future_match[DATE] !=
                                     datetime.datetime.today()]
                    # present on screen!
                for match in new_goals_matches:
                    print "present on screen!"
                self.__live = updated
                # update the screen according to the changes
                if self.__user_place == "live":
                    self.show_live()
                elif self.__user_place == "finished":
                    self.show_finished()
                else:
                    self.show_future()

    def show_games(self, to_show, type_time):
        """Clear the screen and present the given information.


        Receives:
            to_show - A list of dictionaries that contains the matches to show.
            type_time - A string that contains the word "date"/"time".
        """
        # clear the screen
        self.grid.clear_widgets()
        self.grid.add_widget(Label(height=15, size_hint_y=None))
        if to_show:
            for match in to_show:
                match[HOME] = self.__app.special_names(match[HOME])
                match[AWAY] = self.__app.special_names(match[AWAY])
                self.add_match(match, type_time)
        elif self.__user_place == "live":
            self.grid.add_widget(Label(text=self.NO_LIVE_MATCHES))
        elif self.__user_place == "finished":
            self.grid.add_widget(Label(text=self.NO_FINISHED_MATCHES))
        else:
            self.grid.add_widget(Label(text=self.NO_FUTURE_MATCHES))

    def show_live(self):
        self.__user_place = "live"
        self.show_games(self.__live, TIME)

    def show_finished(self):
        self.__user_place = "finished"
        self.show_games(self.__finished, DATE)

    def show_future(self):
        self.__user_place = "future"
        self.show_games(self.__future, DATE)

    def add_match(self, match, type_time):
        """Present a live match on the screen.


        Receives:
            match - A dictionary that contains the match information.
            type_time - A string that contains the word "date"/"time".
        """
        # present the minute
        time_label = MatchLabel(text=str(match["%s" % type_time]),
                                height=30, size_hint_y=None)
        self.grid.add_widget(time_label)
        # present the score and teams' names
        label = MatchLabel(text="{0:>33}{1:11}{2:<5}{3:<5}{4:<11}{5:<6}".format(
            match[HOME], " ", match[HOME_GOALS],
            "-", match[AWAY_GOALS], match[AWAY]),
            font_name=self.FONT, padding_x=0,
            height=25, width=480, size_hint_y=None)
        label.bind(size=label.setter("text_size"))
        self.grid.add_widget(label)
        self.grid.add_widget(Label(height=50, size_hint_y=None))
        self.__match_labels.append(time_label)

    def change_minutes(self, live):
        """Change the minutes of the live matches.


        Receives:
            live - A list of dictionaries that contains the live matches.
        """
        for i in xrange(len(live)):
            self.__match_labels[i].text = live[i][TIME]
            self.__match_labels[i].texture_update()


class CheckButton(ToggleButton):
    def __init__(self, team, root, **kwargs):
        """Set the class's attributes."""
        super(CheckButton, self).__init__(**kwargs)
        self.__team = team
        self.__root = root

    def add_remove_team(self):
        """if a button was pressed, add the team that the button belongs to
           or remove the team in case the button was already pressed."""
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
        """if a button was pressed, add the team that the button belongs to
           or remove the team in case the button was already pressed.


        Receives:
            team - A string that contains the team
                   that the pressed button points on.
        """
        if team in self.__selected_teams:
            self.__selected_teams.remove(team)
        else:
            self.__selected_teams.append(team)


class LoginScreen(Screen):
    EMPTY_NAME_MESSAGE = "Please enter something!"

    def __init__(self, app, **kwargs):
        """Set the class's attributes."""
        super(LoginScreen, self).__init__(**kwargs)
        self.__app = app

    @staticmethod
    def update_input_padding(text_input):
        """Set the text to the middle of the screen.


        Receives:
            text_input - A string that contains the user's input.
        """
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

    def check_username(self, username):
        """Update the username.


        Receives:
            text_input - A string that contains the user's name.
        """
        # if the user didn't enter nothing, present a message
        if username.text == "":
            username.hint_text = self.EMPTY_NAME_MESSAGE
            # manually calculated padding
            username.padding_x = 118
        else:
            self.__app.update_username(username.text)


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
