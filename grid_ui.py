from tkinter import *

import main

class GridUI():
    """
    A class to handle the GUI grid element.
    """

    def __init__(self, GUI : main.GUI):
        self.main = GUI
        self.grid_canvas = Canvas(self.main.ui,
                                bg = self.main.col_bg_dis_norm,
                                highlightthickness = 0)
        self.grid_size = 9 * self.main.tile_size
        self.grid_ui = self.init_grid_ui()
        self.font = "Calibri " + str(int(self.main.tile_size / 2))
    
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
            valid_entry = (self.main.ui.register(self.validate_entry), '%P')
            cell = Entry(self.grid_canvas,
                        borderwidth = 2,
                        justify="center",
                        validate = "key",
                        validatecommand = valid_entry,
                        font = self.font,
                        fg = self.main.col_fg_en_norm,
                        disabledforeground = self.main.col_fg_dis_norm,
                        bg = self.main.col_bg_en_norm,
                        disabledbackground = self.main.col_bg_dis_norm,
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