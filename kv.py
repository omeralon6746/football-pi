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
            on_text: root.update_input_padding(self)
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
    on_press: root.add_remove_team()

<ButtonNew>:
    background_normal: "button-before-press.png"
    background_down: "button-after-press.png"
    border: 20, 20, 20, 20

<HomeScreen>:
    app: app
    layout: layout
    view: view
    bar: bar
    pos_hint_x: .03
    ScrollView:
        id: view
        pos_hint_x: .03
        size_hint: 1, None
        GridLayout:
            id: layout
            cols: 1
            size_hint_y: None
            spacing: 35
            GridLayout:
                id: bar
                cols: 4
                ButtonNew:
                    text: "Home"
                ButtonNew:
                    text: "Preferences"
                ButtonNew:
                    text: "About"
                ButtonNew:
                    text: "Exit"


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
            on_press: app.end_team_selection_screen(root.selected_teams)

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
    ''')


# to add class
class TeamName(Label):
    pass


class ButtonNew(Button):
    pass


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        # cause scroll to work
        self.layout.bind(minimum_height=self.layout.setter("height"))
        self.bar.bind(minimum_height=self.bar.setter("height"))
        self.view.size = (Window.width, Window.height)

    def update(self):
        finished, live, future = self.app.user.get_games_categorized()
        while True:
            new_games, ended_games, new_goals_games = self.app.user.get_changes_categorized()
            for game in ended_games:
                finished.append(game)
                live = [live_game for live_game in live if live_game["homeTeamName"] != game["homeTeamName"]]
                if ended_games:
                    print finished
                    print live
                    print future
            for game in new_games:
                live.append(game)
                future = [future_game for future_game in future if future_game["homeTeamName"] != game["homeTeamName"] and future_game["date"] == datetime.datetime.today()]
                print "new game: %s vs %s" % (game["homeTeamName"], game["awayTeamName"])
                print live
                print future
            for game in new_goals_games:
                for live_game in live:
                    if live_game["homeTeamName"] == game["homeTeamName"]:
                        live_game["goalsHomeTeam"] = game["goalsHomeTeam"]
                        live_game["goalsAwayTeam"] = game["goalsAwayTeam"]
                        print "goal! for %s or %s, score: %d - %d" % (live_game["homeTeamName"], live_game["awayTeamName"], live_game["goalsHomeTeam"], live_game["goalsAwayTeam"])
                        print live
                        print future

class CheckButton(ToggleButton):
    def __init__(self, team, root, **kwargs):
        super(CheckButton, self).__init__(**kwargs)
        self.__team = team
        self.__root = root

    def add_remove_team(self):
        self.__root.add_remove_team(self.__team)


class TeamSelectionScreen(ScreenNew):
    def __init__(self, teams, **kwargs):
        super(TeamSelectionScreen, self).__init__(**kwargs)
        self.__selected_teams = []
        
        for team in teams:
            if "Alav" in team:
                show_team = "Deportivo Alav\xc3\xa9s"
            elif "Deportivo La" in team:
                show_team = "Deportivo La Coruna"
            else:
                show_team = team
            self.layout.add_widget(CheckButton(team, self))
            self.layout.add_widget(TeamName(text=show_team))

    @property
    def selected_teams(self):
        return self.__selected_teams

    def add_remove_team(self, team):
        if team in self.__selected_teams:
            self.__selected_teams.remove(team)
        else:
            self.__selected_teams.append(team)

        print self.__selected_teams


class LoginScreen(Screen):
    def __init__(self, app, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.__app = app

    @staticmethod
    def update_input_padding(text_input):
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
        if text_input.text == "":
            text_input.hint_text = "Please enter something!"
            # manually calculated padding
            text_input.padding_x = 118
        else:
            self.__app.update_username(text_input.text)


class ScreenManagerNew(ScreenManager):
    def __init__(self, app, teams, **kwargs):
        Window.size = (800, 480)
        super(ScreenManagerNew, self).__init__(**kwargs)
        self.__app = app
        self.home_screen = HomeScreen(name="home")
        self.add_widget(LoginScreen(app, name="login"))
        self.add_widget(TeamSelectionScreen(teams, name="team_selection"))
        self.add_widget(self.home_screen)
