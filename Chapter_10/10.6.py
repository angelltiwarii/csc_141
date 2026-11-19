try:
    number1 = input("Enter the first number: ")
    number2 = input("Enter the second number: ")

    number1 = int(number1)
    number2 = int(number2)

    result = number1 + number2

    print(f"The sum is: {result}")

except ValueError:
    print("Please enter valid numbers.")