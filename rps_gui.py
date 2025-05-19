import tkinter as tk
import random

class RPSGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors")
        self.root.geometry("500x560")
        self.root.configure(bg="#f0f0f0")

        self.choices = ["Rock", "Paper", "Scissors"]
        self.user_score = 0
        self.computer_score = 0
        self.player1_score = 0
        self.player2_score = 0
        self.player_turn = 1  # For 2-player mode

        self.two_player_mode = False

        self.player1_name = tk.StringVar(value="You")
        self.player2_name = tk.StringVar(value="Computer")

        self.title_label = tk.Label(root, text="Rock-Paper-Scissors", font=("Georgia", 20, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=15)

        self.mode_button = tk.Button(root, text="Switch to 2-Player Mode", font=("Georgia", 12), command=self.toggle_mode)
        self.mode_button.pack(pady=5)

        self.names_visible = True
        self.toggle_names_button = tk.Button(root, text="Hide Name Edit", font=("Georgia", 12), command=self.toggle_name_edit)
        self.toggle_names_button.pack(pady=5)

        self.name_frame = tk.Frame(root, bg="#f0f0f0")
        self.name_frame.pack(pady=5)

        tk.Label(self.name_frame, text="Player 1 Name:", font=("Georgia", 12), bg="#f0f0f0").grid(row=0, column=0, sticky="e")
        self.player1_entry = tk.Entry(self.name_frame, font=("Georgia", 12), textvariable=self.player1_name, width=15)
        self.player1_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.name_frame, text="Player 2 Name:", font=("Georgia", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="e")
        self.player2_entry = tk.Entry(self.name_frame, font=("Georgia", 12), textvariable=self.player2_name, width=15)
        self.player2_entry.grid(row=1, column=1, padx=5)

        self.name_display_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.player1_name_label = tk.Label(self.name_display_frame, text="", font=("Georgia", 12, "bold"), bg="#f0f0f0")
        self.player2_name_label = tk.Label(self.name_display_frame, text="", font=("Georgia", 12, "bold"), bg="#f0f0f0")

        self.result_label = tk.Label(root, text="", font=("Georgia", 16), bg="#f0f0f0")
        self.result_label.pack(pady=20)

        self.score_label = tk.Label(root, text="", font=("Georgia", 14), bg="#f0f0f0")
        self.score_label.pack(pady=10)

        self.turn_label = tk.Label(root, text="", font=("Georgia", 14), bg="#f0f0f0")
        self.turn_label.pack(pady=5)

        self.button_frame = tk.Frame(root, bg="#f0f0f0")
        self.button_frame.pack(pady=20)

        self.choice_colors = {
            "Rock": "#add8e6",      # Light Blue
            "Paper": "#90ee90",     # Light Green
            "Scissors": "#f08080"   # Light Coral
        }
        self.default_button_color = None  # To store default bg color

        self.buttons = []
        for choice in self.choices:
            btn = tk.Button(self.button_frame, text=choice, font=("Georgia", 14), width=10,
                            command=lambda c=choice: self.start_round(c))
            btn.pack(side=tk.LEFT, padx=12)
            self.buttons.append(btn)

        self.root.after(100, self.set_default_button_color)  # Capture default color after init

        self.reset_button = tk.Button(root, text="Reset Game", font=("Georgia", 12), command=self.reset_game)
        self.reset_button.pack(pady=15)

        self.animation_steps = ["Rock...", "Paper...", "Scissors..."]
        self.anim_index = 0

        self.player1_choice = None
        self.player2_choice = None

        self.update_name_edit_visibility()
        self.update_labels()

    def set_default_button_color(self):
        if self.buttons:
            self.default_button_color = self.buttons[0].cget("bg")

    def toggle_mode(self):
        self.two_player_mode = not self.two_player_mode
        if self.two_player_mode:
            self.mode_button.config(text="Switch to Single Player Mode")
            self.player2_name.set("Player 2")
            self.player1_score = 0
            self.player2_score = 0
        else:
            self.mode_button.config(text="Switch to 2-Player Mode")
            self.player2_name.set("Computer")
            self.user_score = 0
            self.computer_score = 0

        self.player_turn = 1
        self.player1_choice = None
        self.player2_choice = None
        self.result_label.config(text="")
        self.update_name_edit_visibility()
        self.update_labels()
        for btn in self.buttons:
            btn.config(state=tk.NORMAL, bg=self.default_button_color)

    def toggle_name_edit(self):
        if self.names_visible:
            self.name_frame.pack_forget()
            self.show_name_labels()
            self.toggle_names_button.config(text="Show Name Edit")
            self.names_visible = False
        else:
            self.name_display_frame.pack_forget()
            self.name_frame.pack(pady=5)
            self.toggle_names_button.config(text="Hide Name Edit")
            self.names_visible = True

        self.update_name_edit_visibility()
        self.update_labels()

    def show_name_labels(self):
        self.name_display_frame.pack(pady=5)
        self.player1_name_label.config(text=f"Player 1: {self.player1_name.get()}")
        self.player1_name_label.grid(row=0, column=0, padx=10)

        if self.two_player_mode:
            self.player2_name_label.config(text=f"Player 2: {self.player2_name.get()}")
        else:
            self.player2_name_label.config(text=f"Player 2: Computer")
        self.player2_name_label.grid(row=0, column=1, padx=10)

    def update_name_edit_visibility(self):
        if self.two_player_mode and self.names_visible:
            self.player2_entry.grid()
        else:
            self.player2_entry.grid_remove()

    def update_labels(self):
        if self.two_player_mode:
            self.score_label.config(text=f"{self.player1_name.get()}: {self.player1_score}  |  {self.player2_name.get()}: {self.player2_score}")
            self.turn_label.config(text=f"{self.player1_name.get()}'s turn" if self.player_turn == 1 else f"{self.player2_name.get()}'s turn")
        else:
            self.score_label.config(text=f"{self.player1_name.get()}: {self.user_score}  |  Computer: {self.computer_score}")
            self.turn_label.config(text=f"Your turn, {self.player1_name.get()}")

    def start_round(self, choice):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
            if btn["text"] == choice:
                btn.config(bg=self.choice_colors.get(choice, "white"))
            else:
                btn.config(bg=self.default_button_color)

        self.update_labels()

        if self.two_player_mode:
            if self.player_turn == 1:
                self.player1_choice = choice
                self.player_turn = 2
                self.result_label.config(text=f"{self.player1_name.get()} chose. Now {self.player2_name.get()}'s turn.")
                self.turn_label.config(text=f"{self.player2_name.get()}'s turn")
                for btn in self.buttons:
                    btn.config(state=tk.NORMAL)
            else:
                self.player2_choice = choice
                self.anim_index = 0
                self.result_label.config(text="")
                self.turn_label.config(text="")
                self.animate_countdown()
        else:
            self.user_choice = choice
            self.computer_choice = random.choice(self.choices)
            self.anim_index = 0
            self.result_label.config(text="")
            self.update_labels()
            self.animate_countdown()

    def animate_countdown(self):
        if self.anim_index < len(self.animation_steps):
            self.result_label.config(text=self.animation_steps[self.anim_index])
            self.anim_index += 1
            self.root.after(700, self.animate_countdown)
        else:
            self.show_result()

    def show_result(self):
        if self.two_player_mode:
            user = self.player1_choice
            comp = self.player2_choice
            result_text = f"{self.player1_name.get()} chose: {user} | {self.player2_name.get()} chose: {comp}\n"

            if user == comp:
                result_text += "It's a tie! 🤝"
            elif (user == "Rock" and comp == "Scissors") or \
                 (user == "Paper" and comp == "Rock") or \
                 (user == "Scissors" and comp == "Paper"):
                result_text += f"{self.player1_name.get()} wins this round! 🎉"
                self.player1_score += 1
            else:
                result_text += f"{self.player2_name.get()} wins this round! 🎉"
                self.player2_score += 1

            self.result_label.config(text=result_text)
            self.player_turn = 1
            self.player1_choice = None
            self.player2_choice = None
            self.update_labels()
        else:
            user = self.user_choice
            comp = self.computer_choice
            result_text = f"{self.player1_name.get()} chose: {user} | Computer chose: {comp}\n"

            if user == comp:
                result_text += "It's a tie! 🤝"
            elif (user == "Rock" and comp == "Scissors") or \
                 (user == "Paper" and comp == "Rock") or \
                 (user == "Scissors" and comp == "Paper"):
                result_text += f"{self.player1_name.get()} wins this round! 🎉"
                self.user_score += 1
            else:
                result_text += "Computer wins this round! 🎉"
                self.computer_score += 1

            self.result_label.config(text=result_text)
            self.update_labels()

        for btn in self.buttons:
            btn.config(bg=self.default_button_color, state=tk.NORMAL)

    def reset_game(self):
        self.user_score = self.computer_score = self.player1_score = self.player2_score = 0
        self.player_turn = 1
        self.player1_choice = None
        self.player2_choice = None
        self.result_label.config(text="")
        self.update_labels()
        for btn in self.buttons:
            btn.config(state=tk.NORMAL, bg=self.default_button_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = RPSGame(root)
    root.mainloop()
