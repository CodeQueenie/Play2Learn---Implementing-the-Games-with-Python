import threading
import random
import time

class Game:
    def __init__(self):
        """Initializes a new instance of the Game class."""
        self.reset_game()

    def reset_game(self):
        """Resets the game's state to its initial values."""
        self.score = 0  # Player's score
        self.problem_count = 0  # Number of problems attempted
        self.game_time = 30  # Duration of the game in seconds
        self.timer_stop = threading.Event()  # Event flag to control the timer thread

    def choose_operation(self):
        """Prompts the player to choose a mathematical operation.

        Returns:
            A string representing the chosen operation.
        """
        operators = ["+", "-", "x", "/"]
        operators_formatted = "[" + ", ".join(operators) + "]"
        operation = input(f"Please enter an operation {operators_formatted}: ")
        
        # Validation loop to ensure the correct operation is chosen
        while operation not in operators:
            print("That is not a correct operation.")
            operation = input(f"Please try again {operators_formatted}: ")
        
        return operation

    def choose_max_number(self):
        """Allows the player to set the maximum number used in math problems.
        
        Returns:
            An integer representing the maximum number.
        """
        while True:
            try:
                max_number = int(input("Please enter a max number between 1 and 100: "))
                if 1 <= max_number <= 100:
                    return max_number
                else:
                    raise ValueError
            except ValueError:
                # Handles invalid input by prompting the user to try again
                print("That is not a valid number. Please enter a number between 1 and 100.")
                continue

    def start_timer(self):
        """Starts a count-down timer for the game duration."""
        self.start_time = time.time()  # Captures the start time
        time.sleep(self.game_time)  # Wait for the duration of the game
        self.timer_stop.set()  # Trigger the event indicating the end of the game time

    def generate_problem(self, operation, max_number):
        """Generates a random math problem based on the operation and max_number.
        
        Args:
            operation: The math operation as a string.
            max_number: The maximum number for generating problems.
        
        Returns:
            A tuple containing the problem as a string and the correct answer as an integer.
        """
        rand_num1 = random.randint(1, max_number)
        rand_num2 = random.randint(1, max_number)
        
        # Calculate the correct answer based on the operation
        if operation == "x":
            correct_answer = rand_num1 * rand_num2
        elif operation == "/":
            # Ensure the division is without remainder
            while rand_num1 % rand_num2 != 0:
                rand_num1 = random.randint(1, max_number)
                rand_num2 = random.randint(1, max_number)
            correct_answer = rand_num1 // rand_num2
        elif operation == "+":
            correct_answer = rand_num1 + rand_num2
        elif operation == "-":
            # Ensure no negative results
            if rand_num1 < rand_num2:
                rand_num1, rand_num2 = rand_num2, rand_num1  
            correct_answer = rand_num1 - rand_num2
        
        return f"{rand_num1} {operation} {rand_num2}", correct_answer

    def run_game_logic(self, operation, max_number):
        """Executes the core game logic, looping until the timer ends."""
        while not self.timer_stop.is_set():
            problem, answer = self.generate_problem(operation, max_number)
            correct = False

            while not correct:
                remaining_time = max(0, int(self.game_time - (time.time() - self.start_time)))
                print(f"{problem} = ?\nYou have {remaining_time} seconds left.")
                user_answer = input("Enter an answer: ")

                if self.timer_stop.is_set():
                    print("\nTime is up!\nSorry, you didn’t get that answer in on time.\n")
                    self.end_game()
                    return

                try:
                    if int(user_answer) == answer:
                        self.score += 1
                        correct = True
                        print(f"{user_answer} is correct!\n")
                    else:
                        print(f"{user_answer} is not correct. Try again!")
                except ValueError:
                    # Handles non-integer inputs from the user
                    print("Please enter a valid number.")

            self.problem_count += 1

        self.end_game()

    def end_game(self):
        """Handles the end-of-game sequence, including the possibility to restart."""
        print(f"\nYou answered {self.problem_count} problems!")
        response = input("Press Enter to play again. ")

        if response == '':
            self.reset_game()
            self.start_game()
        else:
            print("Thank you for playing!")

    def start_game(self):
        """Begins a new game, setting up and starting the timer and game logic."""
        self.reset_game()
        operation = self.choose_operation()
        max_number = self.choose_max_number()

        # Timer thread to limit the game duration
        timer_thread = threading.Thread(target=self.start_timer)
        timer_thread.start()

        self.run_game_logic(operation, max_number)
        timer_thread.join()

if __name__ == "__main__":
    game = Game()
    game.start_game()
