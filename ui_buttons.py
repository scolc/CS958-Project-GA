import threading
from tkinter import *

import sudoku_grid as sg
import grid_solver as gsol
import gui
import ui_grid
import sudoku_generator as gen
import ui_output_box
import ui_message_box


class UIButtons():
    """
    A class to handle the button UI elements and running the general
    program functionality.
    """

    def __init__(self, ui: Tk,
                 tile_size: int,
                 grid_ui: ui_grid,
                 output_box: ui_output_box):
        self.ui = ui
        self.tile_size = tile_size
        self.grid_ui = grid_ui
        self.colours = gui.Colours()
        self.grid = sg.SudokuGrid()
        self.output = output_box
        self.generator = gen.SudokuGenerator()
        self.running_ga = False
        self.ga_thread = threading.Thread()
        self.message_box = ui_message_box.UIMessageBox(ui=self.ui,
                                                       tile_size=tile_size)

        self.btn_font = "Calibri " + str(int(tile_size / 2.5))

        # Buttons
        # Right Buttons
        self.solve_btn = Button()
        self.show_sol_btn = Button()
        self.show_hint_btn = Button()
        self.valid_entry_btn = Button()
        self.clear_entry_btn = Button()
        self.reset_btn = Button()
        #self.gen_btn = Button()

        # Number Buttons
        self.num_1_btn = Button()
        self.num_2_btn = Button()
        self.num_3_btn = Button()
        self.num_4_btn = Button()
        self.num_5_btn = Button()
        self.num_6_btn = Button()
        self.num_7_btn = Button()
        self.num_8_btn = Button()
        self.num_9_btn = Button()

    # Display Buttons

    def display_buttons(self, right_x, right_y, right_width,
                        num_x, num_y, frame_pad):
        """
        A function to display the buttons for the user interaction.
        """
        # Right Buttons
        self.display_right_buttons(right_x, right_y, right_width, frame_pad)

        # Number buttons
        self.display_number_buttons(num_x, num_y, frame_pad)

    def display_right_buttons(self, x_pos, y_pos, width, frame_pad):
        """
        A function to display the right hand buttons.
        """
        # Frame list
        fg_col = self.colours.fg_en_norm
        solve_btn_frame = Frame(self.ui,
                                bg=self.colours.bg_en_norm,
                                highlightthickness=1,
                                highlightbackground=fg_col)
        show_sol_btn_frame = Frame(self.ui,
                                   bg=self.colours.bg_en_norm,
                                   highlightthickness=1,
                                   highlightbackground=fg_col)
        show_hint_btn_frame = Frame(self.ui,
                                    bg=self.colours.bg_en_norm,
                                    highlightthickness=1,
                                    highlightbackground=fg_col)
        valid_entry_btn_frame = Frame(self.ui,
                                      bg=self.colours.bg_en_norm,
                                      highlightthickness=1,
                                      highlightbackground=fg_col)
        clear_entry_btn_frame = Frame(self.ui,
                                      bg=self.colours.bg_en_norm,
                                      highlightthickness=1,
                                      highlightbackground=fg_col)
        reset_btn_frame = Frame(self.ui,
                                bg=self.colours.bg_en_norm,
                                highlightthickness=1,
                                highlightbackground=fg_col)
        #gen_btn_frame = Frame(self.ui,
        #                      bg=self.colours.bg_en_norm,
        #                      highlightthickness=1,
        #                      highlightbackground=fg_col)
        frame_list = []
        frame_list.append(solve_btn_frame)
        frame_list.append(show_sol_btn_frame)
        frame_list.append(show_hint_btn_frame)
        frame_list.append(valid_entry_btn_frame)
        frame_list.append(clear_entry_btn_frame)
        frame_list.append(reset_btn_frame)
        #frame_list.append(gen_btn_frame)

        # Button list
        self.solve_btn = Button(solve_btn_frame,
                                text="START",
                                font=self.btn_font,
                                command=self.solve_btn_press)
        self.show_sol_btn = Button(show_sol_btn_frame,
                                   text="Show Solution",
                                   font=self.btn_font,
                                   command=self.show_solution,
                                   state="disabled")
        self.show_hint_btn = Button(show_hint_btn_frame,
                                    text="Show Hint",
                                    font=self.btn_font,
                                    command=self.show_hint,
                                    state="disabled")
        self.valid_entry_btn = Button(valid_entry_btn_frame,
                                      text="Validate",
                                      font=self.btn_font,
                                      command=self.validate_user_entry,
                                      state="disabled")
        self.clear_entry_btn = Button(clear_entry_btn_frame,
                                      text="Clear Entries",
                                      font=self.btn_font,
                                      command=self.clear_entries,
                                      state="disabled")
        self.reset_btn = Button(reset_btn_frame,
                                text="RESET GRID",
                                font=self.btn_font,
                                command=self.reset_grid)
        #self.gen_btn = Button(gen_btn_frame,
        #                      text="Generate Grid",
        #                      font=self.btn_font,
        #                      command=self.generate_user_grid)
        btn_list = []
        btn_list.append(self.solve_btn)
        btn_list.append(self.show_sol_btn)
        btn_list.append(self.show_hint_btn)
        btn_list.append(self.valid_entry_btn)
        btn_list.append(self.clear_entry_btn)
        btn_list.append(self.reset_btn)
        #btn_list.append(self.gen_btn)

        self.place_buttons(frames=frame_list,
                           buttons=btn_list,
                           btn_x=x_pos,
                           btn_y=y_pos,
                           btn_width=width,
                           pad=frame_pad)

    def display_number_buttons(self, x_pos, y_pos, frame_pad):
        """
        A function to display the bottom row of buttons.
        """
        # Frame list
        num_1_frame = Frame(self.ui,
                            bg=self.colours.bg_en_norm,
                            highlightthickness=1,
                            highlightbackground=self.colours.fg_en_norm)
        num_2_frame = Frame(self.ui,
                            bg=self.colours.bg_en_norm,
                            highlightthickness=1,
                            highlightbackground=self.colours.fg_en_norm)
        num_3_frame = Frame(self.ui,
                            bg=self.colours.bg_en_norm,
                            highlightthickness=1,
                            highlightbackground=self.colours.fg_en_norm)
        num_4_frame = Frame(self.ui,
                            bg=self.colours.bg_en_norm,
                            highlightthickness=1,
                            highlightbackground=self.colours.fg_en_norm)
        num_5_frame = Frame(self.ui,
                            bg=self.colours.bg_en_norm,
                            highlightthickness=1,
                            highlightbackground=self.colours.fg_en_norm)
        num_6_frame = Frame(self.ui,
                            bg=self.colours.bg_en_norm,
                            highlightthickness=1,
                            highlightbackground=self.colours.fg_en_norm)
        num_7_frame = Frame(self.ui,
                            bg=self.colours.bg_en_norm,
                            highlightthickness=1,
                            highlightbackground=self.colours.fg_en_norm)
        num_8_frame = Frame(self.ui,
                            bg=self.colours.bg_en_norm,
                            highlightthickness=1,
                            highlightbackground=self.colours.fg_en_norm)
        num_9_frame = Frame(self.ui,
                            bg=self.colours.bg_en_norm,
                            highlightthickness=1,
                            highlightbackground=self.colours.fg_en_norm)
        frame_list = []
        frame_list.append(num_1_frame)
        frame_list.append(num_2_frame)
        frame_list.append(num_3_frame)
        frame_list.append(num_4_frame)
        frame_list.append(num_5_frame)
        frame_list.append(num_6_frame)
        frame_list.append(num_7_frame)
        frame_list.append(num_8_frame)
        frame_list.append(num_9_frame)

        # Button list
        num_1_btn = Button(num_1_frame, text="1",
                           font=self.btn_font,
                           command=lambda: self.num_button_press(1))
        num_2_btn = Button(num_2_frame, text="2",
                           font=self.btn_font,
                           command=lambda: self.num_button_press(2))
        num_3_btn = Button(num_3_frame, text="3",
                           font=self.btn_font,
                           command=lambda: self.num_button_press(3))
        num_4_btn = Button(num_4_frame, text="4",
                           font=self.btn_font,
                           command=lambda: self.num_button_press(4))
        num_5_btn = Button(num_5_frame, text="5",
                           font=self.btn_font,
                           command=lambda: self.num_button_press(5))
        num_6_btn = Button(num_6_frame, text="6",
                           font=self.btn_font,
                           command=lambda: self.num_button_press(6))
        num_7_btn = Button(num_7_frame, text="7",
                           font=self.btn_font,
                           command=lambda: self.num_button_press(7))
        num_8_btn = Button(num_8_frame, text="8",
                           font=self.btn_font,
                           command=lambda: self.num_button_press(8))
        num_9_btn = Button(num_9_frame, text="9",
                           font=self.btn_font,
                           command=lambda: self.num_button_press(9))
        btn_list = []
        btn_list.append(num_1_btn)
        btn_list.append(num_2_btn)
        btn_list.append(num_3_btn)
        btn_list.append(num_4_btn)
        btn_list.append(num_5_btn)
        btn_list.append(num_6_btn)
        btn_list.append(num_7_btn)
        btn_list.append(num_8_btn)
        btn_list.append(num_9_btn)

        btn_width = self.tile_size

        self.place_buttons(frames=frame_list,
                           buttons=btn_list,
                           btn_x=x_pos,
                           btn_y=y_pos,
                           btn_width=btn_width,
                           pad=frame_pad)

    def place_buttons(self, frames, buttons, btn_x, btn_y, btn_width, pad):
        """
        A function to place a list of buttons along the y axis.
        """
        # Button frame positioning variables
        if len(frames) > 1 and len(buttons) > 1:
            # Set button heights to fit grid size or use tile_size
            if len(frames) >= 9:
                btn_pad = 1 + pad
                btn_height = self.grid_ui.grid_size / len(frames) - btn_pad * 2
            else:
                btn_height = self.tile_size

            empty_y_space = self.grid_ui.grid_size - len(frames) * btn_height
            y_space = empty_y_space / (len(frames) - 1) + btn_height
        else:  # In case there is only 1 button created
            y_space = 0

        # Make sure there are the same number of frames and buttons
        if len(frames) == len(buttons):
            for i in range(len(frames)):
                frame = frames[i]
                frame.place(x=btn_x - pad,
                            y=btn_y - pad,
                            width=btn_width + pad * 2,
                            height=btn_height + pad * 2)
                buttons[i].place(x=pad - frame["highlightthickness"],
                                 y=pad - frame["highlightthickness"],
                                 width=btn_width,
                                 height=btn_height)
                btn_y += y_space

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

        else:  # Grid isn't valid, show message box to user
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
        #num_btn_list.append(self.gen_btn)

        for btn in num_btn_list:
            btn["state"] = "disable"

        self.output("Solving...\nClick 'STOP' to stop solving.\n\n")

        # Run the GA in its own thread
        solver = gsol.GridSolver(self.grid, self.output)
        solve_thread = threading.Thread(target=solver.run)
        solve_thread.daemon = True
        solve_thread.start()

        # Wait for the GA thread to finish itself or when stopped by user
        while solve_thread.is_alive():
            self.ui.update()
            if not self.running_ga:
                solver.thread_running = False

        # Update ui based on solution found
        # Reset button states
        self.solve_btn["text"] = "START"
        self.reset_btn["state"] = "normal"
        for btn in num_btn_list:
            btn["state"] = "normal"

        # Re-enable the grid, reset Solve button, enable buttons if solved
        if solver.solved:
            self.grid_ui.enable_grid_solved()
            self.solve_btn["state"] = "disabled"
            self.show_sol_btn["state"] = "normal"
            self.show_hint_btn["state"] = "normal"
            self.valid_entry_btn["state"] = "normal"
            self.clear_entry_btn["state"] = "normal"
            #self.gen_btn["state"] = "disabled"

            # Output new instructions to user
            message = ("Click 'Show Solution' to display the solution.\n" +
                       "Click 'Show Hint' to display a random cell " +
                       "solution.\n" +
                       "Click 'Validate' after entering some attempts to " +
                       "check if they are correct.\n" +
                       "Click 'Clear Entries' to remove values not part of " +
                       "the original puzzle.\n" +
                       "Click 'RESET GRID' to begin again.\n\n")
            self.output(message)
        else:
            self.grid_ui.enable_grid()

    def show_solution(self):
        """
        A function to handle the user clicking the
        'Show Solution' button and displaying the solution
        on the grid
        """
        # Update grid
        self.grid_ui.update_grid_solution_ui(self.grid)
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
        #self.gen_btn["state"] = "normal"

        # Reset output window
        self.output.init_output_box()

    def num_button_press(self, num: int):
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
        # Display confirmation dialogue to user
        title = "Generate A Grid"
        message = "Would you like to generate a grid?"
        if self.message_box(title, message, "yesno"):
            generator = threading.Thread(target=lambda: self.run_generator())
            generator.daemon = True
            generator.start()

    def run_generator(self):
        """
        A function to handle the grid generation in a thread.
        """
        # Disable user interaction
        btn_list = []
        btn_list.append(self.num_1_btn)
        btn_list.append(self.num_2_btn)
        btn_list.append(self.num_3_btn)
        btn_list.append(self.num_4_btn)
        btn_list.append(self.num_5_btn)
        btn_list.append(self.num_6_btn)
        btn_list.append(self.num_7_btn)
        btn_list.append(self.num_8_btn)
        btn_list.append(self.num_9_btn)
        #btn_list.append(self.gen_btn)
        btn_list.append(self.solve_btn)
        btn_list.append(self.reset_btn)

        for btn in btn_list:
            btn["state"] = "disable"
        self.grid_ui.disable_grid()

        self.output("Contacting server to generate grid...\n")

        if self.generator.generate():
            self.grid.user_rows.clear()
            self.grid.user_rows = self.generator.grid
            # Update the display
            self.grid_ui.update_changed_user_grid(self.grid)
            message = "Grid generated successfully!\n"
        else:
            message = "There was an issue communicating with the server!\n\n"
        self.output(message)

        # Re-enable user interaction
        for btn in btn_list:
            btn["state"] = "normal"
        self.grid_ui.enable_grid()
