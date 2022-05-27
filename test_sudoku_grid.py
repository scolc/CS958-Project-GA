import sudoku_grid
import unittest

class TestMain(unittest.TestCase):
    """
    A class to perform unittests on functions
    in sudoku_grid
    """

    def test_fitness(self):
        """
        A function to test the fitness function
        of the SudokuGrid class
        """
        grid = sudoku_grid.SudokuGrid()
        list1 = [1,2,3,4,5,6,7,8,9]
        list2 = [1] * 9
        list3 = [] * 9
        list4 = [1,1,2,2,2,3,3,3,3]
        self.assertEqual(grid.fitness(list1), 9)
        self.assertEqual(grid.fitness(list2), 1)
        self.assertEqual(grid.fitness(list3), 0)
        self.assertEqual(grid.fitness(list4), 3)

    def test_call(self):
        """
        A function to test the __call__ function
        of the SudokuGrid class
        """
        grid = sudoku_grid.SudokuGrid()
        list1 = [1,2,3,4,5,6,7,8,9]
        list2 = [1] * 9
        list3 = [] * 9
        self.assertEqual(grid(list1), 9)
        self.assertEqual(grid(list2), 1)
        self.assertEqual(grid(list3), 0)

if __name__ == "__main__":
    unittest.main()
