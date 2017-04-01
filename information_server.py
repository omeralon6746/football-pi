"""
Program Name: information_server
By: Omer Alon
Date: 08/01/17
Program Version: 1.0.0
"""
import requests


class InformationSource(object):
    LIVE_RESULTS_API = "http://soccer-cli.appspot.com/"
    OTHER_INFO_API = "http://api.football-data.org/v1/"

    def __init__(self):
        self.__last_scores = None

    def last_scores(self):
        return self.__last_scores

    def update_scores(self):
        live = self.get_live_games()

        last_home_teams = [game['homeTeamName'] for game in self.__last_scores]
        new_home_teams = [game['homeTeamName'] for game in live]
        # get new games
        new = [game for game in live if game['homeTeamName']
               not in last_home_teams]

        # get finished games
        finished = [game for game in self.__last_scores if game['homeTeamName']
                    not in new_home_teams]

        # get new goals
        new_goals = []
        for game in self.__last_scores:
            for live_game in live:
                if live_game['homeTeamName'] == game['homeTeamName']:
                    if live_game['goalsHomeTeam'] != game['goalsHomeTeam'] \
                            or live_game['goalsAwayTeam'] != game['goalsAwayTeam']:
                        new_goals.append(((game['homeTeamName'],
                                           live_game['goalsHomeTeam'] - game['goalsHomeTeam']),
                                        (game['homeTeamName'],
                                         live_game['goalsAwayTeam'] - game['goalsAwayTeam'])))

        new_goals += [((game['homeTeamName'], game['goalsHomeTeam'])(game['awayTeamName'], game['goalsAwayTeam']))
                      for game in new if game['goalsAwayTeam'] != 0
                      or game['goalsAwaysTeam'] != 0]

    def get_live_games(self):
        """Get the live games.


        Returns:
            live - A list of dictionaries, each containing information
            about the game, in the following format:
            {'league': -,
            'goalsAwayTeam': -,
            'time': -,
            'homeTeamName': -,
            'awayTeamName': -,
            'goalsHomeTeam': -
            }
        """
        try:
            games = requests.get(self.LIVE_RESULTS_API).json()
        except ValueError:
            return self.get_live_games()
        # filter the live games
        live = [game for game in games['games'] if -1 not in game.values()]
        return live

    def get_team_code(team):
        """Return the team's code.


        Receives:
            team - string that contains the team's name(for example: 'Barcelona').

        Returns:
            code - string that contains the team's code(for example: 'FCB').
        """
    pass


def get_team_league(team):
    pass


def main():
    i = InformationSource()
    print i.get_live_games()


if __name__ == '__main__':
    main()