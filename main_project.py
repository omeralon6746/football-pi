"""
Program Name: main_project
By: Omer Alon
Date: 08/03/17
Program Version: 1.0.0
"""
import information_server
import user


def show_updates(updates):
    """Show the updates that relevant to the user.


    Receives:
        updates - A list of the user's updates that weren't showed yet.
    """


def get_user_updates(user_details, updates):
    """Check if the user's league or teams are on the updates that was found.


    Receives:
        user_details - A list of two lists that contains the teams and the leagues.
        updates - A list of lists that contains the updates on the live games.

    Returns:
        user_updates - A list of tuples that contains the updates on the
        live games that relevant to the user's choices.
    """


def get_user_games(user_details, live_games):
    """Check if the user's leagues or teams are on the live games.


    Receives:
        user_details - A list of two lists that contains the teams and the leagues.
        live_games - A list of dictionaries, each containing information
        about the currently live games.

    Returns:
        user_live_games - A list of dictionaries, each containing information
        about the currently live games of the user.
    """
    pass


def menu(current_user):
    """Represent the menu of the project.


    Receives:
        file_name - A string that contains the file's name of the current user.
    """
    exit_request = False
    info = information_server.InformationSource()
    while not exit_request:
        live_games = info.get_live_games()
        user_live_games = get_user_games(current_user.get_details(), live_games)
        updates = info.get_changes()
        user_updates = get_user_updates(current_user.get_details(), updates)
        show_updates(user_updates)
        user_updates = None


def pick_leagues():
    """Let the user pick the leagues that he wants to follow.


    Returns:
        leagues - A list of the chosen leagues.
    """
    pass


def pick_teams():
    """Let the user pick the teams that he wants to follow.


    Returns:
        teams - A list of the chosen teams.
    """
    pass


def fill_details(current_user, new_user=True):
    """Set the user's details(teams and leagues).


    Receives:
        username - A string that contains the user's name.
        new_user - A bool that indicates if the username is new or not.
    """
    teams = pick_teams()
    current_user.set_teams(teams)
    leagues = pick_leagues()
    current_user.set_leagues(leagues)
    current_user.create_user_data(new_user)


def check_username(username):
    """Check if the username already exists in one of the saves.


    Receives:
        username - A string that contains the user's name that was entered by the user.

    Returns:
        check_exist - A bool that indicates if the username exists or not.
    """
    pass


def log_in_page():
    """Create the log in page.

    Returns:
        username - A string that contains the user's name.
    """
    username = raw_input()
    return username


def main():
    username = log_in_page()
    current_user = user.User(username)
    check_exist = check_username(username)
    if check_exist:
        current_user.restore_data()
        menu(current_user)
    else:
        fill_details(current_user)


if __name__ == '__main__':
    main()