import requests


class SudokuGenerator():
    """
    A class to handle generating a sudoku grid by requesting a JSON for
    a 'board' from an API at sugoku.herokuapp.com. Grids returned are
    based on the difficulty 'easy' given to the API.
    """

    def __init__(self):
        self.grid = []

    def generate(self):
        """
        A function to handle the request to the API and
        store the generated grid as a list.
        Returns True or False based on success.
        """
        generating = True
        attempts = 0
        success = False
        while generating:
            attempts += 1
            try:
                url = "https://sugoku.herokuapp.com/board?difficulty=easy"
                connection = requests.get(url)
            except requests.exceptions.ConnectionError:
                break
            except requests.exceptions.Timeout:
                break

            if connection.status_code == 200:
                grid = connection.json()['board']

                # Check that grid is acceptable, no empty rows, min 2 digits
                acceptable = True
                for row in grid:
                    if len(set(row)) < 3:  # less than 2 digits above 0
                        acceptable = False

                if acceptable:
                    self.grid.clear()
                    self.grid = grid
                    generating = False
                    success = True
                    break  # Grid found, stop communication attempts

                if attempts == 5:  # Grid not found
                    generating = False
            else:
                generating = False

        return success
