from tkinter import *

import gui


class UIMessageBox():
    """
    A class to handle the custom message boxes.
    """

    def __init__(self, ui: Tk,
                 tile_size: int):
        self.ui = ui
        self.colours = gui.Colours()
        self.tile_size = tile_size
        self.pad = int(self.tile_size / 2)

        self.m_box_width = self.tile_size * 8
        self.m_box_height = self.tile_size * 5
        self.m_box_font = "Calibri " + str(int(self.tile_size / 3))
        self.m_box_frame_pad = 3

    def __call__(self, title, message, type):
        """
        A function that allows the class to be called.
        """
        return self.display_message_box(title, message, type)

    def display_message_box(self, title, message, type):
        """
        A function to create a custom empty message box shell.
        """
        m_box = Toplevel(self.ui)

        # Prevent user interacting with the base window until closed
        m_box.grab_set()
        m_box.resizable(width=False,
                        height=False)
        m_box.wm_transient(self.ui)

        # Set position based on main window
        main_win_x = self.ui.winfo_x()
        main_win_y = self.ui.winfo_y()
        window_width = self.ui.winfo_width()
        window_height = self.ui.winfo_height()
        box_win_x = int(main_win_x +
                        (window_width / 2 - self.m_box_width / 2))
        box_win_y = int(main_win_y +
                        (window_height / 3 - self.m_box_height / 2))
        m_box.geometry(str(self.m_box_width) +
                       "x" + str(self.m_box_height) +
                       "+" + str(box_win_x) +
                       "+" + str(box_win_y))
        m_box["bg"] = self.colours.bg_window
        try:
            m_box.iconbitmap("grid.ico")
        except TclError:
            m_box.iconbitmap()

        # Build the message box
        m_box.title(title)

        # Display message frame
        message_frame = Frame(m_box,
                              bg=self.colours.bg_dis_norm,
                              highlightthickness=0)
        message = Label(message_frame,
                        text=message,
                        font=self.m_box_font)

        message_height = self.tile_size * 2.5
        message_width = self.m_box_width - self.pad * 2
        message_frame.place(x=self.pad - self.m_box_frame_pad,
                            y=self.pad - self.m_box_frame_pad,
                            width=message_width + self.m_box_frame_pad * 2,
                            height=message_height + self.m_box_frame_pad * 2)
        message.place(x=self.m_box_frame_pad,
                      y=self.m_box_frame_pad,
                      width=message_width,
                      height=message_height)

        btn_y_pos = message_height + self.pad * 2

        # Display appropriate buttons based on type
        if type == "ok":
            return self.display_message_ok(m_box, btn_y_pos)
        elif type == "yesno":
            return self.display_message_yes_no(m_box, btn_y_pos)
        else:
            return False

    def display_message_ok(self, m_box: Toplevel, y_pos):
        """
        A function to display an 'ok' button on the message box and
        return to the main window once it is pressed.
        """
        # Display the button
        user_confirm = BooleanVar()  # Updated depending on button pressed
        user_confirm.set(False)
        btn_frame = Frame(m_box,
                          bg=self.colours.bg_en_norm,
                          highlightthickness=1,
                          highlightbackground=self.colours.fg_en_norm)
        btn = Button(btn_frame,
                     text="Ok",
                     font=self.m_box_font,
                     command=lambda: self.message_box_choice(m_box, True,
                                                             user_confirm))

        btn_width = self.tile_size * 3
        x_pos = self.m_box_width / 2 - btn_width / 2
        btn_frame.place(x=x_pos - self.m_box_frame_pad,
                        y=y_pos - self.m_box_frame_pad,
                        width=btn_width + self.m_box_frame_pad * 2,
                        height=self.tile_size + self.m_box_frame_pad * 2)
        btn.place(x=self.m_box_frame_pad - btn_frame["highlightthickness"],
                  y=self.m_box_frame_pad - btn_frame["highlightthickness"],
                  width=btn_width,
                  height=self.tile_size)

        # Wait for the confirmation box to be closed
        self.ui.wait_window(m_box)
        return user_confirm.get()

    def display_message_yes_no(self, m_box: Toplevel, y_pos):
        """
        A function to display yes or no buttons on the message box.
        Returns a Boolean depending on button pressed and returns to the
        main window.
        """
        # Display the buttons
        user_confirm = BooleanVar()  # Updated depending on button pressed
        user_confirm.set(False)

        y_frame = Frame(m_box,
                        bg=self.colours.bg_en_norm,
                        highlightthickness=1,
                        highlightbackground=self.colours.fg_en_norm)
        y_btn = Button(y_frame,
                       text="Yes",
                       font=self.m_box_font,
                       command=lambda: self.message_box_choice(m_box, True,
                                                               user_confirm))

        no_frame = Frame(m_box,
                         bg=self.colours.bg_en_norm,
                         highlightthickness=1,
                         highlightbackground=self.colours.fg_en_norm)
        no_btn = Button(no_frame,
                        text="No",
                        font=self.m_box_font,
                        command=lambda: self.message_box_choice(m_box, False,
                                                                user_confirm))

        btn_width = self.tile_size * 3
        yes_x_pos = self.m_box_width / 2 - btn_width - self.pad / 2

        y_frame.place(x=yes_x_pos - self.m_box_frame_pad,
                      y=y_pos - self.m_box_frame_pad,
                      width=btn_width + self.m_box_frame_pad * 2,
                      height=self.tile_size + self.m_box_frame_pad * 2)
        y_btn.place(x=self.m_box_frame_pad - y_frame["highlightthickness"],
                    y=self.m_box_frame_pad - y_frame["highlightthickness"],
                    width=btn_width,
                    height=self.tile_size)

        no_x_pos = self.m_box_width / 2 + self.pad / 2

        no_frame.place(x=no_x_pos - self.m_box_frame_pad,
                       y=y_pos - self.m_box_frame_pad,
                       width=btn_width + self.m_box_frame_pad * 2,
                       height=self.tile_size + self.m_box_frame_pad * 2)
        no_btn.place(x=self.m_box_frame_pad - no_frame["highlightthickness"],
                     y=self.m_box_frame_pad - no_frame["highlightthickness"],
                     width=btn_width,
                     height=self.tile_size)

        # Wait for the confirmation box to be closed
        self.ui.wait_window(m_box)
        return user_confirm.get()

    # Button Functions
    def message_box_choice(self, m_box: Toplevel, choice, confirm):
        """
        A function to handle a message box choice.
        """
        # Update the confirm with the choice
        confirm.set(choice)

        # Destroy the current message box
        m_box.destroy()
