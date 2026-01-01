# Day 6 - Calculator Program with Functions and Logging
# This program performs basic math operations and logs everything to a file

# Import the logging module - it helps us track what our program does
import logging

# Set up logging - this creates TWO outputs:
# 1. A file called 'calculator.log' that saves everything
# 2. Console output so we can still see messages on screen
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('calculator.log'),  # Save to file
        logging.StreamHandler()  # Also show on screen
    ]
)

# FUNCTIONS - These are reusable pieces of code!
# Each function does ONE specific job

def add(num1, num2):
    """This function adds two numbers together"""
    result = num1 + num2
    logging.info(f"Calculation: {num1} + {num2} = {result}")
    return result

def subtract(num1, num2):
    """This function subtracts the second number from the first"""
    result = num1 - num2
    logging.info(f"Calculation: {num1} - {num2} = {result}")
    return result

def multiply(num1, num2):
    """This function multiplies two numbers"""
    result = num1 * num2
    logging.info(f"Calculation: {num1} × {num2} = {result}")
    return result

def divide(num1, num2):
    """This function divides the first number by the second"""
    if num2 == 0:
        logging.error(f"Division by zero attempted: {num1} ÷ 0")
        return "ERROR: Can't divide by zero!"
    else:
        result = num1 / num2
        logging.info(f"Calculation: {num1} ÷ {num2} = {result}")
        return result

# MAIN PROGRAM STARTS HERE
logging.info("="*40)
logging.info("🧮 Calculator Program Started 🧮")
logging.info("="*40)

# Step 1: Get the first number
first_number = float(input("\nWhat's your first number? "))
logging.debug(f"User entered first number: {first_number}")

# Step 2: Ask which operation they want
logging.info("Operations available: + - * /")
operation = input("\nPick an operation (+, -, *, /): ")
logging.debug(f"User selected operation: {operation}")

# Step 3: Get the second number
second_number = float(input("\nWhat's your second number? "))
logging.debug(f"User entered second number: {second_number}")

# Step 4: Call the right function based on the operation
if operation == "+":
    answer = add(first_number, second_number)
    logging.info(f"✓ Result: {answer}")

elif operation == "-":
    answer = subtract(first_number, second_number)
    logging.info(f"✓ Result: {answer}")

elif operation == "*":
    answer = multiply(first_number, second_number)
    logging.info(f"✓ Result: {answer}")

elif operation == "/":
    answer = divide(first_number, second_number)
    if "ERROR" not in str(answer):
        logging.info(f"✓ Result: {answer}")
    else:
        logging.error(f"❌ {answer}")

else:
    logging.warning(f"Invalid operation entered: '{operation}' - Please use +, -, *, or /")

# Say goodbye
logging.info("\nCalculator program ended successfully")
logging.info("Check calculator.log for full history!")
logging.info("="*40)

# LEARNING NOTES:
# - We replaced ALL print() with logging statements
# - logging.DEBUG = detailed info for debugging
# - logging.INFO = general information messages
# - logging.WARNING = something unexpected happened
# - logging.ERROR = an error occurred
# - Everything appears both on screen AND in calculator.log file!