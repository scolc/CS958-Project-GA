import random
from tkinter import *
from typing import Callable

import sudoku_grid as sg
import main

class UIGrid():
    """
    A class to handle the GUI grid element.
    """

    def __init__(self, ui : Tk, tile_size : int):
        self.ui = ui
        self.tile_size = tile_size
        self.colours = main.Colours()
        
        self.grid_size = 9 * self.tile_size
        
        self.font = "Calibri " + str(int(self.tile_size / 2))
        self.canvas = Canvas(self.ui,
                                bg = self.colours.col_bg_dis_norm,
                                highlightthickness = 0)
        self.grid = self.init_grid_ui()
    
    # Initialisation Functions

    def init_grid_ui(self):
        """
        A function to create the grid ui element.
        """
        new_grid = []
        for _ in range(9):
            new_grid.append(self.init_row_ui())
        
        return new_grid

    def init_row_ui(self):
        """
        A function to create a new row of entry boxes for the grid ui.
        """
        new_row = []
        for _ in range(9):
            valid_entry = (self.ui.register(self.validate_entry), '%P')
            cell = Entry(self.canvas,
                        borderwidth = 2,
                        justify="center",
                        validate = "key",
                        validatecommand = valid_entry,
                        font = self.font,
                        fg = self.colours.col_fg_en_norm,
                        disabledforeground = self.colours.col_fg_dis_norm,
                        bg = self.colours.col_bg_en_norm,
                        disabledbackground = self.colours.col_bg_dis_norm,
                        border = 0,
                        highlightthickness = 0)
            new_row.append(cell)
            
        return new_row

    def validate_entry(self, entry):
        """
        A function to validate the value entered into any cell
        should always be a digit between 1 and 9 and refuses
        any other entry.
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

    def display_grid_ui(self, x_pos, y_pos, frame_pad):
        """
        A function to display the grid ui.
        """
        canvas_width = self.grid_size + 2 * frame_pad
        canvas_height = self.grid_size + 2 * frame_pad
        self.canvas.place(x = x_pos - frame_pad,
                        y = y_pos - frame_pad,
                        width = canvas_width,
                        height = canvas_height)
        
        # Background rectangle to fill any gaps in the grid
        self.canvas.create_rectangle(frame_pad,
                                    frame_pad,
                                    frame_pad + self.grid_size,
                                    frame_pad + self.grid_size,
                                    fill = self.colours.col_bg_en_norm,
                                    width = 0)
        
        # Place cells
        cell_pad = 1.5
        for entry in range(len(self.grid)):
            self.display_row_ui(self.grid[entry], entry, cell_pad, frame_pad)
        
        # Draw thick grid lines
        line_width = cell_pad * 2
        for row in range(3):
            y1 = 3 * row * self.tile_size + frame_pad
            y2 = y1 + self.tile_size * 3
            for column in range(3):
                x1 = 3 * column * self.tile_size + frame_pad
                x2 = x1 + self.tile_size * 3
                self.canvas.create_rectangle(x1, y1, x2, y2, width = line_width)
        
    def display_row_ui(self, this_row, row_num, cell_pad, frame_pad):
        """
        A function to display each row of the grid.
        """
        y_pos = row_num * self.tile_size + frame_pad
        
        for entry in range(len(this_row)):
            x_pos = entry * self.tile_size + frame_pad
            this_row[entry].place(x = x_pos + cell_pad, 
                                y = y_pos + cell_pad,
                                width = self.tile_size - 2 * cell_pad,
                                height = self.tile_size - 2 * cell_pad)
            # Create the grid line around the cell
            self.canvas.create_rectangle(x_pos, 
                                        y_pos,
                                        x_pos + self.tile_size,
                                        y_pos + self.tile_size,
                                        width = cell_pad / 2)
    
    def disable_grid(self):
        """
        A function to disable all the cells in the grid.
        """
        for ui_row in range(len(self.grid)):
            for cell_num in range(len(self.grid[ui_row])):
                self.grid[ui_row][cell_num]["state"] = "disabled"
    
    def enable_grid(self):
        """
        A function to enable all the cells in the grid.
        """
        for ui_row in range(len(self.grid)):
            for cell_num in range(len(self.grid[ui_row])):
                self.grid[ui_row][cell_num]["state"] = "normal"
    
    def enable_grid_solved(self):
        """
        A function to enable the empty cells in the grid when
        a solution has been found.
        """
        for ui_row in range(len(self.grid)):
            for cell_num in range(len(self.grid[ui_row])):
                current_cell = self.grid[ui_row][cell_num]
                entry = current_cell.get()
                if entry.isdigit():
                    current_cell["disabledforeground"] = self.colours.col_fg_dis_clue
                else:
                    current_cell["state"] = "normal"
    
    # Operation Functions
    
    def get_user_rows(self):
        """
        A function to read user entry and return it as a list
        """
        rows = []
        for ui_row in range(len(self.grid)):
            this_row = []
            for cell_num in range(len(self.grid[ui_row])):
                entry = self.grid[ui_row][cell_num].get()
                if entry.isdigit():
                    this_row.append(int(entry))
                else:
                    this_row.append(0)
            rows.append(this_row)

        return rows
    
    def update_grid_solution_ui(self, solution_grid : sg.SudokuGrid):
        """
        A function to update the grid ui with the solution
        """
        for ui_row in range(len(self.grid)):
            for cell_num in range(len(self.grid[ui_row])):
                if solution_grid.user_rows[ui_row][cell_num] == 0:
                    self.grid[ui_row][cell_num]["state"] = "normal" # In case cell is disabled from hint
                    self.grid[ui_row][cell_num].delete(0, END) # Clear any input after solution found
                    self.grid[ui_row][cell_num].insert(0, solution_grid.current_solution[ui_row][cell_num])
                    
                    # Imitate an active cell while disabled
                    self.grid[ui_row][cell_num]["disabledforeground"] = self.colours.col_fg_en_norm
                    self.grid[ui_row][cell_num]["disabledbackground"] = self.colours.col_valid
                    self.grid[ui_row][cell_num]["state"] = "disabled"

    def show_hint(self, solution_grid :sg.SudokuGrid, output : Callable):
        """
        A function to Check the displayed grid for unsolved
        cells and randomly fills one in.
        """
        # Create list of unsolved cells
        unsolved_cells = []
        for ui_row in range(len(self.grid)):
            for cell_num in range(len(self.grid[ui_row])):
                # Check cell has a value that is incorrect or is empty
                entry = self.grid[ui_row][cell_num].get()
                if ((entry.isdigit()
                and not solution_grid.user_rows[ui_row][cell_num] == int(entry)
                and not solution_grid.current_solution[ui_row][cell_num]  == int(entry))
                or not entry.isdigit()):
                    unsolved_cells.append((ui_row, cell_num))
        
        # Proceed if valid list of cells created
        if unsolved_cells:
            # Randomly pick a cell from the list and fill it in
            random.shuffle(unsolved_cells)
            row = unsolved_cells[0][0]
            col = unsolved_cells[0][1]

            self.grid[row][col].delete(0, END)
            self.grid[row][col].insert(0, solution_grid.current_solution[row][col])

            # Cell is completed so disable it
            self.grid[row][col]["disabledbackground"] = self.colours.col_hint
            self.grid[row][col]["disabledforeground"] = self.colours.col_fg_en_norm
            self.grid[row][col]["state"] = "disabled"
            #print(f"Hint shown at row {row + 1}, cell {col + 1}")
            output("Hint", "hint")
            output(f" shown at row {row + 1}, column {col + 1}\n\n")
        else: # No valid cells found
            #print("No cells valid to provide hint")
            output("No hints available.\n\n")

    def validate_user_entry(self, solution_grid : sg.SudokuGrid):
        """
        Checks the displayed grid for entries that are not part of the
        initial clues and checks for correctness. Changes the cell
        background depending on correctness.
        """
        for ui_row in range(len(self.grid)):
            for cell_num in range(len(self.grid[ui_row])):
                # Check the cell has a value and not part of the initial clues
                entry = self.grid[ui_row][cell_num].get()
                if (entry.isdigit()
                and not solution_grid.user_rows[ui_row][cell_num] == int(entry)):
                    # Check value against cell and change background accordingly
                    if solution_grid.current_solution[ui_row][cell_num] == int(entry):
                        # Correct background
                        self.grid[ui_row][cell_num]["bg"] = self.colours.col_valid
                    else:
                        # Incorrect background
                        self.grid[ui_row][cell_num]["bg"] = self.colours.col_invalid
    
    def clear_entries(self, solution_grid : sg.SudokuGrid):
        """
        Resets any cells that are not part of the initial clues.
        """
        for ui_row in range(len(self.grid)):
            for cell_num in range(len(self.grid[ui_row])):
                # Check the cell is not part of the initial clues
                entry = self.grid[ui_row][cell_num].get()
                if not (entry.isdigit()
                and solution_grid.user_rows[ui_row][cell_num] == int(entry)):
                    self.grid[ui_row][cell_num]["state"] = "normal"
                    self.grid[ui_row][cell_num].delete(0, END)
                    self.grid[ui_row][cell_num]["bg"] = self.colours.col_bg_en_norm
    
    def reset_grid(self):
        """
        Resets all cells back to initial run state.
        """
        for ui_row in range(len(self.grid)):
            for cell_num in range(len(self.grid[ui_row])):
                self.grid[ui_row][cell_num]["state"] = "normal"
                self.grid[ui_row][cell_num].delete(0, END)
                self.grid[ui_row][cell_num]["fg"] = self.colours.col_fg_en_norm
                self.grid[ui_row][cell_num]["disabledforeground"] = self.colours.col_fg_dis_norm
                self.grid[ui_row][cell_num]["bg"] = self.colours.col_bg_en_norm
                self.grid[ui_row][cell_num]["disabledbackground"] = self.colours.col_bg_dis_norm

    def update_changed_user_grid(self, solution_grid : sg.SudokuGrid):
        """
        Updates the grid with the changes to the user grid.
        """
        self.reset_grid()
        for ui_row in range(len(self.grid)):
            for cell_num in range(len(self.grid[ui_row])):
                if solution_grid.user_rows[ui_row][cell_num] > 0:
                    self.grid[ui_row][cell_num].delete(0, END)
                    self.grid[ui_row][cell_num].insert(0, solution_grid.user_rows[ui_row][cell_num])