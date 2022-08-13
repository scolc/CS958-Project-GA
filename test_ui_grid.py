import ui_grid
import unittest
from tkinter import *


class TestGridUi(unittest.TestCase):
    """
    A class to perform unittests on functions
    in grid_ui
    """

    def test_init_row_ui(self):
        """
        A function to test the init_row function
        of the GridUI class returns a list that has 9 entries
        """
        print("\nTesting init_row_ui")
        ui = Tk()
        tile_size = 40
        grid = ui_grid.UIGrid(ui, tile_size)
        self.assertEqual(len(grid.init_row_ui()), 9)

    def test_validate_entry(self):
        """
        A function to test the validate_entry function
        of the GridUI class returns true for valid entry
        and false otherwise
        """
        print("\nTesting validate_entry")
        ui = Tk()
        tile_size = 40
        grid = ui_grid.UIGrid(ui, tile_size)
        # Correct entry 1 to 9
        self.assertTrue(grid.validate_entry("1"))
        self.assertTrue(grid.validate_entry("2"))
        self.assertTrue(grid.validate_entry("3"))
        self.assertTrue(grid.validate_entry("4"))
        self.assertTrue(grid.validate_entry("5"))
        self.assertTrue(grid.validate_entry("6"))
        self.assertTrue(grid.validate_entry("7"))
        self.assertTrue(grid.validate_entry("8"))
        self.assertTrue(grid.validate_entry("9"))

        # Incorrect entry - digits
        self.assertFalse(grid.validate_entry("0"))
        self.assertFalse(grid.validate_entry("10"))
        self.assertFalse(grid.validate_entry("25"))
        self.assertFalse(grid.validate_entry("37"))
        self.assertFalse(grid.validate_entry("49"))

        # Incorrect entry - other characters
        self.assertFalse(grid.validate_entry("a"))
        self.assertFalse(grid.validate_entry("b"))
        self.assertFalse(grid.validate_entry("c"))
        self.assertFalse(grid.validate_entry("A"))
        self.assertFalse(grid.validate_entry("B"))
        self.assertFalse(grid.validate_entry("C"))
        self.assertFalse(grid.validate_entry("#"))
        self.assertFalse(grid.validate_entry("+"))
        self.assertFalse(grid.validate_entry("_"))

    def test_init_grid_ui(self):
        """
        A function to test the init_grid function
        of the GridUI class returns a list that has 9 entries
        """
        print("\nTesting init_grid_ui")
        ui = Tk()
        tile_size = 40
        grid = ui_grid.UIGrid(ui, tile_size)
        self.assertEqual(len(grid.init_grid_ui()), 9)

    def test_get_user_rows(self):
        """
        A function to test the get_user_rows function
        of the GridUI class
        """
        print("\nTesting init_grid_ui")
        ui = Tk()
        tile_size = 40
        grid = ui_grid.UIGrid(ui, tile_size)

        test_grid = [[0]*9] * 9

        self.assertEqual(grid.get_user_rows(), test_grid)

        test_grid[0] = [1, 0, 0, 0, 0, 0, 0, 0, 0]
        grid.grid[0][0].delete(0, END)
        grid.grid[0][0].insert(0, "1")

        self.assertEqual(grid.get_user_rows(), test_grid)


if __name__ == "__main__":
    unittest.main()
