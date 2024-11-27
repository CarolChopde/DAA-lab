import random

# Karatsuba multiplication algorithm
def karatsuba(x, y):
    if not isinstance(x, int) or not isinstance(y, int):
        return "Error, Invalid datatype"
    
    # Handling negative numbers correctly
    if x < 0 and y < 0:
        return karatsuba(-x, -y)  # Both negative
    elif x < 0 or y < 0:
        return -karatsuba(abs(x), abs(y))  # One negative

    # Base case (n = 1)
    if abs(x) < 10 and abs(y) < 10:
        return x * y

    # Positive integers
    n = max(len(str(abs(x))), len(str(abs(y))))  # Use abs to calculate length
    m = n // 2  
    a, b = divmod(x, 10 ** m)
    c, d = divmod(y, 10 ** m)
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    pq = karatsuba(a + b, c + d)

    # Karatsuba formula
    adbc = pq - ac - bd
    return (10 ** (2 * m)) * ac + (10 ** m) * adbc + bd

# Generate large random numbers with a specified number of digits
def generate_large_number(digits):
    return random.randint(10**(digits-1), 10**digits - 1)

# Test cases with different digit lengths
def test_karatsuba():
    test_cases = [5, 10, 50, 100, 500, 1000]  # Number of digits for each test case
    for digits in test_cases:
        # Generate two large random numbers of the specified digit length
        num1 = generate_large_number(digits)
        num2 = generate_large_number(digits)

        # Run Karatsuba multiplication
        result = karatsuba(num1, num2)

        # Print the result (you can print the first few digits for large numbers)
        print(f"Multiplying two {digits}-digit numbers:")
        print(f"\n{str(num1)} * {str(num2)} = {str(result)}\n")

# Run the tests
test_karatsuba()
