"""
A program to solve sudoku puzzles using genetic algorithm optimisation.

Employs a GUI to allow a user to enter an unsolved sudoku puzzle and run the
genetic algorithm to solve the puzzle. The solution can then be displayed
to the user through the GUI. The user can also request hints or validate
their guesses to check for correctness against the solution.
"""

import gui


if __name__ == "__main__":

    # Create the GUI and start the program
    solver = gui.GUI()
    solver.display_window()
