"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Student Id: 150126070
Name: Pavithra Subramaniyam
Email:xgpasu@tuni.fi

Dice game Project

***
A dice game with lots of dice or multiple players each of which require the GUI
to display one or more components which are created in a loop
****

"""

from tkinter import *
import time
import random

WIN_POINTS = 500
TOTAL_PLAYERS = 25      # can vary up to 25 for this given UI settings
NO_OF_DICE = 24         # can vary up to 24 for this given UI settings
MAX_DICE_IN_ROW = 6     # no changes, to be within the frame

# Image files in the project folder to show in interface
IMAGE_FILES = ["1S.gif", "2.gif", "3.gif", "4.gif", "5.gif", "6.gif"]

# Score table - size of the increment for fitting inside the window
if TOTAL_PLAYERS <= 5:
    INCR_SIZE = 0.75/TOTAL_PLAYERS
elif TOTAL_PLAYERS <= 10:
    INCR_SIZE = 0.5/TOTAL_PLAYERS
elif TOTAL_PLAYERS <= 25:
    INCR_SIZE = 0.75/TOTAL_PLAYERS
else:
    INCR_SIZE = 1/TOTAL_PLAYERS
    # If players are more than 25 then height of the frame should be adjusted

# Dice - size of the increment for fitting inside the window
INCR_WIDE = 0.08

class DiceGame:

    def __init__(self):
        """
        constructor initializing UI settings and game attributes
        :param:
        :return:
        """
        # Window layout and its geometry
        self.__window = Tk()
        self.__window.title("Dice game")
        width = 1600
        height = 1000   # If players are more than 25 then height should be adjusted
        dimensions = f"{width}"+"x"+f"{height}"
        self.__window.geometry(dimensions)

        # Dice rolling space layout
        center = Frame(self.__window, bg='Grey', width=750, height=800, padx=2, pady=2)
        center.place(relx=0.4, rely=0.4, anchor='center')

        self.__window.option_add("*Font", "Arial 16")
        self.__dice_label_list = []
        self.__points = [0] * TOTAL_PLAYERS
        self.__total_points = [0] * TOTAL_PLAYERS
        self.__curr_score = 0
        self.__total_score = 0
        self.__whose_turn = 0
        self.__display_message = ""

        # ======================================================================
        # Create PhotoImage-objects of the image files and store them in a list.
        self.__dice_images = []
        for image_file in IMAGE_FILES:
            new_image = PhotoImage(file=image_file)
            self.__dice_images.append(new_image)

        # 86x86 pixels initial value of empty image.
        self.__empty_image = PhotoImage(width=86, height=86)

        # ======================================================================
        # Defining Button formats and operations
        self.__newGame_button = Button(self.__window, text="New game", command=self.new_game, fg="Black")
        self.__newGame_button.place(relx=0.1, rely=0.1, anchor='center')

        self.__throw_button = Button(self.__window, text="THROW", command=self.throw, bg="Yellow", fg="Black")
        self.__throw_button.place(relx=0.1, rely=0.4, anchor='center')

        self.__handOver_button = Button(self.__window, text="Hand-over", command=self.hand_over, bg="Green", fg="White")
        self.__handOver_button.place(relx=0.1, rely=0.5, anchor='center')

        self.__quit_button = Button(self.__window, text="Quit game", command=self.__window.destroy, bg="red", fg="White")
        self.__quit_button.place(relx=0.1, rely=0.9, anchor='center')

        # ======================================================================
        # Dice image placement
        incr_side = 0
        incr_down = 0
        for i in range(NO_OF_DICE):
            if NO_OF_DICE < MAX_DICE_IN_ROW:    # Should proceed if no. of dice lies within the maximum frame limit
                self.__dice_label = Label(self.__window, anchor=N)
                self.__dice_label.place(relx=0.2+incr_side, rely=0.15, anchor='center')
                self.__dice_label_list.append(self.__dice_label)
                incr_side += INCR_WIDE          # increment the position to evenly place the dice

            else:
                if i % MAX_DICE_IN_ROW == 0:    # Should set proper increment value based on the maximum frame limit
                    incr_side = 0
                    if i != 0:                  # Should not increment for the first row first dice
                        incr_down += 0.2
                self.__dice_label = Label(self.__window, anchor=N)
                self.__dice_label.place(relx=0.2+incr_side, rely=0.15+incr_down, anchor='center')
                incr_side += INCR_WIDE          # increment the position to evenly place the dice
                self.__dice_label_list.append(self.__dice_label)

        # Header for the Dice space
        formatting_line = "-"*40
        self.__diceLabel = Label(self.__window, text=f"{formatting_line}Dice rolling space{formatting_line}",\
                                 anchor="center", bg="White", fg="Black", relief="sunken")
        self.__diceLabel.place(relx=0.4, rely=0.05, anchor='center')

        # ======================================================================
        # Display labels
        if NO_OF_DICE < 2:
            self.__display_label = Label(self.__window, anchor="center", bg="Black", fg="White", relief="solid")
            self.__display_label.place(relx=0.4, rely=0.9, anchor='center')

        else:
            self.__display_label = Label(self.__window, anchor="center", bg="Black", fg="White", relief="solid")
            self.__display_label.place(relx=0.4, rely=0.9, anchor='center')

        # ======================================================================
        # Text labels for the current score and total scores
        increment = 0
        for i in range(TOTAL_PLAYERS):
            self.__Player_label = Label(self.__window, text="Player " + str(i + 1))
            self.__Player_label.place(relx=0.68, rely=0.2+increment, anchor='center')
            increment += INCR_SIZE

        self.__newScore_label = Label(self.__window, text="New score", bg="White", fg="Blue", relief="ridge")
        self.__newScore_label.place(relx=0.79, rely=0.12, anchor='center')

        self.__TotScore_label = Label(self.__window, text="Total score", bg="White", fg="Red", relief="ridge")
        self.__TotScore_label.place(relx=0.9, rely=0.12, anchor='center')

        # ======================================================================
        # Labels where new scores are displayed.

        self.__new_score_labels = []
        increment = 0
        for i in range(TOTAL_PLAYERS):
            new_point_label = Label(self.__window, width=8, relief="groove", anchor=E)
            new_point_label.place(relx=0.79, rely=0.2+increment, anchor='center')
            increment += INCR_SIZE
            self.__new_score_labels.append(new_point_label)

        # ======================================================================
        # Labels where total scores are displayed.

        self.__total_score_labels = []
        increment = 0
        for i in range(TOTAL_PLAYERS):
            total_point_label = Label(self.__window, width=8, relief="groove", anchor=E)
            total_point_label.place(relx=0.9, rely=0.2+increment, anchor='center')
            increment += INCR_SIZE
            self.__total_score_labels.append(total_point_label)

        # ======================================================================

        self.new_game()
        self.__window.mainloop()

# ==================================================================================================================== #
    # User interface part is over, Game logical part begins
    def new_game(self):
        """
        starts a new game
        - initializes the attributes
        :param:
        :return:
        """
        self.__points = [0] * TOTAL_PLAYERS
        self.__total_points = [0] * TOTAL_PLAYERS
        self.__total_score = 0
        self.__whose_turn = 0
        self.__display_message = "Player " + str(self.__whose_turn + 1) + " throw the dice or hand over the turn!"

        self.update_gui()
        for dice_label in self.__dice_label_list:
            dice_label.configure(image=self.__empty_image)

        # Activate the buttons that can be deactivated
        self.__throw_button.configure(state=NORMAL)
        self.__handOver_button.configure(state=NORMAL)

    def update_gui(self):
        """
        Method that updates the texts in the GUI components
        :param:
        :return:
        """
        for i in range(TOTAL_PLAYERS):
            self.__new_score_labels[i].configure(text=self.__points[i])
            self.__total_score_labels[i].configure(text=self.__total_points[i])
        self.__display_label.configure(text=self.__display_message)

    def throw(self):
        """
        Throws the dice when the button is pressed and updates the
        :param:
        :return:
        """
        random_list = []
        itr = 0
        for dice_label in self.__dice_label_list:
            # any random numbers from 1 to 6
            random_list.append(random.randint(1, 6))
            dice_label["image"] = self.__dice_images[random_list[itr] - 1]
            self.__window.update_idletasks()
            time.sleep(0.05)
            itr += 1

        if all(elem == 1 for elem in random_list):
            self.change_turn()
        else:
            self.__curr_score = sum(random_list)
        # storing in the temporary memory before hand over
        self.__points[self.__whose_turn] += self.__curr_score
        self.update_gui()

    def hand_over(self):
        """
        When player clicks hand over, changes the turn to next player after assigning the total score
        and resetting the new score list
        :param:
        :return:
        """
        self.__total_points[self.__whose_turn] += self.__curr_score
        self.__points = [0] * TOTAL_PLAYERS     # resetting after accumulating to the total points
        self.change_turn()

    def change_turn(self):
        """
        Changes the turn to next, clears the new score in GUI, when player clicks hand over
        :param:
        :return:
        """
        if self.__whose_turn == TOTAL_PLAYERS - 1:
            if self.is_over():
                return

        self.__whose_turn = (self.__whose_turn + 1) % TOTAL_PLAYERS
        self.__display_message = "Player " + str(self.__whose_turn + 1) + " throw the dice or hand over the turn"
        self.__curr_score = 0
        self.update_gui()

    #
    def is_over(self):
        """
        check whether the game is over and set the message announcing the player
        :param:
        :return: return True
        """
        winners_list = []
        for i in range(len(self.__points)):
            if self.__points[i] >= WIN_POINTS:
                winners_list.append(i)

        if len(winners_list) == 0:
            return False
        elif len(winners_list) == 1:
            self.__display_message = "Player " + str(winners_list[0] + 1) + " has won!"
        elif len(winners_list) == 2:
            self.__display_message = "Game ends in draw between Player " + str(winners_list[0] + 1) and \
                                     "Player" + str(winners_list[1] + 1) + "!"
        else:
            self.__display_message = "Game Drawn!"
        self.update_gui_texts()

        # Disable the buttons that should not be clicked when the game is over.
        self.__throw_button.configure(state=DISABLED)
        self.__handOver_button.configure(state=DISABLED)
        return True


def main():
    DiceGame()


if __name__ == "__main__":
    main()
