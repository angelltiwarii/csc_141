import json


def get_stored_username():
    filename = 'Chapter_10/username.json'

    try:
        with open(filename) as file_object:
            username = json.load(file_object)

    except FileNotFoundError:
        return None

    else:
        return username


def get_new_username():
    username = input("What is your name? ")

    filename = 'Chapter_10/username.json'

    with open(filename, 'w') as file_object:
        json.dump(username, file_object)

    return username


def greet_user():
    username = get_stored_username()

    if username:
        correct = input(f"Is {username} your username? (yes/no): ")

        if correct.lower() == 'yes':
            print(f"Welcome back, {username}!")

        else:
            username = get_new_username()
            print(f"We'll remember you when you come back, {username}!")

    else:
        username = get_new_username()
        print(f"We'll remember you when you come back, {username}!")


greet_user()