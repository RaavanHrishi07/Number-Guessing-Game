
import json
import random
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


SCORE_FILE = Path.home() / ".number_guessing_game_scores.json"


def evaluate_guess(guess, secret_number, max_number):
    """Validate a guess and return its result."""
    if not 1 <= guess <= max_number:
        return "invalid"

    if guess == secret_number:
        return "correct"

    if guess < secret_number:
        return "low"

    return "high"


def load_best_scores():
    """Load saved best scores from disk."""
    try:
        with SCORE_FILE.open("r", encoding="utf-8") as file:
            scores = json.load(file)

        if not isinstance(scores, dict):
            return {}

        return {
            key: value
            for key, value in scores.items()
            if isinstance(key, str)
            and isinstance(value, int)
            and not isinstance(value, bool)
            and value > 0
        }
    except (OSError, json.JSONDecodeError):
        return {}


def save_best_scores(scores):
    """Save best scores to disk."""
    try:
        with SCORE_FILE.open("w", encoding="utf-8") as file:
            json.dump(scores, file, indent=4)
        return True
    except OSError:
        return False


class NumberGuessingGame:
    """A GUI-based number guessing game."""

    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("520x660")
        self.root.resizable(False, False)
        self.root.configure(bg="#121826")

        self.colors = {
            "bg": "#121826",
            "card": "#1E293B",
            "text": "#F8FAFC",
            "muted": "#94A3B8",
            "accent": "#38BDF8",
            "green": "#4ADE80",
            "red": "#FB7185",
            "button": "#0284C7",
        }

        self.difficulties = {
            "Easy (1-50)": 50,
            "Medium (1-100)": 100,
            "Hard (1-500)": 500,
        }

        self.max_number = 100
        self.secret_number = 0
        self.attempts = 0
        self.game_over = False
        self.best_scores = load_best_scores()

        self.build_ui()
        self.new_game()

    def build_ui(self):
        """Create the game interface."""

        tk.Label(
            self.root,
            text="NUMBER GUESSING GAME",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"],
        ).pack(pady=(24, 4))

        tk.Label(
            self.root,
            text="Can you find the secret number?",
            font=("Segoe UI", 11),
            bg=self.colors["bg"],
            fg=self.colors["muted"],
        ).pack(pady=(0, 20))

        self.card = tk.Frame(
            self.root,
            bg=self.colors["card"],
            padx=24,
            pady=20,
        )
        self.card.pack(fill="both", padx=28, pady=4)

        tk.Label(
            self.card,
            text="CHOOSE DIFFICULTY",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["card"],
            fg=self.colors["muted"],
        ).pack(anchor="w")

        self.difficulty_var = tk.StringVar(
            value="Medium (1-100)"
        )

        self.difficulty_menu = ttk.Combobox(
            self.card,
            textvariable=self.difficulty_var,
            values=list(self.difficulties.keys()),
            state="readonly",
            font=("Segoe UI", 11),
        )
        self.difficulty_menu.pack(fill="x", pady=(8, 18))
        self.difficulty_menu.bind(
            "<<ComboboxSelected>>",
            lambda event: self.new_game(),
        )

        self.range_label = tk.Label(
            self.card,
            text="Guess a number between 1 and 100",
            font=("Segoe UI", 12),
            bg=self.colors["card"],
            fg=self.colors["text"],
        )
        self.range_label.pack(pady=(0, 12))

        self.guess_entry = tk.Entry(
            self.card,
            font=("Segoe UI", 20),
            justify="center",
            bg="#0F172A",
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            width=12,
        )
        self.guess_entry.pack(ipady=9, fill="x")
        self.guess_entry.bind(
            "<Return>",
            lambda event: self.check_guess(),
        )

        self.guess_button = tk.Button(
            self.card,
            text="GUESS",
            command=self.check_guess,
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["button"],
            fg="white",
            activebackground="#0369A1",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
        )
        self.guess_button.pack(
            fill="x",
            pady=(14, 8),
            ipady=8,
        )

        self.feedback_label = tk.Label(
            self.card,
            text="Enter your first guess!",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["card"],
            fg=self.colors["accent"],
            wraplength=390,
        )
        self.feedback_label.pack(pady=10)

        self.attempts_label = tk.Label(
            self.card,
            text="Attempts: 0",
            font=("Segoe UI", 11),
            bg=self.colors["card"],
            fg=self.colors["muted"],
        )
        self.attempts_label.pack(pady=(4, 0))

        self.best_score_label = tk.Label(
            self.card,
            text="Best Score: —",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["card"],
            fg=self.colors["green"],
        )
        self.best_score_label.pack(pady=(8, 0))

        self.restart_button = tk.Button(
            self.root,
            text="↻  PLAY AGAIN",
            command=self.new_game,
            font=("Segoe UI", 11, "bold"),
            bg="#334155",
            fg=self.colors["text"],
            activebackground="#475569",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
        )
        self.restart_button.pack(
            pady=18,
            ipadx=18,
            ipady=8,
        )

        tk.Label(
            self.root,
            text="Tip: Each guess gives you a useful hint.",
            font=("Segoe UI", 9),
            bg=self.colors["bg"],
            fg=self.colors["muted"],
        ).pack()

    def update_best_score_label(self):
        """Display the best score for the selected difficulty."""
        difficulty = self.difficulty_var.get()
        best = self.best_scores.get(difficulty)

        if best is None:
            text = "Best Score: —"
        else:
            attempt_word = "attempt" if best == 1 else "attempts"
            text = f"Best Score: {best} {attempt_word}"

        self.best_score_label.config(text=text)

    def record_best_score(self):
        """Save a new record when the player beats their best score."""
        difficulty = self.difficulty_var.get()
        previous_best = self.best_scores.get(difficulty)

        if previous_best is None or self.attempts < previous_best:
            self.best_scores[difficulty] = self.attempts
            save_best_scores(self.best_scores)

        self.update_best_score_label()

    def new_game(self):
        """Start a fresh game."""
        self.max_number = self.difficulties.get(
            self.difficulty_var.get(),
            100,
        )

        self.secret_number = random.randint(1, self.max_number)
        self.attempts = 0
        self.game_over = False

        self.range_label.config(
            text=(
                f"Guess a number between 1 and "
                f"{self.max_number}"
            )
        )

        self.feedback_label.config(
            text="Enter your first guess!",
            fg=self.colors["accent"],
        )

        self.attempts_label.config(text="Attempts: 0")
        self.update_best_score_label()

        self.guess_entry.config(state="normal")
        self.guess_entry.delete(0, tk.END)
        self.guess_button.config(state="normal")

        self.guess_entry.focus_set()

    def check_guess(self):
        """Validate a guess and display the appropriate feedback."""
        if self.game_over:
            return

        value = self.guess_entry.get().strip()

        if not value:
            self.feedback_label.config(
                text="Please enter a number!",
                fg=self.colors["red"],
            )
            self.guess_entry.focus_set()
            return

        try:
            guess = int(value)
        except ValueError:
            self.feedback_label.config(
                text="Enter a whole number, please.",
                fg=self.colors["red"],
            )
            self.guess_entry.focus_set()
            return

        result = evaluate_guess(
            guess,
            self.secret_number,
            self.max_number,
        )

        if result == "invalid":
            self.feedback_label.config(
                text=(
                    f"Choose a number from 1 to "
                    f"{self.max_number}."
                ),
                fg=self.colors["red"],
            )
            self.guess_entry.focus_set()
            return

        self.attempts += 1
        self.attempts_label.config(
            text=f"Attempts: {self.attempts}"
        )

        if result == "correct":
            self.game_over = True
            self.record_best_score()

            attempt_word = (
                "attempt" if self.attempts == 1 else "attempts"
            )

            self.feedback_label.config(
                text=(
                    f"Correct! You got it in "
                    f"{self.attempts} {attempt_word}!"
                ),
                fg=self.colors["green"],
            )

            self.guess_entry.config(state="disabled")
            self.guess_button.config(state="disabled")

            messagebox.showinfo(
                "You Won!",
                f"Congratulations!\n"
                f"The secret number was {self.secret_number}.\n"
                f"Attempts: {self.attempts}",
            )

        elif result == "low":
            self.feedback_label.config(
                text="Too low! Try a higher number.",
                fg=self.colors["accent"],
            )

        else:
            self.feedback_label.config(
                text="Too high! Try a lower number.",
                fg=self.colors["red"],
            )

        if not self.game_over:
            self.guess_entry.delete(0, tk.END)
            self.guess_entry.focus_set()


def main():
    """Launch the game."""
    root = tk.Tk()
    NumberGuessingGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
