from tkinter import Tk, Label, ttk
import threading
import tkinter as tk
import pygame
import easy_level, medium_level, hard_level


class GameApp:
    def __init__(self, root, options):
        self.root = root
        self.root.title("Dead and Injured")
        self.root.configure(bg="#1d1e1f")

        # Create a StringVar to store the selected value
        self.selected_option = tk.StringVar(self.root)

        # Set up the GUI layout
        self.create_gui_layout(options)

        # Start the background music thread
        self.start_background_music()

    def create_gui_layout(self, options):
        guide_panel = Label(self.root, text="\t\t        WELCOME TO DEAD AND INJURED\t\t\t", bg="#1d1e1f", font=('FixedSys', 18, 'bold'))
        guide_panel.pack()

        guide_panel = Label(self.root, text="\t\t          Version 1.0.0\t\t\t", bg="#1d1e1f", fg="red", font=('FixedSys', 10, 'bold'))
        guide_panel.pack()

        space = Label(self.root, text="\n", bg="#1d1e1f", font=('Helvetica', 15, 'bold'))
        space.pack(pady=10)

        label_name = Label(self.root, text="Select a difficulty level", bg="#1d1e1f")
        label_name.pack()

        # Create the dropdown menu
        dropdown_menu = tk.OptionMenu(self.root, self.selected_option, *options)
        dropdown_menu.pack(pady=20)

        space = Label(self.root, text="\n", bg="#1d1e1f", font=('Helvetica', 15, 'bold'))
        space.pack(pady=10)

        start_button = ttk.Button(self.root, text="Start", command=self.start_game, style="TButton")
        start_button.pack()

        space = Label(self.root, text="\n", bg="#1d1e1f", font=('Helvetica', 15, 'bold'))
        space.pack(pady=10)

        exit_button = ttk.Button(self.root, text="Exit", command=self.root.destroy, style="TButton")
        exit_button.pack()

        space = Label(self.root, text="\n", bg="#1d1e1f", font=('Helvetica', 15, 'bold'))
        space.pack(pady=10)

    def start_background_music(self):
        # Create a separate thread for playing background music
        thread1 = threading.Thread(target=self.play_audio, args=("main_menu_tracks.mp3",))
        thread1.start()

    def play_audio(self, file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1)  # -1 plays the music indefinitely

    def start_game(self):
        # Function to be executed when the "Start" button is clicked
        difficulty = self.selected_option.get()

        if difficulty not in ["Easy (3 Digits)", "Medium (4 Digits)", "Hard (5 Digits)"]:
            return
        
        
        pygame.mixer.music.stop()
        pygame.quit()
        self.root.destroy()

        if difficulty == "Easy (3 Digits)":
            easy_level.new_game()

        if difficulty == "Medium (4 Digits)":
            medium_level.new_game()

        if difficulty == "Hard (5 Digits)":
            hard_level.new_game()

    

def new_game():
    options = ["Easy (3 Digits)", "Medium (4 Digits)", "Hard (5 Digits)"]
    root = Tk()
    GameApp(root, options)
    root.mainloop()

if __name__ == "__main__":
    new_game()