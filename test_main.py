import main
import unittest
from tkinter import *

class TestMain(unittest.TestCase):
    """
    A class to perform unittests on functions
    in main
    """

    def test_gui_init_row_ui(self):
        """
        A function to test the init_row function
        of the GUI class returns a list that has 9 entries
        """
        gui = main.GUI()
        self.assertEqual(len(gui.init_row_ui()), 9)

    def test_gui_validate_entry(self):
        """
        A function to test the validate_entry function
        of the GUI class returns true for valid entry
        and false otherwise
        """
        gui = main.GUI()
        # Correct entry 1 to 9
        self.assertTrue(gui.validate_entry("1"))
        self.assertTrue(gui.validate_entry("2"))
        self.assertTrue(gui.validate_entry("3"))
        self.assertTrue(gui.validate_entry("4"))
        self.assertTrue(gui.validate_entry("5"))
        self.assertTrue(gui.validate_entry("6"))
        self.assertTrue(gui.validate_entry("7"))
        self.assertTrue(gui.validate_entry("8"))
        self.assertTrue(gui.validate_entry("9"))

        # Incorrect entry - digits
        self.assertFalse(gui.validate_entry("0"))
        self.assertFalse(gui.validate_entry("10"))
        self.assertFalse(gui.validate_entry("25"))
        self.assertFalse(gui.validate_entry("37"))
        self.assertFalse(gui.validate_entry("49"))

        # Incorrect entry - other characters
        self.assertFalse(gui.validate_entry("a"))
        self.assertFalse(gui.validate_entry("b"))
        self.assertFalse(gui.validate_entry("c"))
        self.assertFalse(gui.validate_entry("A"))
        self.assertFalse(gui.validate_entry("B"))
        self.assertFalse(gui.validate_entry("C"))
        self.assertFalse(gui.validate_entry("#"))
        self.assertFalse(gui.validate_entry("+"))
        self.assertFalse(gui.validate_entry("_"))

    def test_gui_init_grid_ui(self):
        """
        A function to test the init_grid function
        of the GUI class returns a list that has 9 entries"""
        gui = main.GUI()
        self.assertEqual(len(gui.init_grid_ui()), 9)

    def test_get_user_rows(self):
        """
        A function to test the get_user_rows function
        of the GUI class
        """

        gui = main.GUI()
        test_grid = [[0]*9] * 9
        user_grid = gui.get_user_rows()
        
        self.assertEqual(user_grid, test_grid)

        
        test_grid[0] = [1, 0, 0, 0, 0, 0, 0, 0, 0]
        gui.grid_ui[0][0].delete(0, END)
        gui.grid_ui[0][0].insert(0, "1")
        user_grid = gui.get_user_rows()

        self.assertEqual(user_grid, test_grid)
        

if __name__ == "__main__":
    unittest.main()
