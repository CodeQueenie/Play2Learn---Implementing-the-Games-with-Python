from pathlib import Path
from main import Game  # Main game class imported from main.py
import threading  # For running the timer on a separate thread
import random  # To select random elements (e.g., words, anagrams)
import json  # For loading words from a JSON file


class AnagramHunt(Game):
    """Anagram Game Class implementing game logic for finding anagrams."""

    def users_choice(self):
        """Prompt the user to choose a word length within an acceptable range."""
        self.word_length = 0  # Variable to store user's chosen word length
        acceptable_range = [5, 6, 7, 8]  # Valid word lengths
        
        # Prompt user to select a word length from the acceptable range
        print(f"Please enter a word length {acceptable_range}: ", end="")
        
        while self.word_length not in acceptable_range:
            try:
                user_input = input()  # Capture user input
                self.word_length = int(user_input)  # Attempt to convert input to integer
                if self.word_length not in acceptable_range:  # Check if input is within the valid range
                    print(f"That is not a correct word length. Please try again {acceptable_range}: ", end="")
            except ValueError:
                # Handle case where conversion to integer fails
                print(f"That is not a correct word length. Please try again {acceptable_range}: ", end="")

        return self.word_length  # Return the validated word length chosen by the user

    def file_path(self, relative_path):
        """Construct an absolute file path from a relative path."""
        start_dir = Path(__file__).parent  # Get directory of the current script
        return Path(start_dir, relative_path)  # Return the full path

    def get_words(self):
        """Load words from a JSON file and format them for the game."""
        anagrams = Path("data/anagrams.json")  # Relative path to the JSON file
        path_to_file = self.file_path(anagrams)  # Get the absolute path to the file
        with path_to_file.open(encoding="utf-8") as f:  # Open file as UTF-8
            words = json.load(f)  # Load words from file
            words = dict(words)  # Ensure the data is in dictionary format
            # Convert all words to uppercase for consistency
            words = {
                k: [[word.upper() for word in sublist] for sublist in v]
                for k, v in words.items()
            }
            return words  # Return the formatted words

    def create_words_to_play(self, words):
        """Select a subset of words based on the chosen length."""
        # Use the chosen word length as a key to get the corresponding words
        key = str(self.word_length)
        words_to_guess = words.pop(key)  # Remove and return words of the chosen length

        return words_to_guess  # List of words to be guessed in the game

    def game_word_lists(self, words_to_guess):
        """Select a random block of words for the player to guess."""
        # Randomly choose a set of words for the round
        current_words_to_play = random.choice(words_to_guess)
        # Remove the chosen set from the pool of available words
        words_to_guess.remove(current_words_to_play)

        # Return the words for the current round and the remaining words
        return current_words_to_play, words_to_guess

    def check_guess(self, user_guess, current_words):
        """Check if the player's guess matches any of the current words."""
        # Return True if guess is correct, False otherwise
        return user_guess in current_words

    def run(self):
        """Main game loop responsible for running the Anagram Hunt game."""
        # Initialization of variables
        display_word = None
        num_of_words = None
        user_guess = None
        user_guesses = []  # Track user's guesses to provide feedback

        num_of_char = self.users_choice()  # Prompt user for word length choice

        if num_of_char:
            timer_thread = threading.Thread(target=self.start_timer)  # Start the game timer on a separate thread
            timer_thread.start()

        words = self.get_words()  # Load words from file

        words_to_guess = self.create_words_to_play(words)  # Prepare words for the game based on chosen length

        # Prepare the first set of words for the player
        current_words, game_play_words = self.game_word_lists(words_to_guess)
        words_on_hold = game_play_words  # Keep the remaining words for subsequent rounds

        display_word = random.choice(current_words)  # Select a word for display
        current_words.remove(display_word)  # Remove the displayed word from the current round's list
        num_of_words = len(current_words)  # Update the count of remaining words

        guessed_all = False  # Flag to track if all words have been guessed

        # Game loop: continues until all words are guessed or time runs out
        while (not guessed_all) and self.game_time > 0:
            # Display game information to the player
            print(f"The word is: {display_word}")
            print(f"There are {num_of_words} unguessed anagrams.")
            print(f"You have {self.game_time} seconds left.")

            user_guess = input("Make a guess: ").upper()  # Take player's guess in uppercase
            checked = self.check_guess(user_guess, current_words)  # Check if the guess is correct

            # Process the player's guess based on whether it's correct, already guessed, or invalid
            if not checked:
                if user_guess in user_guesses:
                    message = f"You already got {user_guess}. Try again."
                else:
                    message = f"{user_guess} is not a valid anagram. Please try again."
                user_guesses.append(user_guess)  # Add guess to the list of guesses
                
                # Handle time-up scenario
                if self.game_time == 0:
                    you_won = False  # Flag to indicate the player has lost
                    self.end_game(you_won)
                else:
                    print(message)  # Print feedback for incorrect guess
                    print("-" * 50)   # Print separator for clarity
            else:
                # Handle correct guess
                self.score += 1  # Increment player's score
                user_guesses.append(user_guess)  # Add correct guess to the list
                current_words.remove(user_guess)  # Remove guessed word from the current list
                num_of_words = len(current_words)  # Update count of remaining words

                # Provide feedback for correct guess or time-up scenario
                if self.game_time == 0:
                    print(f"\nSorry, you didn't get that answer in on time.")
                    you_won = False  # Flag to indicate the player has lost
                    self.end_game(you_won)
                else:
                    print(f"{user_guess} is correct!")
                    print("-" * 50)

            # Check if all words have been guessed in the current round
            if num_of_words == 0 and self.game_time > 0:
                guessed_all = True  # Set flag to indicate round completion
                print(f"You got all the anagrams for {display_word}!")  # Congratulate player
                print("-" * 50)

            # Prepare for the next round if there are still words to be guessed and time remains
            if guessed_all and game_play_words and self.game_time > 0:
                current_words, game_play_words = self.game_word_lists(words_on_hold)  # Get the next set of words
                user_guesses = []  # Reset guesses for the next round
                display_word = random.choice(current_words)  # Choose the next word for display
                current_words.remove(display_word)  # Remove the displayed word from the list
                num_of_words = len(current_words)  # Update count of remaining words

            # Update flags based on remaining words and the game situation
            if game_play_words:
                guessed_all = False

            if num_of_words:
                guessed_all = False

            # Final victory condition: no more words to guess and all rounds completed
            if not game_play_words and num_of_words == 0:
                guessed_all = True
                you_won = True  # Player has won the game
                print("Congratulations! You've guessed all anagrams.")
                break  # Exit the game loop


if __name__ == "__main__":
    while True:
        # Create a new game instance with a 60-second timer and run the game
        anagram_hunt = AnagramHunt(60)
        anagram_hunt.run()
