from sre_parse import State
from tkinter import *
import sudoku_grid as sg
import ga_solver
import grid_solver as gsol
import threading


class GUI():
    """
    A class to handle the GUI for accepting user input,
    call the genetic algorithm and display output for the user
    """

    def __init__(self):
        self.ui = Tk()
        
        # Window proportions
        self.tile_size = 32 # tile pixel size to base gui proportions on
        self.max_window_columns = 11
        self.max_window_rows = 13
        self.window_width = self.max_window_columns * self.tile_size
        self.window_height = self.max_window_rows * self.tile_size

        # Set the window properties
        self.ui.title("Sudoku Puzzle Solver")
        self.ui.resizable(width = False, height = False)
        self.ui.geometry(str(self.window_width) + "x" + str(self.window_height))

        # Initialise the ui elements
        self.grid_ui = self.init_grid_ui()
        self.solve_btn = Button(self.ui, text = "SOLVE", command = self.solve_grid)

    # Initialisation Functions

    def init_grid_ui(self):
        """
        A function to create the grid ui
        """
        new_grid = []
        for entry in range(9):
            new_grid.append(self.init_row_ui())
        
        return new_grid

    def init_row_ui(self):
        """
        A function to create a new row for the grid ui
        """
        new_row = []
        for entry in range(9):
            valid_entry = (self.ui.register(self.validate_entry), '%P')
            cell = Entry(self.ui, borderwidth = 2, justify="center", validate = "key", validatecommand = valid_entry)
            cell["font"] = "Calibri " + str(int(self.tile_size / 2))
            new_row.append(cell)
        
        return new_row

    def validate_entry(self, entry):
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

    # Display Functions

    def display_grid_ui(self):
        """
        A function to display the grid ui
        """
        for entry in range(len(self.grid_ui)):
            self.display_row_ui(self.grid_ui[entry], entry)

    def display_row_ui(self, this_row, row_num):
        """
        A function to display each row of the grid
        """
        for entry in range(len(this_row)):
            this_row[entry].place(x = (entry * self.tile_size) + self.tile_size, 
                                y = (row_num * self.tile_size) + self.tile_size,
                                width = self.tile_size,
                                height = self.tile_size)
    
    def display_buttons(self):
        """
        A function to display the buttons for the user interaction
        """
        btn_width = self.tile_size * 5
        self.solve_btn.place(x = (self.window_width / 2) - (btn_width / 2),
                            y = self.tile_size * 11,
                            width = btn_width,
                            height = self.tile_size)

    def display_window(self):
        """
        A function to display the various elements of the window to
        allow the user interaction and run the various program functions
        """
        # Add the grid
        self.display_grid_ui()

        # Add buttons
        self.display_buttons()
        # Add output box

        # Display the window
        self.ui.mainloop()

    # Operation Functions
    
    def solve_grid(self):
        """
        A function to handle the user clicking on the solve button.
        Checks user entry and begins the process for solving the grid
        """
        # Confirm user choice to continue

        # Check user entry follows sudoku rules

        # Build grid class from user entry
        grid = sg.SudokuGrid()
        rows = self.get_user_rows()

        #rows = []
        #rows.append([0, 0, 2, 1, 0, 0, 0, 7, 0])
        #rows.append([0, 8, 0, 0, 0, 6, 0, 0, 1])
        #rows.append([1, 3, 0, 0, 8, 0, 0, 0, 2])
        #rows.append([0, 5, 9, 0, 0, 8, 2, 0, 0])
        #rows.append([0, 0, 0, 3, 9, 1, 0, 0, 0])
        #rows.append([0, 0, 7, 5, 0, 0, 3, 8, 0])
        #rows.append([2, 0, 0, 0, 5, 0, 0, 3, 7])
        #rows.append([8, 0, 0, 6, 0, 0, 0, 2, 0])
        #rows.append([0, 7, 0, 0, 0, 3, 4, 0, 0])

        grid.user_rows.clear()
        grid.user_rows = rows
        print(grid)
        
        # Run GA
        t1 = threading.Thread(target=self.run_ga, args=[grid])
        t1.start()

    def get_user_rows(self):
        """
        A function to read user entry and return it as a list
        """
        rows = []
        for ui_row in range(len(self.grid_ui)):
            this_row = []
            for cell in range(len(self.grid_ui[ui_row])):
                entry = self.grid_ui[ui_row][cell].get()
                if entry.isdigit():
                    this_row.append(int(entry))
                    self.grid_ui[ui_row][cell].config(fg='blue')
                    #self.grid_ui[ui_row][cell].config(disabledb='green')

                else:
                    this_row.append(0)
            rows.append(this_row)

        return rows
        
        

        

    def run_ga(self, grid: sg.SudokuGrid):
        """
        A function to handle running the genetic algorithm to
        complete the grid
        """
        # Disable Solve button and grid to prevent entry
        self.solve_btn.config(state='disabled')
        for ui_row in range(len(self.grid_ui)):
            for cell in range(len(self.grid_ui[ui_row])):
                self.grid_ui[ui_row][cell].config(state='disabled')
                


        # Run GA
        solver = gsol.GridSolver(grid)
        solved = solver.run()

        # Update grid ui
        for ui_row in range(len(self.grid_ui)):
            for cell in range(len(self.grid_ui[ui_row])):
                self.grid_ui[ui_row][cell].config(state='normal')
        if solved:
            self.update_grid_ui(grid)
            print(grid.current_solution)
        self.solve_btn.config(state='active')



    def update_grid_ui(self, grid: sg.SudokuGrid):
        """
        A function to update the grid ui
        """
        for ui_row in range(len(self.grid_ui)):
            for cell in range(len(self.grid_ui[ui_row])):
                self.grid_ui[ui_row][cell].delete(0, END)
                self.grid_ui[ui_row][cell].insert(0, grid.current_solution[ui_row][cell])

        






"""
A program to solve sudoku puzzles using genetic algorithm optimisation.

Employs a GUI to allow a user to enter an unsolved sudoku puzzle and run the
genetic algorithm to solve the puzzle. The solution will then be displayed 
to the user through the GUI.
"""
if __name__ == "__main__":
    
    # Create the GUI and start the program
    gui = GUI()
    gui.display_window()
