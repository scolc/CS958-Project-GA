#import random
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText

#import grid_solver as gsol
import sudoku_grid as sg
import sudoku_generator as gen
import ui_grid
import ui_buttons
import ui_output_box

class Colours():
    """
    A class to hold all the colour options.
    """

    def __init__(self):
        # Colour for windows
        self.col_window_bg = "#f8feb5"

        # Colours for cells and other elements
        # Normal
        self.col_fg_en_norm = "#000000" 
        self.col_fg_dis_norm = "#525252"
        self.col_bg_en_norm = "#fafafa"
        self.col_bg_dis_norm = "#c8c8c8"

        # Puzzle clues for solution
        self.col_fg_dis_clue = "#2e00ff"

        # Hints
        self.col_hint = "#ffec00"
        
        # Validate
        self.col_valid = "#67ff76"
        self.col_invalid = "#ff4444"

        # Output box
        self.col_out_fg = "#ffffff"
        self.col_out_bg = "#000000"

class GUI():
    """
    A class to handle the GUI for accepting user input,
    call the genetic algorithm and display output for the user.
    """
    

    def __init__(self):
        self.ui = Tk()
        self.colours = Colours()
        
        # Window proportions
        self.tile_size = 40 # Tile pixel size to base gui proportions on
        self.x_pad = int(self.tile_size / 2)
        self.y_pad = int(self.tile_size / 2)
        
        self.max_window_columns = 14 # Space for 9 grid columns, a button and padding in between
        self.max_window_rows = 20 # Space for 9 grid rows, other elements and padding
        
        self.window_width = self.max_window_columns * self.tile_size
        self.window_height = self.max_window_rows * self.tile_size
        
        # Set the window properties
        self.ui.title("Sudoku Puzzle Solver")
        self.ui.resizable(width = False, height = False)
        self.ui.geometry(str(self.window_width) + "x" + str(self.window_height))
        self.ui["bg"] = self.colours.col_window_bg

        # Initialise the ui elements
        self.frame_pad = 5 # A padding for all frame or canvas elements
        
        # Title Box
        self.title_frame = Frame(self.ui,
                                bg = self.colours.col_bg_dis_norm,
                                highlightthickness=0)
        self.title_box_width = self.window_width - 2 * self.x_pad
        self.title_box_height = self.tile_size * 1.5
        
        self.title_box = Label(self.title_frame,
                                text = "Sudoku Puzzle Solver",
                                font = "Calibri " + str(int(self.tile_size / 1.25)))
        
        # Grid
        self.grid_ui = ui_grid.UIGrid(ui = self.ui, tile_size = self.tile_size)
        self.grid_x = self.x_pad
        self.grid_y = self.title_box_height + self.y_pad * 2
        self.grid_size = self.grid_ui.grid_size
        
        # Operation Buttons Variables
        #self.btn_height = self.tile_size
        self.right_btn_width = self.window_width - self.grid_ui.grid_size - 3 * self.x_pad
        self.right_btn_x = self.grid_ui.grid_size + 2 * self.x_pad
        self.right_btn_y = self.title_box_height + self.y_pad * 2
        self.bot_btn_x = self.x_pad
        self.bot_btn_y = self.grid_y + self.grid_ui.grid_size + self.y_pad
        
        # Output Box Variables
        self.output_x = self.x_pad
        self.output_y = self.bot_btn_y + self.tile_size + self.y_pad
        self.output_width = self.window_width - 2 * self.x_pad
        self.output_height = self.window_height - self.output_y - self.y_pad
                                                #(self.title_box_height +
                                                  #  self.grid_ui.grid_size +
                                                  #  self.tile_size +
                                                  #  5 * self.y_pad)
        
        # Grid and Buttons objects
        self.output_box = ui_output_box.UIOutputBox(ui = self.ui, tile_size = self.tile_size)
        self.btn_ui = ui_buttons.UIButtons(ui = self.ui,
                                            tile_size = self.tile_size,
                                            grid_ui = self.grid_ui,
                                            right_btn_width = self.right_btn_width,
                                            output_box = self.output_box)


        
        # Message Boxes
        self.m_box_width = self.tile_size * 8
        self.m_box_height = self.tile_size * 5
        self.m_box_font = "Calibri " + str(int(self.tile_size / 3))
        self.m_box_frame_pad = 3


        # Other Variables
        self.running_ga = False
        self.ga_thread = threading.Thread()
        self.grid = sg.SudokuGrid()
        self.generator = gen.SudokuGenerator()


    # Initialisation Functions


    # Display Functions

    def display_title_box(self):
        """
        A function to display the title box.
        """
        x_pos = self.x_pad - self.frame_pad
        y_pos = self.y_pad - self.frame_pad
        frame_width = (self.window_width -
                        2 * self.x_pad +
                        2 * self.frame_pad)
        frame_height = self.title_box_height + 2 * self.frame_pad
        self.title_frame.place(x = x_pos,
                                y = y_pos,
                                width = frame_width,
                                height = frame_height)
        self.title_box.place(x = self.frame_pad,
                            y = self.frame_pad,
                            width = self.title_box_width,
                            height = self.title_box_height)

    def display_window(self):
        """
        A function to display the various elements of the window to
        allow the user interaction and run the various program functions
        """
        # Add title box
        self.display_title_box()

        # Add the grid
        self.grid_ui.display_grid_ui(x_pos = self.grid_x,
                                    y_pos = self.grid_y,
                                    frame_pad = self.frame_pad)

        # Add buttons
        self.btn_ui.display_buttons(right_x = self.right_btn_x,
                                    right_y = self.right_btn_y,
                                    bot_x = self.bot_btn_x,
                                    bot_y = self.bot_btn_y,
                                    frame_pad = self.frame_pad)

        # Add output box
        self.output_box.display_output_box(x_pos = self.output_x,
                                            y_pos = self.output_y,
                                            output_width = self.output_width,
                                            output_height = self.output_height,
                                            frame_pad = self.frame_pad)
        
        # Display the window
        self.ui.mainloop()
        

        


        






"""
A program to solve sudoku puzzles using genetic algorithm optimisation.

Employs a GUI to allow a user to enter an unsolved sudoku puzzle and run the
genetic algorithm to solve the puzzle. The solution can then be displayed 
to the user through the GUI. The user can also request hints or validate
their guesses to check for correctness against the solution.
"""
if __name__ == "__main__":
    
    # Create the GUI and start the program
    gui = GUI()
    gui.display_window()
