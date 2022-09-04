
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("smarticus_high_scores")


def main_screen():

    """ Present the user with the name of the game and three options.
    1 lets the user start the game
    2 lets the user know how to play
    3 lets the user view the top 10 high scores
    """


def play():
    """ Start the game """
    

def get_question():
    """ Get the question from the API """
    

def how_to():
    """ Explains how to play the game """


def high_scores():
    """ Create and Show the High Scores Leaderboard """


def check_score(score):
    """ Check if player has made it into the Leaderboard """
    
    
main_screen()
