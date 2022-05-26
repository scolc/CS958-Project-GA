from tkinter import *

class GUI():
    """
    A class to handle the GUI for accepting user input,
    call the genetic algorithm and display output for the user
    """

    def __init__(self):
        self.ui = Tk()
        self.grid_ui = []

    def validate_entry(entry):
        """
        A function to validate the value entered into any cell
        should always be a digit between 1 and 9 and refuses
        any other entry
        """
        if len(entry) == 0:
            return True
        elif len(entry) == 1 and entry.isdigit():
            if entry not in "0":
                return True
            else:
                return False
        else:
            return False

    def init_row():
        """
        A function to create a new row for the grid ui
        """
        new_row = []
        for entry in range(9):
            valid_entry = (gui.register(validate_entry), '%P')
            cell = Entry(gui, borderwidth = 2, justify="center", validate = "key", validatecommand = valid_entry)
            new_row.append(cell)
        
        return new_row

    def init_grid(self):
        """
        A function to create the grid ui
        """
        for entry in range(9):
            row = init_row()
            self.grid_ui.append(row)




"""
A program to solve sudoku puzzles using genetic algorithm optimisation.

Employs a GUI to allow a user to enter an unsolved sudoku puzzle and run the
genetic algorithm to solve the puzzle. The solution will then be displayed 
to the user through the GUI.
"""
if __name__ == "__main__":
    
    # Create the GUI
    gui = GUI()