import grid_solver as gsol
import sudoku_grid as sg
import unittest


def grid_for_tests():
    """
    A function to build the grid used in tests
    """
    grid = sg.SudokuGrid()

    # test grid for solving
    rows = [
        [0, 0, 2, 1, 0, 0, 0, 7, 0],
        [0, 8, 0, 0, 0, 6, 0, 0, 1],
        [1, 3, 0, 0, 8, 0, 0, 0, 2],
        [0, 5, 9, 0, 0, 8, 2, 0, 0],
        [0, 0, 0, 3, 9, 1, 0, 0, 0],
        [0, 0, 7, 5, 0, 0, 3, 8, 0],
        [2, 0, 0, 0, 5, 0, 0, 3, 7],
        [8, 0, 0, 6, 0, 0, 0, 2, 0],
        [0, 7, 0, 0, 0, 3, 4, 0, 0]
    ]

    grid.user_rows.clear()
    grid.user_rows = rows

    return grid


def output(text, tag=""):
    """
    A function to redirect output for the user to the console.
    """
    print(text)


class TestGridSolver(unittest.TestCase):
    """
    A class to perform unitests on functions
    in grid_solver
    """

    def test_run(self):
        """
        A function to test the run function
        in grid_solver
        """

        print("\nTesting run")
        grid = grid_for_tests()
        solver = gsol.GridSolver(grid, output)

        solver.run()
        self.assertTrue(solver.solved)

    def test_run_ga_solver(self):
        """
        A function to test the run_ga_solver function
        in grid_solver
        """
        print("\nTesting run_ga_solver")

        grid = grid_for_tests()
        solver = gsol.GridSolver(grid, output)

        grid.phase = 1
        grid.current_row = 0

        # Good Grid
        # Test first row
        row = [0, 0, 2, 1, 0, 0, 0, 7, 0]
        cells = []
        possible_values = [3, 4, 5, 6, 8, 9]
        for entry in row:
            if entry == 0:
                cells.append(possible_values)
            else:
                cells.append([entry])

        grid.ga_p1_pos_cells.clear()
        grid.ga_p1_pos_cells.append(cells)

        self.assertTrue(solver.run_ga_solver(cells))

        # Test a possible box row
        row1 = [9, 6, 2, 1, 4, 5, 8, 7, 3]
        row2 = [7, 8, 4, 2, 3, 6, 5, 9, 1]
        row3 = [1, 3, 5, 7, 8, 9, 6, 4, 2]

        grid.ga_p2_pos_rows.clear()
        grid.ga_p2_pos_rows.append([row1])
        grid.ga_p2_pos_rows.append([row2])
        grid.ga_p2_pos_rows.append([row3])

        boxrow = []
        boxrow.append([row1])
        boxrow.append([row2])
        boxrow.append([row3])

        grid.phase = 2

        self.assertTrue(solver.run_ga_solver(boxrow))

        # Test full grid
        row4 = [3, 5, 9, 4, 7, 8, 2, 1, 6]
        row5 = [6, 2, 8, 3, 9, 1, 7, 5, 4]
        row6 = [4, 1, 7, 5, 6, 2, 3, 8, 9]

        boxrow1 = []
        boxrow1.append(row1)
        boxrow1.append(row2)
        boxrow1.append(row3)

        boxrow2 = []
        boxrow2.append(row4)
        boxrow2.append(row5)
        boxrow2.append(row6)

        row7 = [2, 9, 6, 8, 5, 4, 1, 3, 7]
        row8 = [8, 4, 3, 6, 1, 7, 9, 2, 5]
        row9 = [5, 7, 1, 9, 2, 3, 4, 6, 8]

        boxrow3 = []
        boxrow3.append(row7)
        boxrow3.append(row8)
        boxrow3.append(row9)

        grid.ga_p3_pos_box_rows.append([boxrow])
        grid.ga_p3_pos_box_rows.append([boxrow2])
        grid.ga_p3_pos_box_rows.append([boxrow3])

        posgrid = []
        posgrid.append([boxrow])
        posgrid.append([boxrow2])
        posgrid.append([boxrow3])

        self.assertTrue(solver.run_ga_solver(posgrid))

        # Bad Grid Row
        row = [0, 0, 2, 1, 0, 0, 0, 7, 0]
        cells = []
        possible_values = [0]
        for entry in row:
            if entry == 0:
                cells.append(possible_values)
            else:
                cells.append([entry])

        grid.ga_p1_pos_cells.clear()
        grid.ga_p1_pos_cells.append(cells)
        grid.phase = 1

        self.assertFalse(solver.run_ga_solver(cells))

    def test_setup_phase_1(self):
        """
        A function to test the setup_phase_1 function
        in grid_solver
        """
        print("\nTesting setup_phase_1")

        grid = grid_for_tests()
        grid.current_solution = grid.user_rows
        solver = gsol.GridSolver(grid, output)

        # Good Grid
        self.assertTrue(solver.setup_phase_1())

        # Bad Grid
        bad_rows = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 1, 2, 2, 1, 2, 2, 1],
            [3, 3, 3, 3, 3, 3, 3, 3, 3],
            [4, 4, 4, 4, 4, 4, 4, 4, 4],
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
            [6, 6, 6, 6, 6, 6, 6, 6, 6],
            [7, 7, 7, 7, 7, 7, 7, 7, 7],
            [8, 8, 8, 8, 8, 8, 8, 8, 8],
            [9, 9, 9, 9, 9, 9, 9, 9, 9]
        ]
        grid.current_solution.clear
        grid.current_solution = bad_rows

        self.assertFalse(solver.setup_phase_1())

    def test_run_phase_1(self):
        """
        A function to test the run_phase_1 function
        in grid_solver
        """
        print("\nTesting run_phase_1")

        grid = grid_for_tests()
        grid.current_solution = grid.user_rows
        solver = gsol.GridSolver(grid, output)
        solver.setup_phase_1()

        # Good Grid
        self.assertTrue(solver.run_phase_1())

        # Bad Grid
        grid.ga_p1_pos_cells.clear
        grid.ga_p1_pos_cells = [[[0]] * 9] * 9

        self.assertFalse(solver.run_phase_1())

    def test_run_phase_2(self):
        """
        A function to test the run_phase_2 function
        in grid_solver
        """
        print("\nTesting run_phase_2")

        grid = grid_for_tests()
        solver = gsol.GridSolver(grid, output)

        grid.phase = 2

        # Good Grid
        grid.ga_p2_pos_rows.clear()

        grid.ga_p2_pos_rows.append([[9, 6, 2, 1, 4, 5, 8, 7, 3]])
        grid.ga_p2_pos_rows.append([[7, 8, 4, 2, 3, 6, 5, 9, 1]])
        grid.ga_p2_pos_rows.append([[1, 3, 5, 7, 8, 9, 6, 4, 2]])
        grid.ga_p2_pos_rows.append([[3, 5, 9, 4, 7, 8, 2, 1, 6]])
        grid.ga_p2_pos_rows.append([[6, 2, 8, 3, 9, 1, 7, 5, 4]])
        grid.ga_p2_pos_rows.append([[4, 1, 7, 5, 6, 2, 3, 8, 9]])
        grid.ga_p2_pos_rows.append([[2, 9, 6, 8, 5, 4, 1, 3, 7]])
        grid.ga_p2_pos_rows.append([[8, 4, 3, 6, 1, 7, 9, 2, 5]])
        grid.ga_p2_pos_rows.append([[5, 7, 1, 9, 2, 3, 4, 6, 8]])

        self.assertTrue(solver.run_phase_2())

        # Bad Grid
        grid.ga_p2_pos_rows.clear()

        grid.ga_p2_pos_rows.append([[0] * 9])
        grid.ga_p2_pos_rows.append([[0] * 9])
        grid.ga_p2_pos_rows.append([[0] * 9])
        grid.ga_p2_pos_rows.append([[0] * 9])
        grid.ga_p2_pos_rows.append([[0] * 9])
        grid.ga_p2_pos_rows.append([[0] * 9])
        grid.ga_p2_pos_rows.append([[0] * 9])
        grid.ga_p2_pos_rows.append([[0] * 9])
        grid.ga_p2_pos_rows.append([[0] * 9])

        self.assertFalse(solver.run_phase_2())

    def test_run_phase_3(self):
        """
        A function to test the run_phase_3 function
        in grid_solver
        """
        print("\nTesting run_phase_3")

        grid = grid_for_tests()
        solver = gsol.GridSolver(grid, output)

        # Good Grid
        row1 = [9, 6, 2, 1, 4, 5, 8, 7, 3]
        row2 = [7, 8, 4, 2, 3, 6, 5, 9, 1]
        row3 = [1, 3, 5, 7, 8, 9, 6, 4, 2]
        row4 = [3, 5, 9, 4, 7, 8, 2, 1, 6]
        row5 = [6, 2, 8, 3, 9, 1, 7, 5, 4]
        row6 = [4, 1, 7, 5, 6, 2, 3, 8, 9]
        row7 = [2, 9, 6, 8, 5, 4, 1, 3, 7]
        row8 = [8, 4, 3, 6, 1, 7, 9, 2, 5]
        row9 = [5, 7, 1, 9, 2, 3, 4, 6, 8]

        boxrow1 = []
        boxrow1.append(row1)
        boxrow1.append(row2)
        boxrow1.append(row3)

        boxrow2 = []
        boxrow2.append(row4)
        boxrow2.append(row5)
        boxrow2.append(row6)

        boxrow3 = []
        boxrow3.append(row7)
        boxrow3.append(row8)
        boxrow3.append(row9)

        grid.ga_p3_pos_box_rows.clear()

        grid.ga_p3_pos_box_rows.append([boxrow1])
        grid.ga_p3_pos_box_rows.append([boxrow2])
        grid.ga_p3_pos_box_rows.append([boxrow3])

        self.assertTrue(solver.run_phase_3())

        # Bad Grid
        bad_row1 = [0] * 9
        bad_row2 = [0] * 9
        bad_row3 = [0] * 9
        bad_row4 = [0] * 9
        bad_row5 = [0] * 9
        bad_row6 = [0] * 9
        bad_row7 = [0] * 9
        bad_row8 = [0] * 9
        bad_row9 = [0] * 9

        boxrow1 = []
        boxrow1.append(bad_row1)
        boxrow1.append(bad_row2)
        boxrow1.append(bad_row3)

        boxrow2 = []
        boxrow2.append(bad_row4)
        boxrow2.append(bad_row5)
        boxrow2.append(bad_row6)

        boxrow3 = []
        boxrow3.append(bad_row7)
        boxrow3.append(bad_row8)
        boxrow3.append(bad_row9)

        grid.ga_p3_pos_box_rows.clear()

        grid.ga_p3_pos_box_rows.append([boxrow1])
        grid.ga_p3_pos_box_rows.append([boxrow2])
        grid.ga_p3_pos_box_rows.append([boxrow3])

        self.assertFalse(solver.run_phase_3())

    def test_check_boxes(self):
        """
        A function to test the check_boxes function
        in grid_solver
        """
        print("\nTesting check_boxes")

        grid = grid_for_tests()
        solver = gsol.GridSolver(grid, output)

        row1 = [9, 6, 2, 1, 4, 5, 8, 7, 3]
        row2 = [7, 8, 4, 2, 3, 6, 5, 9, 1]
        row3 = [1, 3, 5, 7, 8, 9, 6, 4, 2]
        row4 = [3, 5, 9, 4, 7, 8, 2, 1, 6]
        row5 = [6, 2, 8, 3, 9, 1, 7, 5, 4]
        row6 = [4, 1, 7, 5, 6, 2, 3, 8, 9]
        row7 = [2, 9, 6, 8, 5, 4, 1, 3, 7]
        row8 = [8, 4, 3, 6, 1, 7, 9, 2, 5]
        row9 = [5, 7, 1, 9, 2, 3, 4, 6, 8]

        boxrow1 = []
        boxrow1.append(row1)
        boxrow1.append(row2)
        boxrow1.append(row3)

        boxrow2 = []
        boxrow2.append(row4)
        boxrow2.append(row5)
        boxrow2.append(row6)

        boxrow3 = []
        boxrow3.append(row7)
        boxrow3.append(row8)
        boxrow3.append(row9)

        grid.ga_p3_pos_box_rows.append([boxrow1])
        grid.ga_p3_pos_box_rows.append([boxrow2])
        grid.ga_p3_pos_box_rows.append([boxrow3])

        grid.ga_p2_pos_rows = [[0]] * 9

        solver.check_boxes()

        self.assertEqual(grid.ga_p2_pos_rows[0][0], row1)
        self.assertEqual(grid.ga_p2_pos_rows[1][0], row2)
        self.assertEqual(grid.ga_p2_pos_rows[2][0], row3)
        self.assertEqual(grid.ga_p2_pos_rows[3][0], row4)
        self.assertEqual(grid.ga_p2_pos_rows[4][0], row5)
        self.assertEqual(grid.ga_p2_pos_rows[5][0], row6)
        self.assertEqual(grid.ga_p2_pos_rows[6][0], row7)
        self.assertEqual(grid.ga_p2_pos_rows[7][0], row8)
        self.assertEqual(grid.ga_p2_pos_rows[8][0], row9)

    def test_check_rows(self):
        """
        A function to test the check_rows function
        in grid_solver
        """
        print("\nTesting check_rows")

        grid = grid_for_tests()
        grid.current_solution = grid.user_rows
        solver = gsol.GridSolver(grid, output)

        # When no rows found
        grid.ga_p2_pos_rows = [[[0]*9]] * 9
        self.assertFalse(solver.check_rows())

        # When 1 row found
        row1 = [9, 6, 2, 1, 4, 5, 8, 7, 3]
        grid.ga_p2_pos_rows[0] = [row1]
        self.assertTrue(solver.check_rows())

        # When whole grid found
        row2 = [7, 8, 4, 2, 3, 6, 5, 9, 1]
        row3 = [1, 3, 5, 7, 8, 9, 6, 4, 2]
        row4 = [3, 5, 9, 4, 7, 8, 2, 1, 6]
        row5 = [6, 2, 8, 3, 9, 1, 7, 5, 4]
        row6 = [4, 1, 7, 5, 6, 2, 3, 8, 9]
        row7 = [2, 9, 6, 8, 5, 4, 1, 3, 7]
        row8 = [8, 4, 3, 6, 1, 7, 9, 2, 5]
        row9 = [5, 7, 1, 9, 2, 3, 4, 6, 8]

        grid.ga_p2_pos_rows.clear()

        grid.ga_p2_pos_rows.append([row1])
        grid.ga_p2_pos_rows.append([row2])
        grid.ga_p2_pos_rows.append([row3])
        grid.ga_p2_pos_rows.append([row4])
        grid.ga_p2_pos_rows.append([row5])
        grid.ga_p2_pos_rows.append([row6])
        grid.ga_p2_pos_rows.append([row7])
        grid.ga_p2_pos_rows.append([row8])
        grid.ga_p2_pos_rows.append([row9])

        self.assertTrue(solver.check_rows())

    def test_convert_time(self):
        """
        A function to test the convert_time function
        in grid_solver
        """
        print("\nTesting convert_time")

        time1 = 0  # 0 seconds for string return "00"
        time2 = 1  # 1 second, string should show singular with leading 0
        time3 = 5  # less than 10 with leading 0 and plural
        time4 = 20  # less than a minute, greater than 10 seconds
        time5 = 60  # 1 minute, should contain "00" same as time1
        time6 = 61  # 1 minute 1 second same as time2
        time7 = 65  # 1 minute + same as time3
        time8 = 80  # 1 minute + same as time4
        time9 = 120  # 2 minutes, string should show plural minutes

        time1_string = "00 seconds"
        time2_string = "01 second"
        time3_string = "05 seconds"
        time4_string = "20 seconds"
        time5_string = "1 minute 00 seconds"
        time6_string = "1 minute 01 second"
        time7_string = "1 minute 05 seconds"
        time8_string = "1 minute 20 seconds"
        time9_string = "2 minutes 00 seconds"

        grid = grid_for_tests()
        grid.current_solution = grid.user_rows
        solver = gsol.GridSolver(grid, output)

        self.assertEqual(solver.convert_time(time1), time1_string)
        self.assertEqual(solver.convert_time(time2), time2_string)
        self.assertEqual(solver.convert_time(time3), time3_string)
        self.assertEqual(solver.convert_time(time4), time4_string)
        self.assertEqual(solver.convert_time(time5), time5_string)
        self.assertEqual(solver.convert_time(time6), time6_string)
        self.assertEqual(solver.convert_time(time7), time7_string)
        self.assertEqual(solver.convert_time(time8), time8_string)
        self.assertEqual(solver.convert_time(time9), time9_string)


if __name__ == "__main__":
    unittest.main()
