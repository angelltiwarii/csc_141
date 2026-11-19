while True:
    print("\nEnter two numbers to add.")
    print("Enter 'q' to quit.")

    first_number = input("First number: ")

    if first_number == 'q':
        break

    second_number = input("Second number: ")

    if second_number == 'q':
        break

    try:
        first_number = int(first_number)
        second_number = int(second_number)

    except ValueError:
        print("Please enter valid numbers.")

    else:
        result = first_number + second_number
        print(f"The sum is: {result}")