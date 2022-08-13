class SudokuGrid:
    """
    A class to represent a 9x9 sudoku grid.
    Contains a callable function to act as
    the fitness function for the genetic algorithm.
    """

    def __init__(self):
        self.user_rows = []
        self.current_solution = []
        self.ga_p1_pos_cells = []
        self.ga_p2_pos_rows = []
        self.ga_p3_pos_box_rows = []

        for _ in range(9):
            this_row = [0] * 9
            self.user_rows.append(this_row)

        self.current_row = 0
        self.phase = 0

    def __repr__(self):
        result = "Grid\n"
        rownum = 0

        for row in self.user_rows:
            rownum += 1
            cellnum = 0

            for cell in row:
                cellnum += 1
                result += f"[{cell}] "
                if cellnum % 3 == 0 and cellnum < 9:
                    result += " |  "

            result += "\n"
            if rownum % 3 == 0 and rownum < 9:
                result += "--- " * 11
                result += "\n"

        return result

    def __call__(self, params):
        """
        A function that allows the fitness function to be called
        and returns the fitness value.
        """
        return self.fitness(params)

    def fitness(self, params):
        """
        A function that calculates the fitness value for parameters
        from a genetic algorithm.
        """
        if self.phase == 1:  # Cells
            temp_row = []
            param_index = 0
            max_fitness = 9

            # Build a row
            for cell in self.ga_p1_pos_cells[self.current_row]:
                temp_row.append(cell[params[param_index]])
                param_index += 1

            return self.calculate_fitness([temp_row]) / max_fitness * 100

        elif self.phase == 2:  # Boxes
            temp_box_row = []
            max_fitness = 27

            # Build box row
            for index in range(3):
                temp_box_row.append(self.ga_p2_pos_rows
                                    [(self.current_row * 3) + index]
                                    [params[index]])

            return self.fitness_box_row(temp_box_row) / max_fitness * 100

        elif self.phase == 3:  # Grid
            temp_grid = []
            max_fitness = 81

            # Build a grid
            for index in range(len(params)):
                temp_box_row = self.ga_p3_pos_box_rows[index][params[index]]
                for entry in temp_box_row:
                    temp_grid.append(entry)

            return self.fitness_columns(temp_grid) / max_fitness * 100
        else:
            return 0

    def fitness_columns(self, grid):
        """
        A function that returns total fitness for each column in a grid
        """
        col_list = self.get_columns(grid)
        return self.calculate_fitness(col_list)  # max 81

    def fitness_box_row(self, box_row):
        """
        A function that takes a list representing a box row
        and returns a fitness value
        """
        box_list = self.get_box_row(box_row)
        return self.calculate_fitness(box_list)  # max 27

    def calculate_fitness(self, grid):
        """
        A function that takes a list representing a grid configuration
        of rows, columns or boxes and returns a fitness value
        """
        fitness = 0

        # Base fitness on number of unique digits, 9 max
        for entry in grid:
            fitness += len(set(entry))

            # Remove fitness caused by 0 in the set
            if entry.count(0) > 0:
                fitness -= 1

        return fitness

    def get_columns(self, grid):
        """
        A function that creates and returns a list
        of the columns in a grid
        """
        col_list = []

        for col_num in range(9):
            this_col = []

            for row_num in range(9):
                this_col.append(grid[row_num][col_num])

            col_list.append(this_col)

        return col_list

    def get_boxes(self, grid):
        """
        A function that creates and returns a list
        of the boxes in a grid
        """
        box_list = []
        box_row = []

        for box_row_num in range(3):  # 3 rows - 0,1,2
            box_row.clear()
            box_row.append(grid[box_row_num * 3])
            box_row.append(grid[box_row_num * 3 + 1])
            box_row.append(grid[box_row_num * 3 + 2])
            box_list += self.get_box_row(box_row)

        return box_list

    def get_box_row(self, box_row):
        """
        A function that takes a box row and returns
        the three boxes as a list of 3 box lists
        """
        box_row_list = []

        for box_col in range(3):
            box_row_list.append(box_row[0][box_col * 3: (box_col * 3) + 3] +
                                box_row[1][box_col * 3: (box_col * 3) + 3] +
                                box_row[2][box_col * 3: (box_col * 3) + 3])

        return box_row_list

    def check_solution(self):
        """
        A function to check if the current solution has
        been completed and returns True or False
        """
        boxes = self.get_boxes(self.current_solution)
        fitness = 0

        # Check all cells are filled
        for row in self.current_solution:
            if row.count(0) > 0:
                return False  # Empty cells found

        # Check solution is valid
        fitness += self.calculate_fitness(self.current_solution)
        fitness += self.fitness_columns(self.current_solution)
        fitness += self.calculate_fitness(boxes)

        return fitness == 3 * 81  # 81 max for each fitness

    def check_user_grid(self):
        """
        A function to check that the user grid is valid.
        """
        # Setup lists for columns and boxes
        columns = self.get_columns(self.user_rows)
        boxes = self.get_boxes(self.user_rows)

        # Create a list of each version of the grid layout
        grids = []
        grids.append(self.user_rows)
        grids.append(columns)
        grids.append(boxes)

        # Check each row, column and box has no duplicates of digits 1 - 9
        for grid in grids:
            for row in grid:
                if self.check_duplicates(row):
                    return False

        return True

    def check_duplicates(self, row):
        """
        A function to check a given list has duplicates of digits 1 to 9.
        Returns True if duplicates found, False otherwise.
        """
        # Create a list with '0's removed
        new_row = []
        for entry in row:
            if entry > 0:
                new_row.append(entry)

        return len(set(new_row)) < len(new_row)
