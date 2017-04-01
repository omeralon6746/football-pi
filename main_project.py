"""
Program Name: main_project
By: Omer Alon
Date: 08/01/17
Program Version: 1.0.0
"""
import information_server


def menu(file_name):
    """Represent the menu of the project.


    Receives:
        file_name - string that contains the file's name of the current user.
    """
    pass


def add_request(request, file_name):
    """Add to the user's file the requested information from the user.


    Receives:
        file_name - string that contains the file's name of the current user.
        request - string that contains the user's requested information.
    """
    pass


def pick_leagues():
    """Let the user pick the teams that he wants to follow.


    Returns:
        teams - the list of the chosen teams.
    """
    pass


def pick_teams():
    """Let the user pick the teams that he wants to follow.


    Returns:
        teams - the list of the chosen teams.
    """
    pass


def create_user_data(name):
    """Create a text file with the user's name.


    Receives:
        name - string that contains the user's name.
    """
    pass


def handle_new_user(username):
    """Set the new user settings(teams, leagues).


    Receives:
        username - string that contains the user's name.
    """
    create_user_data(username)
    teams = pick_teams()
    for team in teams:
        add_request(team, username)
    leagues = pick_leagues()
    for league in leagues:
        add_request(league, username)

    pass


def check_username(username):
    """Check if the username already exists in one of the saves.


    Receives:
        username - string that contains the user's name that was entered by the user.

    Returns:
        check_exist - bool that indicates if the username exists or not.
    """
    pass


def log_in_page():
    """Create the log in page.

    Returns:
        username - string that contains the user's name.
    """
    username = raw_input()
    return username


def main():
    username = log_in_page()
    check_exist = check_username(username)
    if check_exist:
        menu(username)
    else:
        handle_new_user(username)


if __name__ == '__main__':
    main()