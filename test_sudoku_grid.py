import sudoku_grid
import unittest

class TestMain(unittest.TestCase):
    """
    A class to perform unittests on functions
    in sudoku_grid
    """

    def build_test_grid(self):
        """
        A function to build the grid used in tests
        """
        grid = sudoku_grid.SudokuGrid()

        # lists for cells
        test_lists = []
        list1 = [1,2,3,4,5,6,7,8,9] # 9 out of  9
        test_lists.append(list1)
        test_lists.append(list1)
        list2 = [1] * 9             # 1 out of 9
        test_lists.append(list2)
        list3 = [] * 9              # 0 out of 9
        test_lists.append(list3)
        list4 = [1,1,2,2,2,3,3,3,3] # 3 out of 9
        test_lists.append(list4)

        for list in test_lists:
            row = []
            for entry in list:
                cell = []
                cell.append(entry)
                row.append(cell)
            grid.ga_p1_pos_cells.append(row)

        # lists for rows
        rows = []
        rows.append([8, 9, 1, 2, 3, 5, 7, 4, 6])
        rows.append([6, 7, 4, 9, 8, 1, 5, 3, 2])
        rows.append([3, 5, 2, 7, 4, 6, 1, 8, 9])
        rows.append([9, 4, 5, 3, 6, 2, 8, 7, 1])
        rows.append([1, 6, 3, 8, 5, 7, 2, 9, 4])
        rows.append([2, 8, 7, 1, 9, 4, 6, 5, 3])
        rows.append([5, 3, 6, 4, 2, 8, 9, 1, 7])
        rows.append([7, 2, 9, 5, 1, 3, 4, 6, 8])
        rows.append([4, 1, 8, 6, 7, 9, 3, 2, 5])

        for entry in rows:
            current_row = []
            current_row.append(entry)
            grid.ga_p2_pos_rows.append(current_row)

        # lists for box rows
        box_rows = []
        box_rows.append([[8, 9, 1, 2, 3, 5, 7, 4, 6],[6, 7, 4, 9, 8, 1, 5, 3, 2],[3, 5, 2, 7, 4, 6, 1, 8, 9]])
        box_rows.append([[9, 4, 5, 3, 6, 2, 8, 7, 1],[1, 6, 3, 8, 5, 7, 2, 9, 4],[2, 8, 7, 1, 9, 4, 6, 5, 3]])
        box_rows.append([[5, 3, 6, 4, 2, 8, 9, 1, 7],[7, 2, 9, 5, 1, 3, 4, 6, 8],[4, 1, 8, 6, 7, 9, 3, 2, 5]])

        for entry in box_rows:
            current_box = []
            current_box.append(entry)
            grid.ga_p3_pos_box_rows.append(current_box)

        return grid



    def test_fitness(self):
        """
        A function to test the fitness function
        of the SudokuGrid class
        """
        print("\nTesting fitness")

        grid = self.build_test_grid()
        params = [0] * 9
        grid.phase = 1

        # row[0] is list1, 9 out of  9 correct
        grid.current_row = 0
        self.assertEqual(grid.fitness(params), 100)

        # row[1] is list1, testing changing row number
        grid.current_row = 1
        self.assertEqual(grid.fitness(params), 100)

        # row[2] is list2, 1 out of 9 correct
        grid.current_row = 2
        self.assertEqual(grid.fitness(params), 1/9 * 100)
        
        # row[3] is list3, 0 out of 9 correct
        grid.current_row = 3
        self.assertEqual(grid.fitness(params), 0)

        # row[4] is list4, 3 out of 9 correct
        grid.current_row = 4
        self.assertEqual(grid.fitness(params), 3/9 * 100)
    
    
    def test_call(self):
        """
        A function to test the __call__ function
        of the SudokuGrid class
        """
        print("\nTesting call")

        grid = self.build_test_grid()
        
        # phase 1, find rows
        params = [0] * 9
        grid.phase = 1
        # row[0] is list1
        grid.current_row = 0
        self.assertEqual(grid(params), 100)

        # row[1] is list1
        grid.current_row = 1
        self.assertEqual(grid(params), 100)

        # row[2] is list2
        grid.current_row = 2
        self.assertEqual(grid(params), 1/9 * 100)
        
        # row[3] is list3
        grid.current_row = 3
        self.assertEqual(grid(params), 0)

        # row[4] is list4
        grid.current_row = 4
        self.assertEqual(grid(params), 3/9 * 100)

        # phase 2, find box rows (groups of 3 rows)
        grid.phase = 2
        params = [0] * 3
        # box row 0, top 3 rows
        grid.current_row = 0
        self.assertEqual(grid(params), 100)
        # box row 1, mid 3 rows
        grid.current_row = 1
        self.assertEqual(grid(params), 100)
        # box row 2, mid 3 rows
        grid.current_row = 2
        self.assertEqual(grid(params), 100)
        
        # phase 3, find grid (groups of 3 box rows)
        grid.phase = 3
        params = [0] * 3
        self.assertEqual(grid(params), 100)


    def test_fitness_columns(self):
        """
        A function to test the fitness_columns function
        of the SudokuGrid class
        """
        print("\nTesting fitness_columns")


        grid = sudoku_grid.SudokuGrid()
        rows1 = []
        rows1.append([8, 9, 1, 2, 3, 5, 7, 4, 6])
        rows1.append([6, 7, 4, 9, 8, 1, 5, 3, 2])
        rows1.append([3, 5, 2, 7, 4, 6, 1, 8, 9])
        rows1.append([9, 4, 5, 3, 6, 2, 8, 7, 1])
        rows1.append([1, 6, 3, 8, 5, 7, 2, 9, 4])
        rows1.append([2, 8, 7, 1, 9, 4, 6, 5, 3])
        rows1.append([5, 3, 6, 4, 2, 8, 9, 1, 7])
        rows1.append([7, 2, 9, 5, 1, 3, 4, 6, 8])
        rows1.append([4, 1, 8, 6, 7, 9, 3, 2, 5])

        self.assertEqual(grid.fitness_columns(rows1), 81)

        rows2 = [[1] * 9] * 9
        self.assertEqual(grid.fitness_columns(rows2), 9)


    def test_fitness_box_row(self):
        """
        A function to test the fitness_boxes function
        of the SudokuGrid class
        """
        print("\nTesting fitness_box_row")


        grid = sudoku_grid.SudokuGrid()
        box_row1 = ([[8, 9, 1, 2, 3, 5, 7, 4, 6],[6, 7, 4, 9, 8, 1, 5, 3, 2],[3, 5, 2, 7, 4, 6, 1, 8, 9]])
        box_row2 = ([[9, 4, 5, 3, 6, 2, 8, 7, 1],[1, 6, 3, 8, 5, 7, 2, 9, 4],[2, 8, 7, 1, 9, 4, 6, 5, 3]])
        box_row3 = ([[5, 3, 6, 4, 2, 8, 9, 1, 7],[7, 2, 9, 5, 1, 3, 4, 6, 8],[4, 1, 8, 6, 7, 9, 3, 2, 5]])
        self.assertEqual(grid.fitness_box_row(box_row1), 27)
        self.assertEqual(grid.fitness_box_row(box_row2), 27)
        self.assertEqual(grid.fitness_box_row(box_row3), 27)

        box_row4 = ([[1] * 9,[1] * 9,[1]] * 9)
        self.assertEqual(grid.fitness_box_row(box_row4), 3)

    def test_calculate_fitness(self):
        """
        A function to test the calculate_fitness function
        of the SudokuGrid class
        """
        print("\nTesting calculate_fitness")

        grid = sudoku_grid.SudokuGrid()
        list1 = ([[8, 9, 1, 2, 3, 5, 7, 4, 6]]) # single row
        list2 = ([[9, 4, 5, 3, 6, 2, 8, 7, 1],[1, 6, 3, 8, 5, 7, 2, 9, 4],[2, 8, 7, 1, 9, 4, 6, 5, 3]]) # a box row
        list3 = ([[1] * 9,[1] * 9,[1] * 9])

        self.assertEqual(grid.calculate_fitness(list1), 9)
        self.assertEqual(grid.calculate_fitness(list2), 27)
        self.assertEqual(grid.calculate_fitness(list3), 3)

    def test_get_columns(self):
        """
        A function to test the get_columns function
        of the SudokuGrid class
        """
        print("\nTesting get_columns")

        grid = sudoku_grid.SudokuGrid()
        rows1 = []
        rows1.append([1] * 9)
        rows1.append([2] * 9)
        rows1.append([3] * 9)
        rows1.append([4] * 9)
        rows1.append([5] * 9)
        rows1.append([6] * 9)
        rows1.append([7] * 9)
        rows1.append([8] * 9)
        rows1.append([9] * 9)

        rows2 = [[1, 2, 3, 4, 5, 6, 7, 8, 9]] * 9

        self.assertEqual(grid.get_columns(rows1), rows2)


    def test_get_box_row(self):
        """
        A function to test the get_box_row function
        of the SudokuGrid class
        """
        print("\nTesting get_box_row")

        grid = sudoku_grid.SudokuGrid()
        
        box_row1 = ([[8, 9, 1, 2, 3, 5, 7, 4, 6],[6, 7, 4, 9, 8, 1, 5, 3, 2],[3, 5, 2, 7, 4, 6, 1, 8, 9]])
        box_list = ([[8, 9, 1, 6, 7, 4, 3, 5, 2],[2, 3, 5, 9, 8, 1, 7, 4, 6],[7, 4, 6, 5, 3, 2, 1, 8, 9]])

        self.assertEqual(grid.get_box_row(box_row1), box_list)

    def test_get_boxes(self):
        """
        A function to test the get_boxes function
        of the SudokuGrid class
        """
        print("\nTesting get_boxes")

        grid = sudoku_grid.SudokuGrid()
        rows = []

        rows.append([8, 9, 1, 2, 3, 5, 7, 4, 6])
        rows.append([6, 7, 4, 9, 8, 1, 5, 3, 2])
        rows.append([3, 5, 2, 7, 4, 6, 1, 8, 9])
        rows.append([9, 4, 5, 3, 6, 2, 8, 7, 1])
        rows.append([1, 6, 3, 8, 5, 7, 2, 9, 4])
        rows.append([2, 8, 7, 1, 9, 4, 6, 5, 3])
        rows.append([5, 3, 6, 4, 2, 8, 9, 1, 7])
        rows.append([7, 2, 9, 5, 1, 3, 4, 6, 8])
        rows.append([4, 1, 8, 6, 7, 9, 3, 2, 5])

        box_list = []
        box_list.append([8, 9, 1, 6, 7, 4, 3, 5, 2])
        box_list.append([2, 3, 5, 9, 8, 1, 7, 4, 6])
        box_list.append([7, 4, 6, 5, 3, 2, 1, 8, 9])
        box_list.append([9, 4, 5, 1, 6, 3, 2, 8, 7])
        box_list.append([3, 6, 2, 8, 5, 7, 1, 9, 4])
        box_list.append([8, 7, 1, 2, 9, 4, 6, 5, 3])
        box_list.append([5, 3, 6, 7, 2, 9, 4, 1, 8])
        box_list.append([4, 2, 8, 5, 1, 3, 6, 7, 9])
        box_list.append([9, 1, 7, 4, 6, 8, 3, 2, 5])

        self.assertEqual(grid.get_boxes(rows), box_list)

    def test_check_solution(self):
        """
        A function to test the check_solution function
        of the sudoku_grid class
        """
        print("\nTesting check_solution")
        
        grid = sudoku_grid.SudokuGrid()

        # Good Grid
        rows = []
        rows.append([8, 9, 1, 2, 3, 5, 7, 4, 6])
        rows.append([6, 7, 4, 9, 8, 1, 5, 3, 2])
        rows.append([3, 5, 2, 7, 4, 6, 1, 8, 9])
        rows.append([9, 4, 5, 3, 6, 2, 8, 7, 1])
        rows.append([1, 6, 3, 8, 5, 7, 2, 9, 4])
        rows.append([2, 8, 7, 1, 9, 4, 6, 5, 3])
        rows.append([5, 3, 6, 4, 2, 8, 9, 1, 7])
        rows.append([7, 2, 9, 5, 1, 3, 4, 6, 8])
        rows.append([4, 1, 8, 6, 7, 9, 3, 2, 5])

        grid.current_solution.clear()
        grid.current_solution = rows

        self.assertTrue(grid.check_solution())

        # Bad Grid
        rows = [[0]*9] * 9

        grid.current_solution.clear()
        grid.current_solution = rows

        self.assertFalse(grid.check_solution())

    def test_check_user_grid(self):
        """
        A function to test the check_user_grid function
        of the sudoku_grid class.
        """
        print("\nTesting check_user_grid")
        
        grid = sudoku_grid.SudokuGrid()

        # Good grids

        # Empty
        grid.user_rows.clear()
        grid.user_rows = [[0] * 9] * 9

        self.assertTrue(grid.check_user_grid())

        # Full grid
        grid.user_rows.clear()

        grid.user_rows.append([8, 9, 1, 2, 3, 5, 7, 4, 6])
        grid.user_rows.append([6, 7, 4, 9, 8, 1, 5, 3, 2])
        grid.user_rows.append([3, 5, 2, 7, 4, 6, 1, 8, 9])
        grid.user_rows.append([9, 4, 5, 3, 6, 2, 8, 7, 1])
        grid.user_rows.append([1, 6, 3, 8, 5, 7, 2, 9, 4])
        grid.user_rows.append([2, 8, 7, 1, 9, 4, 6, 5, 3])
        grid.user_rows.append([5, 3, 6, 4, 2, 8, 9, 1, 7])
        grid.user_rows.append([7, 2, 9, 5, 1, 3, 4, 6, 8])
        grid.user_rows.append([4, 1, 8, 6, 7, 9, 3, 2, 5])

        self.assertTrue(grid.check_user_grid())

        # Bad grids
        
        # All 1s
        grid.user_rows.clear()
        grid.user_rows = [[1] * 9] * 9

        self.assertFalse(grid.check_user_grid())

        # Single duplicate
        grid.user_rows.clear()

        grid.user_rows.append([8, 9, 1, 2, 3, 5, 7, 4, 6])
        grid.user_rows.append([6, 7, 4, 9, 8, 1, 5, 3, 2])
        grid.user_rows.append([3, 5, 2, 7, 4, 6, 1, 8, 9])
        grid.user_rows.append([9, 4, 5, 3, 6, 2, 8, 7, 1])
        grid.user_rows.append([1, 6, 3, 8, 5, 7, 2, 9, 4])
        grid.user_rows.append([2, 8, 7, 1, 9, 4, 6, 5, 3])
        grid.user_rows.append([5, 3, 6, 4, 2, 8, 9, 1, 7])
        grid.user_rows.append([7, 2, 9, 5, 1, 3, 4, 6, 8])
        grid.user_rows.append([4, 1, 8, 6, 7, 9, 3, 2, 1]) # Duplicate 1 here

        self.assertFalse(grid.check_user_grid())

    def test_check_duplicates(self):
        """
        A function to test the check_duplicates function
        of the sudoku_grid class.
        """
        print("\nTesting check_duplicates")

        grid = sudoku_grid.SudokuGrid()

        # Good Rows
        row1 = [0] * 9
        row2 = [0] * 8 + [1]
        row3 = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.assertFalse(grid.check_duplicates(row1))
        self.assertFalse(grid.check_duplicates(row2))
        self.assertFalse(grid.check_duplicates(row3))


        # Bad Rows
        row4 = [1] * 9
        row5 = [0] * 7 + [1] * 2
        row6 = [1, 1, 3, 4, 5, 6, 7, 8, 9]

        self.assertTrue(grid.check_duplicates(row4))
        self.assertTrue(grid.check_duplicates(row5))
        self.assertTrue(grid.check_duplicates(row6))


        



if __name__ == "__main__":
    unittest.main()
