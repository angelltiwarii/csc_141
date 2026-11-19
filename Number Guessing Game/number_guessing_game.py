import random


# --------------------------------------------------
# GAME LOGIC
# --------------------------------------------------

def choose_difficulty():
    """Allow the player to select a difficulty level."""

    print("\nChoose your difficulty:")
    print("1. Easy   (1-20, 6 attempts)")
    print("2. Medium (1-50, 7 attempts)")
    print("3. Hard   (1-100, 8 attempts)")

    while True:
        choice = input("\nEnter your choice (1, 2, or 3): ")

        if choice == '1':
            return 20, 6

        elif choice == '2':
            return 50, 7

        elif choice == '3':
            return 100, 8

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


def get_secret_number(max_number):
    """Generate a random secret number."""

    return random.randint(1, max_number)


def get_hint(guess, secret_number):
    """Return a hint based on the player's guess."""

    if guess < secret_number:
        return "Too low!"

    elif guess > secret_number:
        return "Too high!"

    else:
        return "Correct!"


def get_player_guess(max_number):
    """Ask the player for a valid number."""

    while True:
        guess = input(f"Enter your guess (1-{max_number}): ")

        try:
            guess = int(guess)

            if 1 <= guess <= max_number:
                return guess

            else:
                print("Please enter a number within the range.")

        except ValueError:
            print("Please enter a valid whole number.")


# --------------------------------------------------
# LYING COMPUTER MODE
# --------------------------------------------------

def lying_hint(guess, secret_number):
    """Sometimes give the player an incorrect hint."""

    correct_hint = get_hint(guess, secret_number)

    # There is a 25% chance of giving a false hint.
    if random.randint(1, 4) == 1:

        if correct_hint == "Too high!":
            return "Too low!"

        elif correct_hint == "Too low!":
            return "Too high!"

    return correct_hint


# --------------------------------------------------
# MAIN GAME
# --------------------------------------------------

def play_game():

    print("\n===================================")
    print("       NUMBER GUESSING GAME")
    print("===================================")

    max_number, attempts = choose_difficulty()

    secret_number = get_secret_number(max_number)

    # Ask whether the player wants lying mode.
    lying_mode = input(
        "\nWould you like to enable Lying Computer Mode? (yes/no): "
    ).lower()

    if lying_mode == "yes":
        print("\nLying Computer Mode ACTIVATED!")
        print("Warning: Some hints may be incorrect!")

    else:
        lying_mode = "no"
        print("\nRegular Mode ACTIVATED!")

    print(f"\nI have selected a number between 1 and {max_number}.")
    print(f"You have {attempts} attempts to guess it.")

    attempts_used = 0
    won = False

    # Continue until the player wins or runs out of attempts.
    while attempts > 0:

        print(f"\nAttempts remaining: {attempts}")

        guess = get_player_guess(max_number)

        attempts -= 1
        attempts_used += 1

        # Get the appropriate hint.
        if lying_mode == "yes":
            hint = lying_hint(guess, secret_number)

        else:
            hint = get_hint(guess, secret_number)

        print("\nComputer says:", hint)

        # Check whether the player guessed correctly.
        if guess == secret_number:

            won = True
            break

    # Display the final result.
    print("\n===================================")

    if won:
        print("CONGRATULATIONS! YOU WON!")
        print(f"You guessed the number in {attempts_used} attempts.")

    else:
        print("GAME OVER!")
        print(f"The correct number was {secret_number}.")

    print("===================================")


# --------------------------------------------------
# USER INTERFACE AND REPLAY OPTION
# --------------------------------------------------

def main():

    print("\nWelcome to the Number Guessing Game!")

    while True:

        play_game()

        # Ask whether the player wants another round.
        replay = input("\nWould you like to play again? (yes/no): ").lower()

        if replay != "yes":
            print("\nThank you for playing!")
            print("See you next time!")
            break


# Start the game.
if __name__ == "__main__":
    main()