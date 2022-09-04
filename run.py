import os
import time
import gspread
from google.oauth2.service_account import Credentials
from pyfiglet import figlet_format
from termcolor import colored

SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('smarticus_high_scores')


def main_screen():

    # Present the user with the name of the game and three options.
    #1 lets the user start the game
    #2 lets the user know how to play
    #3 lets the user view the top 10 high scores

    clear_terminal()
    print(
        colored(
            figlet_format(
                'Welcome to Smarticus', font='bulbhead', justify='center'
            ),
            'cyan',
        )
    )
    print('\n' * 2)
    print(colored(' ' * 30 + '1 - Play Game', 'yellow'))
    print(colored(' ' * 30 + '2 - How to play', 'yellow'))
    print(colored(' ' * 30 + '3 - High Scores Table', 'yellow'))
    print('\n' * 2)
    num = input(' ' * 22 + 'Please enter one of the three options: ').strip()
    if num == '1':
        play()
    elif num == '2':
        how_to()
    elif num == '3':
        high_scores()
    else:
        # Input validation
        clear_terminal()
        print('\n' * 6)
        print(colored(figlet_format('CHOOSE  A VALID  NUMBER',
              font='bubble', justify='center'), 'red'))
        time.sleep(2)
        main_screen()


def clear_terminal():
    # clear terminal window depending on os
    os.system('cls||clear')


#def play():
    # Start the game
    

#def get_question():
    # Get the question from the API
    

def how_to():
    # Explains how to play the game

    clear_terminal()
    print(
        colored(
            figlet_format('How to Play', font='bulbhead', justify='center'),
            'cyan',
        )
    )
    print('\n' * 2)
    print(
        colored(
            ' ' * 5 + 
            '- You will be given 100 multiple choice questions listed as' + 
            'A, B, C, and D',
            'yellow',
        )
    )
    print(
        colored(
            ' ' * 5 + '- Answer the question by entering A, B, C, or D',
            'yellow',
        )
    )
    print(colored(' ' * 5 + '- Each correct answer is 10 points', 'yellow'))
    print(colored(' ' * 5 + '- Try and get on to the Leadboard', 'yellow'))
    print(
        colored(' ' * 5 + '- Answer incorrectly and it\'s game over', 'yellow')
    )
    print('\n' * 5)
    input(' ' * 22 + 'Press Enter to return to main screen ')
    main_screen()


def high_scores():
    # Create and Show the High Scores Leaderboard

    clear_terminal()
    print(
        colored(
            figlet_format(
                "Leaderboard", font="bulbhead", justify="center"
            ),
            "cyan",
        )
    )
    print("\n" * 1)
    high_scores_data = SHEET.worksheet("HS").get_all_values()

    """ Align High Scores when printed out """
    for i in range(10):
        if len(high_scores_data[0][i]) < 10:
            high_scores_data[0][i] = high_scores_data[0][i] + " " * (
                10 - len(high_scores_data[0][i])
            )
    """  Sort order of Leaderboard by score """
    high_scores_dict = dict(zip(high_scores_data[0], high_scores_data[1]))
    high_scores = sorted(
        high_scores_dict.items(), key=lambda item: int(item[1]), reverse=True
    )
    i = 1
    for value in high_scores:
        if i == 10:
            print(
                " " * 20 + str(i) + ".",
                str(value[0]) + "  -       High Score: " + str(value[1]),
            )
            i += 1
        else:
            print(
                " " * 20 + str(i) + ". ",
                str(value[0]) + "  -       High Score: " + str(value[1]),
            )
            i += 1
    print("\n" * 1)
    input(" " * 20 + "Press Enter to return to main screen ")
    main_screen()


#def check_score(score):
    # Check if player has made it into the Leaderboard 
    
    
main_screen()
