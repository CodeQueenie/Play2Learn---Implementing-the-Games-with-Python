import threading
import time

class Game:
    def __init__(self, game_time):
        """Initialize the game with a set time limit."""
        self.game_time = game_time  # Game time in seconds
        self.timer = threading.Thread(target=self.start_timer)  # Timer thread
        self.score = 0  # Initialize score
        self.game_over = threading.Event()  # Event to signal game over
        self.word_length = None  # The chosen word length for the anagrams

    def start_timer(self):
        """Start the timer and decrement game time every second."""
        while self.game_time > 0 and not self.game_over.is_set():
            time.sleep(1)  # Wait for a second
            self.game_time -= 1  # Decrement the game time
        if self.game_time <= 0:  # If no time is left, set game_over event
            self.game_over.set()
            self.end_game(False)  # End game due to time running out

    def end_game(self, completed):
        """End the game with different messages based on how the game ended."""
        if self.game_over.is_set() and not completed:
            # Case when time runs out
            print("\nTime is Up!")
            print(f"\nSorry, you didn't get that last one in on time.")
        elif completed:
            # Case when all anagrams are found before time runs out
            print("\nYou Won!")

        # Common ending message
        print(f"You got {self.score} anagrams for {self.word_length}-letter words!")
        print("Press Enter to play again or 'q' to quit:")
        self.quit_game()  # Option to quit or r to be implemented here

    def quit_game(self):
        """Stops the game timer thread and sets the game_over event."""
        self.game_over.set()
        if self.timer.is_alive():
            self.timer.join()

    def run(self):
        """Placeholder for the run method. Must be implemented."""
        raise NotImplementedError("You must implement the run method.")
