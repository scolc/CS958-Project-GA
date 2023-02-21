from tkinter import *
from tkinter.scrolledtext import ScrolledText

import gui


class UIOutputBox():
    """
    A class to handle the output box for providing feedback and
    instruction to the user.
    """

    def __init__(self, ui: Tk,
                 tile_size: int):
        self.ui = ui
        self.tile_size = tile_size
        self.output_font = "Calibri " + str(int(self.tile_size / 3))
        self.colours = gui.Colours()

        self.output_frame = Frame(self.ui,
                                  bg=self.colours.bg_dis_norm,
                                  highlightthickness=0)
        self.output_box = ScrolledText(self.output_frame,
                                       fg=self.colours.fg_output,
                                       bg=self.colours.bg_output,
                                       font=self.output_font,
                                       wrap=WORD,
                                       state="disabled",
                                       padx=5,
                                       pady=5)

        self.output_box.tag_config("hint",
                                   foreground=self.colours.bg_hint)
        self.output_box.tag_config("valid",
                                   foreground=self.colours.bg_valid)
        self.output_box.tag_config("invalid",
                                   foreground=self.colours.bg_invalid)
        self.output_box.tag_config("normal",
                                   foreground=self.colours.fg_output)

        self.init_output_box()

    def __call__(self, text: str, tag="normal"):
        """
        A function that allows the class to be called.
        """
        self.output(text, tag)

    # Initialisation

    def init_output_box(self):
        """
        A function to set the output box initial state.
        """
        self.output_box["state"] = "normal"
        self.output_box.delete(1.0, END)
        message = ("Please enter the initial clues (digits 1-9) " +
                   "for the puzzle into the grid above.\n" +
                   "Type or click on the number buttons to fill " +
                   "each cell.\n" +
                   #"Click 'Generate Grid' to generate a new " +
                   #"puzzle grid.\n" +
                   "Click 'START' to find the solution.\n" +
                   "Click 'RESET GRID' to clear the grid.\n\n")
        self.output(message)

    # Display

    def display_output_box(self,
                           x_pos,
                           y_pos,
                           output_width,
                           output_height,
                           frame_pad):
        """
        A function to display the output box.
        """
        frame_width = output_width + 2 * frame_pad
        frame_height = output_height + 2 * frame_pad

        self.output_frame.place(x=x_pos - frame_pad,
                                y=y_pos - frame_pad,
                                width=frame_width,
                                height=frame_height)
        self.output_box.place(x=frame_pad,
                              y=frame_pad,
                              width=output_width,
                              height=output_height)

    # Operation

    def output(self, text: str, tag="normal"):
        """
        A function to add given text to the displayed output box.
        The tag can be used to modify the text displayed.
        Tags are "normal" (default), "hint", "valid" and "invalid".
        """
        # Enable the output box and insert text
        self.output_box["state"] = "normal"
        self.output_box.insert(END, text, tag)

        # Scroll to the bottom and disable the output box
        self.output_box.see(END)
        self.output_box["state"] = "disabled"
