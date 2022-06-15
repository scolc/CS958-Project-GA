import grid_solver as gsol
import sudoku_grid as sg
import unittest

class TestGridSolver(unittest.TestCase):
    """
    A class to perform unitests on functions 
    in grid_solver
    """

    def build_test_grid(self):
        """
        A function to build the grid used in tests
        """
        
        grid = sg.SudokuGrid()

        # test grid for solving
        rows = []
        rows.append([0, 0, 2, 1, 0, 0, 0, 7, 0])
        rows.append([0, 8, 0, 0, 0, 6, 0, 0, 1])
        rows.append([1, 3, 0, 0, 8, 0, 0, 0, 2])
        rows.append([0, 5, 9, 0, 0, 8, 2, 0, 0])
        rows.append([0, 0, 0, 3, 9, 1, 0, 0, 0])
        rows.append([0, 0, 7, 5, 0, 0, 3, 8, 0])
        rows.append([2, 0, 0, 0, 5, 0, 0, 3, 7])
        rows.append([8, 0, 0, 6, 0, 0, 0, 2, 0])
        rows.append([0, 7, 0, 0, 0, 3, 4, 0, 0])

        grid.user_rows.clear()
        grid.user_rows = rows
        
        return grid

    def test_run(self):
        """
        A function to test the run function
        in grid_solver
        """

        print("\nTesting test_run")
        grid = self.build_test_grid()
        solver = gsol.GridSolver(grid)

        
        self.assertTrue(solver.run())

    def test_run_ga_solver(self):
        """
        A function to test the run_ga_solver function
        in grid_solver
        """
        print("\nTesting run_ga_solver")

        grid = self.build_test_grid()
        solver = gsol.GridSolver(grid)

        grid.phase = 1
        grid.current_row = 0

        # test first row ie rows.append([0, 0, 2, 1, 0, 0, 0, 7, 0])
        row = [0, 0, 2, 1, 0, 0, 0, 7, 0]
        cells = []
        possible_values = [3,4,5,6,8,9]
        for entry in row:
            if entry == 0:
                cells.append(possible_values)
            else:
                cells.append([entry])
        
        grid.ga_p1_pos_cells.clear()
        grid.ga_p1_pos_cells.append(cells)

        self.assertTrue(solver.run_ga_solver(cells))

        # test a possible box row

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

        # test grid

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

    def test_setup_phase_1(self):
        """
        A function to test the setup_phase_1 function
        in grid_solver
        """
        print("\nTesting setup_phase_1")

        grid = self.build_test_grid()
        grid.current_solution = grid.user_rows
        solver = gsol.GridSolver(grid)

        self.assertTrue(solver.setup_phase_1())

    def test_run_phase_1(self):
        """
        A function to test the run_phase_1 function
        in grid_solver
        """

        print("\nTesting run_phase_1")

        grid = self.build_test_grid()
        solver = gsol.GridSolver(grid)

        self.assertTrue(solver.run_phase_1())

    def test_run_phase_2(self):
        """
        A function to test the run_phase_2 function
        in grid_solver
        """
        print("\nTesting run_phase_2")

        grid = self.build_test_grid()
        solver = gsol.GridSolver(grid)

        rows = []

        rows.append([9, 6, 2, 1, 4, 5, 8, 7, 3])
        rows.append([7, 8, 4, 2, 3, 6, 5, 9, 1])
        rows.append([1, 3, 5, 7, 8, 9, 6, 4, 2])
        rows.append([3, 5, 9, 4, 7, 8, 2, 1, 6])
        rows.append([6, 2, 8, 3, 9, 1, 7, 5, 4])
        rows.append([4, 1, 7, 5, 6, 2, 3, 8, 9])
        rows.append([2, 9, 6, 8, 5, 4, 1, 3, 7])
        rows.append([8, 4, 3, 6, 1, 7, 9, 2, 5])
        rows.append([5, 7, 1, 9, 2, 3, 4, 6, 8])
        
        grid.phase = 2

        grid.ga_p2_pos_rows.clear()

        for entry in rows:
            grid.ga_p2_pos_rows.append([entry])

        self.assertTrue(solver.run_phase_2())

    def test_run_phase_3(self):
        """
        A function to test the run_phase_3 function
        in grid_solver
        """
        print("\nTesting run_phase_3")

        grid = self.build_test_grid()
        solver = gsol.GridSolver(grid)

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
        
        self.assertTrue(solver.run_phase_3())

    def test_check_boxes(self):
        """
        A function to test the check_boxes function 
        in grid_solver
        """
        print("\nTesting check_boxes")

        grid = self.build_test_grid()
        solver = gsol.GridSolver(grid)

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

        grid = self.build_test_grid()
        grid.current_solution = grid.user_rows
        solver = gsol.GridSolver(grid)

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

        
        





if __name__ == "__main__":
    unittest.main()