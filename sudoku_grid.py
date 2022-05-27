class SudokuGrid:
    """
    A class to represent a 9x9 sudoku grid.
    Contains a callable function to act as
    the fitness function for the genetic algorithm.
    """

    def __init__(self):
        self.row = []
        for entry in range(9):
            this_row = [0] * 9
            self.row.append(this_row)

    def __repr__(self):
        result = "Grid\n"
        rownum = 0
        for row in self.row:
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
        """
        return self.fitness(params)
        
    def fitness(self, params):
        """
        A function that calculates the fitness value for parameters
        from a genetic algorithm
        """
        valid = 0
        for entry in params:
            # Check entry is a number
            if entry >= 1 and entry <= 9:
                valid += 1
        if valid == len(params):
            # remove duplicates and return difference as fitness
            return len(set(params))
        else:
            return 0
