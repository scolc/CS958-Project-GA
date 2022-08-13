from typing import Callable
import ga_solver as ga
import sudoku_grid as sg
import time


class GridSolver():
    """
    A class to handle the solve operation for the grid.
    Requires the genetic algorithm class and a passed grid object.
    """

    def __init__(self, grid: sg.SudokuGrid, output: Callable):
        self.grid = grid
        self.solved = False
        self.thread_running = True  # Changed to False when a stop is needed
        self.output = output  # Output function from GUI to allow feedback

    def run(self):
        """
        A function that handles running the genetic algorithm on the grid
        """
        running = True  # Becomes False when the ga should stop
        running_attempts = 0  # Counts the process repetitions
        self.solved = False  # Becomes True when the solution is found
        start_time = time.time()

        # Inititialise the current solution state from user entry
        self.grid.current_solution.clear()
        for entry in self.grid.user_rows:
            this_row = []
            for cell in entry:
                this_row.append(cell)
            self.grid.current_solution.append(this_row)

        while running:
            solvable = self.setup_phase_1()
            can_p2 = False
            can_p3 = False

            if solvable:
                running_attempts += 1
                self.output(f"Attempt {running_attempts}:\n")

                # Phase 1, find possible rows if not already solved in setup
                if self.thread_running and not self.solved:
                    self.output("        Phase 1 ")
                    can_p2 = self.run_phase_1()

                # Phase 2, find possible box rows
                if self.thread_running and not self.solved:
                    if can_p2:
                        self.output(" Ok\n        Phase 2 ")
                        can_p3 = self.run_phase_2()
                    else:
                        self.output(" X")

                # Phase 3, try to solve the grid
                if self.thread_running:
                    if can_p3:
                        self.output(" Ok\n        Phase 3 ")
                        self.solved = self.run_phase_3()

                        if self.thread_running:
                            if self.solved:
                                self.output(" Ok")
                            else:
                                self.output(" X")
                    else:
                        if can_p2:
                            self.output(" X")

                if self.thread_running:
                    self.output("\n")

                    # Solved condition
                    if self.solved:
                        running = False
                        message = ("Valid solution found after " +
                                   f"{running_attempts} attempt")

                        if running_attempts > 1:
                            message += "s"

                        end_time = time.time()
                        time_dif = end_time - start_time
                        message += ("!\nSolver ran for " +
                                    f"{self.convert_time(time_dif)}.\n\n")
                        self.output(message)
                    else:
                        updated = False

                        # Update the solution depending on phases complete
                        if can_p3:  # Phase 2 completed ok
                            self.check_boxes()
                            updated = self.check_rows()
                        elif can_p2:  # Only phase 1 completed ok
                            updated = self.check_rows()

                        # Run max 5 attempts unless still updating
                        if updated:
                            self.output
                            end_time = time.time()
                            time_dif = end_time - start_time
                            message = ("Found part of the solution, " +
                                       "starting new attempt.\n" +
                                       "Current time elapsed: " +
                                       f"{self.convert_time(time_dif)}.\n\n")
                            self.output(message)
                        elif running_attempts >= 5:
                            running = False
                            end_time = time.time()
                            time_dif = end_time - start_time
                            message = ("Unable to find the solution after " +
                                       f"{running_attempts} attempts.\n" +
                                       "Solver ran for " +
                                       f"{self.convert_time(time_dif)}.\n\n")
                            self.output(message)
                        else:
                            end_time = time.time()
                            time_dif = end_time - start_time
                            message = ("Didn't find anything this try, " +
                                       "starting new attempt.\n" +
                                       "Current time elapsed: " +
                                       f"{self.convert_time(time_dif)}.\n\n")
                            self.output(message)
                else:  # Thread is stopping
                    running = False
                    self.output("\nStopped solving grid.\n\n")

            else:
                running = False
                end_time = time.time()
                message = ("Unable to find the solution.\n" +
                           "Got stuck due to conflicts in cell values.\n" +
                           "Check that grid entry is correct.\n" +
                           "Click 'START' when ready to try again.\n" +
                           "Solver ran for " +
                           f"{self.convert_time(end_time - start_time)}.\n\n")
                self.output(message)

    def check_boxes(self):
        """
        A function to check if box rows returned during phase 2
        shared a common row indicating a solved row and updates
        the lists used for checking rows.
        """
        for box_row_index in range(3):
            this_box_row = self.grid.ga_p3_pos_box_rows[box_row_index]

            # Separate individual rows of the box row, store the unique rows
            top = []
            mid = []
            bot = []
            for entry in this_box_row:
                if top.count(entry[0]) == 0:
                    top.append(entry[0])
                if mid.count(entry[1]) == 0:
                    mid.append(entry[1])
                if bot.count(entry[2]) == 0:
                    bot.append(entry[2])

            # Check if the returned rows for each position were a single row
            if len(top) == 1:
                self.grid.ga_p2_pos_rows[box_row_index*3].clear()
                self.grid.ga_p2_pos_rows[box_row_index*3] = top

            if len(mid) == 1:
                self.grid.ga_p2_pos_rows[(box_row_index*3) + 1].clear()
                self.grid.ga_p2_pos_rows[(box_row_index*3) + 1] = mid

            if len(bot) == 1:
                self.grid.ga_p2_pos_rows[(box_row_index*3) + 2].clear()
                self.grid.ga_p2_pos_rows[(box_row_index*3) + 2] = bot

    def check_rows(self):
        """
        A function to check if each row returned during phase 1
        share possible rows with a common cell indicating a solved cell
        """
        grid_updated = False

        for row_index in range(9):
            this_pos_row = self.grid.ga_p2_pos_rows[row_index]
            temp_row = []
            row_updated = False

            for index in range(9):  # each index for a row
                temp_entries = []

                # Check each entry in the possible row list
                for entry in this_pos_row:
                    if temp_entries.count(entry[index]) == 0:
                        temp_entries.append(entry[index])
                if len(temp_entries) == 1:  # Same digit in same cell
                    temp_row.append(temp_entries[0])
                else:  # Different digits in same cell so not possible solution
                    temp_row.append(0)

            # Check the temp_row against the current solution
            temp_solution_row = [0] * 9
            for sol_index in range(9):  # Each cell
                current_row = self.grid.current_solution[row_index]
                if (current_row[sol_index] == 0 and
                        temp_row[sol_index] > 0):  # Entry is possible solution
                    temp_solution_row[sol_index] = temp_row[sol_index]
                    row_updated = True
                else:  # Keep the current solution
                    temp_solution_row[sol_index] = current_row[sol_index]

            # Check each entry above 0 in temp_solution_row is unique
            row_ok = True
            for entry_index in range(9):
                this_entry = temp_solution_row[entry_index]
                if this_entry > 0 and temp_solution_row.count(this_entry) > 1:
                    # Error occurred
                    row_ok = False

            # All entries in temp_solution_row are 0 or unique digit 1 - 9
            if row_ok:
                self.grid.current_solution[row_index].clear()
                self.grid.current_solution[row_index] = temp_solution_row

                # Set the grid updated status
                if row_updated:
                    grid_updated = True

        return grid_updated

    def setup_phase_1(self):
        """
        A function to check the grid for possible cell values
        and setup phase 1
        """
        updating = True
        self.grid.ga_p1_pos_cells = [[[0]] * 9] * 9

        while updating:
            updating = False
            column_grid = self.grid.get_columns(self.grid.current_solution)
            box_grid = self.grid.get_boxes(self.grid.current_solution)

            # Check for possible entries in each cell
            for row_num in range(9):
                this_row = self.grid.current_solution[row_num]
                temp_row = []

                for col_num in range(9):
                    cell = this_row[col_num]
                    cell_vals = []
                    if cell > 0:  # Cell has been set
                        cell_vals.append(cell)
                    else:
                        this_col = column_grid[col_num]
                        box_top_row = row_num - (row_num % 3)
                        box_left_col = col_num - (col_num % 3)
                        this_box = box_grid[box_top_row +
                                            int(box_left_col / 3)]

                        # Check for digits missing in the row, column or box
                        for num in range(9):
                            if (this_row.count(num + 1) == 0 and
                                    this_col.count(num + 1) == 0 and
                                    this_box.count(num + 1) == 0):
                                cell_vals.append(num + 1)

                    # Check if cell_vals has been filled
                    if cell_vals:
                        temp_row.append(cell_vals)
                    else:  # cell_vals is empty so error occurred
                        return False

                # Check if temp_row has new solved entries for any cells
                for index in range(9):
                    if len(temp_row[index]) == 1 and this_row[index] == 0:
                        # New solved cell, update current solution
                        this_row[index] = temp_row[index][0]
                        updating = True

                if updating:
                    break  # restart
                else:  # Solution not updated so set phase 1 possible cells
                    self.grid.ga_p1_pos_cells[row_num].clear()
                    self.grid.ga_p1_pos_cells[row_num] = temp_row

        # Check if the solution has been found
        self.solved = self.grid.check_solution()
        return True

    def run_phase_1(self):
        """
        A function to handle running the genetic algorithm
        to find possible rows
        """
        self.grid.phase = 1
        self.grid.ga_p2_pos_rows.clear()

        # Run each row through ga
        for row_num in range(len(self.grid.ga_p1_pos_cells)):
            self.grid.current_row = row_num
            cell_values = self.grid.ga_p1_pos_cells[row_num]
            possible_rows = self.run_ga_solver(cell_values)

            # Convert possible_row indices to their corresponding values
            if possible_rows:
                converted_rows = []

                for entry in possible_rows:
                    temp_row = []
                    current_row = self.grid.ga_p1_pos_cells[row_num]
                    entry_index = 0

                    for cell_vals in current_row:
                        temp_row.append(cell_vals[entry[entry_index]])
                        entry_index += 1
                    converted_rows.append(temp_row)

                self.grid.ga_p2_pos_rows.append(converted_rows)
            else:  # Possible rows is empty so error occurred
                return False

        return True

    def run_phase_2(self):
        """
        A function to handle running the genetic algorithm
        to find possible box rows
        """
        self.grid.phase = 2
        self.grid.ga_p3_pos_box_rows.clear()

        # Run each set of 3 rows through the ga to see which groupings work
        for box_row in range(3):
            self.grid.current_row = box_row
            possible_rows = []

            # Get the rows depending on box_row, 0 is top 3, 1 is mid, 2 is bot
            possible_rows.append(self.grid.ga_p2_pos_rows[box_row * 3])
            possible_rows.append(self.grid.ga_p2_pos_rows[(box_row * 3) + 1])
            possible_rows.append(self.grid.ga_p2_pos_rows[(box_row * 3) + 2])

            possible_box_rows = self.run_ga_solver(possible_rows)

            # Convert possible box indices into their corresponding lists
            if possible_box_rows:
                converted_boxes = []

                for entry in possible_box_rows:
                    pos_box_row = []
                    for index in range(len(entry)):
                        pos_box_row.append(self.grid.ga_p2_pos_rows
                                           [(box_row * 3) + index]
                                           [entry[index]])
                    converted_boxes.append(pos_box_row)

                self.grid.ga_p3_pos_box_rows.append(converted_boxes)
            else:  # possible_box_rows is empty, no box rows returned
                return False

        return True

    def run_phase_3(self):
        """
        A function to handle running the genetic algorithm
        to find the grid solution
        """
        self.grid.phase = 3
        solved = False

        # Pass the possible box rows to find possible solution
        solution = self.run_ga_solver(self.grid.ga_p3_pos_box_rows)

        # Check if a solution was found and update the current solution
        if solution:
            # Get box rows
            temp_grid = []
            entry = solution[0]  # Only 1 solution required
            box_rows = []

            for index in range(3):
                box_rows.append(self.grid.ga_p3_pos_box_rows
                                [index][entry[index]])

            # Unpack rows
            for row in box_rows:
                for entry in row:
                    temp_grid.append(entry)

            # Update current solution
            self.grid.current_solution.clear()
            self.grid.current_solution = temp_grid
            solved = True

        return solved

    def run_ga_solver(self, values: list):
        """
        A function that runs the genetic algorithm with given values.
        Returns the results of the genetic algorithm as a list.
        """
        limit_list = []

        # Get the index range of stored cell values
        for entry in values:
            max = len(entry)
            limit_list.append((0, max-1, int))

        # Produce list of possible indices
        # Multiple attempts to increase unique results depending on phase
        attempts = [50, 20, 3]
        points = [40, 100, 500]
        results = []
        solver = ga.GaSolver(f=self.grid,
                             limits=limit_list,
                             mutation=0.2,
                             deletion=0.2)

        for _ in range(attempts[self.grid.phase - 1]):
            if self.thread_running:
                solver.solve(n_iterations=30,
                             n_initial_points=points[self.grid.phase - 1])
                for point in solver.population:
                    if point.fitness == 100:
                        if results.count(point.parameters) == 0:  # unique
                            results.append(point.parameters)

        self.output(".")
        return results

    def convert_time(self, run_time: int):
        """
        A function to convert a run time in seconds into
        minutes and seconds and returns it as a string.
        """
        minutes = int(run_time / 60)
        seconds = int(run_time % 60)
        result = ""

        if minutes > 0:
            result += f"{minutes} minute"
            if minutes > 1:
                result += "s"
            result += " "

        if seconds < 10:
            result += "0"

        result += f"{seconds} second"
        if not seconds == 1:
            result += "s"
        return result
