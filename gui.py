from tkinter import *

import ui_grid
import ui_buttons
import ui_output_box


class Colours():
    """
    A class to hold all the colour options to be used across the application.
    """

    def __init__(self):
        # Colour for windows
        self.bg_window = "#f8feb5"

        # Colours for cells and other elements
        # Normal
        self.fg_en_norm = "#000000"
        self.fg_dis_norm = "#525252"
        self.bg_en_norm = "#fafafa"
        self.bg_dis_norm = "#c8c8c8"

        # Puzzle clues for solution
        self.fg_dis_clue = "#2e00ff"

        # Hints
        self.bg_hint = "#ffec00"

        # Validate
        self.bg_valid = "#67ff76"
        self.bg_invalid = "#ff4444"

        # Output box
        self.fg_output = "#ffffff"
        self.bg_output = "#000000"


class GUI():
    """
    A class to handle the GUI for accepting user input,
    call the genetic algorithm and display output for the user.
    """

    def __init__(self):
        self.ui = Tk()
        self.colours = Colours()

        # Window proportions
        self.tile_size = 40  # Tile pixel size to base gui proportions on
        self.main_pad = int(self.tile_size / 2)

        # Columns and rows to fit elements and padding
        self.window_columns = 16
        self.window_rows = 20

        self.window_width = self.window_columns * self.tile_size
        self.window_height = self.window_rows * self.tile_size

        self.frame_pad = 5  # A padding for all frame or canvas elements

    # Display Functions

    def display_title_box(self, width, height):
        """
        A function to display the title box.
        """
        # Create objects
        title_frame = Frame(self.ui,
                            bg=self.colours.bg_dis_norm,
                            highlightthickness=0)

        title_box = Label(title_frame,
                          text="Sudoku Puzzle Solver",
                          font="Calibri " + str(int(self.tile_size / 1.25)))

        # Set attributes
        x_pos = self.main_pad - self.frame_pad
        y_pos = self.main_pad - self.frame_pad
        frame_width = (self.window_width -
                       2 * self.main_pad +
                       2 * self.frame_pad)
        frame_height = height + 2 * self.frame_pad

        # Display
        title_frame.place(x=x_pos,
                          y=y_pos,
                          width=frame_width,
                          height=frame_height)
        title_box.place(x=self.frame_pad,
                        y=self.frame_pad,
                        width=width,
                        height=height)

    def display_window(self):
        """
        A function to display the various elements of the window to
        allow the user interaction and run the various program functions
        """
        # Add title box
        title_box_width = self.window_width - 2 * self.main_pad
        title_box_height = self.tile_size * 1.5

        self.display_title_box(title_box_width, title_box_height)

        # Add the grid
        grid_ui = ui_grid.UIGrid(ui=self.ui, tile_size=self.tile_size)
        grid_x = self.tile_size + 2 * self.main_pad
        grid_y = title_box_height + self.main_pad * 2
        grid_size = grid_ui.grid_size

        grid_ui.display_grid_ui(x_pos=grid_x,
                                y_pos=grid_y,
                                frame_pad=self.frame_pad)

        # Add output box
        output_box = ui_output_box.UIOutputBox(ui=self.ui,
                                               tile_size=self.tile_size)
        output_x = self.main_pad
        output_y = grid_y + grid_size + self.main_pad
        output_width = self.window_width - 2 * self.main_pad
        output_height = self.window_height - output_y - self.main_pad

        output_box.display_output_box(x_pos=output_x,
                                      y_pos=output_y,
                                      output_width=output_width,
                                      output_height=output_height,
                                      frame_pad=self.frame_pad)

        # Add buttons
        btn_ui = ui_buttons.UIButtons(ui=self.ui,
                                      tile_size=self.tile_size,
                                      grid_ui=grid_ui,
                                      output_box=output_box)
        right_btn_x = grid_x + grid_ui.grid_size + self.main_pad
        right_btn_y = title_box_height + self.main_pad * 2
        right_btn_width = self.window_width - right_btn_x - self.main_pad
        num_btn_x = self.main_pad
        num_btn_y = title_box_height + 2 * self.main_pad

        btn_ui.display_buttons(right_x=right_btn_x,
                               right_y=right_btn_y,
                               right_width=right_btn_width,
                               num_x=num_btn_x,
                               num_y=num_btn_y,
                               frame_pad=self.frame_pad)

        # Display the window
        # Set the window properties
        self.ui.title("Sudoku Puzzle Solver")
        self.ui.resizable(width=False, height=False)
        self.ui["bg"] = self.colours.bg_window
        screen_width = self.ui.winfo_screenwidth()
        screen_height = self.ui.winfo_screenheight()

        # Place in adjusted middle of screen width, near the top of the screen
        win_x = int(screen_width / 2 - self.window_width / 2)
        win_y = int(screen_height * 5/100)
        self.ui.geometry(str(self.window_width) +
                         "x" +
                         str(self.window_height) +
                         "+" + str(win_x) + "+" + str(win_y))
        try:
            self.ui.iconbitmap("grid.ico")
        except TclError:
            self.ui.iconbitmap()
        self.ui.mainloop()
