"""
Program Name: changes
By: Omer Alon
Date: 01/04/17
Program Version: 1.0.0
"""


from team_codes import *


class Changes(object):

    def __init__(self, updated_matches, old_matches):
        """Set the class's attributes."""
        self.__updated_matches = updated_matches
        self.__old_matches = old_matches

    def find_new_matches(self):
        """Find new matches that started.


        Returns:
            new_matches - A list of dictionaries that contains
            the new matches that started.
        """
        last_home_teams = [match[HOME] for match in self.__old_matches]
        # get new matches
        new_matches = [match for match in self.__updated_matches if match[HOME]
                       not in last_home_teams]
        return new_matches

    def find_finished_matches(self):
        """Find the matches that finished.


        Returns:
            finished - A list of dictionaries that contains
            the matches that finished
        """
        new_home_teams = [match[HOME] for match in self.__updated_matches]
        # get finished matches
        finished = [match for match in self.__old_matches if match[HOME]
                    not in new_home_teams]
        return finished

    def find_new_goals(self):
        """Find new goals on the live matches.


        Returns:
            new_matches - A list of tuples that contains
            the new goals on the live matches.
        """
        index = 0
        new_goals = []
        for match in self.__old_matches:
            for live_match in self.__updated_matches:
                if live_match[HOME] == match[HOME]:
                    if live_match[HOME_GOALS] != match[HOME_GOALS]:
                        new_goals.append(live_match)
                        # add "homeGoal" and "awayGoal" labels in order
                        # to know which team has scored
                        new_goals[index]["homeGoal"] = True
                        if live_match[AWAY_GOALS] != match[AWAY_GOALS]:
                            new_goals[index]["awayGoal"] = True
                        else:
                            new_goals[index]["awayGoal"] = False
                        index += 1
                    elif live_match[AWAY_GOALS] != match[AWAY_GOALS]:
                        new_goals.append(live_match)
                        new_goals[index]["awayGoal"] = True
                        new_goals[index]["homeGoal"] = False
                        index += 1
        return new_goals

    def find_all_changes(self):
        """Find updates on new matches, finished matches and goals.


        Returns:
            changes - A list of lists that contains the new updates.
        """
        return [self.find_new_matches(),
                self.find_finished_matches(), self.find_new_goals()]
