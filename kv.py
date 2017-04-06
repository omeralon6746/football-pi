from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton

Builder.load_string('''

<LoginScreen>:
    RelativeLayout:
        Label:
            text: "Football Pi"
            pos: 0, 200
            font_size: "64sp"
        TextInput:
            pos_hint: {'x': 0.25, 'y': 0.5}
            size_hint: 0.5, 0.07
            multiline: False
            hint_text: "Enter Your Name"
            padding_x: 150
            id: username
            on_text: root.update_input_padding(self)
            on_text_validate: root.check_username(self)

<TeamSelectionScreen>:
    RelativeLayout:
        size_hint: 0.03, 0.05
        ToggleButton:
            background_normal: 'button-before-check.png'
            background_down: 'button-after-check-2.png'
            pos: 10, 420
        # Button:
        #     text: 'Next'
        #     on_press: root.manager.current = 'login'
''')


class TeamSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(TeamSelectionScreen, self).__init__(**kwargs)
        # self.add_widget(CheckBox(size_hint=(0.06, 0.06)))


class LoginScreen(Screen):
    def __init__(self, app, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.__app = app

    @staticmethod
    def update_input_padding(text_input):
        if text_input.text != '':
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
        if text_input.text == '':
            text_input.hint_text = "Please enter something!"
            # manually calculated padding
            text_input.padding_x = 118
        else:
            self.__app.update_username(text_input.text)


class ScreenManagerNew(ScreenManager):
    def __init__(self, app, **kwargs):
        super(ScreenManagerNew, self).__init__(**kwargs)
        self.__app = app
        self.add_widget(LoginScreen(app, name='login'))
        self.add_widget(TeamSelectionScreen(name='team_selection'))
