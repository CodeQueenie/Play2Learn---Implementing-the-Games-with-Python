import threading
import time

class Game:
    def __init__(self, game_time):
        # Initialize the game with a specified duration (in seconds)
        self.game_time = game_time
        # Create a background thread to manage the game timer
        self.timer = threading.Thread(target=self.start_timer)
        # Initialize the player's score
        self.score = 0
        # A threading event to signal when the game is concluded
        self.game_over = threading.Event()
        # Variable to hold the length of the words used in the game
        self.word_length = None
        # Lock to manage concurrent access to game-ending conditions
        self.lock = threading.Lock()
        # Flag to avoid multiple calls to end the game
        self.end_game_called = False
        # Indicates if all words targeted in the game have been found
        self.completed = False

    def update_time(self, num_of_words):
        # Check if no more words are needed, indicating game completion
        if num_of_words == 0:
            self.completed = True
            self.game_over.set()  # Signal that the game is over

    def start_timer(self):
        # Countdown the game time until it reaches 0 or the game is marked as over
        while self.game_time > 0 and not self.game_over.is_set():
            time.sleep(1)  # Wait for one second
            self.game_time -= 1  # Decrement the game timer
        if self.game_time <= 0:
            # If time expired, signal the game to conclude
            self.game_over.set()
            # Call end game with the completion status
            self.end_game(False)

    def end_game(self, completed, play_again=False):
        # Ensures that this method runs only once
        with self.lock:
            if self.end_game_called:
                return
        self.end_game_called = True

        # Display different messages based on the game's ending conditions
        if self.completed:  # All words were found
            print("\nCongratulations!")
            print(f"You found all anagrams for {self.word_length}-letter words!")
        elif completed:  # Game considered complete (can be used for different game logic)
            print("\nTime is up!")
            print(f"You got {self.score} anagrams for {self.word_length}-letter words!")
        else:  # Game not completed - time ran out
            print("\nTime is Up!")
            print(f"Sorry, you didn't get that last one in on time.")
            print(f"You got {self.score} anagrams for {self.word_length}-letter words!")

        # Offer a prompt to play again, note: implementation for play again is not provided 
        print("Press Enter to play again.")
        
        # Ensure the game is properly concluded
        self.quit_game()

    def quit_game(self):
        # Signal all threads that the game is over
        self.game_over.set()
        # Wait for the timer thread to complete if it is still running
        if self.timer.is_alive():
            self.timer.join()

    def run(self):
        # Placeholder for game logic - to be implemented by the developer
        raise NotImplementedError("You must implement the run method.")
