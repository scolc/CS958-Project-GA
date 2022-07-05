import requests
import json

class SudokuGenerator():
    """
    A class to handle generating a sudoku grid by requesting a JSON for 
    a 'board' from an API at sugoku.herokuapp.com. Grids returned are
    based on the difficulty 'easy', 'medium' or 'hard' given to the API.
    """

    def __init__(self):
        self.grid = []

    def generate(self, difficulty = 'easy'):
        """
        A function to handle the request to the API and store the
        generated grid as a list.
        Returns True or False based on success.
        """
        try:
            connection = requests.get(f"https://sugoku.herokuapp.com/board?difficulty={difficulty}")
        except:
            return False
            
        if connection.status_code == 200:
            # Successful connection  
            self.grid = connection.json()['board']
        else:
            return False

        return True
