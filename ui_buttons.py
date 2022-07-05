#import random
import threading
from tkinter import *
from typing import Callable

import sudoku_grid as sg
import grid_solver as gsol
import main
import ui_grid
import sudoku_generator as gen
import ui_output_box
import ui_message_box

class UIButtons():
    """
    A class to handle the button UI elements and running the general
    program functionality.
    """

    def __init__(self, ui : Tk,
                tile_size : int,
                grid_ui : ui_grid,
                right_btn_width : int,
                output_box : ui_output_box):
        self.ui = ui
        self.tile_size = tile_size
        self.grid_ui = grid_ui
        self.colours = main.Colours()
        self.grid = sg.SudokuGrid()
        self.output = output_box
        self.generator = gen.SudokuGenerator()
        self.running_ga = False
        self.ga_thread = threading.Thread()
        self.message_box = ui_message_box.UIMessageBox(ui = self.ui, tile_size = self.tile_size)
        
        
        self.btn_font = "Calibri " + str(int(self.tile_size / 2.5))

        # Frames
        # Right Buttons
        self.solve_btn_frame = Frame(self.ui,
                                    bg = self.colours.col_bg_en_norm,
                                    highlightthickness = 1,
                                    highlightbackground = self.colours.col_fg_en_norm)
        self.show_sol_btn_frame = Frame(self.ui,
                                    bg = self.colours.col_bg_en_norm,
                                    highlightthickness = 1,
                                    highlightbackground = self.colours.col_fg_en_norm)
        self.show_hint_btn_frame = Frame(self.ui,
                                    bg = self.colours.col_bg_en_norm,
                                    highlightthickness = 1,
                                    highlightbackground = self.colours.col_fg_en_norm)
        self.valid_entry_btn_frame = Frame(self.ui,
                                    bg = self.colours.col_bg_en_norm,
                                    highlightthickness = 1,
                                    highlightbackground = self.colours.col_fg_en_norm)
        self.clear_entry_btn_frame = Frame(self.ui,
                                    bg = self.colours.col_bg_en_norm,
                                    highlightthickness = 1,
                                    highlightbackground = self.colours.col_fg_en_norm)
        self.reset_btn_frame = Frame(self.ui,
                                    bg = self.colours.col_bg_en_norm,
                                    highlightthickness = 1,
                                    highlightbackground = self.colours.col_fg_en_norm)
        
        # Bottom Buttons
        self.num_1_frame = Frame(self.ui,
                                bg = self.colours.col_bg_en_norm,
                                highlightthickness = 1,
                                highlightbackground = self.colours.col_fg_en_norm)
        self.num_2_frame = Frame(self.ui,
                                bg = self.colours.col_bg_en_norm,
                                highlightthickness = 1,
                                highlightbackground = self.colours.col_fg_en_norm)
        self.num_3_frame = Frame(self.ui,
                                bg = self.colours.col_bg_en_norm,
                                highlightthickness = 1,
                                highlightbackground = self.colours.col_fg_en_norm)
        self.num_4_frame = Frame(self.ui,
                                bg = self.colours.col_bg_en_norm,
                                highlightthickness = 1,
                                highlightbackground = self.colours.col_fg_en_norm)
        self.num_5_frame = Frame(self.ui,
                                bg = self.colours.col_bg_en_norm,
                                highlightthickness = 1,
                                highlightbackground = self.colours.col_fg_en_norm)
        self.num_6_frame = Frame(self.ui,
                                bg = self.colours.col_bg_en_norm,
                                highlightthickness = 1,
                                highlightbackground = self.colours.col_fg_en_norm)
        self.num_7_frame = Frame(self.ui,
                                bg = self.colours.col_bg_en_norm,
                                highlightthickness = 1,
                                highlightbackground = self.colours.col_fg_en_norm)
        self.num_8_frame = Frame(self.ui,
                                bg = self.colours.col_bg_en_norm,
                                highlightthickness = 1,
                                highlightbackground = self.colours.col_fg_en_norm)
        self.num_9_frame = Frame(self.ui,
                                bg = self.colours.col_bg_en_norm,
                                highlightthickness = 1,
                                highlightbackground = self.colours.col_fg_en_norm)
        self.gen_btn_frame = Frame(self.ui,
                                bg = self.colours.col_bg_en_norm,
                                highlightthickness = 1,
                                highlightbackground = self.colours.col_fg_en_norm)

        # Buttons
        # Right Buttons
        self.solve_btn = Button(self.solve_btn_frame, text = "START",
                                font = self.btn_font,
                                command = self.solve_btn_press)
        self.show_sol_btn = Button(self.show_sol_btn_frame, text = "Show Solution",
                                font = self.btn_font,
                                command = self.show_solution,
                                state = "disabled")
        self.show_hint_btn = Button(self.show_hint_btn_frame, text = "Show Hint",
                                font = self.btn_font,
                                command = self.show_hint,
                                state = "disabled")
        self.valid_entry_btn = Button(self.valid_entry_btn_frame, text = "Validate",
                                font = self.btn_font,
                                command = self.validate_user_entry,
                                state = "disabled")
        self.clear_entry_btn = Button(self.clear_entry_btn_frame, text = "Clear Entries",
                                font = self.btn_font,
                                command = self.clear_entries,
                                state = "disabled")
        self.reset_btn = Button(self.reset_btn_frame, text = "RESET GRID",
                                font = self.btn_font,
                                command = self.reset_grid)
        
        # Bottom Buttons
        self.num_1_btn = Button(self.num_1_frame, text = "1",
                                font = self.btn_font,
                                command = lambda : self.num_button_press(1))
        self.num_2_btn = Button(self.num_2_frame, text = "2",
                                font = self.btn_font,
                                command = lambda : self.num_button_press(2))
        self.num_3_btn = Button(self.num_3_frame, text = "3",
                                font = self.btn_font,
                                command = lambda : self.num_button_press(3))
        self.num_4_btn = Button(self.num_4_frame, text = "4",
                                font = self.btn_font,
                                command = lambda : self.num_button_press(4))
        self.num_5_btn = Button(self.num_5_frame, text = "5",
                                font = self.btn_font,
                                command = lambda : self.num_button_press(5))
        self.num_6_btn = Button(self.num_6_frame, text = "6",
                                font = self.btn_font,
                                command = lambda : self.num_button_press(6))
        self.num_7_btn = Button(self.num_7_frame, text = "7",
                                font = self.btn_font,
                                command = lambda : self.num_button_press(7))
        self.num_8_btn = Button(self.num_8_frame, text = "8",
                                font = self.btn_font,
                                command = lambda : self.num_button_press(8))
        self.num_9_btn = Button(self.num_9_frame, text = "9",
                                font = self.btn_font,
                                command = lambda : self.num_button_press(9))
        self.gen_btn = Button(self.gen_btn_frame, text = "Generate Grid",
                                font = self.btn_font,
                                command = self.generate_user_grid)

        
        # Buttons Sizes
        self.right_btn_width = right_btn_width
        self.right_btn_height = self.tile_size
         

    # Display Buttons
    def display_buttons(self, right_x, right_y, bot_x, bot_y, frame_pad):
        """
        A function to display the buttons for the user interaction.
        """
        # Right Buttons
        self.display_right_buttons(right_x, right_y, frame_pad)

        # Number buttons
        self.display_bottom_buttons(bot_x, bot_y, frame_pad, right_x)
        

    def display_right_buttons(self, x_pos, y_pos, frame_pad):
        """
        A function to display the right hand buttons.
        """    
        # Create a button frame list to iterate over
        frame_list = []
        frame_list.append(self.solve_btn_frame)
        frame_list.append(self.show_sol_btn_frame)
        frame_list.append(self.show_hint_btn_frame)
        frame_list.append(self.valid_entry_btn_frame)
        frame_list.append(self.clear_entry_btn_frame)
        frame_list.append(self.reset_btn_frame)

        # Create a button list to iterate over
        btn_list = []
        btn_list.append(self.solve_btn)
        btn_list.append(self.show_sol_btn)
        btn_list.append(self.show_hint_btn)
        btn_list.append(self.valid_entry_btn)
        btn_list.append(self.clear_entry_btn)
        btn_list.append(self.reset_btn)

        # Button frame positioning variables
        if len(frame_list) > 1 and len(btn_list) > 1:
            empty_y_space = self.grid_ui.grid_size - len(frame_list) * self.right_btn_height
            y_space = empty_y_space / (len(frame_list) - 1) + self.right_btn_height
        else: # In case there is only 1 button created in error
            y_space = 0

        if len(frame_list) == len(btn_list):
            for i in range(len(frame_list)):
                frame = frame_list[i]
                frame.place(x = x_pos - frame_pad,
                            y = y_pos - frame_pad,
                            width = self.right_btn_width + frame_pad * 2,
                            height = self.right_btn_height + frame_pad * 2)
                btn_list[i].place(x = frame_pad - frame["highlightthickness"],
                                    y = frame_pad - frame["highlightthickness"],
                                    width = self.right_btn_width,
                                    height = self.right_btn_height)
                y_pos += y_space
        
    def display_bottom_buttons(self, x_pos, y_pos, frame_pad, right_x):
        """
        A function to display the bottom row of buttons.
        """
        # Frame list
        num_frame_list = []
        num_frame_list.append(self.num_1_frame)
        num_frame_list.append(self.num_2_frame)
        num_frame_list.append(self.num_3_frame)
        num_frame_list.append(self.num_4_frame)
        num_frame_list.append(self.num_5_frame)
        num_frame_list.append(self.num_6_frame)
        num_frame_list.append(self.num_7_frame)
        num_frame_list.append(self.num_8_frame)
        num_frame_list.append(self.num_9_frame)

        # Button list
        num_btn_list = []
        num_btn_list.append(self.num_1_btn)
        num_btn_list.append(self.num_2_btn)
        num_btn_list.append(self.num_3_btn)
        num_btn_list.append(self.num_4_btn)
        num_btn_list.append(self.num_5_btn)
        num_btn_list.append(self.num_6_btn)
        num_btn_list.append(self.num_7_btn)
        num_btn_list.append(self.num_8_btn)
        num_btn_list.append(self.num_9_btn)

        num_btn_pad = 1 + frame_pad
        num_btn_size = self.tile_size - num_btn_pad * 2
        num_x_pos = x_pos + num_btn_pad - frame_pad
        num_y_pos = y_pos + num_btn_pad - frame_pad

        if len(num_frame_list) == len(num_btn_list):
            for i in range(len(num_frame_list)):
                frame = num_frame_list[i]
                frame.place(x = num_x_pos,
                            y = num_y_pos,
                            width = num_btn_size + frame_pad * 2,
                            height = num_btn_size + frame_pad * 2)
                num_btn_list[i].place(x = frame_pad - frame["highlightthickness"],
                                    y = frame_pad - frame["highlightthickness"],
                                    width = num_btn_size,
                                    height = num_btn_size)
                num_x_pos += self.tile_size

        gen_x_pos = right_x
        gen_y_pos = num_y_pos

        self.gen_btn_frame.place(x = gen_x_pos - frame_pad,
                                y = gen_y_pos,
                                width = self.right_btn_width + frame_pad * 2,
                                height = num_btn_size + frame_pad * 2)

        self.gen_btn.place(x = frame_pad,
                            y = frame_pad,
                            width = self.right_btn_width,
                            height = num_btn_size)

    
    # Button Functions
    def solve_btn_press(self):
        """
        A function to handle the user cliking on the solve button.
        Allows start/stop functionality depending on if the
        genetic algorithm is running
        """
        if self.ga_thread.is_alive():
            # GA running, stop the GA
            self.running_ga = False
            #self.output("\nStopped solving grid.\n\n")

        else:
            # Run the GA
            self.solve_grid()

    def solve_grid(self):
        """
        A function to handle the user clicking on the solve button to start.
        Checks user entry and begins the process for solving the grid
        """
        # Build grid class from user entry
        self.grid.user_rows.clear()
        self.grid.user_rows = self.grid_ui.get_user_rows()

        # Hard coded grid for testing
        #rows = []
        ##Easy
        #rows.append([0, 0, 4, 0, 0, 9, 0, 1, 8])
        #rows.append([0, 0, 1, 0, 0, 0, 0, 0, 9])
        #rows.append([0, 3, 0, 0, 8, 1, 0, 7, 6])
        #rows.append([0, 6, 0, 0, 0, 5, 2, 9, 7])
        #rows.append([0, 0, 0, 4, 0, 2, 0, 0, 0])
        #rows.append([7, 2, 3, 9, 0, 0, 0, 5, 0])
        #rows.append([5, 8, 0, 1, 9, 0, 0, 4, 0])
        #rows.append([1, 0, 0, 0, 0, 0, 9, 0, 0])
        #rows.append([3, 9, 0, 7, 0, 0, 8, 0, 0])
        #self.grid.user_rows = rows
        #self.grid_ui.update_changed_user_grid(self.grid)
        
        # Check user entry follows sudoku rules for duplicates
        if self.grid.check_user_grid():
            # Confirm user choice to continue
            title = "Confirmation to start"
            message = "Ready to find the solution?\n"
            message += "Click 'Yes' to start.\n"
            message += "Click 'No' to return to entry."
            

            if self.message_box(title, message, "yesno"):
                # Run GA
                self.running_ga = True
                self.ga_thread = threading.Thread(target=self.run_ga)
                self.ga_thread.daemon = True
                self.ga_thread.start()

        else: # Grid isn't valid, show message box to user
            error_title = "Values Entered Conflict"
            error_message = "Duplicate values found in a\n"
            error_message += "row, column or 3x3 box.\n"
            error_message += "Please check entry is correct."
            
            self.message_box(error_title, error_message, "ok")

    def run_ga(self):
        """
        A function to handle running the genetic algorithm to
        complete the grid
        """
        # Update solve and reset buttons and disable grid to prevent entry
        self.solve_btn["text"] = "STOP"
        self.grid_ui.disable_grid()
        self.reset_btn["state"] = "disabled"

        # Disable the number buttons
        num_btn_list = []
        num_btn_list.append(self.num_1_btn)
        num_btn_list.append(self.num_2_btn)
        num_btn_list.append(self.num_3_btn)
        num_btn_list.append(self.num_4_btn)
        num_btn_list.append(self.num_5_btn)
        num_btn_list.append(self.num_6_btn)
        num_btn_list.append(self.num_7_btn)
        num_btn_list.append(self.num_8_btn)
        num_btn_list.append(self.num_9_btn)
        num_btn_list.append(self.gen_btn)

        for btn in num_btn_list:
            btn["state"] = "disable"

        self.output("Solving...\nClick 'STOP' to stop solving.\n\n")
        
        # Run the GA in its own thread
        solver = gsol.GridSolver(self.grid, self.output)
        solve_thread = threading.Thread(target = solver.run)
        solve_thread.daemon = True
        solve_thread.start()

        # Wait for the GA thread to finish itself or when stopped by user
        while solve_thread.is_alive():
            self.ui.update()
            if not self.running_ga:
                solver.thread_running = False
        
        # Update grid ui based on solution found
        # Re-enable the grid and reset Solve button
        if solver.solved:
            self.grid_ui.enable_grid_solved()
        else:
            self.grid_ui.enable_grid()

        self.solve_btn["text"] = "START"
        self.reset_btn["state"] = "normal"
        for btn in num_btn_list:
            btn["state"] = "normal"
        
        # Set button states if solved
        if solver.solved:
            self.solve_btn["state"] = "disabled"
            self.show_sol_btn["state"] = "normal"
            self.show_hint_btn["state"] = "normal"
            self.valid_entry_btn["state"] = "normal"
            self.clear_entry_btn["state"] = "normal"
            self.gen_btn["state"] = "disabled"

            # Output new instructions to user
            message = "Click 'Show Solution' to display the solution.\n"
            message += "Click 'Show Hint' to display a random cell solution.\n"
            message += "Click 'Validate' after entering some attempts to check if correct.\n"
            message += "Click 'Clear Entries' to remove values not part of the original puzzle.\n"
            message += "Click 'RESET GRID' to begin again.\n\n"
            self.output(message)
    
    def show_solution(self):
        """
        A function to handle the user clicking the
        'Show Solution' button and displaying the solution
        on the grid
        """
        # Update grid
        self.grid_ui.update_grid_solution_ui(self.grid)
        #print("solution shown")
        self.output("Solution shown.\nClick 'RESET GRID' to begin again.\n")
        
        # Update button states
        self.solve_btn["state"] = "disabled"
        self.show_sol_btn["state"] = "disabled"
        self.show_hint_btn["state"] = "disabled"
        self.valid_entry_btn["state"] = "disabled"
        self.clear_entry_btn["state"] = "disabled"

    def show_hint(self):
        """
        A function to handle the user clicking on the
        'Hint' button. Checks the displayed grid for unsolved
        cells and randomly fills one in.
        """
        self.grid_ui.show_hint(self.grid, self.output)

    def validate_user_entry(self):
        """
        A function to handle the user clicking on the
        'Validate' button. Checks the displayed grid for
        entries that are not part of the initial clues
        and checks for correctness. Changes the cell
        background depending on correctness.
        """
        self.grid_ui.validate_user_entry(self.grid)

        self.output("Entries validated.\n")
        self.output("Green", "valid")
        self.output(" = Correct\n")
        self.output("Red", "invalid")
        self.output(" = Wrong\n\n")

    def clear_entries(self):
        """
        A function to handle the user clicking on the 'Clear Entries' button.
        Resets any cells that are not part of the initial clues.
        """
        self.grid_ui.clear_entries(self.grid)

        self.output("All entries cleared.\n\n")

    def reset_grid(self):
        """
        A function to handle the user clicking on the 'RESET GRID' button.
        Resets all elements back to initial run state.
        """
        # Reset grid
        self.grid_ui.reset_grid()

        # Reset buttons
        self.solve_btn["state"] = "normal"
        self.show_sol_btn["state"] = "disabled"
        self.show_hint_btn["state"] = "disabled"
        self.valid_entry_btn["state"] = "disabled"
        self.clear_entry_btn["state"] = "disabled"
        self.gen_btn["state"] = "normal"

        # Reset output window
        self.output.init_output_box()

    def num_button_press(self, num : int):
        """
        A function to handle the user clicking on a number button
        and placing the value into the currently selected cell.
        """
        focused_entry = self.ui.focus_get()
        if type(focused_entry) == Entry:
            focused_entry.delete(0, END)
            focused_entry.insert(0, num)

    def generate_user_grid(self):
        """
        A function to handle the user clicking on the 'Generate'
        button.
        """
        # Display confirmation to user
        title = "Generate A Grid"
        message = "Would you like to generate a grid?"
        if self.message_box(title, message, "yesno"):
            title = "Choose A Difficulty"
            message = "Choose the difficulty for the puzzle."
            difficulty = str(self.message_box(title, message, "difficulty"))
            if self.generator.generate(difficulty):
                self.grid.user_rows.clear()
                self.grid.user_rows = self.generator.grid
                # Update the display
                self.grid_ui.update_changed_user_grid(self.grid)
                output_msg = "Grid generated successfully!\n"
                output_msg += f"Difficulty = {difficulty.capitalize()}\n\n"
            else:
                output_msg = "There was an issue communicating with the server!\n\n"
            self.output(output_msg)




