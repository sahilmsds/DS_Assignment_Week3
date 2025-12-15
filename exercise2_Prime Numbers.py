import math

# Function to check whether a number is prime
def is_prime(number):
    if number <= 1:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(number)) + 1, 2):
        if number % i == 0:
            return False
    return True

# Main function to generate prime numbers
def generate_primes():
    try:
        # Taking range start input from user
        start = int(input("Enter start of range (positive integer): "))
        end = int(input("Enter end of range (positive integer): "))
        if start <= 0 or end <= 0:
            raise ValueError("Both numbers must be positive integers.")
        if start > end:
            raise ValueError("Start of range cannot be greater than end.")

        
        primes = [] # List to store prime numbers
        for num in range(start, end + 1):
            if is_prime(num):
                primes.append(num)
        if not primes:
            print("No prime numbers found in the given range.")
            return

        print("\nPrime numbers in the given range:\n")

        count = 0

        for prime in primes:
            print(f"{prime:5}", end=" ")
            count += 1
            if count % 10 == 0:
                print()
        print()

    except ValueError as ve:
        print("Error:", ve)

    except Exception as e:
        print("An unexpected error occurred:", e)

generate_primes()