from datetime import datetime

# Defining the main function
def calculate_age():
    try:
        # Asking user to enter birth date in mm/dd/yyyy format
        birth_date_input = input("Enter your birth date in this format(mm/dd/yyyy): ")

        birth_date = datetime.strptime(birth_date_input, "%m/%d/%Y")
        today = datetime.today()

        # Checking if the birth date is in the future
        if birth_date > today:
            raise ValueError("Birth date cannot be in the future.")
        age = today.year - birth_date.year

        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        indian_format = birth_date.strftime("%d-%m-%Y")

        # Displaying the calculated age
        print(f"Your current age is: {age} years")
        print(f"Your birth date in Indian format is: {indian_format}")

    except ValueError as ve:
        print("Error:", ve)

    except Exception as e:
        print("An unexpected error occurred:", e)

calculate_age()