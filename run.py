import os
import time
import gspread
from google.oauth2.service_account import Credentials
from pyfiglet import figlet_format
from termcolor import colored
import requests
import random
import json
import html.parser

SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('smarticus_high_scores')
KEYS = ["A", "B", "C", "D"]


def main_screen():
    # Present the user with the name of the game and three options.
    # 1 lets the user start the game
    # 2 lets the user know how to play
    # 3 lets the user view the top 10 high scores

    clear_terminal()
    print(
        colored(
            figlet_format(
                'Welcome to', font='bulbhead', justify='center'
            ),
            'cyan',
        )
    )
    print(
        colored(
            figlet_format(
                'Smarticus', font='bulbhead', justify='center'
            ),
            'cyan',
        )
    )
    print('\n' * 2)
    print(colored(' ' * 30 + '1 - Play Game', 'yellow'))
    print(colored(' ' * 30 + '2 - How to play', 'yellow'))
    print(colored(' ' * 30 + '3 - High Scores Table', 'yellow'))
    print('\n' * 2)
    num = input(' ' * 22 + 'Please enter one of the three options: \n').strip()
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


def play():
    # Start the game

    score = 0
    for i in range(1, 101):
        clear_terminal()
        question_num = i
        print(
            colored(
                figlet_format(
                    f"Question {question_num}",
                    font="bulbhead",
                    justify="center",
                ),
                "cyan",
            )
        )
        print("\n" * 2)
        question, correct_answer, lettered_options = get_question()
        colored_question = colored(f"{question}", "yellow")
        print(f"{colored_question}".center(80))
        print("\n" * 1)
        for letter in KEYS:
            print(" " * 20 + letter + ": " + lettered_options[letter])
        print("\n" * 4)
        player_answer = ""
        while player_answer not in KEYS:
            player_answer = input(
                " " * 22 + "Please enter your answer A, B, C or D: \n"
            ).capitalize()
        if correct_answer == lettered_options[player_answer]:
            score += 1
            clear_terminal()
            print(
                colored(
                    figlet_format(
                        "Correct", font="bulbhead", justify="center"
                    ),
                    "green",
                )
            )
            print("\n" * 2)
            print(f"Score = {score}".center(80))
            print("\n" * 5)
            if i != 10:
                input("Press Enter to continue to next question\n".center(80))
            else:
                check_score(score)
        elif correct_answer != lettered_options[player_answer]:
            clear_terminal()
            print(
                colored(
                    figlet_format(
                        "Incorrect",
                        font="bulbhead",
                        justify="center",
                    ),
                    "red",
                )
            ) 
            print(
                colored(
                    figlet_format(
                        "Game Over",
                        font="bulbhead",
                        justify="center",
                    ),
                    "yellow",
                )
            )
            print("\n" * 2)
            print(f"Score = {score}".center(80))
            print("\n" * 5)
            input("Press Enter to see how you did\n".center(80))
            check_score(score)
        else:
            break


def get_question():
    # Get the question from the API

    trivia_API = requests.get(
        "https://opentdb.com/api.php?amount=1&type=multiple"
    )
    data = trivia_API.text
    parse_json = json.loads(data)
    question = html.parser.unescape(parse_json["results"][0]["question"])
    correct_answer = html.parser.unescape(
        parse_json["results"][0]["correct_answer"]
    )
    incorrect_answers = parse_json["results"][0]["incorrect_answers"]
    options = incorrect_answers.copy()
    converted_options = convert_ascii_list(options)
    converted_options.append(correct_answer)
    random.shuffle(converted_options)
    lettered_options = dict(zip(KEYS, converted_options))
    return question, correct_answer, lettered_options


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
            ' A, B, C, and D',
            'yellow',
        )
    )
    print(
        colored(
            ' ' * 5 + '- Answer the question by entering A, B, C, or D',
            'yellow',
        )
    )
    print(colored(' ' * 5 + '- Each correct answer is worth 1 point', 'yellow'))
    print(colored(' ' * 5 + '- Try and get on the Leadboard', 'yellow'))
    print(
        colored(' ' * 5 + '- Answer incorrectly and it\'s game over', 'yellow')
    )
    print('\n' * 5)
    input(' ' * 22 + 'Press Enter to return to main screen\n')
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

    #Align High Scores when printed out
    for i in range(10):
        if len(high_scores_data[0][i]) < 10:
            high_scores_data[0][i] = high_scores_data[0][i] + " " * (
                10 - len(high_scores_data[0][i])
            )
    #Sort order of Leaderboard by score
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
    input(" " * 22 + "Press Enter to return to main screen\n")
    main_screen()


def convert_ascii_list(list):
    # Translate html ascii characters
    converted = []
    for text in list:
        converted_text = html.parser.unescape(text)
        converted.append(converted_text)
    return converted


def check_score(score):
    # Check if player has made it onto the Leaderboard

    high_scores_data = SHEET.worksheet("HS").get_all_values()
    high_scores_dict = dict(zip(high_scores_data[0], high_scores_data[1]))
    scores = list(high_scores_dict.values())
    int_scores = [int(i) for i in scores]
    min_high_score = min(int_scores)
    if score > min_high_score:
        clear_terminal()

        # Remove lowest score from Leaderboard
        value = {
            i
            for i in high_scores_dict
            if high_scores_dict[i] == str(min_high_score)
        }.pop()
        del high_scores_dict[value]

        print(
            colored(
                figlet_format("Congrats", font="bulbhead", justify="center"),
                "cyan",
            )
        )
        print("\n" * 2)
        print(
            colored(
                " " * 22 + "You made our High Scores Leaderboard", "yellow"
            )
        )
        print("\n" * 4)

        # Add player to the Leaderboard
        player_name = input(" " * 25 + "Please enter your name: \n")
        high_scores_dict[player_name] = score

        high_scores_data = [
            list(high_scores_dict.keys()),
            list(high_scores_dict.values()),
        ]
        SHEET.worksheet("HS").clear()
        SHEET.worksheet("HS").update(high_scores_data)
        high_scores()
    else:
        clear_terminal()
        print(
            colored(
                figlet_format("Hard Luck", font="bulbhead", justify="center"),
                "cyan",
            )
        )
        print("\n" * 2)
        print(
            colored(
                " " * 18 + "You did not make the High Score Leader board",
                "yellow",
            )
        )
        print("\n" * 4)
        input(
            " " * 16 + 
            "Press Enter to continue to the High Score Leaderboard\n"
        )
        high_scores()

main_screen()
