# Import necssary libraries
import random
import tkinter as tk
from tkinter import Label, ttk, Text, Scrollbar
import threading
import pygame
import time
import main

def new_game():
        game = DeadAndInjuredGame()
        game.run_game()

class DeadAndInjuredGame:
    def __init__(self):
        """
        Initializes the Dead and Injured game GUI and sets up initial configurations.
        """
        self.root = tk.Tk()
        self.root.title("Dead and Injured")
        self.root.configure(bg="#1d1e1f")
        self.style = ttk.Style()
        self.style.configure("Rounded.TFrame", background="black", relief="groove")
        self.style.configure("TButton", font=('FixedSys', 13), foreground='white')

        self.initialize_variables()
        self.setup_gui_layout()
        self.configure_gui_styles()


    def show_guide(self):
        """
        Displays the guide for playing the Dead and Injured game.
        """
        self.guide = tk.Tk()
        self.guide.title("Guide")
        self.guide.configure(bg="#1d1e1f")

        guide_text = """
        INTRODUCTION
        Welcome to the "Dead and Injured" game version 1.0.0! This is a number guessing game where your goal is to figure out a secret four-digit number. As you make guesses, the game provides feedback on the number of correct digits in the correct position (Dead) and the number
        of correct digits in the wrong position (Injured). Use this information to refine your guesses and win the game!

        HOW TO PLAY
        1. Getting Started:
        Run the application provided to launch the game interface. Upon starting the game, a random four-digit number will be generated for you to guess. This number is your target, and the game will provide feedback based on your guesses.

        2. Making a Guess:
        Enter your four-digit guess into the input field labeled "Enter your guess below." Click the "Done" button to submit your guess and receive feedback.

        3. Feedback:
        The game will display the number of correct digits in the correct position as "Dead" and the number of correct digits in the wrong position as "Injured." Use this feedback to refine your guesses and make progress towards the correct solution.

        4. Winning:
        If you correctly guess all four digits in the correct positions, you win! The game will display your winning message along with the number of attempts made and the elapsed time.

        5. Restarting the Game:
        If you want to play again, click the "Restart" button to generate a new target number and reset the game.

        6. Audio Controls:
        The game features background music. You can use the "Mute" and "Unmute" buttons to control the audio.

        ERROR MESSAGES
        1. Invalid Input:
        If you enter a guess that is not a four-digit number, the game will display an error message. Example: "Error: Number must be 4 digits, i.e., XXXX. Try Again."

        2. Repeated Digits:
        If your guess contains repeated digits, the game will prompt you to enter a number with four different digits. Example: "Error: Number must have 4 different digits. Example: '1234' is allowed, but '1224' is invalid. Try Again."

        3. General Errors:
        If an unexpected error occurs, the game will display a generic "Invalid Input. Try Again." message.

        ADDITIONAL INFORMATION
        1. Game History:
        The game keeps track of your guesses in a history panel, showing the number, Dead, and Injured counts for each attempt.

        2. Exiting the Game:
        Click the "Exit" button to close the game window.

        Enjoy the Game!
        Thank you for playing the "Dead and Injured" game. Have fun and good luck in solving the mystery number!
        """

        space = Label(self.guide, text="\n\n\n", bg="#1d1e1f", font=('Helvetica', 15, 'bold'))
        space.pack(pady=10)

        guide_frame_1 = ttk.Frame(self.guide, style="Rounded.TFrame")
        guide_frame_2 = ttk.Frame(guide_frame_1, style="Rounded.TFrame")
        guide_frame = Text(guide_frame_2, bg="#131313", fg="red", wrap="none", font=('FixedSys', 12), height=30, width=200)

        scrollbar = Scrollbar(guide_frame_2, command=self.history_text.yview)
        guide_frame.config(yscrollcommand=scrollbar.set)

        guide_frame_1.pack(pady=10)
        guide_frame_2.pack(pady=5, padx=5)
        guide_frame.pack(side=tk.LEFT, fill=tk.Y, pady=20, padx=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        guide_frame.insert(tk.END, guide_text)

        space = Label(self.guide, text="\n\n\n", bg="#1d1e1f", font=('Helvetica', 15, 'bold'))
        space.pack(pady=10)

        exit_button = ttk.Button(self.guide, text="Exit", command=self.guide.destroy, style="TButton")
        exit_button.pack(side="bottom", anchor="s")

        self.guide.mainloop()

    def initialize_variables(self):
        """
        Initializes the game variables.
        """
        self.start_time = time.time()
        self.end_time = 0
        self.four_digit_number = random.sample(range(10), 4)
        self.initial_guess = ''.join(map(str, self.four_digit_number))
        self.final_answer = '{:04}'.format(self.initial_guess)
        print("final_answer = " + self.final_answer) # For self-check debugging
        self.trials_used = 1
        self.mute = False

    def setup_gui_layout(self):
        """
        Sets up the layout of the Dead and Injured game GUI.
        """
        self.setup_game_panel()
        self.setup_entry_widget()
        self.setup_done_button()
        self.setup_result_label()
        self.setup_audio_buttons()
        self.setup_history_frame()
        self.setup_guide_and_exit_buttons()

    def setup_game_panel(self):
        """
        Sets up the game panel in the GUI.
        """
        guide_panel = Label(self.root, text="\t\t        WELCOME TO DEAD AND INJURED\t\t\t",  bg="#1d1e1f", font=('FixedSys', 18, 'bold'))
        guide_panel.pack()

        version_label = Label(self.root, text="\t\t          Version 1.0.0 (Medium)\t\t\t",  bg="#1d1e1f", fg="red", font=('FixedSys', 10, 'bold'))
        version_label.pack()

    def setup_entry_widget(self):
        """
        Sets up the entry widget for entering guesses in the GUI.
        """
        label_name = Label(self.root, text="Enter your 4-digit guess below",  bg="#1d1e1f")
        label_name.pack()

        self.entry_widget = tk.Entry(self.root)
        self.entry_widget.pack()

    def setup_done_button(self):
        """
        Sets up the "Done" button in the GUI.
        """
        done_button = ttk.Button(self.root, text="Done", command=lambda: self.evaluate(), style="TButton")
        done_button.pack()

    def setup_result_label(self):
        """
        Sets up the result label in the GUI.
        """
        result_label_frame_1 = ttk.Frame(self.root, style="Rounded.TFrame")
        result_label_frame_2 = ttk.Frame(result_label_frame_1, style="Rounded.TFrame")
        self.result_label = Label(result_label_frame_2, text="\t\t\t\t\n", bg="#131313", fg="white", wraplength=400, font=('FixedSys', 12))
        result_label_frame_1.pack(pady=10)
        result_label_frame_2.pack(pady=5, padx=5)
        self.result_label.pack()

    def setup_audio_buttons(self):
        """
        Sets up the audio control buttons (Mute/Unmute) in the GUI.
        """
        mute_button = ttk.Button(self.root, text="Mute", command=self.mute_audio, style="TButton")
        umute_button = ttk.Button(self.root, text="Unmute", command=self.unmute_audio, style="TButton")
        mute_button.pack(side=tk.TOP)
        umute_button.pack(side=tk.TOP)

    def setup_history_frame(self):
        """
        Sets up the history frame to display the game history in the GUI.
        """
        history_frame_1 = ttk.Frame(self.root, style="Rounded.TFrame")
        history_frame_2 = ttk.Frame(history_frame_1, style="Rounded.TFrame")
        self.history_text = Text(history_frame_2, bg="#131313", fg="white", wrap="none", font=('FixedSys', 12), height=10, width=50)

        scrollbar = Scrollbar(history_frame_2, command=self.history_text.yview, background="red")
        self.history_text.config(yscrollcommand=scrollbar.set)

        history_frame_1.pack(pady=10)
        history_frame_2.pack(pady=5, padx=5)
        self.history_text.pack(side=tk.LEFT, fill=tk.Y)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.insert(tk.END, "\n\t|------------------HISTORY-------------------|\n\n\t|----| NUMBER |-----| DEAD |---| INJURED |----|\n")

    def setup_guide_and_exit_buttons(self):
        """
        Sets up the guide, restart, and exit buttons in the GUI.
        """
        guide_button = ttk.Button(self.root, text="Guide", command=self.show_guide, style="TButton")
        guide_button.pack()

        space = Label(self.root, text="\n\n\n",  bg="#1d1e1f", font=('Helvetica', 15, 'bold'))
        space.pack(pady=10)

        exit_button = ttk.Button(self.root, text="Exit", command=self.root.destroy, style="TButton")
        exit_button.pack(side="bottom", anchor="s")

        main_menu_button = ttk.Button(self.root, text="Menu", command=self.main_menu, style="TButton")
        main_menu_button.pack(side="bottom", anchor="s")

        restart_button = ttk.Button(self.root, text="Restart", command=self.restart, style="TButton")
        restart_button.pack(side="bottom", anchor="s")

    def configure_gui_styles(self):
        """
        Configures the styles for various GUI elements.
        """
        style = ttk.Style()
        style.configure("Rounded.TEntry", borderwidth=0, bordercolor="blue", relief="flat", background="blue", padding=(5, 5), width=200)
        style.configure("Rounded.TFrame", background="black", relief="groove")
        style.configure("TButton", font=('FixedSys', 13), foreground='white')

    def evaluate(self):
        """
        Evaluates the user's guess and provides feedback in the GUI.
        """
        try:
            num_of_dead = 0
            num_of_injured = 0

            number = self.entry_widget.get()

            if self.check_input(number) == False:
                return

            for i in range(0, len(number)):
                if number[i] == self.final_answer[i]:
                    num_of_dead += 1

            for i in range(0, len(number)):
                if number[i] != self.final_answer[i] and number[i] in self.final_answer:
                    num_of_injured += 1

            if num_of_dead == 4:
                self.handle_successful_response()
            else:
                self.handle_unsuccessful_response(num_of_dead, num_of_injured)

            self.trials_used += 1
            self.update_history(num_of_dead, num_of_injured, self.entry_widget.get())

        except Exception as e:
            self.result_label.config(text="Invalid Input\nTry Again")
            self.style.configure("Rounded.TFrame", background="red", relief="groove")

    def check_input(self, number):
        """
        Checks the validity of the user's input.
        """
        if len(number) != 4:
            self.result_label.config(text=f"Error: Number must be 4 digit\n i.e XXXX\nTry Again")
            self.style.configure("Rounded.TFrame", background="red", relief="groove")
            return False

        new_list = []
        for digit in number:
            if digit not in new_list:
                new_list.append(digit)
            else:
                self.result_label.config(text=f"Error: Number must have 4 different digits\nExample: '1234' is allowed but '1224' is invalid.\nTry Again")
                self.style.configure("Rounded.TFrame", background="red", relief="groove")
                return False

        return True

    def handle_successful_response(self):
        """
        Handles the case when the user successfully guesses the number.
        """
        self.end_time = time.time()
        timer_seconds = self.end_time - self.start_time
        self.result_label.config(text=f"4 Dead --------- 0 Injured\nYou won\n\nAttempts: {self.trials_used}\nElasped Time: {(timer_seconds // 60):.0f} mins {(timer_seconds % 60):.0f} seconds")
        self.style.configure("Rounded.TFrame", background="green", relief="groove")

        if not self.mute:
            self.play_audio("Soundtrack.mp3")

    def handle_unsuccessful_response(self, num_of_dead, num_of_injured):
        """
        Handles the case when the user's guess is unsuccessful.
        """
        self.result_label.config(text=f"{num_of_dead} Dead --------- {num_of_injured} Injured\nTry Again")
        self.style.configure("Rounded.TFrame", background="yellow", relief="groove")

    def update_history(self, num_of_dead, num_of_injured, number):
        """
        Updates the game history in the GUI.
        """
        current = self.history_text.get("1.0", tk.END)
        new_text = f"\t|------| {number} |---------| {num_of_dead} |-----------| {num_of_injured} |------|\n"
        self.history_text.delete("1.0", tk.END)
        self.history_text.insert(tk.END, current + new_text)



    def play_audio(self, file_path):
        """
        Plays the specified audio file.
        """
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1)

    def mute_audio(self):
        """
        Mutes the game audio.
        """
        self.mute = True
        pygame.mixer.init()
        pygame.mixer.music.stop()

    def unmute_audio(self):
        """
        Unmutes the game audio.
        """
        self.mute = False
        self.play_audio("Background_soundtrack.mp3")

    def restart(self):
        """
        Restarts the game with new settings.
        """
        self.initialize_variables()
        self.result_label.config(text="\t\t\t\t\n")
        self.style.configure("Rounded.TFrame", background="blue", relief="groove")
        self.entry_widget.delete(0, tk.END)
        self.history_text.delete("1.0", tk.END)
        self.history_text.insert(tk.END, "\n\t|------------------HISTORY-------------------|\n\n\t|----| NUMBER |-----| DEAD |---| INJURED |----|\n")
        if not self.mute:
            self.play_audio("Background_soundtrack.mp3")

    def run_game(self):
        """
        Runs Dead and Injured game.
        """
        thread1 = threading.Thread(target=self.play_audio, args=("Background_soundtrack.mp3",))
        thread1.start()
        self.root.mainloop()

    def main_menu(self):
        pygame.mixer.music.stop()
        pygame.quit()
        self.root.destroy()
        main.new_game()

if __name__ == "__main__":
    new_game()