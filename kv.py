"""
Program Name: kv
By: Omer Alon
Date: 02/04/17
Program Version: 1.0.0
"""
import time
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from screen import ScreenNew, ScreenManager
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.uix.button import Button
import datetime
from team_codes import *


Builder.load_file("kivy.kv")


TEXT_ORGANIZE = "{0:>33}{1:11}{2:<5}{3:<5}{4:<11}{5:<6}"


class AlertScreen(ScreenNew):

    def __init__(self, goal_for, score, background, **kwargs):
        super(AlertScreen, self).__init__(**kwargs)
        self.text_label0.text = goal_for
        self.text_label1.text = score
        self.button.background_normal = background
        self.button.background_down = background


class GoalScreen(AlertScreen):

    def __init__(self, match, **kwargs):
        """Set the class's attributes."""
        # check which team scored the goal
        goal_for = match[HOME] if match["homeGoal"] else match[AWAY]
        score = "{:<45}{} - {}{:>45}".format(
            match[HOME], match[HOME_GOALS], match[AWAY_GOALS], match[AWAY])
        super(GoalScreen, self).__init__(
            "goal for %s" % goal_for, score, "goal.png", **kwargs)
        # unique name to avoid confusing the screen manager
        self.name = match[TIME] + match[HOME] + match[AWAY]


class MatchStartScreen(AlertScreen):

    def __init__(self, match, **kwargs):
        score = "{:<45}{} - {}{:>45}".format(
            match[HOME], match[HOME_GOALS], match[AWAY_GOALS], match[AWAY])
        super(MatchStartScreen, self).__init__(
            "", score, "started.png", **kwargs)
        self.name = "started" + match[DATE] + match[HOME] + match[AWAY]


class MatchEndScreen(AlertScreen):

    def __init__(self, match, **kwargs):
        score = "{:<45}{} - {}{:>45}".format(
            match[HOME], match[HOME_GOALS], match[AWAY_GOALS], match[AWAY])
        super(MatchEndScreen, self).__init__(
            "", score, "finished.png", **kwargs)
        self.name = "finished" + match[DATE] + match[HOME] + match[AWAY]


class TeamName(Label):
    pass


class ButtonNew(Button):
    pass


class MatchLabel(Label):
    pass


class OpeningScreen(Screen):
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
        self.__user_place = "Live matches"
        self.__match_labels = []
        self.__app = app

    def update(self):
        """Update the home screen according to the user's live updates."""
        self.grid.add_widget(Label(
            text=self.LOADING, height=50, size_hint_y=None, font_size=32))
        # get the finished, live and future matches of the user
        self.__finished, bla, self.__future =\
            self.app.user.get_matches_categorized()
        self.__live = [{"homeTeamName": "Liverpool", "awayTeamName": "Manchester United", "homeGoal": True, "awayGoal": False, "time": "73'", "goalsHomeTeam": 4, "goalsAwayTeam": 0}]
        self.show_live()
        self.bar.disabled = False
        while True:
            if True:
                time.sleep(5)
                self.__live = [{"homeTeamName": "Liverpool", "awayTeamName": "Manchester United", "homeGoal": True, "awayGoal": False, "time": "74'", "goalsHomeTeam": 5, "goalsAwayTeam": 0}]
                self.change_minutes(self.__live)
                time.sleep(5)
                self.__live = [{"homeTeamName": "Liverpool", "awayTeamName": "Manchester United", "homeGoal": True, "awayGoal": False, "time": "73'", "goalsHomeTeam": 5, "goalsAwayTeam": 0}]
                self.__app.audio("goal-sound.mp3")
                self.__app.add_and_switch_screen(GoalScreen(self.__live[0]))
            else:
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
                        self.__app.audio("final-whistle.mp3")
                        # present the finished match message
                        self.__app.add_and_switch_screen(MatchEndScreen(match))
                    for match in new_matches:
                        self.__future = [future_match for future_match in
                                         self.__future if future_match[HOME] !=
                                         match[HOME] or future_match[DATE] !=
                                         datetime.datetime.today()]
                        self.__app.audio("whistle.mp3")
                        # present the new match message
                        self.__app.add_and_switch_screen(MatchStartScreen(match))
                    for match in new_goals_matches:
                        self.__app.audio("goal-sound.mp3")
                        # present the goal message
                        self.__app.add_and_switch_screen(GoalScreen(match))
                    self.__live = updated
                    # update the screen according to the changes
                    if self.__user_place == "Live matches":
                        self.show_live()
                    elif self.__user_place == "Finished matches":
                        self.show_finished()
                    else:
                        self.show_future()

    def show_matches(self, to_show, type_time):
        """Clear the screen and present the given information.


        Receives:
            to_show - A list of dictionaries that contains the matches to show.
            type_time - A string that contains the word "date"/"time".
        """
        # clear the screen
        self.grid.clear_widgets()
        self.grid.add_widget(Label(height=15, size_hint_y=None))
        if to_show:
            self.grid.add_widget(Label(
                text=self.__user_place, height=40,
                size_hint_y=None, font_size=24))
            for match in to_show:
                match[HOME] = self.__app.special_names(match[HOME])
                match[AWAY] = self.__app.special_names(match[AWAY])
                self.add_match(match, type_time)
        elif self.__user_place == "Live matches":
            self.grid.add_widget(Label(text=self.NO_LIVE_MATCHES, height=40,
                                       size_hint_y=None, font_size=32))
        elif self.__user_place == "Finished matches":
            self.grid.add_widget(Label(text=self.NO_FINISHED_MATCHES,
                                       height=40, size_hint_y=None,
                                       font_size=32))
        else:
            self.grid.add_widget(Label(text=self.NO_FUTURE_MATCHES, height=40,
                                       size_hint_y=None, font_size=32))

    def show_live(self):
        """Present the live matches on the screen."""
        self.__user_place = "Live matches"
        self.show_matches(self.__live, TIME)

    def show_finished(self):
        """Present the finished matches on the screen."""
        self.__user_place = "Finished matches"
        self.show_matches(self.__finished, DATE)

    def show_future(self):
        """Present the future matches on the screen."""
        self.__user_place = "Future matches"
        self.show_matches(self.__future, DATE)

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
        label = MatchLabel(text=TEXT_ORGANIZE.format(
            match[HOME], " ", match[HOME_GOALS], "-",
            match[AWAY_GOALS], match[AWAY]), font_name=self.FONT,
            padding_x=0, height=25, width=480, size_hint_y=None)
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
        """Get the selected teams."""
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
                text_input._label_cached)
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
        self.opening_screen = OpeningScreen()
        self.add_widget(self.opening_screen)
        self.home_screen = HomeScreen(app, name="home")
        self.add_widget(LoginScreen(app, name="login"))
        self.add_widget(TeamSelectionScreen(app, teams, name="team_selection"))
        self.add_widget(self.home_screen)
